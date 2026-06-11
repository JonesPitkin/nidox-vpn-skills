# TLS Modes

## Режимы

- `Flexible`: browser-edge HTTPS, edge-origin HTTP. Не использовать для защищенной панели/origin.
- `Full`: edge-origin TLS, но origin certificate не валидируется строго.
- `Full (strict)`: edge-origin TLS с проверкой срока, hostname и доверия/Origin CA.
- `Strict (SSL-Only Origin Pull)`: отдельный строгий режим, доступность зависит от продукта/config.

Рекомендуемый baseline: `Full (strict)`.

## Пошаговая настройка

1. Установить на origin публичный CA certificate или Cloudflare Origin CA.
2. Certificate SAN должен соответствовать origin hostname/SNI.
3. Проверить chain и private key.
4. В Cloudflare `SSL/TLS -> Overview` выбрать `Full (strict)`.
5. Проверить edge URL.
6. Отключить legacy protocols/ciphers на origin по возможностям stack.

## Почему не Flexible

Flexible оставляет Cloudflare-origin leg незашифрованным и часто вызывает redirect loops, если origin принудительно перенаправляет HTTP на HTTPS.

## Ошибки

- 525: TLS handshake edge-origin не состоялся.
- 526: certificate не прошел strict validation.
- Redirect loop: Flexible + HTTPS redirect на origin.
- Hostname mismatch после Origin Rule.

## Проверка

```sh
openssl s_client -connect <origin-ip>:443 -servername <origin-host> -showcerts </dev/null
curl -I https://<public-host>/
```

## Источники

- [Cloudflare SSL modes](https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/)
- [Full (strict)](https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/full-strict/)
