# TLS/SSL

## Безопасные схемы

- ACME certificate непосредственно в panel.
- Reverse proxy завершает TLS, panel слушает loopback/private address.
- Cloudflare Origin CA только между Cloudflare и origin, при постоянном proxied режиме.

## 3X-UI certificate management

Menu `SSL Certificate Management` включает получение domain certificate, revoke, force renew, просмотр domains, установку panel cert paths и short-lived IP certificate. Cloudflare DNS challenge подходит для wildcard/proxied DNS.

## Пошаговая настройка ACME

1. Проверить DNS A/AAAA.
2. Для HTTP challenge освободить/разрешить port 80.
3. Запустить:

```sh
x-ui
# SSL Certificate Management
```

4. Получить certificate и задать panel paths.
5. Перезапустить panel.
6. Проверить hostname, chain и expiry.

Для Cloudflare DNS challenge использовать API Token с минимальным scope `Zone:DNS:Edit` для конкретной zone; global API key не предпочитать.

## Reverse proxy

Panel backend не публиковать. Если HSTS завершает внешний proxy, учитывать `XUI_SKIP_HSTS` из текущей документации/окружения и проверять реальный header flow.

## Проверка

```sh
openssl s_client -connect panel.example.com:443 -servername panel.example.com </dev/null
curl -I https://panel.example.com/<path>/
```

## Ошибки

- A/AAAA указывает не на VPS.
- Certificate hostname не совпадает.
- Reverse proxy не передает path/headers.
- Origin CA открыт напрямую: browser ему не доверяет.
- Private key имеет слишком широкие permissions.

## Источники

- [3X-UI Wiki: SSL](https://github.com/MHSanaei/3x-ui/wiki/Configuration)
- [3X-UI certificate flow](https://github.com/MHSanaei/3x-ui/blob/main/x-ui.sh)
- [Cloudflare Origin CA](https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/)
