# Сертификаты

## Варианты origin certificate

- Public CA (например ACME): доверяется browsers и Cloudflare.
- Cloudflare Origin CA: доверяется Cloudflare edge, но не обычным browsers при DNS-only/direct access.

## 3X-UI ACME

```sh
x-ui
# SSL Certificate Management
```

Для proxied/wildcard hostname использовать Cloudflare DNS challenge со scoped API Token. После issuance задать panel/reverse proxy cert paths.

## Origin CA

1. Создать certificate только для нужных hostnames.
2. Сохранить private key непосредственно на origin.
3. Ограничить permissions:

```sh
chown root:root /path/to/origin.key
chmod 600 /path/to/origin.key
```

4. Настроить reverse proxy.
5. Включить `Full (strict)`.
6. Не переводить hostname в DNS-only без замены на public-trusted certificate.

## Проверка

```sh
openssl x509 -in /path/to/cert.pem -noout -subject -issuer -dates -ext subjectAltName
openssl s_client -connect <origin-ip>:443 -servername <hostname> -showcerts </dev/null
```

## Ошибки

- Certificate expired/not yet valid.
- SAN не содержит hostname.
- Incomplete chain.
- Origin Rule меняет SNI.
- Key/certificate pair не совпадают.

## Источники

- [Cloudflare Origin CA](https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/)
- [Cloudflare Full strict](https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/full-strict/)
- [3X-UI Wiki SSL](https://github.com/MHSanaei/3x-ui/wiki/Configuration)
