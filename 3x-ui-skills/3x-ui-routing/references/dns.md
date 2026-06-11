# DNS и DNS Routing

## Описание

Встроенный DNS Xray может выбирать сервер по доменам, проверять ожидаемые IP, управлять fallback/cache и предоставлять результаты routing engine. Это не системный resolver VPS, если конфигурация явно не направляет запросы через него.

## Поля актуальной панели

Global: `tag`, `hosts`, `servers`, `clientIp`, `queryStrategy`, `disableCache`, `disableFallback`, `disableFallbackIfMatch`, `enableParallelQuery`, `useSystemHosts`, `serveStale`, `serveExpiredTTL`.

Server object: `address`, `port`, `domains`, `expectedIPs`, `unexpectedIPs`, `skipFallback`, `finalQuery`, `tag`, `clientIP`, `queryStrategy`, `disableCache`, `timeoutMs`, `serveStale`, `serveExpiredTTL`.

## Пошаговая настройка

1. Определить policy: local/system DNS, public DoH/DoT/UDP или split DNS.
2. Добавить наиболее специфичный DNS server с `domains`.
3. При необходимости задать `expectedIPs`/`unexpectedIPs`.
4. Выбрать `queryStrategy`: `UseIP`, `UseIPv4`, `UseIPv6` или `UseSystem`.
5. Настроить fallback только после проверки основной ветки.
6. Если DNS traffic должен идти отдельным outbound, использовать DNS outbound/routing tag согласно Xray docs.
7. Перезапустить Xray и проверить query + route.

Пример server object:

```json
{
  "address": "https://1.1.1.1/dns-query",
  "port": 443,
  "domains": ["geosite:geolocation-!cn"],
  "queryStrategy": "UseIPv4",
  "timeoutMs": 4000,
  "tag": "dns-remote"
}
```

## Диагностика

```sh
getent ahosts example.com
dig A example.com
journalctl -u x-ui -n 200 --no-pager | grep -iE 'dns|timeout|fallback'
```

`dig` проверяет resolver ОС, а не обязательно DNS Xray. Для Xray использовать трафик тестового клиента и временный `dnsLog`, не оставляя избыточное логирование постоянно.

## Ошибки

- DoH hostname требует bootstrap DNS, но bootstrap не работает.
- `disableFallback` включен до проверки domain match.
- `UseIPv6` выбран на VPS без рабочего IPv6.
- DNS rule уходит через outbound, который сам требует DNS: цикл.
- В Podkop/FakeIP изменяется client-side DNS, но причина ищется только в 3X-UI.

## sing-box и Podkop

DNS schema sing-box отличается от Xray. Переносить policy вручную, а не копировать JSON. Podkop управляет DNS/FakeIP на OpenWrt отдельно; 3X-UI отвечает только за серверную часть.

## Источники

- [3X-UI DNS schema](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/schemas/dns.ts)
- [Xray DNS](https://xtls.github.io/en/config/dns.html)
- [sing-box DNS](https://sing-box.sagernet.org/configuration/dns/)
- [Podkop DNS](https://podkop.net/docs/dns/)
