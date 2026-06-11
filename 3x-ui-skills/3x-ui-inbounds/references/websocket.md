# WebSocket

## Описание

`network=ws` переносит proxy stream через WebSocket. Поля 3X-UI: path, host, headers, heartbeatPeriod, acceptProxyProtocol.

## Когда использовать

- TLS reverse proxy;
- CDN, который поддерживает WebSocket;
- один domain/443 с path routing;
- широкая legacy client compatibility.

## Преимущества

- хорошо поддержан reverse proxies и клиентами;
- удобно маршрутизировать по path;
- может проходить через CDN.

## Недостатки

- overhead и HTTP fingerprint;
- path/Host легко рассинхронизировать;
- CDN видит edge traffic, IP limit получает edge IP без real-IP/proxy setup;
- текущий Xray ecosystem мигрирует часть use cases к XHTTP.

## Требования

- domain и TLS для public deployment;
- reverse proxy/CDN с WebSocket Upgrade;
- одинаковые path и Host;
- опубликованный origin port.

## Настройка в панели

1. Protocol VLESS/Trojan.
2. Transport WebSocket.
3. Security TLS при public endpoint.
4. Уникальный path, например `/api/v2`.
5. Host = public domain.
6. Reverse proxy должен передавать Upgrade/Connection.

```nginx
location /api/v2 {
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_pass http://127.0.0.1:<inbound-port>;
}
```

Не использовать REALITY: 3X-UI capability matrix не разрешает REALITY+WS.

## Настройка клиента

- `type=ws`;
- тот же path и Host;
- TLS SNI = public domain;
- sing-box transport `type: ws`, `path`, headers;
- v2rayNG/Shadowrocket обычно импортируют WS links, но сверить Host/path.

## Типовые ошибки

- HTTP 404: wrong path/location;
- 400/426: Upgrade headers потеряны;
- TLS succeeds, proxy fails: backend path/port;
- CDN 521/522: origin недоступен;
- IP limit банит CDN edges.

## Диагностика

```sh
curl -vk https://<domain>/<path>
nginx -t
journalctl -u nginx -n 100 --no-pager
journalctl -u x-ui -n 150 --no-pager
```

Проверить origin напрямую до подключения CDN.

## Источники

- [WS schema](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/schemas/protocols/stream/ws.ts)
- [WS fixture](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/test/golden/fixtures/inbound-full/vless-ws-tls.json)
- [Wiki reverse proxy](https://github.com/MHSanaei/3x-ui/wiki/Configuration#reverse-proxy)
- [sing-box V2Ray transports](https://sing-box.sagernet.org/configuration/shared/v2ray-transport/)
