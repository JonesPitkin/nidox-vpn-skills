# DNS Guide

## Теория

Актуальный блок DNS в `sing-box` включает:

```json
{
  "dns": {
    "servers": [],
    "rules": [],
    "final": "",
    "strategy": "",
    "disable_cache": false,
    "disable_expire": false,
    "independent_cache": false,
    "cache_capacity": 0,
    "reverse_mapping": false,
    "client_subnet": "",
    "fakeip": {}
  }
}
```

Ключевые идеи:

- `servers` задают, куда реально уходят запросы;
- `rules` выбирают сервер или действие по условиям;
- `final` задаёт сервер по умолчанию;
- `strategy` влияет на IPv4/IPv6-предпочтение;
- `domain_resolver` в Dial Fields теперь важен для доменных outbounds и endpoints.

Замечание по версии:

- в alpha-документации `1.14.0` есть дополнительные DNS-поля;
- baseline этого репозитория для stable `1.13.13` их не делает обязательными.

## Поддерживаемые DNS server типы

По официальной документации стоит ориентироваться на:

- `local`
- `https` (DoH)
- `tls` (DoT)
- `quic`
- `http3`
- `udp`
- `tcp`
- `resolved`
- `dhcp`
- `hosts`
- `fakeip`
- `mdns`
- `tailscale`

## Практика: локальный DNS + DoH + split

```json
{
  "dns": {
    "servers": [
      {
        "tag": "local",
        "type": "local"
      },
      {
        "tag": "doh-remote",
        "type": "https",
        "server": "1.1.1.1",
        "server_port": 443,
        "path": "/dns-query",
        "tls": {
          "enabled": true,
          "server_name": "cloudflare-dns.com"
        }
      }
    ],
    "rules": [
      {
        "domain_suffix": [
          ".lan",
          ".local"
        ],
        "action": "route",
        "server": "local"
      }
    ],
    "final": "doh-remote",
    "strategy": "prefer_ipv4",
    "reverse_mapping": true,
    "cache_capacity": 8192
  }
}
```

## Практика: FakeIP для TUN

Идея схемы:

- DNS-запросы клиентов приходят в `sing-box`;
- домены, которые должны маршрутизироваться по доменному правилу даже после connect, получают FakeIP;
- `reverse_mapping` помогает обратному связыванию IP с доменом;
- route rules затем работают по домену и/или rule set.

Минимальный пример:

```json
{
  "dns": {
    "servers": [
      {
        "tag": "fakeip-dns",
        "type": "fakeip",
        "inet4_range": "198.18.0.0/15",
        "inet6_range": "fc00::/18"
      },
      {
        "tag": "upstream",
        "type": "https",
        "server": "1.1.1.1",
        "server_port": 443,
        "path": "/dns-query",
        "tls": {
          "enabled": true,
          "server_name": "cloudflare-dns.com"
        }
      }
    ],
    "rules": [
      {
        "domain_suffix": [
          ".lan"
        ],
        "action": "route",
        "server": "upstream"
      }
    ],
    "final": "fakeip-dns",
    "reverse_mapping": true
  }
}
```

## DNS leak prevention

Практические правила из официальной модели:

- при TUN включать DNS-путь через `sing-box`, а не оставлять системный DNS без контроля;
- использовать `domain_resolver` для доменных outbounds;
- не смешивать маршрутизацию трафика через proxy с резолвингом через случайный системный DNS;
- проверять, какой `dns.final` реально используется;
- для split DNS разделять локальные и внешние домены через `dns.rules`.

## Domain Resolver

С версии `1.12.0` официальная документация продвигает `domain_resolver` в Dial Fields. Это нужно, когда outbound или endpoint использует доменное имя. Если resolver не задан и DNS topology сложная, возникает типичный сбой: proxy не поднимается, хотя клиентский DNS визуально работает.

## Типовые ошибки

- `cache_capacity` меньше `1024` игнорируется.
- старые outbound DNS rules продолжают жить после миграции.
- FakeIP настроен, но TUN не перехватывает DNS-запросы.
- включён `reverse_mapping`, но платформа кеширует DNS вне контроля `sing-box`, что особенно заметно на macOS.

## Диагностика

- Проверить `dns.final`.
- Проверить, какой server tag выбирается по `dns.rules`.
- Проверить `domain_resolver` у проблемного outbound.
- Убедиться, что нет deprecated DNS server format.
- Если используется FakeIP, проверить, что диапазон не конфликтует с реальной сетью и что route rules рассчитаны на такую схему.

## Рекомендации

- Для новых конфигов сразу задавать `timeout` и `cache_capacity`.
- Для сложных конфигов использовать `evaluate` и `respond` в DNS rules только там, где реально нужен match по ответу.
- Для OpenWrt и transparent proxy держать DNS и routing как единую схему, а не как независимые куски.
