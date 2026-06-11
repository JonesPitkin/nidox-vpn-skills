---
name: sing-box-dns
description: "Production skill по DNS в sing-box: local DNS, DoH, DoT, FakeIP, DNS rules, split DNS, domain_resolver, anti-leak схемы и миграция между версиями. Использовать при проектировании client/server/router deployment и при диагностике DNS-сбоев."
---

# sing-box DNS

DNS в `sing-box` нельзя трактовать как техническую мелочь или как отдельный блок “укажи 1.1.1.1 и поехали”. Для production deployment DNS является отдельным policy layer. Он определяет не только ответы на запросы клиентов, но и путь резолвинга доменных upstream-серверов, работу FakeIP, split tunneling, анти-утечки и корректность route rules. Неверно собранный DNS-слой разрушает даже идеально выглядящий transport.

Этот skill нужен, когда AI-агент или инженер должен:

- спроектировать DNS path для desktop client, Linux server, OpenWrt router или VPS;
- выбрать между `local`, `https`, `tls`, `udp`, `tcp`, `fakeip` и другими official server types;
- организовать split DNS;
- понять, когда нужен `domain_resolver`;
- мигрировать со старых DNS форматов и старых outbound-DNS assumptions;
- отловить DNS leak, DNS timeout, FakeIP mismatch или неявный direct resolve.

## Official Source Map

- DNS index: `https://sing-box.sagernet.org/configuration/dns/`
- DNS servers: `https://sing-box.sagernet.org/configuration/dns/server/`
- DNS rules: `https://sing-box.sagernet.org/configuration/dns/rule/`
- DNS rule actions: `https://sing-box.sagernet.org/configuration/dns/rule_action/`
- FakeIP: `https://sing-box.sagernet.org/configuration/dns/fakeip/`
- Dial fields: `https://sing-box.sagernet.org/configuration/shared/dial/`
- Migration: `https://sing-box.sagernet.org/migration/`
- Deprecated: `https://sing-box.sagernet.org/deprecated/`

## Stable Version Baseline

Для stable `1.13.13` DNS-модель строится вокруг:

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

Из stable deprecated notes следует помнить:

- legacy DNS server formats считаются deprecated;
- outbound DNS rule items были вытеснены в сторону `domain_resolver`;
- DNS design нужно строить так, чтобы и client queries, и upstream domain resolution были контролируемыми.

## DNS Architecture in sing-box

Production-модель DNS в `sing-box` включает четыре слоя.

### 1. DNS Servers

Это backend-резолверы и специальные DNS transports. Среди официально документированных типов нужно учитывать:

- `local`
- `https`
- `tls`
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

### 2. DNS Rules

Они определяют, какой server tag использовать, какое действие применить и при каких условиях. Это основа split DNS.

### 3. DNS Rule Actions

Для stable production особенно важны:

- `route`
- `route-options`
- `reject`
- `predefined`

При работе с будущими версиями нужно не путать stable с более новыми action-расширениями.

### 4. Domain Resolver

Это critical piece для доменных upstreams. Даже если клиентские DNS-запросы выглядят рабочими, outbound к `server: example.com` всё равно может ломаться, если `domain_resolver` не согласован с общей схемой.

## Core Production Questions

Перед проектированием DNS нужно ответить на вопросы:

- кто является источником DNS-запросов: клиентские приложения, TUN, router clients, сам `sing-box`?
- есть ли split DNS?
- нужно ли возвращать real IP или FakeIP?
- требуется ли reverse mapping для маршрутизации по домену после connect?
- какой resolver должен использоваться для доменных upstreams?
- нужен ли EDNS subnet?
- допустим ли direct local resolve или вся схема должна идти через proxy-aware path?

Без ответов на эти вопросы DNS-конфиг обычно получается visually valid, но production-incoherent.

## Real DNS Configurations

### Minimal Local DNS

```json
{
  "dns": {
    "servers": [
      {
        "tag": "local",
        "type": "local"
      }
    ],
    "final": "local"
  }
}
```

Use case:

- simple desktop setup;
- server-side deployment, где DNS должен следовать системной политике;
- diagnostic baseline.

Риск:

- если основная сеть сама по себе не trustworthy или system resolver не соответствует policy, такой baseline не подходит.

### DoH Baseline

```json
{
  "dns": {
    "servers": [
      {
        "tag": "doh",
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
    "final": "doh",
    "strategy": "prefer_ipv4",
    "cache_capacity": 8192
  }
}
```

Production use:

- external DNS with controlled TLS path;
- router and VPS setups, где не хочется доверять system local resolver.

### DoT Baseline

```json
{
  "dns": {
    "servers": [
      {
        "tag": "dot",
        "type": "tls",
        "server": "1.1.1.1",
        "server_port": 853,
        "tls": {
          "enabled": true,
          "server_name": "cloudflare-dns.com"
        }
      }
    ],
    "final": "dot"
  }
}
```

### Split DNS for Local Domains

```json
{
  "dns": {
    "servers": [
      {
        "tag": "local",
        "type": "local"
      },
      {
        "tag": "remote-doh",
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
    "final": "remote-doh"
  }
}
```

Это базовый и очень production-полезный паттерн:

- локальные домены не уходят наружу;
- все остальные запросы идут в controlled remote resolver.

### FakeIP Baseline

```json
{
  "dns": {
    "servers": [
      {
        "tag": "fakeip",
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
    "final": "fakeip",
    "reverse_mapping": true
  }
}
```

Production warning:

- FakeIP — это не просто “особый DNS-сервер”, а целая модель маршрутизации;
- он особенно полезен для TUN и transparent routing;
- его нужно согласовывать с route rules и исключениями адресов.

### Domain Resolver for Outbounds

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
      },
      "domain_resolver": {
        "server": "remote-doh"
      }
    }
  ]
}
```

Это critical production pattern. Если upstream задан доменом, а DNS design сложный, отсутствие `domain_resolver` приводит к трудноуловимым сбоям: приложение говорит “proxy не работает”, хотя проблема на самом деле в том, как `sing-box` сам резолвит адрес сервера.

## DNS Rules Design

DNS rules позволяют матчить по:

- `domain`
- `domain_suffix`
- `domain_keyword`
- `domain_regex`
- `rule_set`
- source/IP/process/network and other criteria в рамках официальной модели версии

Production-практика:

- сначала писать narrow local exceptions;
- потом policy domains;
- затем fallback `final`.

Пример DNS rules для bypass корпоративных доменов:

```json
{
  "dns": {
    "servers": [
      {
        "tag": "corp-local",
        "type": "local"
      },
      {
        "tag": "remote",
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
          ".corp.example",
          ".lan"
        ],
        "action": "route",
        "server": "corp-local"
      }
    ],
    "final": "remote"
  }
}
```

## OpenWrt Examples

### OpenWrt Split DNS

```json
{
  "dns": {
    "servers": [
      {
        "tag": "local",
        "type": "local"
      },
      {
        "tag": "proxy-dns",
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
        "server": "local"
      }
    ],
    "final": "proxy-dns",
    "reverse_mapping": true
  }
}
```

### OpenWrt FakeIP-Oriented Router Example

```json
{
  "dns": {
    "servers": [
      {
        "tag": "fakeip",
        "type": "fakeip",
        "inet4_range": "198.18.0.0/15"
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
    "final": "fakeip",
    "reverse_mapping": true
  }
}
```

Роутерный смысл:

- клиенты получают synthetic answers;
- router-side route rules потом принимают решение по домену.

## Linux Server Examples

### Linux Server with Controlled Upstream Resolve

```json
{
  "dns": {
    "servers": [
      {
        "tag": "remote",
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
    "final": "remote",
    "strategy": "prefer_ipv4",
    "cache_capacity": 4096
  }
}
```

Полезно, когда сервер должен предсказуемо резолвить transport upstreams независимо от host resolver quirks.

## VPS Examples

### VPS Server-Side Clean DNS

```json
{
  "dns": {
    "servers": [
      {
        "tag": "local",
        "type": "local"
      }
    ],
    "final": "local",
    "cache_capacity": 2048
  }
}
```

Почему это production-legit:

- server-side inbound often does not need exotic DNS for client traffic itself;
- главное — чтобы certificate, route и listener paths не зависели от хаотичного DNS behavior.

### VPS With Proxy-Aware Upstream Resolve

Если сам сервер ещё и строит outbound-соединения к доменным peer endpoints, нужен `domain_resolver`, а не blind reliance на host DNS.

## Podkop-Compatible Examples

Так как допускаются только official sing-box facts, для Podkop даём только sing-box-side patterns.

### Podkop-Compatible FakeIP Core

```json
{
  "dns": {
    "servers": [
      {
        "tag": "fakeip",
        "type": "fakeip",
        "inet4_range": "198.18.0.0/15"
      },
      {
        "tag": "remote",
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
    "final": "fakeip",
    "reverse_mapping": true
  }
}
```

Это полезно как conceptual template для systems, которые импортируют или генерируют sing-box-compatible DNS logic.

## 3x-ui-Compatible Examples

Для 3x-ui мы не описываем UI-операции, но можем показать нужный DNS counterpart на стороне `sing-box` client:

```json
{
  "dns": {
    "servers": [
      {
        "tag": "remote",
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
    "final": "remote"
  },
  "outbounds": [
    {
      "type": "vless",
      "tag": "proxy",
      "server": "panel-generated.example.com",
      "server_port": 443,
      "uuid": "11111111-1111-1111-1111-111111111111",
      "tls": {
        "enabled": true,
        "server_name": "panel-generated.example.com"
      },
      "domain_resolver": {
        "server": "remote"
      }
    }
  ]
}
```

## Routing Schemes and DNS

DNS design должен соответствовать routing design.

### Direct-First Scheme

- local/corp domains -> `local`
- everything else -> remote secure DNS
- `route.final` often `direct`

### Proxy-First Scheme

- DNS itself should not silently bypass the intended proxy path for upstream resolution
- `domain_resolver` becomes critical

### FakeIP Transparent Scheme

- DNS returns synthetic addresses
- route logic restores domain semantics via reverse mapping
- best used with TUN/transparent paths

## Comparison Table

| Pattern | Best For | Main Benefit | Main Risk |
|---|---|---|---|
| `local` only | simple server/client | lowest complexity | system resolver trust |
| DoH | clients, routers, VPS | controlled encrypted DNS | wrong SNI/path |
| DoT | simple secure upstream | straightforward TLS DNS | cert/SNI mismatch |
| FakeIP | TUN, transparent policy routing | domain-aware routing after resolve | app compatibility and route complexity |
| Split DNS | corporate/LAN/home router | keep local names local | rule ordering mistakes |

## Common Mistakes

### 1. DNS and route are designed separately

Результат:

- route rules ждут доменную семантику, а DNS already lost that context;
- direct and proxy paths diverge unexpectedly.

### 2. No `domain_resolver` for domain upstream

Результат:

- outbound server name resolves via wrong path;
- connection instability masked as transport failure.

### 3. FakeIP without reverse mapping or route awareness

Результат:

- synthetic IP exists, but policy by domain no longer works as intended.

### 4. Wrong assumption that DoH alone prevents DNS leak

Результат:

- client queries may still bypass `sing-box`;
- system resolver may still be used by parts of the deployment.

### 5. Legacy DNS formats copied from old configs

Результат:

- migration problems;
- confusion between stable and deprecated syntax.

## Troubleshooting

### Symptom: domains time out, IPs work

Check:

- `dns.final`
- real chosen server tag
- `domain_resolver`
- TLS settings for DoH/DoT

### Symptom: some domains resolve, some do not

Check:

- DNS rule ordering
- `domain_suffix` and `rule_set` coverage
- split DNS assumptions

### Symptom: proxy transport fails only with domain server, not IP server

Check:

- `domain_resolver`
- upstream DNS path
- whether route policies interfere with resolving the proxy host itself

### Symptom: FakeIP returns answers but apps break

Check:

- whether the app tolerates synthetic answers
- whether transparent path is complete
- whether excluded networks overlap with fake ranges

### Symptom: DNS leak

Check:

- is the client really sending DNS into `sing-box`?
- if TUN/transparent, is DNS interception complete?
- is upstream resolution using host DNS accidentally?

## Best Practices

- Treat DNS as a first-class policy layer.
- Always decide who resolves proxy upstream names.
- Keep a minimal local-DNS baseline for rollback.
- Use split DNS intentionally, not incidentally.
- Introduce FakeIP only when routing semantics require it.
- Keep cache sizes explicit on routers and servers with predictable load.
- Verify every secure DNS server with the correct TLS `server_name`.

## Version Compatibility

### 1.10

- DNS structure is simpler;
- later migration pressure already begins.

### 1.11

- route and endpoint changes indirectly affect DNS topology planning.

### 1.12

- legacy DNS server formats become explicitly deprecated;
- ECH and resolver semantics shift;
- `domain_resolver` becomes a strategic concept.

### 1.13 stable

- production baseline for this skill;
- deprecated warnings remain operationally relevant.

### 1.14 alpha

- official future path contains more DNS fields and actions;
- do not force them into `1.13` production unless the target version is explicitly upgraded.

## Completion Criteria

Skill считается применённым правильно, если:

- DNS topology описана словами и JSON;
- ясно, кто делает client DNS and upstream DNS resolution;
- split/FakeIP use justified;
- `domain_resolver` checked where needed;
- version-specific DNS traps and deprecated formats identified before deployment.

## Production Design Patterns

### Pattern: Secure Upstream Resolver

Use when:

- host resolver is not trusted enough;
- router or VPS needs deterministic external DNS;
- proxy upstream names must resolve consistently.

Recommended components:

- DoH or DoT server;
- explicit `final`;
- explicit `server_name`;
- explicit `domain_resolver` for domain-based outbounds.

### Pattern: Split DNS for Home or Office Networks

Use when:

- `.lan`, `.local` or corp suffixes must stay local;
- external traffic must use a secure remote resolver.

Recommended components:

- local server tag;
- remote secure server tag;
- narrow `dns.rules` for local suffixes;
- remote `final`.

### Pattern: FakeIP Transparent Policy

Use when:

- TUN or transparent routing needs domain semantics after resolution;
- domain-based policy must survive connect phase.

Required companions:

- route design aware of FakeIP;
- `reverse_mapping`;
- tested client compatibility.

## Environment Playbooks

### OpenWrt DNS Rollout

1. Validate router-local DNS first.
2. Keep local domain handling explicit.
3. Introduce remote secure DNS.
4. Only then add FakeIP or transparent DNS capture.

### Linux Server DNS Rollout

1. Start with explicit `local` or secure remote resolver.
2. Validate outbound hostname resolution.
3. Add split or special rules only when required by workload.

### VPS DNS Rollout

1. Keep server-side DNS boring unless there is a clear policy reason.
2. If VPS relays to domain-based peers, define resolver ownership explicitly.

## Validation Checklist

- `dns.final` set intentionally.
- DNS rule ordering reviewed.
- Secure DNS `server_name` correct.
- `domain_resolver` defined where needed.
- FakeIP justified, not decorative.
- Local/private/corp domains handled consciously.
- No legacy DNS server formats in new configs.

## Senior Review Questions

- What resolves the proxy host itself?
- Is DNS policy aligned with route policy?
- Will this design still work if the app bypasses system proxy and uses raw network APIs?
- If FakeIP is removed, what policy capability is lost?

## Field Notes

### `final`

Если `dns.final` не проговорён явно, это почти всегда latent bug. Даже когда первый server tag technically acceptable, engineer should still document the intent, because later reordering of servers silently changes behavior.

### `strategy`

`prefer_ipv4`, `prefer_ipv6`, `ipv4_only`, `ipv6_only` нельзя выставлять механически. Это operational statement about the network. На VPS или router edge in dual-stack environments, wrong strategy can be mistaken for transport instability.

### `reverse_mapping`

Это поле имеет высокий strategic value в transparent and FakeIP designs. Но в environments, где DNS is cached or proxied outside `sing-box`, оно может вести себя не так, как engineer mentally expects. Senior review должен спрашивать, кто actually performs the original resolution.

### `client_subnet`

EDNS subnet should be treated as policy, not decoration. Если включено, у инженера должна быть причина: geographic shaping, resolver behavior tuning or compatibility requirement.

## Scenario Catalog

### Scenario: Corporate Laptop with Split DNS

Нужен local/corp resolution path, но external traffic should use secure remote resolver. Recommended path:

- `local` for corp suffixes
- secure remote `final`
- avoid FakeIP unless route semantics require it

### Scenario: Home Router with Transparent Proxy

Если goal is client-transparent routing, DNS design almost always becomes the critical success factor. Senior design should decide early whether routing depends on real answers or FakeIP-backed domain restoration.

### Scenario: VPS Relay with Domain Upstreams

Here the DNS question is not “how do clients resolve?”, but “how does this relay itself resolve its peer hostnames?” That is why `domain_resolver` becomes a first-order design concern.

## Change Management Notes

DNS changes should rarely be bundled with transport and routing changes in the same rollout window. Senior change management for `sing-box` DNS prefers:

1. freeze route and transport;
2. change resolver topology;
3. validate domain-based upstream reachability;
4. validate client-facing DNS behavior;
5. only then reintroduce more advanced FakeIP or split logic.

This sequencing matters because DNS mistakes impersonate almost every other category of failure.
