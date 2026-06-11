# gRPC

## Описание

`network=grpc` использует HTTP/2-style gRPC transport. Поля: `serviceName`, `authority`, `multiMode`.

## Когда использовать

- HTTP/2 reverse proxy;
- direct TLS или REALITY;
- инфраструктура, где gRPC end-to-end поддержан.

## Преимущества

- компактная форма;
- поддерживает REALITY в 3X-UI;
- sing-box имеет официальный gRPC transport;
- может работать за reverse proxy с корректным HTTP/2.

## Недостатки

- CDN/proxy может не поддерживать gRPC;
- serviceName mismatch ломает соединение;
- HTTP/2 timeout/keepalive policy может обрывать idle streams;
- Vision недоступен, так как transport не TCP Raw.

## Требования

- HTTP/2 end-to-end или direct REALITY;
- одинаковый `serviceName`;
- proxy/CDN с gRPC support;
- актуальный client core.

## Настройка в панели

1. Transport `gRPC`.
2. `serviceName`: непустое согласованное имя.
3. `authority`: только если требуется virtual host.
4. `multiMode`: включать после baseline test.
5. Security TLS или REALITY.

## Настройка клиента

3X-UI share link передает `serviceName`, `authority`, `mode=multi`.

sing-box:

```json
"transport": {
  "type": "grpc",
  "service_name": "<service>"
}
```

## Типовые ошибки

- `UNIMPLEMENTED`/404: proxy routing не попал в service;
- HTTP/1.1 upstream вместо h2;
- serviceName URL-encoded или потерян;
- multiMode unsupported client.

## Диагностика

Проверить ALPN:

```sh
openssl s_client -connect <host>:443 -servername <sni> -alpn h2 </dev/null
```

Тестировать direct backend, затем reverse proxy/CDN. Отключить multiMode.

## Источники

- [gRPC schema](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/schemas/protocols/stream/grpc.ts)
- [3X-UI capability matrix](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/lib/xray/protocol-capabilities.ts)
- [3X-UI share links](https://github.com/MHSanaei/3x-ui/blob/main/sub/subService.go)
- [sing-box gRPC](https://sing-box.sagernet.org/configuration/shared/v2ray-transport/)
