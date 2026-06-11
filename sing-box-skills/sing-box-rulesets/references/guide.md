# Rule Sets Guide

## Почему rule_set

С `1.8.0` rule sets стали официальным путём, а `GeoIP` и `Geosite` были задепрекейчены и затем удалены из актуального path в `1.12.0`.

Практическое правило:

- новая конфигурация: только `rule_set`;
- legacy конфигурация: мигрировать.

## Варианты

### Inline

Подходит для:

- маленьких политик;
- встроенных headless rules;
- случаев, где не нужен внешний файл.

### Local

Подходит для:

- version-controlled локальных наборов;
- офлайн-эксплуатации;
- OpenWrt/Linux server deployments.

### Remote

Подходит для:

- централизованного обновления;
- повторного использования одной политики многими инстансами.

## Форматы

- `source`
- `binary`

Практически:

- `binary` удобен для production distribution;
- `source` лучше читаем при разработке и ревью.

## Пример local rule set

```json
{
  "route": {
    "rule_set": [
      {
        "type": "local",
        "tag": "corp",
        "format": "source",
        "path": "/etc/sing-box/rules/corp.json"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "corp"
        ],
        "action": "route",
        "outbound": "direct"
      }
    ]
  }
}
```

## Пример remote rule set

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "streaming",
        "format": "binary",
        "url": "https://example.invalid/streaming.srs",
        "update_interval": "1d"
      }
    ]
  },
  "experimental": {
    "cache_file": {
      "enabled": true
    }
  }
}
```

## Обновление наборов правил

Практические моменты по официальной документации:

- remote rule set обновляется по `update_interval`;
- кэширование опирается на `experimental.cache_file.enabled`;
- в stable `1.13.13` используется `download_detour`;
- в official mainline уже документируется будущий переход к `http_client`, но это не baseline для текущего stable.

## Migrating from Geosite

Официальная migration-страница показывает новый путь:

- `route.rules[].geosite` -> `route.rules[].rule_set`
- `route.geosite` -> `route.rule_set[]`

При этом документация прямо упоминает URL вида:

- `https://raw.githubusercontent.com/SagerNet/sing-geosite/rule-set/geosite-cn.srs`

Важно:

- это migration reference;
- для нового материала не возвращаться к старым `geosite` полям;
- `sing-geosite` полезен как официальный источник rule-set артефактов и конвертации custom geosite.

## Типовые ошибки

- объявлен `rule_set`, но правило ссылается на другой `tag`;
- remote rule set не кэшируется, хотя ожидается offline reuse;
- используется deprecated `download_detour`;
- новые конфиги продолжают содержать `geosite`/`geoip`.

## Рекомендации

- хранить naming policy для `tag`;
- по умолчанию выбирать `rule_set` как reusable слой политик;
- перед релизом проверять, что в конфиге нет legacy route fields.
