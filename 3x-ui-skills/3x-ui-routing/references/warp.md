# Cloudflare WARP Outbound

## 3X-UI v3.3.0

3X-UI поддерживает создание WARP outbound и manual/automatic WARP IP rotation. API requests ротации проходят через panel proxy.

WARP здесь является egress WireGuard path, а не Cloudflare orange-cloud proxy перед inbound.

## Рабочий процесс

1. Создать WARP profile в `Xray Configs → Outbounds → WARP`.
2. Добавить outbound с уникальным tag.
3. Создать routing rules только для нужных destinations.
4. Проверить egress IP через тестовый домен.
5. Настроить rotation schedule только после стабильного baseline.
6. После rotation повторно проверить доступность, IPv4/IPv6 и rules.

## Ограничения

- WARP IP не фиксирован и может менять геолокацию/reputation.
- Rotation не гарантирует обход 403.
- Routing всего трафика через WARP увеличивает blast radius.
- Не публиковать WireGuard keys/profile.
- В sing-box 1.13 собственный WireGuard path моделировать endpoint-ом, а не legacy outbound.

## Источники

- [3X-UI v3.3.0 release](https://github.com/MHSanaei/3x-ui/releases/tag/v3.3.0)
- [3X-UI Wiki WARP](https://github.com/MHSanaei/3x-ui/wiki/Advanced#setting-cloudflare-warp)
- [3X-UI Wiki WARP routing](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems#11-some-sites-dont-open-for-me-what-is-warp-and-how-do-i-use-it)
