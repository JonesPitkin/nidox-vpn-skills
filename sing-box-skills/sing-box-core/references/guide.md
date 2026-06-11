# Core Guide

## Назначение

`sing-box` в официальной документации позиционируется как universal proxy platform. Практически это движок, который:

- принимает трафик через `inbounds`;
- обрабатывает DNS через отдельный DNS-модуль;
- принимает решения через `route.rules` и `route.rule_set`;
- отправляет трафик через `outbounds` и современные `endpoints`;
- использует общие поля `dial`, `tls`, `listen`, `transport`, `multiplex`.

## Актуальная структура конфигурации

Официальный индекс конфигурации показывает полный корневой JSON:

```json
{
  "log": {},
  "dns": {},
  "ntp": {},
  "certificate": {},
  "certificate_providers": [],
  "http_clients": [],
  "endpoints": [],
  "inbounds": [],
  "outbounds": [],
  "route": {},
  "services": [],
  "experimental": {}
}
```

Вывод: если агент видит старые гайды только с `inbounds/outbounds/route`, это уже неполная модель.

## Основные компоненты

- `log`: уровень и формат логирования.
- `dns`: DNS servers, rules, FakeIP и резолвинг для outbounds.
- `ntp`: встроенный NTP-клиент.
- `certificate` и `certificate_providers`: TLS-материалы и провайдеры сертификатов.
- `http_clients`: транспорт для remote rule sets и сервисных HTTP-запросов.
- `endpoints`: современные endpoint-типы, включая актуальный WireGuard endpoint.
- `inbounds`: точки входа трафика.
- `outbounds`: direct/block/dns/proxy-логика выхода.
- `route`: route rules, rule_set, final outbound, auto-detection.
- `services`: служебные runtime-сервисы.
- `experimental`: cache file, Clash API, V2Ray API.

## log

Практический смысл:

- задаёт verbosity и формат логов;
- нужен первым при любой диагностике;
- для production лучше начинать с `info`, для сложной отладки временно поднимать уровень.

Базовый пример:

```json
{
  "log": {
    "level": "info"
  }
}
```

Типовые ошибки:

- слишком тихий лог при диагностике сложного TUN/DNS сценария;
- постоянный debug-log в production.

## ntp

Практический смысл:

- встроенный NTP-клиент полезен, когда конфиг или transport чувствительны к времени;
- особенно важно помнить про это в TLS/REALITY-сценариях, где сильный time drift может давать ложные сетевые симптомы.

Базовый подход:

- включать только когда реально нужен контролируемый time source;
- проверять, не конфликтует ли это с системной политикой времени.

## experimental

В stable-линии особенно важны:

- `cache_file`
- Clash API и V2Ray API, если они реально используются

Практический пример для remote rule sets:

```json
{
  "experimental": {
    "cache_file": {
      "enabled": true
    }
  }
}
```

Типовые ошибки:

- ожидание, что remote rule set будет жить локально без cache file;
- включение experimental-подсистем без operational причины.

## Жизненный цикл конфигурации

1. Подготовка JSON.
2. Форматирование:
   ```bash
   sing-box format -w -c config.json -D config_directory
   ```
3. Проверка:
   ```bash
   sing-box check -c config.json -D config_directory
   ```
4. При split-конфигурации:
   ```bash
   sing-box merge output.json -c config.json -D config_directory
   ```
5. Запуск:
   ```bash
   sing-box run -c config.json -D config_directory
   ```

## Практический базовый шаблон

```json
{
  "log": {
    "level": "info"
  },
  "dns": {
    "servers": [
      {
        "tag": "local-dns",
        "type": "local"
      }
    ],
    "final": "local-dns"
  },
  "inbounds": [
    {
      "type": "mixed",
      "tag": "mixed-in",
      "listen": "127.0.0.1",
      "listen_port": 2080
    }
  ],
  "outbounds": [
    {
      "type": "direct",
      "tag": "direct"
    },
    {
      "type": "block",
      "tag": "block"
    }
  ],
  "route": {
    "final": "direct"
  }
}
```

## Проверка и отладка запуска

- `check` ловит структурные ошибки и часть несовместимостей.
- `format` полезен перед ревью: проще замечать лишние поля и старый синтаксис.
- если ошибка связана с DNS server format, ECH, `domain_strategy`, `geosite`, `geoip`, TUN old fields, надо сверяться с `migration` и `deprecated`.

## Типовые ошибки

- Использование `geosite` или `geoip` в новой конфигурации.
- Старые TUN поля `inet4_address`, `inet6_address`, `inet4_route_address`.
- Использование outbound DNS rules вместо `domain_resolver`.
- Попытка трактовать WireGuard как старый outbound, хотя текущая документация ведёт к `endpoint/wireguard`.
- Отсутствие `experimental.cache_file.enabled` при ожидании кэширования remote rule sets.

## Рекомендации

- Держать `route.rule_set` и `dns.rules` как first-class конфигурацию, а не как дополнение.
- Для доменных outbounds заранее задавать `domain_resolver` или `route.default_domain_resolver`.
- Перед миграцией между версиями всегда открывать `deprecated` и нужный раздел в `migration`.
