# Безопасность установки

## Содержание

1. Модель угроз
2. Credentials и 2FA
3. TLS и bind address
4. Firewall
5. Fail2ban
6. Docker и секреты
7. Обновления и backups
8. Проверка
9. Источники

## 1. Модель угроз

Панель управляет Xray, users, keys, subscriptions и database. Компрометация панели равна компрометации proxy infrastructure. README отдельно указывает, что проект предназначен для personal use и не рекомендует production.

## 2. Credentials и 2FA

Native installer генерирует случайные username/password/path. Docker Wiki стартует с `admin/admin`.

Сразу после установки:

1. Сменить username и длинный уникальный password.
2. Включить 2FA в `Panel Settings`.
3. Задать custom web base path.
4. Не передавать API token и credentials в чат/issue/log.

CLI reset:

```sh
x-ui
```

Использовать `Reset Username & Password` и при необходимости `Reset Web Base Path`.

## 3. TLS и bind address

Допустимые безопасные модели:

- panel получает ACME certificate;
- reverse proxy завершает TLS, panel слушает loopback;
- panel доступна только через SSH tunnel.

В menu `SSL Certificate Management` доступны domain certificate, revoke, force renew, show domains, set cert paths и short-lived IP certificate. Cloudflare DNS validation поддерживает wildcard и proxied domain.

Для domain ACME проверить DNS и port 80:

```sh
getent ahostsv4 content.example.com
ss -ltnp | grep ':80 '
```

Для loopback:

```sh
x-ui
# SSH Port Forwarding Management -> Set listen IP -> 127.0.0.1
ssh -L 2222:127.0.0.1:<panel-port> root@<server-ip>
```

Plain HTTP допустим только за TLS reverse proxy или через SSH tunnel. Не вводить password через публичный HTTP.

При reverse proxy учитывать Wiki note: panel URL должен оканчиваться `/`; subscription URI должен совпадать с configured path.

## 4. Firewall

Сначала разрешить текущий SSH:

```sh
ufw allow <ssh-port>/tcp
```

Затем разрешать только нужное:

```sh
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow <panel-port>/tcp
ufw allow <inbound-port>/tcp
ufw status numbered
```

Если panel bind к loopback или доступна через reverse proxy, public panel port не открывать.

Wiki советует ограничивать panel по source IP:

```sh
ufw allow from <admin-ip> to any port <panel-port> proto tcp
```

Перед удалением старого SSH rule открыть новую сессию через новый port.

## 5. Fail2ban

3X-UI integration реализует per-client IP limits, а не общую защиту login page. Настройка menu: `IP Limit Management`.

Для работы требуется access log:

```json
"log": {
  "access": "./access.log",
  "dnsLog": false,
  "error": "./error.log",
  "loglevel": "warning"
}
```

Проверки:

```sh
systemctl status fail2ban --no-pager
fail2ban-client status
fail2ban-client status 3x-ipl
x-ui banlog
```

В Docker bundled Fail2ban требует `NET_ADMIN`; `NET_RAW` покрывает IPv6 rules. Без capabilities ban может логироваться, но не применяться.

Не считать IP-limit защитой panel login. Для brute force дополнительно применять TLS, strong credentials, 2FA, source IP restriction/reverse proxy controls.

## 6. Docker и секреты

- Не использовать `POSTGRES_PASSWORD: xui` из example.
- Не коммитить compose `.env`, DSN, cert private keys и `db/`.
- Ограничить host permissions:
  ```sh
  chmod 700 /opt/3x-ui/db /opt/3x-ui/cert
  ```
- Не выдавать `privileged`; официальный compose просит только `NET_ADMIN` и `NET_RAW` для Fail2ban.
- `network_mode: host` публикует все listeners; при возможности использовать явные `ports`.
- Проверять provenance image: `ghcr.io/mhsanaei/3x-ui`.

## 7. Обновления и backups

- Обновлять ОС и panel после backup.
- Не запускать неизвестные scripts; Wiki прямо рекомендует этого избегать.
- Включить `Block BitTorrent Protocol`, private IP blocking и необходимые block lists, если это соответствует задаче.
- Хранить backup encrypted/off-host и периодически тестировать restore.
- Проверять release notes на security changes.

## 8. Проверка

```sh
x-ui settings
ss -lntup
ufw status verbose
curl -kI "https://content.example.com/<hidden-panel-path>/"
systemctl is-active x-ui
systemctl is-active fail2ban
```

Проверить:

- default credentials не работают;
- 2FA включена;
- HTTP redirect/closure соответствует архитектуре;
- panel port не доступен из лишних networks;
- certificate chain/hostname корректны;
- backups и DSN имеют ограниченные permissions.

## 9. Источники

- [Wiki: Getting SSL, reverse proxy, Fail2ban](https://github.com/MHSanaei/3x-ui/wiki/Configuration)
- [Wiki FAQ: firewall and brute-force response](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems)
- [Wiki: Docker security notes](https://github.com/MHSanaei/3x-ui/wiki/Installation#docker)
- [Official install.sh TLS flow](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/install.sh)
- [Official x-ui.sh firewall/SSL/IP-limit flow](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/x-ui.sh)
- [Docker entrypoint Fail2ban rules](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/DockerEntrypoint.sh)
