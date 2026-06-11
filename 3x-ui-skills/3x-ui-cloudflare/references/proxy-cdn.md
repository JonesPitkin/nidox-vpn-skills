# Cloudflare Proxy и CDN

## Поддерживаемые HTTP ports

Официально proxied:

- HTTP: `80`, `8080`, `8880`, `2052`, `2082`, `2086`, `2095`;
- HTTPS: `443`, `2053`, `2083`, `2087`, `2096`, `8443`.

Другие ports требуют DNS-only или Spectrum. Для gRPC использовать `443`.

## Настройка

1. Выбрать supported edge port.
2. На origin запустить reverse proxy/Xray transport.
3. Включить orange-cloud.
4. Настроить origin certificate и `Full (strict)`.
5. Ограничить origin firewall Cloudflare source ranges, если direct access не нужен.
6. Проверить path/Host/SNI.

## Ограничения

- standard proxy работает на HTTP layer;
- arbitrary TCP/UDP не поддерживается;
- limits на request size/timeouts и product availability зависят от plan;
- long-lived connections могут разрываться при Cloudflare network changes;
- cache не должен применяться к panel/API/WS/gRPC paths.

## Сценарии

- Panel: proxied HTTPS reverse proxy.
- Subscription: отдельный path/hostname без cache.
- VLESS/Trojan WS: proxied HTTPS.
- REALITY/raw TCP/Hysteria2: DNS-only.

## Ошибки

- Origin port не входит в supported list.
- Firewall блокирует Cloudflare IP.
- Cache Rule кэширует subscription.
- Client подключается к origin port вместо edge port.

## Источники

- [Cloudflare network ports](https://developers.cloudflare.com/fundamentals/reference/network-ports/)
- [Cloudflare cache](https://developers.cloudflare.com/cache/)
- [Cloudflare IP ranges](https://www.cloudflare.com/ips/)
