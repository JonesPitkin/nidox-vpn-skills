# Routing Guide

## Теория

Актуальный `route` блок включает:

- `rules`
- `rule_set`
- `final`
- `auto_detect_interface`
- `default_interface`
- `default_mark`
- `find_process`
- `default_domain_resolver`

Это означает, что routing в `sing-box` уже не только про `domain -> outbound`, а про полный policy engine.

## Match-категории

Официальные route rules покрывают:

- `domain`, `domain_suffix`, `domain_keyword`, `domain_regex`
- `ip_cidr`, `ip_is_private`
- `source_ip_cidr`, `source_ip_is_private`
- `source_port`, `port`, диапазоны портов
- `process_name`, `process_path`, `package_name`, `user`, `user_id`
- `network`, `protocol`, `client`
- `network_type`, `wifi_ssid`, `wifi_bssid`
- `rule_set`

## Final outbound

`route.final` задаёт default outbound tag. Если правила не совпали, трафик идёт сюда.

Практически:

- `final: direct` нужен для bypass-first схем;
- `final: proxy` нужен для full-tunnel/proxy-first схем;
- `final: block` обычно опасен без очень продуманного ruleset.

## Реальный сценарий: selective proxying

```json
{
  "route": {
    "rule_set": [
      {
        "tag": "streaming",
        "type": "remote",
        "format": "binary",
        "url": "https://example.invalid/streaming.srs"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "streaming"
        ],
        "action": "route",
        "outbound": "proxy"
      },
      {
        "ip_is_private": true,
        "action": "route",
        "outbound": "direct"
      }
    ],
    "final": "direct"
  }
}
```

## Реальный сценарий: split tunneling

Цель:

- локальные сети напрямую;
- целевые домены через proxy;
- всё остальное напрямую.

Подход:

- LAN через `ip_is_private` или `route_exclude_address`;
- домены через `rule_set` или `domain_suffix`;
- `final: direct`.

## Реальный сценарий: proxy-first

Цель:

- почти всё через proxy;
- отдельные bypass для локальной инфраструктуры.

Подход:

```json
{
  "route": {
    "rules": [
      {
        "ip_is_private": true,
        "action": "route",
        "outbound": "direct"
      },
      {
        "domain_suffix": [
          ".lan"
        ],
        "action": "route",
        "outbound": "direct"
      }
    ],
    "final": "proxy"
  }
}
```

## Route actions

Ключевые действия:

- `route`
- `bypass`
- `reject`
- `hijack-dns`
- `route-options`

Особенности:

- `bypass` работает только на Linux с `auto_redirect` и нужен для pre-match bypass на kernel level.
- `reject` применим и к ICMP в новых версиях.
- `hijack-dns` отправляет DNS-запросы в DNS-модуль `sing-box`.

## Process matching

Полезно для desktop и некоторых router-сценариев, но надо помнить:

- поиск процесса зависит от платформы;
- на некоторых системах его лучше включать осознанно;
- путь процесса на Windows имеет отдельные migration-особенности.

## Типовые ошибки

- `rule_set` использован, но не объявлен в `route.rule_set`.
- ожидание, что `bypass` будет работать без `auto_redirect`.
- отсутствие `default_domain_resolver` в маршрутизации с доменными upstreams.
- слишком общие `domain_suffix` раньше более точных правил.
- смешение deprecated `geosite`/`geoip` с современными `rule_set`.

## Рекомендации

- сначала писать исключения и bypass, потом широкий proxy-path;
- для прозрачных схем связывать route rules с DNS strategy и TUN;
- использовать `rule_set` как reusable policy-layer.
