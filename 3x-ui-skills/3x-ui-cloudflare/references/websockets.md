# WebSocket через Cloudflare

## Требования

- proxied hostname;
- TLS рекомендуется;
- supported port;
- одинаковые Host/path на client, Cloudflare route/reverse proxy и Xray inbound;
- WebSockets enabled в Cloudflare Network settings, если toggle доступен.
- hostname и path должны выглядеть как часть обычного сайта.

## Настройка 3X-UI

1. Создать VLESS/Trojan inbound с transport `ws`.
2. Задать непустой уникальный site-shaped path, например `/assets/js/runtime-v2.js` или `/static/js/chunk-main.js`.
3. Если используется reverse proxy, направить этот path на Xray listener.
4. Client address — нейтральный Cloudflare hostname вроде `assets.example.com`, edge port обычно 443.
5. Security — TLS на edge; origin leg защищать `Full (strict)`.

Запрещено использовать path вроде `/ws`, `/vpn`, `/proxy`, `/vless` или `/xray`.

Nginx должен передавать upgrade:

```nginx
proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
proxy_set_header Host $host;
```

Это фрагмент; применить в правильном `location`.

## Проверка

```sh
curl -i --http1.1 \
  -H 'Connection: Upgrade' \
  -H 'Upgrade: websocket' \
  https://assets.example.com/assets/js/runtime-v2.js
```

Ответ зависит от Xray/reverse proxy; важны отсутствие обычного 404/redirect и logs handshake.

## Ошибки

- `404`: path/location mismatch.
- `400/426`: upgrade headers не переданы.
- `502`: reverse proxy не достигает Xray.
- Периодические disconnects: long-lived connection terminated; client reconnect должен работать.
- REALITY включен вместе с proxied WS: недопустимая архитектура.
- Path и hostname выглядят как transport label, а не как часть сайта.

## Источники

- [Cloudflare WebSockets](https://developers.cloudflare.com/network/websockets/)
- [3X-UI Wiki: reverse proxy/WebSocket examples](https://github.com/MHSanaei/3x-ui/wiki/Configuration)
- [3X-UI WS schema](https://github.com/MHSanaei/3x-ui/tree/v3.3.0/frontend/src/schemas)
