# gRPC через Cloudflare

## Требования Cloudflare

- hostname proxied;
- TLS;
- edge port `443`;
- HTTP/2;
- request content type `application/grpc`;
- gRPC enabled в Network settings.

## Настройка

1. В 3X-UI создать VLESS/Trojan inbound с transport `grpc`.
2. Задать service name.
3. Настроить TLS/reverse proxy на origin с HTTP/2.
4. Включить orange-cloud и Cloudflare gRPC.
5. Client: address Cloudflare hostname, port 443, TLS/SNI public hostname, тот же service name.
6. Использовать `Full (strict)`.

## Reverse proxy

Конкретная Nginx/Caddy directive зависит от того, принимает ли origin native gRPC/h2 и как Xray слушает порт. Не заменять `grpc_pass` обычным WebSocket proxy snippet.

## Ошибки

- gRPC toggle выключен.
- Origin обслуживает только HTTP/1.1.
- Service name mismatch.
- Content type/path изменен промежуточным proxy.
- Edge port не 443.
- Client пытается REALITY через Cloudflare gRPC endpoint.

## Диагностика

```sh
curl -I --http2 https://grpc.example.com/
openssl s_client -connect <origin-ip>:443 -servername grpc.example.com -alpn h2 </dev/null
journalctl -u x-ui -n 200 --no-pager | grep -iE 'grpc|http2|transport|error'
```

`curl -I` не выполняет полноценный gRPC call, но проверяет TLS/HTTP2 layer.

## Источники

- [Cloudflare gRPC](https://developers.cloudflare.com/network/grpc-connections/)
- [3X-UI gRPC inbound source](https://github.com/MHSanaei/3x-ui/tree/main/frontend/src/pages/inbounds)
- [Xray gRPC transport](https://xtls.github.io/en/config/transports/grpc.html)
