# Диагностика установки и запуска

## Содержание

1. Порядок диагностики
2. Установка и download
3. systemd
4. Панель недоступна
5. Docker
6. База и миграция
7. TLS
8. LXC
9. Сбор отчета
10. Источники

## 1. Порядок диагностики

Идти снизу вверх:

1. ОС, архитектура, disk/RAM.
2. DNS и доступ к GitHub/GHCR.
3. Наличие binary/data.
4. Service/container state.
5. Logs.
6. Listening sockets/firewall.
7. TLS/path/browser.
8. Xray config и inbounds.

Не выполнять reset/reinstall, пока не сохранены DB, settings и logs.

## 2. Установка и download

```sh
cat /etc/os-release
uname -m
df -h /
free -h
getent hosts github.com raw.githubusercontent.com ghcr.io
curl -4I https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh
curl -I https://api.github.com/repos/MHSanaei/3x-ui/releases/latest
```

При GitHub timeout официальный FAQ предлагает installer с `--ipv4`:

```sh
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh --ipv4)
```

Static `/etc/hosts` override из FAQ может устареть; использовать только после проверки актуального IP и удалить после восстановления DNS.

Unsupported architecture: не подставлять `amd64`; сверить `uname -m` со списком supported architectures.

APT lock после прерванного update: сначала проверить, нет ли живого apt/dpkg process:

```sh
ps aux | grep -E '[a]pt|[d]pkg'
```

Только если процессов нет:

```sh
dpkg --configure -a
apt-get -f install
```

Wiki содержит удаление lock files, но это не должно быть первым действием.

## 3. systemd

```sh
systemctl status x-ui --no-pager -l
systemctl is-enabled x-ui
journalctl -u x-ui -b --no-pager
systemctl cat x-ui
ls -l /usr/bin/x-ui /usr/local/x-ui/x-ui /etc/x-ui
```

После исправления unit:

```sh
systemctl daemon-reload
systemctl restart x-ui
```

Типовые причины:

- binary отсутствует или не executable;
- wrong service unit для distro;
- database/env недоступны;
- panel port занят;
- invalid certificate path;
- Xray config invalid;
- update не завершил замену файлов.

Management shortcuts:

```sh
x-ui status
x-ui settings
x-ui restart
x-ui restart-xray
x-ui log
```

`x-ui log` открывает live journal. Для bounded report использовать `journalctl -n`.

## 4. Панель недоступна

Сначала получить фактические settings:

```sh
x-ui settings
ss -ltnp
```

Проверить локально:

```sh
curl -vk "https://127.0.0.1:<port>/<path>/" -o /dev/null
curl -v "http://127.0.0.1:<port>/<path>/" -o /dev/null
```

Интерпретация:

- нет listener: service/config failure;
- local works, remote fails: firewall/NAT/provider security group/bind address;
- TLS hostname error: DNS/certificate mismatch;
- 404: wrong web base path или reverse proxy path;
- connection reset после update: проверить Xray/panel logs и cert paths.

Wiki сообщает, что после update/transfer `Reset Settings` часто исправляет Xray или panel SSL issue. Использовать только после backup и фиксации текущих settings:

```sh
x-ui
# Reset Settings
```

## 5. Docker

```sh
docker compose ps
docker compose logs --tail=200 3xui
docker inspect 3xui_app --format '{{json .State}}'
docker inspect 3xui_app --format '{{json .Mounts}}'
docker inspect 3xui_app --format '{{json .HostConfig.CapAdd}}'
docker port 3xui_app
```

Типовые ошибки:

- panel port опубликован, inbound ports нет;
- bind mount указывает в пустой/другой host directory;
- container пересоздан без прежних volumes;
- Fail2ban не применяет bans без `NET_ADMIN`/`NET_RAW`;
- host port занят;
- `network_mode: host` конфликтует с `ports`;
- PostgreSQL profile не поднят или DSN указывает не на service name `postgres`.

В Docker panel является main process. Управлять:

```sh
docker restart 3xui_app
docker compose restart 3xui
```

## 6. База и миграция

SQLite:

```sh
ls -lh /etc/x-ui/x-ui.db
file /etc/x-ui/x-ui.db
journalctl -u x-ui -n 200 --no-pager | grep -iE 'database|sqlite|locked|migrat'
```

`database is locked`: проверить disk latency/space и access logging; остановить panel для file copy/restore.

PostgreSQL:

```sh
grep -E '^XUI_DB_(TYPE|DSN)=' /etc/default/x-ui | sed -E 's#(://[^:]+:)[^@]+@#\1****@#'
command -v psql pg_dump pg_restore
systemctl status postgresql --no-pager -l
ss -ltnp | grep ':5432 '
```

Не печатать unredacted DSN.

Migration:

```sh
/usr/local/x-ui/x-ui migrate-db -h
x-ui migrateDB /etc/x-ui/x-ui.db /root/test.dump
x-ui migrateDB /root/test.dump /root/test-restored.db
```

Если command сообщает, что conversion не поддерживается, обновить panel до версии с `migrate-db --dump/--restore`.

## 7. TLS

```sh
x-ui settings
find /root/cert -maxdepth 3 -type f -name '*.pem' -ls 2>/dev/null
openssl s_client -connect panel.example.com:443 -servername panel.example.com </dev/null
```

ACME domain:

- DNS должен указывать на server;
- port 80 должен быть доступен для standalone challenge;
- другой web server может занимать port 80;
- Cloudflare DNS mode требует scoped token или Global API Key.

Certbot check:

```sh
certbot renew --dry-run
```

IP certificate в Wiki описан как 6-day auto-renewing; проверять renewal job и certificate dates:

```sh
openssl x509 -in <fullchain.pem> -noout -subject -issuer -dates
```

## 8. LXC

```sh
systemd-detect-virt
cat /proc/1/status | sed -n '1,20p'
cat /proc/self/status | grep Cap
iptables -L -n 2>&1 | sed -n '1,40p'
```

Если service работает, но firewall/Fail2ban/BBR нет:

- выяснить privileged/unprivileged container;
- проверить host policy и delegated capabilities;
- не менять host LXC config без согласования;
- отделить работу панели/Xray от optional IP-limit/BBR.

Ограничение источников: 3X-UI upstream не документирует LXC-specific requirements. Для Proxmox/LXC capability errors обращаться к официальной документации платформы и провайдера.

## 9. Сбор отчета

Собирать с редактированием секретов:

```sh
cat /etc/os-release
uname -a
systemd-detect-virt 2>/dev/null || true
/usr/local/x-ui/x-ui -v 2>/dev/null || true
systemctl status x-ui --no-pager -l
journalctl -u x-ui -n 200 --no-pager
ss -lntup
df -h
free -h
```

Не включать DB, DSN password, API tokens, private keys, UUID и subscription links.

## 10. Источники

- [Wiki: Common Questions & Problems](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems)
- [Wiki: Installation](https://github.com/MHSanaei/3x-ui/wiki/Installation)
- [Wiki: Configuration](https://github.com/MHSanaei/3x-ui/wiki/Configuration)
- [Official x-ui.sh](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/x-ui.sh)
- [Official install.sh](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/install.sh)
- [Official update.sh](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/update.sh)
- [Official DockerEntrypoint.sh](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/DockerEntrypoint.sh)
