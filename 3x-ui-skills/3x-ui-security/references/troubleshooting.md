# Диагностика безопасности

## Потерян доступ к панели

1. Не менять firewall повторно.
2. Проверить service/listener:

```sh
x-ui status
x-ui settings
ss -lntp
journalctl -u x-ui -n 200 --no-pager
```

3. Проверить URL с loopback.
4. Сверить base path, TLS и reverse proxy.
5. Использовать menu reset credentials/path только через доверенную SSH/console.

## TLS error

```sh
openssl s_client -connect <host>:443 -servername <host> </dev/null
```

Проверить DNS, hostname, expiry, chain, file permissions и reverse proxy upstream.

## SSH lockout risk

Не перезапускать вслепую. Использовать provider console, `sshd -t`, effective `sshd -T`, firewall status и вторую session.

## Fail2Ban не блокирует

Проверить jail, access log, action backend, Docker capabilities и IPv4/IPv6. Не тестировать на единственном admin IP.

## Подозрение на компрометацию

1. Изолировать panel source access.
2. Сохранить forensic копии logs/DB без публикации.
3. Ротировать panel/API/Telegram/DB/Cloudflare credentials, client secrets и сертификаты.
4. Проверить users, inbounds, outbounds, cron/systemd/Docker images.
5. Развернуть clean host, если integrity не может быть доказана.

## Проверочный список после hardening

- старые credentials отклоняются;
- 2FA работает;
- panel port не виден запрещенной сети;
- HTTPS chain корректна;
- SSH key login работает, password/root запрещены;
- backup permissions и restore test подтверждены;
- reboot не возвращает старые listeners/rules.

## Источники

- [3X-UI Wiki FAQ](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems)
- [3X-UI Wiki Configuration](https://github.com/MHSanaei/3x-ui/wiki/Configuration)
- [3X-UI issues](https://github.com/MHSanaei/3x-ui/issues)
