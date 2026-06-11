---
name: sing-box-core
description: "Production skill по архитектуре sing-box: назначение, жизненный цикл конфигурации, структура root JSON, запуск, check/format/merge, migration-aware review и эксплуатация на Linux, OpenWrt, VPS и в sing-box-совместимых экосистемах. Использовать при старте проекта, ревью, миграции и первичной диагностике."
---

# sing-box Core

Этот skill является базовым production-entrypoint для всей базы `sing-box-skills`. Его задача не в том, чтобы повторить слово в слово официальную документацию, а в том, чтобы научить AI-агента и инженера читать, проектировать и сопровождать `sing-box` без архитектурных ошибок, с жёсткой привязкой к официальным источникам и к версионной реальности.

В этом skill нужно мыслить как Senior Proxy Engineer: не отдельным transport-полем, не отдельным DNS-сервером и не одним красивым JSON, а целостной системой. Любой production deployment на `sing-box` состоит из пяти слоёв: root-структура конфигурации, входы трафика, DNS, policy/routing, выходы и эксплуатационная обвязка. Если хотя бы один слой собран без понимания соседних, система выглядит “почти рабочей”, но ломается под реальным трафиком, миграцией версии или сменой окружения.

## Official Source Map

Использовать только официальные источники:

- Configuration index: `https://sing-box.sagernet.org/configuration/`
- Migration: `https://sing-box.sagernet.org/migration/`
- Deprecated: `https://sing-box.sagernet.org/deprecated/`
- Changelog: `https://sing-box.sagernet.org/changelog/`
- Main repository: `https://github.com/SagerNet/sing-box`
- Releases: `https://github.com/SagerNet/sing-box/releases`
- sing-geosite repository: `https://github.com/SagerNet/sing-geosite`

Этот skill должен постоянно помнить, что официальный сайт и репозиторий `main` могут опережать текущий stable release. На дату сборки этой базы stable baseline равен `v1.13.13`, а `1.14` присутствует в официальных источниках как alpha line. Это влияет на интерпретацию root-секций, DNS, TLS и remote rule sets.

## Production Scope

Через этот skill решаются следующие задачи:

- определить, подходит ли `sing-box` для сценария пользователя;
- разложить готовый конфиг по root-секциям и увидеть структурные пробелы;
- объяснить, почему конфиг из старого гайда конфликтует с текущей stable-линией;
- выбрать между single-file и split-config;
- подготовить безопасный baseline перед углублением в DNS, routing, TUN, TLS и transport-слои;
- построить процедуру проверки и запуска;
- локализовать первичную точку сбоя при инциденте.

Если задача уже явно о DNS, TUN, route rules или конкретном proxy protocol, после прочтения этого skill нужно переключаться в профильный skill. Но именно этот документ задаёт систему координат и не позволяет агенту запутаться в версиях, секциях и окружении.

## Version Baseline

Production baseline для этого skill:

- `1.10.0`: root включает `log`, `dns`, `ntp`, `inbounds`, `outbounds`, `route`, `experimental`
- `1.11.0`: добавляет `endpoints`
- `1.12.0`: добавляет `certificate` и `services`, усиливает migration pressure на DNS, ECH и WireGuard
- `1.13.13`: актуальный stable baseline для этой базы
- `1.14.0-alpha`: официальный future path, но не production baseline

Практическое правило:

- если поле есть только в `main`/alpha docs, но не подтверждено stable `1.13.13`, не считать его production-required;
- если deprecated notes в stable уже предупреждают о removal, не закладывать такой path в новый конфиг;
- если в `migration` уже есть новый canonical path, проектировать сразу на нём.

## Что Такое sing-box

С точки зрения официальной документации `sing-box` является universal proxy platform. Production-инженеру этого определения мало. Полезнее следующая модель:

- `sing-box` принимает пользовательский или транзитный трафик через `inbounds`;
- принимает и/или генерирует DNS-запросы через отдельный DNS-модуль;
- классифицирует запросы через route rules и rule sets;
- отправляет трафик через `outbounds` и современные `endpoints`;
- использует общие shared fields для listen, dial, TLS, multiplex и transport;
- может быть как клиентом, так и сервером;
- может быть локальным прокси, transparent gateway, VPN-like tunneling engine, router-side policy proxy и transport adapter.

То есть `sing-box` не “просто VLESS-клиент” и не “просто TUN-приложение”. Он ближе к policy-driven networking runtime, внутри которого proxy protocols являются только частью общей системы.

## Root Configuration Structure

Официальная stable root-структура `1.13.13` выглядит так:

```json
{
  "log": {},
  "dns": {},
  "ntp": {},
  "certificate": {},
  "endpoints": [],
  "inbounds": [],
  "outbounds": [],
  "route": {},
  "services": [],
  "experimental": {}
}
```

Из этого следуют несколько production-выводов.

Первый: root JSON уже сам по себе отражает архитектурный выбор версии. Если инженер присылает конфиг, где нет `endpoints`, а WireGuard собран старым способом, это сильный признак legacy-пути. Если кто-то пишет root c `certificate_providers` и `http_clients`, это уже ближе к `1.14` mainline, а не к stable `1.13.13`.

Второй: `dns` и `route` нужно воспринимать как центральные секции. Ошибка многих внедрений в том, что инженер выбирает transport, копирует outbound и только после этого вспоминает про DNS и routing. В `sing-box` это обратный порядок: сначала понять, как система будет принимать трафик и принимать policy decisions, потом выбрать протоколы.

Третий: `experimental` нельзя считать мусорной секцией. Для remote rule sets, Clash API и части runtime-интеграций она влияет на поведение production deployment.

## Назначение Root Sections

### `log`

Контролирует logging behavior и должен быть первой секцией, которую проверяют при любой диагностике. В production безопасный baseline обычно выглядит так:

```json
{
  "log": {
    "level": "info"
  }
}
```

Best practice:

- `info` для обычной эксплуатации;
- временный `debug` только на время controlled troubleshooting;
- не оставлять шумный debug-log на роутере или VPS без причины.

### `dns`

Отвечает за DNS servers, DNS rules, FakeIP и reverse mapping. Production mistake номер один: проектировать `dns` как придаток к transport. В реальности DNS в `sing-box` является отдельной системой принятия решений.

### `ntp`

Встроенный NTP-клиент нужен не всегда, но его наличие в root важно концептуально. Некоторые transport и security-схемы чувствительны к времени, и инженеру полезно помнить, что `sing-box` учитывает time-sensitive окружение.

### `certificate`

Появляется в stable начиная с `1.12`. Это маркер того, что TLS и сертификаты больше не стоит рассматривать исключительно как вложенные поля отдельных inbounds/outbounds.

### `endpoints`

Ключевой evolution-step начиная с `1.11`. Самый важный практический кейс здесь — WireGuard endpoint path и общее движение к более явным transport endpoints.

### `inbounds`

Определяют, откуда трафик приходит в систему: mixed, socks, http, tun, redirect, tproxy, direct и другие.

### `outbounds`

Определяют, как трафик покидает runtime: `direct`, `block`, `dns`, группы выбора и конкретные proxy protocols.

### `route`

Policy engine. Production мышление должно считать `route` не набором if/else, а точкой сборки доменной, IP, source, process и rule-set политики.

### `services`

Появились в stable root c `1.12`. Любой инженер должен видеть эту секцию как часть runtime-возможностей, даже если она не нужна в минимальном конфиге.

### `experimental`

Практически особенно важна для:

- `cache_file`
- Clash API
- V2Ray API

## Configuration Lifecycle

Жизненный цикл production-конфига должен быть детерминированным.

### 1. Проектирование

На этом этапе нужно ответить на вопросы:

- это client, server или gateway?
- нужен user-space proxy, TUN или transparent proxy?
- кто делает DNS?
- будет ли split tunneling?
- есть ли remote rule sets?
- кто обновляет конфиг и как он валидируется?

Плохой признак: конфиг начинается с copied outbound без ответа на эти вопросы.

### 2. Нормализация JSON

Официальная команда:

```bash
sing-box format -w -c config.json -D config_directory
```

Это не косметика. Форматирование помогает:

- привести JSON к каноническому виду;
- заметить дубли и странные поля;
- сделать review и diff читаемыми.

### 3. Проверка

Официальная команда:

```bash
sing-box check -c config.json -D config_directory
```

`check` должен быть встроен в любой production workflow:

- перед ручным запуском;
- перед деплоем на VPS;
- перед заменой конфига на роутере;
- перед публикацией шаблона для агентов.

### 4. Merge для split-config

Официальная команда:

```bash
sing-box merge output.json -c config.json -D config_directory
```

Production смысл:

- useful для многофайловой схемы;
- помогает увидеть итоговую конфигурацию глазами runtime;
- полезен при migration-review.

### 5. Запуск

Типовая команда:

```bash
sing-box run -c config.json -D config_directory
```

Важно разделять:

- локальный foreground run;
- systemd/procd-managed service;
- runtime inside router or appliance.

### 6. Наблюдение

После запуска инженер проверяет не “процесс жив”, а:

- listener действительно слушает нужный адрес и порт;
- DNS идёт туда, куда задумано;
- route.final и rules работают на реальном трафике;
- доменные outbounds резолвятся правильным resolver path;
- no loops, no leaks, no unexpected bypass.

## Real Production Baselines

### Minimal Local Proxy Baseline

```json
{
  "log": {
    "level": "info"
  },
  "dns": {
    "servers": [
      {
        "tag": "local",
        "type": "local"
      }
    ],
    "final": "local"
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

Это не “полезный proxy”, а канонический structural smoke test. Если такой baseline не понятен, нельзя безопасно усложнять конфигурацию.

### Linux Server Baseline

```json
{
  "log": {
    "level": "info"
  },
  "dns": {
    "servers": [
      {
        "tag": "local",
        "type": "local"
      }
    ],
    "final": "local"
  },
  "inbounds": [
    {
      "type": "http",
      "tag": "http-in",
      "listen": "127.0.0.1",
      "listen_port": 8080
    }
  ],
  "outbounds": [
    {
      "type": "direct",
      "tag": "direct"
    }
  ],
  "route": {
    "auto_detect_interface": true,
    "final": "direct"
  }
}
```

Production note: на Linux Server даже при простом local proxy полезно осознанно думать про interface binding и будущие loop scenarios.

### VPS Baseline

```json
{
  "log": {
    "level": "info"
  },
  "dns": {
    "servers": [
      {
        "tag": "local",
        "type": "local"
      }
    ],
    "final": "local"
  },
  "inbounds": [
    {
      "type": "vless",
      "tag": "vless-in",
      "listen": "::",
      "listen_port": 443,
      "users": [
        {
          "uuid": "11111111-1111-1111-1111-111111111111",
          "flow": "xtls-rprx-vision"
        }
      ],
      "tls": {
        "enabled": true,
        "certificate_path": "/etc/sing-box/cert.pem",
        "key_path": "/etc/sing-box/key.pem"
      }
    }
  ],
  "outbounds": [
    {
      "type": "direct",
      "tag": "direct"
    }
  ],
  "route": {
    "final": "direct"
  }
}
```

Это уже server-side baseline, но всё ещё intentionally simple: без exotic routing, без remote rule sets, без multi-transport ambiguity.

### OpenWrt Baseline

```json
{
  "log": {
    "level": "info"
  },
  "dns": {
    "servers": [
      {
        "tag": "local",
        "type": "local"
      }
    ],
    "final": "local"
  },
  "inbounds": [
    {
      "type": "tun",
      "tag": "tun-in",
      "address": [
        "172.19.0.1/30"
      ],
      "auto_route": true,
      "route_exclude_address": [
        "192.168.0.0/16"
      ],
      "stack": "system"
    }
  ],
  "outbounds": [
    {
      "type": "direct",
      "tag": "direct"
    }
  ],
  "route": {
    "auto_detect_interface": true,
    "final": "direct"
  }
}
```

OpenWrt note: это только skeleton. Production router никогда не должен вводиться в эксплуатацию без DNS, exclude paths и доступа к management plane.

### Podkop-Compatible Example

Так как этот репозиторий использует только официальные источники `sing-box`, для Podkop допустимы только sing-box-совместимые patterns, а не UI-specific инструкции. Production-совместимый пример — outbound, который Podkop-like consumer может импортировать как custom sing-box logic:

```json
{
  "outbounds": [
    {
      "type": "vless",
      "tag": "proxy",
      "server": "example.com",
      "server_port": 443,
      "uuid": "11111111-1111-1111-1111-111111111111",
      "flow": "xtls-rprx-vision",
      "tls": {
        "enabled": true,
        "server_name": "example.com"
      }
    }
  ],
  "route": {
    "final": "proxy"
  }
}
```

### 3x-ui-Compatible Example

Здесь тоже допустим только sing-box-side пример, который должен совпасть с server parameters, выданными 3x-ui:

```json
{
  "outbounds": [
    {
      "type": "trojan",
      "tag": "proxy",
      "server": "edge.example.com",
      "server_port": 443,
      "password": "strong-password",
      "tls": {
        "enabled": true,
        "server_name": "edge.example.com"
      }
    }
  ],
  "route": {
    "final": "proxy"
  }
}
```

Важно: skill не должен делать вид, что знает UI-семантику 3x-ui без его официальных источников. Он знает только то, как должен выглядеть корректный `sing-box` client-side counterpart.

## Operational Workflow

Production workflow для этого skill:

1. Определить stable target version.
2. Определить deployment role: client, server, router, gateway, test harness.
3. Разложить JSON по root-секциям.
4. Проверить, нет ли legacy root assumptions.
5. Выполнить `format`.
6. Выполнить `check`.
7. При split-config выполнить `merge`.
8. Проверить runtime listeners, DNS path и final outbound.
9. Только после этого обсуждать protocol-specific tuning.

## Common Mistakes

### 1. Смешение stable и alpha документации

Симптом:

- инженер проектирует под `1.13`, но использует root-поля из `1.14` mainline.

Почему это опасно:

- конфиг может оказаться некорректным;
- агент начнёт требовать несуществующие в stable секции.

### 2. Проектирование с transport-first мышлением

Симптом:

- сначала выбирают VLESS/VMess/Trojan, а DNS и routing догоняют потом.

Результат:

- DNS leaks;
- routing loops;
- несогласованные rule sets.

### 3. Игнорирование `check` и `format`

Симптом:

- конфиг редактируется вручную и сразу катится в сервис.

Результат:

- скрытые синтаксические ошибки;
- неочевидные лишние поля;
- плохой diff quality.

### 4. Игнорирование migration notes

Симптом:

- конфиг “раньше работал”, поэтому его копируют в новую версию.

Результат:

- deprecated DNS format;
- `geosite`/`geoip`;
- старый WireGuard outbound path;
- старые TUN address fields.

### 5. Неявная роль deployment

Симптом:

- один и тот же шаблон называют и client, и server, и router.

Результат:

- путаница в `inbounds`, `outbounds`, TLS роли, route.final и DNS responsibilities.

## Troubleshooting

### Конфиг не запускается

Проверять по порядку:

1. `sing-box format -w -c config.json`
2. `sing-box check -c config.json`
3. root-секции и их поддержка в target version
4. deprecated fields
5. относительные пути и `-D config_directory`

### Конфиг запускается, но система не работает

Разделять проблему на слои:

- listener layer
- DNS layer
- route layer
- outbound layer
- TLS/security layer

Нельзя одновременно чинить transport, DNS и routing. Production troubleshooting всегда начинается с первого сломанного слоя.

### Конфиг “частично работает”

Это самый опасный случай. Обычно означает:

- часть трафика идёт через `direct`;
- часть доменов резолвится мимо `sing-box`;
- `rule_set` совпадает не так, как ожидается;
- старые поля silently игнорируются или работают не по старой ментальной модели.

## Best Practices

- Фиксировать target version до проектирования.
- Для нового deployment проектировать сразу на `rule_set`, а не на `geosite`.
- Держать минимальный reproducible baseline на каждый environment.
- Встраивать `check` в CI/CD и в ручной workflow.
- Перед миграцией сравнивать root structure и deprecated notes между версиями.
- Для каждого сложного конфига иметь минимальный diagnostic profile.
- Не делать assumptions про Podkop/3x-ui/NekoBox beyond official sing-box-compatible behavior.

## Version Compatibility

### 1.10

- минимальная root-модель без `endpoints`, `certificate`, `services`
- уже есть переход к более современным TUN fields
- rule sets уже важны

### 1.11

- появляются `endpoints`
- WireGuard outbound уже официально deprecated в пользу endpoint path

### 1.12

- появляется `certificate`
- появляются `services`
- сильные изменения в DNS, ECH, migration semantics
- `GeoIP` и `Geosite` фактически выталкиваются из production path

### 1.13

- stable baseline этой базы
- root остаётся в модели `certificate + endpoints + services`
- deprecated warnings по DNS formats, WireGuard outbound, ECH legacy и старым TUN fields по-прежнему актуальны

### 1.14 alpha

- official future path с `certificate_providers` и `http_clients`
- не считать baseline для production на дату сборки этого репозитория

## Routing Schemes at Core Level

Хотя подробные route rules раскрыты в профильном skill, этот core-skill должен уметь объяснить три базовые схемы.

### Direct-First

- локальный и основной трафик идёт напрямую
- proxy только для выбранных policy domains
- полезно для conservative deployments

### Proxy-First

- всё уходит через proxy, кроме явно исключённого
- полезно для full-tunnel client setups

### Gateway Policy

- router или VPS принимает чужой трафик
- DNS, route rules и outbound choice должны быть согласованы
- без этого deployment непредсказуем

## Comparison Table

| Deployment Role | Typical Inbound | Typical Final | Main Risk |
|---|---|---|---|
| Desktop client | `mixed` or `tun` | `proxy` or `direct` | DNS leak |
| Linux server proxy | `http`/`socks` | `direct` | wrong bind/interface |
| VPS server | protocol inbound | `direct` | TLS mismatch |
| OpenWrt router | `tun`/`tproxy` | `proxy` or `direct` | loop / loss of LAN access |
| Podkop-like consumer | custom outbound import | `proxy` | unsupported field set |
| 3x-ui companion client | protocol outbound | `proxy` | transport mismatch |

## Completion Criteria

Skill считается применённым правильно, если после его использования:

- целевая версия `sing-box` определена;
- root structure соотнесена с версией;
- deployment role названа явно;
- выбран baseline path для DNS, route и outbounds;
- `check`/`format`/`merge` встроены в workflow;
- legacy and alpha traps отмечены до углубления в профильные секции.

## Production Playbooks

### Playbook: New Client Deployment

1. Зафиксировать stable version.
2. Выбрать acquisition model: local proxy or TUN.
3. Определить DNS ownership.
4. Определить direct-first or proxy-first route scheme.
5. Выбрать один transport.
6. Собрать минимальный JSON.
7. Прогнать `format`, `check`, smoke validation.
8. Только после этого добавлять rule sets, fallback groups and advanced TLS features.

### Playbook: New Server Deployment

1. Выбрать inbound protocol.
2. Подготовить certificate or REALITY materials.
3. Оставить `route.final: direct`, если нет причины для иного.
4. Сделать DNS на сервере максимально скучным и предсказуемым.
5. Проверить listener, certificate identity и inbound users.
6. Добавить observability.

### Playbook: Router Rollout

1. Сначала service baseline без transparent capture.
2. Затем DNS baseline.
3. Затем minimal TUN or TProxy.
4. Затем local/private bypass.
5. Затем основной proxy path.
6. Затем optional rule sets.

### Playbook: Migration Review

1. Выписать текущую версию и target version.
2. Сравнить root structure.
3. Открыть `deprecated` для target stable.
4. Найти old DNS formats, `geosite`, `geoip`, old TUN fields, old WireGuard mental model.
5. Переписать конфиг в current canonical structure.
6. Проверить minimal behavior before restoring complexity.

## Validation Checklist

- Root sections match target version.
- No legacy `geosite`/`geoip` in new design.
- TUN fields use merged address model.
- Domain-based upstreams have resolver ownership defined.
- `final` is explicit where behavior matters.
- `format` and `check` are part of the documented workflow.
- Podkop/3x-ui mentions stay within sing-box-compatible scope only.

## Senior Review Questions

- Какая секция в этом конфиге владеет DNS truth?
- Какая секция владеет policy truth?
- Может ли этот конфиг быть reviewed by diff without external tribal knowledge?
- Что сломается первым при version upgrade?
- Есть ли minimal rollback profile?
- Где здесь проходит management-safe path?

## Field Notes for Senior Review

### `log`

На mature deployment `log` не должен быть ни забытым, ни гиперактивным. Слишком тихий лог делает первые симптомы бесполезными, а слишком подробный лог на роутере или малом VPS сжирает ресурсы и зашумляет анализ. Senior-подход состоит в том, чтобы задавать baseline `info`, а debug применять временно и целенаправленно, фиксируя, какой слой исследуется.

### `dns`

Любой root review должен задавать вопрос: “Кто владеет истиной о доменах?” Если ответ неочевиден, значит конфиг уже опасен. Даже хороший outbound или TUN design не спасёт, если DNS semantics не определены.

### `inbounds` and `outbounds`

Плохой признак — когда эти секции существуют как пара списков без narrative о том, какой трафик они представляют. Senior review должен уметь проговорить каждую inbound/outbound pair как маршрут: кто инициирует трафик, как он классифицируется, что его резолвит, кто его выводит наружу.

### `route`

Нужно проверять не только наличие правил, но и их explainability. Если инженер не может за 60 секунд объяснить top-to-bottom intent `route.rules` и `route.final`, такой policy нельзя считать production-ready.

### `experimental`

Эта секция не должна быть silent dumping ground. Если она включена, review обязан спросить: какая именно runtime-возможность здесь нужна и чем она operationally justified.

## Change Management Notes

Любой production skill по `sing-box` полезен только тогда, когда помогает не просто написать JSON, а безопасно менять живую систему. Поэтому core-skill должен задавать change-management discipline:

- какая версия сейчас работает;
- какой минимальный working profile существует;
- что считается успешным rollout;
- как выглядит rollback;
- какие секции меняются одновременно, а какие лучше менять отдельно.

Senior practice почти всегда разбивает изменения на шаги:

1. сначала структура и синтаксис;
2. затем DNS;
3. затем route;
4. затем transport/security;
5. затем transparent mechanics.
