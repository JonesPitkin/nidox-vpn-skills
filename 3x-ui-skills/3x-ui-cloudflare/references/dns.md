# Cloudflare DNS

## Proxy status

- Proxied A/AAAA/CNAME возвращает Cloudflare anycast IP и включает HTTP proxy.
- DNS-only возвращает origin record и не проксирует traffic.

## Пошаговая настройка

1. Создать отдельные hostnames по назначению:
   - `panel.example.com` — proxied/Tunnel;
   - `ws.example.com` — proxied;
   - `reality.example.com` — DNS-only.
2. Создать A/AAAA/CNAME на origin.
3. Выбрать proxy status по transport.
4. Подождать TTL и проверить authoritative answer.
5. Проверить origin отдельно через IP + SNI.

```sh
dig A panel.example.com
dig AAAA panel.example.com
dig CNAME panel.example.com
```

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

Сравнить ответы нескольких resolvers и Cloudflare dashboard. Для proxied record отсутствие origin IP в публичном ответе ожидаемо.

## Источники

- [Cloudflare proxy status](https://developers.cloudflare.com/dns/proxy-status/)
- [Cloudflare DNS records](https://developers.cloudflare.com/dns/manage-dns-records/)
- [3X-UI Wiki: Cloudflare SSL](https://github.com/MHSanaei/3x-ui/wiki/Configuration)
