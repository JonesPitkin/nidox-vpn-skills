# Обзор архитектур

## DNS-only

Cloudflare отвечает DNS, но client подключается прямо к origin IP.

Использовать для:

- VLESS/Trojan + REALITY;
- raw TCP;
- Hysteria2/UDP;
- неподдерживаемых CDN ports/transports.

Origin IP виден клиенту; CDN/WAF/DDoS proxy protection не применяется.

## Proxied (orange-cloud)

Cloudflare завершает edge TLS и проксирует HTTP(S) к origin.

Использовать для:

- панели и subscription endpoint;
- WebSocket over TLS;
- gRPC over TLS при выполнении требований.

## Tunnel

`cloudflared` устанавливает outbound connection из origin в Cloudflare. Подходит для HTTP panel/subscription без public origin port. Arbitrary non-HTTP access требует отдельного Cloudflare Access/WARP/client-side design; не считать Tunnel прозрачной заменой Xray TCP/UDP listener.

## Выбор

1. REALITY или UDP? DNS-only/direct.
2. HTTP panel/WS/gRPC? Proxied либо Tunnel.
3. Нужен произвольный TCP через Cloudflare? Изучить Spectrum и тариф; standard proxy не подходит.

## Совместимость протоколов

VLESS/Trojan определяют application protocol, а Cloudflare видит transport. Они совместимы с CDN только через поддерживаемый HTTP transport. REALITY должен самостоятельно выполнять handshake с клиентом и потому несовместим с TLS termination стандартного proxy.

## Типовые ошибки

- Orange-cloud включен для REALITY hostname.
- Gray-cloud считается защитой origin.
- Panel и inbound используют один hostname/path без четкого reverse proxy routing.
- CDN применяется для Hysteria2, хотя нужен UDP.

## Источники

- [Cloudflare DNS proxy status](https://developers.cloudflare.com/dns/proxy-status/)
- [Cloudflare network ports](https://developers.cloudflare.com/fundamentals/reference/network-ports/)
- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [3X-UI Wiki Configuration](https://github.com/MHSanaei/3x-ui/wiki/Configuration)
