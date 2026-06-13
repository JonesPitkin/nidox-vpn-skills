# Cloudflare DNS

## Proxy status

- Proxied A/AAAA/CNAME возвращает Cloudflare anycast IP и включает HTTP proxy.
- DNS-only возвращает origin record и не проксирует traffic.

## Пошаговая настройка

1. Создать отдельные hostnames по назначению:
   - `content.example.com` — proxied/Tunnel только для защищенного admin/subscription HTTP service за hidden path и Access/IP restriction;
   - `assets.example.com` — proxied для site-shaped HTTP transport;
   - `files.example.com` — DNS-only для direct endpoint, если transport не должен идти через CDN.
2. Создать A/AAAA/CNAME на origin.
3. Выбрать proxy status по transport.
4. Подождать TTL и проверить authoritative answer.
5. Проверить origin отдельно через IP + SNI.

```sh
dig A content.example.com
dig AAAA content.example.com
dig CNAME content.example.com
```

Не использовать как дефолт:

- `vpn.*`
- `proxy.*`
- `ws.*`
- `panel.*`
- `admin.*`

## DNS challenge для сертификата

3X-UI поддерживает Cloudflare DNS validation в certificate management. Предпочитать scoped API Token:

- permission `Zone:DNS:Edit`;
- resource только нужная zone.

Не оставлять token в shell history, screenshots или repository.

## Ошибки

- Старый AAAA ведет на другой server.
- REALITY record случайно proxied.
- Origin IP изменен, DNS record нет.
- CAA запрещает выбранный CA.
- Split-horizon/local DNS возвращает другой address.

## Проверка

Сравнить ответы нескольких resolvers и Cloudflare dashboard. Для proxied record отсутствие origin IP в публичном ответе ожидаемо. Дополнительно проверить, что нет лишних `A`/`AAAA`/`CNAME`, раскрывающих origin в соседних hostname.

## Источники

- [Cloudflare proxy status](https://developers.cloudflare.com/dns/proxy-status/)
- [Cloudflare DNS records](https://developers.cloudflare.com/dns/manage-dns-records/)
- [3X-UI Wiki: Cloudflare SSL](https://github.com/MHSanaei/3x-ui/wiki/Configuration)
