# VERSION_MATRIX

Матрица совместимости и ключевых изменений `sing-box` по официальным источникам.

Baseline для production в этом репозитории: `v1.13.13`.

`1.14` в официальных источниках на дату проверки присутствует как alpha-line и не считается stable baseline.

## Root Structure Matrix

| Version | Root Sections from Official Config Index | Production Meaning |
|---|---|---|
| `1.10.0` | `log`, `dns`, `ntp`, `inbounds`, `outbounds`, `route`, `experimental` | pre-endpoint, older root model |
| `1.11.0` | `log`, `dns`, `ntp`, `endpoints`, `inbounds`, `outbounds`, `route`, `experimental` | endpoints appear |
| `1.12.0` | `log`, `dns`, `ntp`, `certificate`, `endpoints`, `inbounds`, `outbounds`, `route`, `services`, `experimental` | certificate and services added |
| `1.13.13` | `log`, `dns`, `ntp`, `certificate`, `endpoints`, `inbounds`, `outbounds`, `route`, `services`, `experimental` | stable baseline for this repo |
| `1.14 alpha` | `log`, `dns`, `ntp`, `certificate`, `certificate_providers`, `http_clients`, `endpoints`, `inbounds`, `outbounds`, `route`, `services`, `experimental` | official future path, not stable baseline |

## Key Compatibility Matrix

| Topic | `1.10` | `1.11` | `1.12` | `1.13` | `1.14 alpha` |
|---|---|---|---|---|---|
| `rule_set` as modern path | yes | yes | yes | yes | yes |
| `GeoIP` / `Geosite` status | deprecated, may be removed later | deprecated, removal targeted at `1.12` | removed from modern path, migration required | still legacy-only concept in deprecated docs | not for new configs |
| WireGuard outbound | still seen in old configs | deprecated in favor of endpoint | deprecated | deprecated | deprecated/future endpoint path only |
| TUN merged address fields | modern path | modern path | modern path | modern path | modern path |
| Legacy DNS server formats | older expectations still common | older expectations still common | deprecated | deprecated | future stable likely stricter |
| `default_domain_resolver` | no | no | yes | yes | yes |
| `certificate` root section | no | no | yes | yes | yes |
| `services` root section | no | no | yes | yes | yes |
| `certificate_providers` root section | no | no | no | no | yes in alpha docs |
| `http_clients` root section | no | no | no | no | yes in alpha docs |

## Deprecated and Migration Signals

### `1.10`

Official deprecated page already signals:

- TUN address fields are merged
- `GeoIP` deprecated
- `Geosite` deprecated

Production meaning:

- new configs should already move toward modern TUN and `rule_set` thinking.

### `1.11`

Official deprecated page signals:

- WireGuard outbound deprecated, endpoint is the replacement
- TUN address fields merged
- `GeoIP` and `Geosite` removal targeted for `1.12`

Production meaning:

- avoid designing new configs on old WireGuard or geo mental models.

### `1.12`

Official deprecated page signals:

- legacy DNS server formats deprecated
- legacy ECH fields deprecated
- WireGuard outbound deprecated
- old TUN address fields legacy-only
- `GeoIP` and `Geosite` removed from modern operational path

Production meaning:

- `1.12` is the major migration boundary for many old community configs.

### `1.13`

Official deprecated page still carries the important warnings from `1.12`.

Production meaning:

- even on stable `1.13.13`, new configs should already be fully modernized.

### `1.14 alpha`

Official config index shows future sections:

- `certificate_providers`
- `http_clients`

Production meaning:

- useful for forward planning;
- not to be forced into `1.13` production templates.

## Operational Recommendations by Version

### If you must maintain `1.10`

- keep root structure simple;
- begin migration planning toward `rule_set` and merged TUN fields immediately.

### If you run `1.11`

- treat WireGuard endpoint migration as active work, not optional cleanup.

### If you run `1.12`

- review DNS formats, ECH assumptions, TUN fields and geo legacy aggressively.

### If you run `1.13`

- this is the recommended stable baseline for this repository;
- modernize fully and avoid alpha-only structures.

### If you evaluate `1.14 alpha`

- isolate experiments;
- keep production templates version-gated;
- do not let future root sections silently leak into stable documentation.

