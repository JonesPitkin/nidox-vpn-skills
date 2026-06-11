# TCP / Raw

## Описание

`network=tcp` — прямой Xray stream. 3X-UI называет форму Raw и хранит `tcpSettings`. Header может быть `none` или HTTP/1.1 camouflage.

## Когда использовать

- VLESS REALITY Vision baseline;
- VLESS/Trojan TCP TLS;
- минимальная latency и меньше движущихся частей;
- direct endpoint без CDN.

## Преимущества

- простота и производительность;
- Vision доступен только здесь;
- меньше path/host/reverse proxy ошибок.

## Недостатки

- raw traffic/IP легче блокировать;
- HTTP camouflage не является настоящим HTTPS;
- обычный CDN не проксирует arbitrary raw TCP.

## Требования

- открытый TCP port;
- direct reachability или L4 proxy;
- совпадающие security и header type;
- TCP + TLS/REALITY для Vision.

## Настройка в панели

Transport `TCP (Raw)`:

- `acceptProxyProtocol=false`, если нет trusted L4 proxy;
- HTTP camouflage выключен для REALITY/Vision baseline;
- при включении HTTP header синхронизировать path/Host с клиентом.

```json
"streamSettings": {
  "network": "tcp",
  "tcpSettings": {"header": {"type": "none"}},
  "security": "reality"
}
```

## Настройка клиента

`type=tcp`; для no header `headerType` отсутствует/`none`. Для HTTP camouflage нужны `headerType=http`, path и host.

sing-box не моделирует отдельный TCP V2Ray transport: plain connection задается без `transport`.

## Типовые ошибки

- port closed/occupied;
- HTTP header enabled только на одной стороне;
- PROXY protocol enabled без sender;
- Vision указан при security none.

## Диагностика

```sh
nc -vz <server> <port>
ss -lntp | grep ':<port> '
tcpdump -ni any port <port>
```

Если SYN не приходит — сеть/firewall. Если TCP established и handshake падает — protocol/security fields.

## Источники

- [TCP schema](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/schemas/protocols/stream/tcp.ts)
- [Raw form](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/pages/inbounds/form/transport/raw.tsx)
- [Transport link generation](https://github.com/MHSanaei/3x-ui/blob/main/sub/subService.go)
