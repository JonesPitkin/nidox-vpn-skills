---
name: 3x-ui-routing
description: Проектировать, настраивать, проверять и диагностировать Xray routing, DNS, geosite, geoip, direct/proxy/block outbounds и balancers в 3X-UI. Использовать для серверного split tunneling, WARP/VPN-маршрутов, блокировки private/BitTorrent, выбора domainStrategy, загрузки geofiles, DNS routing, балансировки и согласования правил с sing-box или Podkop.
---

# 3X-UI Routing

Работать только с инфраструктурой, которой пользователь вправе управлять. Считать routing server-side политикой Xray на VPS: она не заменяет правила на клиенте, OpenWrt, sing-box или Podkop.

## Рабочий процесс

1. Зафиксировать версии 3X-UI/Xray, текущие inbounds, outbounds, routing rules, DNS и geofiles.
2. Сохранить backup БД и экспорт Xray settings.
3. Сформулировать требуемый путь каждого класса трафика: `direct`, конкретный proxy/VPN outbound, balancer или `block`.
4. Проверить существование всех `inboundTag`, `outboundTag`, `balancerTag` и geosite/geoip списков.
5. Добавлять правила от частных к общим. Первое совпавшее routing rule определяет действие.
6. Для доменных правил выбрать `domainStrategy` осознанно; не включать IP resolution без необходимости.
7. После сохранения перезапустить Xray и проверить журнал, DNS и фактический внешний IP.

## Навигация

- Общая модель и `domainStrategy`: [references/routing.md](references/routing.md)
- Встроенный DNS Xray и DNS routing: [references/dns.md](references/dns.md)
- Доменные наборы: [references/geosite.md](references/geosite.md)
- IP-наборы: [references/geoip.md](references/geoip.md)
- Поля и порядок правил: [references/rules.md](references/rules.md)
- `direct` / `proxy` / `block`: [references/direct-proxy-block.md](references/direct-proxy-block.md)
- Balancers: [references/balancer.md](references/balancer.md)
- Диагностика: [references/troubleshooting.md](references/troubleshooting.md)

## Обязательные проверки

```sh
x-ui status
x-ui restart-xray
journalctl -u x-ui -n 200 --no-pager
ss -lntup
```

Проверить:

- Xray принимает конфигурацию без `failed to load config`;
- теги в rules существуют;
- нужный домен разрешается ожидаемым DNS server;
- тестовый запрос выходит через ожидаемый public IP;
- block rule действительно блокирует, а не отправляет direct;
- после restart порядок rules и geofile aliases сохраняется.

## Правила безопасности

- Не отправлять private/metadata IP через внешний proxy без явной причины.
- Не публиковать proxy credentials, WARP keys, VPN configs и полный Xray JSON.
- Не создавать catch-all rule до правил панели/API, DNS и исключений.
- `outboundTag` и `balancerTag` не задавать одновременно: текущий UI предупреждает, что `outboundTag` получает приоритет.
- Не переносить `geosite:` напрямую в современный sing-box: с 1.12 legacy geosite удален, нужны rule-sets.
- Для Podkop настраивать client-side policy в Podkop отдельно; серверные rules 3X-UI не экспортируются в него автоматически.

## Обязательный аудит детекта

Перед выдачей финального решения обязательно использовать репозиторий:

- `nidox-vpn-detection-defense-skill`

Проверять:

- GeoIP
- ASN
- hosting
- IP reputation
- DNS
- маршрутизацию
- MTU
- Android признаки VPN
- iOS признаки VPN
- ложноположительные срабатывания
- ограничения методики

Использовать также:

- `references/required-skills.md`
- `references/final-report-template.md`
- `skill-entrypoint.md`

## Mandatory VPN Detection Audit

Before any final recommendation, deployment guide, troubleshooting procedure, architecture review, routing analysis or VPN assessment related to VPN, Proxy, VLESS, Reality, Xray, sing-box, Cloudflare, CDN, Podkop or OpenWrt, the assistant MUST invoke:

nidox-vpn-detection-defense-skill

The final answer MUST include:

Проверка на признаки детекта

## Актуальность

Проверено 2026-06-07 по 3X-UI release `v3.2.8`, repository commit `483952cfa0333a051f78c3aedf37f4c25945042a`, Wiki commit `264a7b202aacc0036a1fbb95a285d3e2981a3578` и bundled Xray-core `94ffd50060f1`.
