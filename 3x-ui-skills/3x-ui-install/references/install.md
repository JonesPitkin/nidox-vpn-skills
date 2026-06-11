# Установка 3X-UI

## Содержание

1. Предварительная проверка
2. Нативная установка
3. Ручная установка
4. Docker Compose
5. Docker CLI
6. VPS и LXC
7. Проверка результата
8. Сценарии и ошибки
9. Источники

## 1. Предварительная проверка

Выполнять от root или через `sudo -i`:

```sh
cat /etc/os-release
uname -m
command -v systemctl
systemd-detect-virt 2>/dev/null || true
df -h /
free -h
ip -br address
ss -lntup
```

Официально поддерживаются Ubuntu, Debian и ряд других Linux. Архитектуры: `amd64`, `386`, `arm64`, `armv7`, `armv6`, `armv5`, `s390x`. Если ОС не поддерживается, Wiki предлагает Docker.

Перед установкой:

```sh
apt-get update
apt-get install -y curl ca-certificates
curl -I https://api.github.com/repos/MHSanaei/3x-ui/releases/latest
```

Проверить firewall и не потерять SSH:

```sh
ss -lntp | grep -E ':(22|2222)[[:space:]]'
ufw status verbose 2>/dev/null || true
```

## 2. Нативная установка

Официальная one-line команда:

```sh
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
```

Более контролируемый вариант с предварительным просмотром:

```sh
curl -fL https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh -o /root/3x-ui-install.sh
less /root/3x-ui-install.sh
bash /root/3x-ui-install.sh
```

Installer:

- требует root;
- определяет ОС и архитектуру;
- устанавливает `cron`, `curl`, `tar`, `tzdata`, `socat`, `ca-certificates`, `openssl`;
- загружает последний release archive;
- ставит файлы в `/usr/local/x-ui`;
- ставит management script в `/usr/bin/x-ui`;
- создает и включает service;
- предлагает SQLite или PostgreSQL;
- генерирует случайные username, password, port и web base path, если значения не заданы;
- предлагает TLS для домена, IP, custom certificate или безопасный пропуск через reverse proxy/SSH tunnel.

SQLite является default, файл: `/etc/x-ui/x-ui.db`. PostgreSQL выбирается в installer; DSN на Ubuntu/Debian сохраняется в `/etc/default/x-ui` с mode `600`.

Не терять выведенные installer credentials и API token. Хранить их в password manager, не в shell history или тикете.

### Проверка

```sh
x-ui settings
x-ui status
systemctl is-enabled x-ui
systemctl is-active x-ui
journalctl -u x-ui -n 100 --no-pager
ls -la /usr/local/x-ui /etc/x-ui
ss -lntup
```

После установки открыть точный URL, напечатанный installer. Если TLS пропущен и панель bind к `127.0.0.1`:

```sh
ssh -L 2222:127.0.0.1:<panel-port> root@<server-ip>
```

Затем открыть `http://localhost:2222/<web-base-path>`.

## 3. Ручная установка

Использовать, когда one-line script неприемлем, но помнить: официальный Wiki recipe удаляет старые binary paths. Сначала сделать backup.

```sh
ARCH=$(uname -m)
case "$ARCH" in
  x86_64|x64|amd64) XUI_ARCH=amd64 ;;
  i*86|x86) XUI_ARCH=386 ;;
  armv8*|arm64|aarch64) XUI_ARCH=arm64 ;;
  armv7*) XUI_ARCH=armv7 ;;
  armv6*) XUI_ARCH=armv6 ;;
  armv5*) XUI_ARCH=armv5 ;;
  s390x) XUI_ARCH=s390x ;;
  *) echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac
wget "https://github.com/MHSanaei/3x-ui/releases/latest/download/x-ui-linux-${XUI_ARCH}.tar.gz"
```

Следовать актуальному разделу Manual installation Wiki. Не заменять неизвестную архитектуру на `amd64`: актуальный installer завершает работу на unsupported architecture.

Минимальные проверки архива:

```sh
tar tzf "x-ui-linux-${XUI_ARCH}.tar.gz" | sed -n '1,40p'
```

После размещения файлов:

```sh
systemctl daemon-reload
systemctl enable x-ui
systemctl restart x-ui
systemctl status x-ui --no-pager -l
```

## 4. Docker Compose

Официальный image: `ghcr.io/mhsanaei/3x-ui:latest`.

```sh
mkdir -p /opt/3x-ui/{db,cert}
cd /opt/3x-ui
```

Compose должен сохранять:

```yaml
services:
  3xui:
    image: ghcr.io/mhsanaei/3x-ui:latest
    container_name: 3xui_app
    cap_add:
      - NET_ADMIN
      - NET_RAW
    volumes:
      - ./db:/etc/x-ui
      - ./cert:/root/cert
    environment:
      XRAY_VMESS_AEAD_FORCED: "false"
      XUI_ENABLE_FAIL2BAN: "true"
    tty: true
    ports:
      - "2053:2053"
    restart: unless-stopped
```

Запуск:

```sh
docker compose config
docker compose pull
docker compose up -d
docker compose ps
docker compose logs --tail=100 3xui
```

Default Docker credentials по Wiki: `admin/admin`. Сменить немедленно, затем включить 2FA и custom web path.

`ports: 2053:2053` публикует только panel port. Каждый inbound port надо добавить отдельно. Альтернатива из Wiki — `network_mode: host`; это расширяет сетевую поверхность и требует осознанного firewall.

Для bundled PostgreSQL официальный compose использует profile:

```sh
docker compose --profile postgres up -d
```

Перед этим заменить default `POSTGRES_PASSWORD`, раскомментировать `XUI_DB_TYPE` и `XUI_DB_DSN`, сохранить также `pgdata`.

## 5. Docker CLI

Официальный шаблон:

```sh
docker run -itd \
  -e XRAY_VMESS_AEAD_FORCED=false \
  -e XUI_ENABLE_FAIL2BAN=true \
  -v "$PWD/db:/etc/x-ui" \
  -v "$PWD/cert:/root/cert" \
  --cap-add=NET_ADMIN \
  --cap-add=NET_RAW \
  --network=host \
  --restart=unless-stopped \
  --name 3x-ui \
  ghcr.io/mhsanaei/3x-ui:latest
```

Проверка:

```sh
docker ps --filter name=3x-ui
docker logs --tail=100 3x-ui
docker inspect 3x-ui --format '{{json .Mounts}}'
```

Внутри Docker `x-ui start/stop/enable` не управляют systemd: main process управляется контейнером. Использовать `docker stop`, `docker restart` и restart policy.

## 6. VPS и LXC

Для обычного VPS использовать native systemd или Docker.

Для LXC:

1. Проверить init:
   ```sh
   ps -p 1 -o comm=
   systemd-detect-virt
   ```
2. Проверить cgroup/network capabilities и возможность слушать нужные порты.
3. Для native install не требовать privileged container только из-за панели.
4. Fail2ban/IP-limit требует firewall capabilities; Docker Fail2ban требует `NET_ADMIN`, `NET_RAW`.
5. BBR меняет kernel/network settings и в unprivileged LXC обычно зависит от host.

TODO: официальный Wiki и README не содержат отдельной LXC-инструкции. Перед рекомендацией privileged mode, nesting, AppArmor или host sysctl изучить официальную документацию конкретной платформы LXC/Proxmox и политику хостинга.

## 7. Проверка результата

Проверить:

```sh
x-ui settings
x-ui status
curl -kI "https://127.0.0.1:<panel-port>/<web-base-path>/" 2>/dev/null
```

Ожидать active service/container, listener на panel port и доступность login page. После входа:

- изменить credentials;
- проверить Xray state;
- создать только необходимый inbound;
- проверить listener;
- перезагрузить сервер и повторить проверки.

## 8. Сценарии и ошибки

**Новый Ubuntu/Debian VPS:** native installer, SQLite, TLS domain/IP или loopback+SSH tunnel.

**Неподдерживаемая ОС:** Docker с persistent volumes.

**Много клиентов/узлов:** рассмотреть PostgreSQL; не выбирать его без backup и контроля DSN.

**GitHub timeout:** повторить installer через IPv4:

```sh
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh --ipv4)
```

Не закреплять IP `raw.githubusercontent.com` без повторной проверки: Wiki предупреждает, что адрес меняется.

**Panel port занят:**

```sh
ss -ltnp | grep ":<port> "
```

Выбрать свободный port через `x-ui` menu или устранить конфликт.

## 9. Источники

- [Wiki: Installation](https://github.com/MHSanaei/3x-ui/wiki/Installation)
- [Wiki: Home / supported OS and architectures](https://github.com/MHSanaei/3x-ui/wiki)
- [README: Quick Start, platforms, databases](https://github.com/MHSanaei/3x-ui/blob/main/README.md)
- [Official install.sh](https://github.com/MHSanaei/3x-ui/blob/main/install.sh)
- [Official docker-compose.yml](https://github.com/MHSanaei/3x-ui/blob/main/docker-compose.yml)
- [Official Dockerfile](https://github.com/MHSanaei/3x-ui/blob/main/Dockerfile)
- [Official DockerEntrypoint.sh](https://github.com/MHSanaei/3x-ui/blob/main/DockerEntrypoint.sh)
