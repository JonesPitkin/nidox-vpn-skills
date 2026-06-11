# Диагностика Cloudflare

## Метод

Проверять по слоям:

1. DNS record/proxy status.
2. Cloudflare edge TLS.
3. Edge-to-origin TCP.
4. Origin TLS/SNI/certificate.
5. Reverse proxy Host/path/HTTP2/upgrade.
6. Xray transport/client fields.

## 522 Connection timed out

Cloudflare не завершил TCP connection к origin.

Проверить:

- origin online и правильный IP;
- port слушает;
- firewall разрешает Cloudflare IP ranges;
- service не перегружен;
- Origin Rule port/host.

```sh
ss -lntp
journalctl -u nginx -n 200 --no-pager
```

## 525 SSL handshake failed

Возникает в `Full`/`Full (strict)`, когда edge не завершил TLS с origin.

Проверить TLS listener, SNI, ciphers/protocols, certificate/key pair и origin logs.

## 526 Invalid SSL certificate

Обычно `Full (strict)`: expired/untrusted certificate, hostname mismatch или incomplete chain. Установить корректный public CA/Origin CA certificate; не оставлять `Full` как постоянный обход.

## WebSocket errors

- 404: path.
- 400/426: Upgrade headers.
- 502: upstream.
- 101 затем disconnect: logs/timeouts/network change.

## gRPC errors

Проверить port 443, HTTP/2 ALPN, gRPC toggle, service name, content-type и origin h2.

## REALITY не подключается

Если DNS record proxied, переключить на DNS-only/direct. Standard Cloudflare TLS termination несовместим с REALITY handshake.

## Команды

```sh
dig +short <host>
curl -vkI https://<host>/<path>/
openssl s_client -connect <origin-ip>:443 -servername <host> -alpn h2 </dev/null
journalctl -u x-ui -n 200 --no-pager
```

## Источники

- [Cloudflare Error 522](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-522/)
- [Cloudflare Error 525](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-525/)
- [Cloudflare Error 526](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-526/)
- [Cloudflare WebSockets](https://developers.cloudflare.com/network/websockets/)
- [Cloudflare gRPC](https://developers.cloudflare.com/network/grpc-connections/)
