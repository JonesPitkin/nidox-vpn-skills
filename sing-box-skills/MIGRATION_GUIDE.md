# MIGRATION_GUIDE

Гид по миграции между версиями `sing-box` на основе официальных docs, deprecated pages, migration pages и stable tags.

Production baseline этого репозитория: `v1.13.13`.

## Migration Principles

1. Всегда фиксировать исходную и целевую версии.
2. Никогда не мигрировать “на глаз” по community snippets.
3. Перед изменениями открыть:
   - `configuration`
   - `migration`
   - `deprecated`
4. Сначала переводить конфиг на current canonical structure.
5. Только потом возвращать advanced routing, TLS, TUN and policy details.

## Recommended Migration Workflow

1. Сделать копию исходного конфига.
2. Выполнить `sing-box format`.
3. Выполнить `sing-box check` на исходной версии, если возможно.
4. Выписать legacy features:
   - `geosite`
   - `geoip`
   - old TUN address fields
   - old WireGuard outbound assumptions
   - old DNS server formats
   - legacy ECH snippets
5. Переписать root structure под target version.
6. Переписать DNS.
7. Переписать route/rule sets.
8. Проверить TUN.
9. Проверить TLS/REALITY.
10. Проверить service lifecycle on target host.

## 1.10 -> 1.11

### Main Change

Официальный config index `1.11` добавляет `endpoints`.

### What to Review

- старые assumptions про transport topology;
- подготовку к endpoint-oriented designs;
- особенно WireGuard-related thinking, если он уже в планах.

### Practical Advice

- можно не менять всё сразу, но уже стоит очищать конфиг от старых паттернов и готовить его к более современной структуре.

## 1.11 -> 1.12

Это самый важный migration jump в рассматриваемом диапазоне.

### Main Changes

- root получает `certificate`
- root получает `services`
- deprecated page фиксирует legacy DNS server formats
- deprecated page фиксирует legacy ECH fields
- WireGuard outbound уже legacy path
- `GeoIP` and `Geosite` окончательно выходят из современного production path

### What to Migrate

#### 1. Move to `rule_set`

Replace:

- route and DNS logic built on `geosite`
- route and DNS logic built on `geoip`

With:

- `route.rule_set`
- `rules[].rule_set`

#### 2. Move to modern TUN fields

Use:

- `address`
- `route_address`
- `route_exclude_address`

Stop relying on:

- `inet4_address`
- `inet6_address`
- `inet4_route_address`
- `inet6_route_address`

#### 3. Review DNS formats

Legacy DNS server formats should be treated as migration debt.

#### 4. Review ECH assumptions

Legacy ECH snippets from old guides need explicit comparison against official `migration` and `deprecated`.

#### 5. Re-think WireGuard

If config still assumes WireGuard as ordinary outbound, start moving the mental and structural model toward endpoint usage.

## 1.12 -> 1.13

### Main Change

`1.13.13` is a stable line that still carries the migration consequences of `1.12`.

### Practical Migration Focus

- complete unfinished `1.12` cleanup;
- ensure DNS, route and security logic are no longer legacy-dependent;
- keep templates stable-baseline safe and do not import alpha-only docs.

### Checklist

- no `geosite` in new configs
- no `geoip` in new configs
- no old TUN address fields
- no unresolved legacy DNS syntax
- no unclear WireGuard outbound design

## 1.13 -> 1.14 alpha planning

This is not a recommended production migration target in this repository, but forward-planning is useful.

### Official Future Signals

Config index on alpha line shows:

- `certificate_providers`
- `http_clients`

### Practical Advice

- track them as future design directions;
- do not silently bake them into `1.13` production skills;
- version-gate every template and explanation.

## Topic-Specific Migration

### DNS Migration

When migrating DNS:

1. rebuild `dns.servers` in modern format
2. make `final` explicit
3. review `domain_resolver`
4. re-check FakeIP only after basic DNS works

### Route Migration

When migrating route:

1. remove geo legacy fields
2. define `rule_set`
3. define explicit `final`
4. re-test local/private bypass

### TUN Migration

When migrating TUN:

1. replace old address fields
2. re-check exclusions
3. re-check route loops
4. re-check admin-plane safety

### Security Migration

When migrating security:

1. remove old ECH assumptions
2. re-check TLS role separation
3. re-check certificate paths and names
4. re-check REALITY role fields

## Migration Checklists

### Pre-Migration Checklist

- current version identified
- target version identified
- deprecated features listed
- rollback copy made
- environment type known: desktop, server, VPS, OpenWrt

### During Migration Checklist

- root structure updated
- DNS updated
- route updated
- TUN updated if present
- TLS/security updated
- service lifecycle checked

### Post-Migration Checklist

- `format` clean
- `check` passes
- minimal baseline works
- real policy works
- admin/management path safe
- no alpha-only assumptions in stable config

## Common Migration Mistakes

### 1. Renaming fields without changing mental model

Example:

- renaming `geosite` usage into partial rule-set syntax without redesigning policy ownership.

### 2. Migrating transport before DNS and route

Result:

- new proxy protocol is blamed for old policy bugs.

### 3. Mixing stable and alpha docs

Result:

- `1.13` config accidentally depends on `1.14` structures.

### 4. Treating OpenWrt like desktop

Result:

- migration succeeds syntactically but fails operationally.

## Final Recommendation

For production in this repository:

- prefer `1.13.13`
- design new configs around `rule_set`
- use modern TUN fields
- treat WireGuard through endpoint thinking
- keep DNS and `domain_resolver` explicit
- track `1.14` only as forward-looking official direction until stable release

