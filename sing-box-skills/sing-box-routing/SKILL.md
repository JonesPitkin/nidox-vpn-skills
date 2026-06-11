---
name: sing-box-routing
description: "Production skill по маршрутизации в sing-box: route rules, rule_set, source/domain/ip/process matching, final outbound, direct bypass, split tunneling и policy routing на Linux, OpenWrt, VPS и sing-box-совместимых client environments."
---

# sing-box Routing

Routing в `sing-box` — это сердце production deployment. Именно здесь решение “какой трафик куда пойдёт” становится формальным, воспроизводимым и проверяемым. Если DNS отвечает на вопрос “какое имя чему соответствует”, то route layer отвечает на вопрос “какую policy применять к конкретному запросу”. На практике это значит, что `route` определяет безопасность, экономику трафика, user experience, resistance to leaks и предсказуемость всей системы.

Этот skill нужен при:

- selective proxying;
- split tunneling;
- proxy-first и direct-first сценариях;
- router-side и VPS-side policy routing;
- работе с remote/local rule sets;
- process/source-aware политике на desktop/server;
- диагностике routing loops и unexpected bypass.

## Official Source Map

- Route index: `https://sing-box.sagernet.org/configuration/route/`
- Route rule: `https://sing-box.sagernet.org/configuration/route/rule/`
- Route rule action: `https://sing-box.sagernet.org/configuration/route/rule_action/`
- Rule Set: `https://sing-box.sagernet.org/configuration/rule-set/`
- Sniff: `https://sing-box.sagernet.org/configuration/route/sniff/`
- Dial fields: `https://sing-box.sagernet.org/configuration/shared/dial/`
- Migration: `https://sing-box.sagernet.org/migration/`
- Deprecated: `https://sing-box.sagernet.org/deprecated/`

## Stable Route Baseline

Для stable `1.13.13` route block ориентируется на:

```json
{
  "route": {
    "rules": [],
    "rule_set": [],
    "final": "",
    "auto_detect_interface": false,
    "override_android_vpn": false,
    "default_interface": "",
    "default_mark": 0,
    "default_domain_resolver": "",
    "default_network_strategy": "",
    "default_network_type": [],
    "default_fallback_network_type": [],
    "default_fallback_delay": ""
  }
}
```

Практически важно:

- `rule_set` — это не optional toy, а основной современный path вместо `geosite` и `geoip`;
- `default_domain_resolver` нужно учитывать в доменно-зависимых egress-схемах;
- `auto_detect_interface` и `default_interface` тесно связаны с TUN and loop avoidance.

## Routing Mental Model

Production routing в `sing-box` состоит из трёх уровней:

### 1. Match

Что мы распознаём:

- domain
- ip
- source
- port
- process
- inbound origin
- network characteristics
- external rule sets

### 2. Action

Что мы делаем:

- `route`
- `bypass`
- `reject`
- `hijack-dns`
- `route-options`

### 3. Fallback

Куда идёт всё, что не совпало:

- `route.final`

Если инженер не может словами объяснить эти три уровня, значит routing design ещё не production-ready.

## Match Categories

Официальные route rules позволяют матчить по:

- `inbound`
- `ip_version`
- `network`
- `auth_user`
- `protocol`
- `client`
- `domain`
- `domain_suffix`
- `domain_keyword`
- `domain_regex`
- `ip_cidr`
- `ip_is_private`
- `source_ip_cidr`
- `source_ip_is_private`
- `port`, `port_range`
- `source_port`, `source_port_range`
- `process_name`
- `process_path`
- `process_path_regex`
- `package_name`
- `user`
- `user_id`
- `network_type`
- `wifi_ssid`, `wifi_bssid`
- `rule_set`

Production смысл:

- route может быть application-aware;
- route может быть source-aware;
- route может быть domain-policy-driven;
- route может опираться на reusable externalized policy через `rule_set`.

## Real Route Configurations

### Direct-First Baseline

```json
{
  "route": {
    "rules": [
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

Use case:

- conservative workstation or server;
- only selected traffic later goes to proxy.

### Proxy-First Baseline

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

Это canonical production pattern для full-tunnel client behavior with local bypass.

### Rule Set-Based Selective Routing

```json
{
  "route": {
    "rule_set": [
      {
        "type": "local",
        "tag": "streaming",
        "format": "source",
        "path": "/etc/sing-box/rules/streaming.json"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "streaming"
        ],
        "action": "route",
        "outbound": "proxy"
      }
    ],
    "final": "direct"
  }
}
```

### Process-Aware Routing

```json
{
  "route": {
    "rules": [
      {
        "process_name": [
          "curl"
        ],
        "action": "route",
        "outbound": "direct"
      }
    ],
    "final": "proxy"
  }
}
```

Production use:

- desktop or server host policy;
- keep admin tooling direct while user traffic goes via proxy.

### Inbound-Aware Routing

```json
{
  "route": {
    "rules": [
      {
        "inbound": [
          "mixed-in"
        ],
        "action": "route",
        "outbound": "proxy"
      },
      {
        "inbound": [
          "admin-socks"
        ],
        "action": "route",
        "outbound": "direct"
      }
    ],
    "final": "direct"
  }
}
```

## Route Actions

### `route`

Основной final action.

```json
{
  "action": "route",
  "outbound": "proxy"
}
```

### `bypass`

Полезен в Linux `auto_redirect` contexts. Это не generic replacement for `route`. Он особенно важен там, где нужно kernel-level bypass behavior для transparent flows.

### `reject`

Для controlled blocking.

```json
{
  "action": "reject",
  "method": "default"
}
```

### `hijack-dns`

Направляет DNS traffic в DNS module `sing-box`.

```json
{
  "action": "hijack-dns"
}
```

### `route-options`

Используется для override поведения маршрутизации без немедленного final route.

## OpenWrt Examples

### OpenWrt Split Tunnel Router

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

### OpenWrt Rule Set Policy

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "policy",
        "format": "binary",
        "url": "https://example.invalid/policy.srs",
        "update_interval": "1d"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "policy"
        ],
        "action": "route",
        "outbound": "proxy"
      }
    ],
    "final": "direct"
  }
}
```

## Linux Server Examples

### Admin Tools Direct, Everything Else Proxy

```json
{
  "route": {
    "rules": [
      {
        "process_name": [
          "ssh",
          "scp",
          "rsync"
        ],
        "action": "route",
        "outbound": "direct"
      }
    ],
    "final": "proxy"
  }
}
```

### Inbound Segmentation on Server

Use different local services with different egress intents by `inbound` tag matching.

## VPS Examples

### VPS Relay with Policy Segmentation

```json
{
  "route": {
    "rules": [
      {
        "ip_is_private": true,
        "action": "route",
        "outbound": "direct"
      }
    ],
    "final": "relay"
  }
}
```

### VPS with Default Resolver Awareness

If relay uses domain server addresses, pair route design with `default_domain_resolver`.

## Podkop-Compatible Examples

Under official-only constraints, Podkop example must remain sing-box-native:

```json
{
  "route": {
    "rules": [
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

This is useful as a custom routing logic template for a system that consumes sing-box-compatible route semantics.

## 3x-ui-Compatible Examples

UI-specific panel behavior is out of scope, but sing-box-side route policy for a 3x-ui-provided outbound is straightforward:

```json
{
  "route": {
    "rules": [
      {
        "ip_is_private": true,
        "action": "route",
        "outbound": "direct"
      }
    ],
    "final": "proxy"
  }
}
```

## Routing Scheme Diagrams

### Direct-First

- DNS/route classify request
- local/LAN/private -> `direct`
- selected policy domains -> `proxy`
- unmatched -> `direct`

### Proxy-First

- local/LAN/private -> `direct`
- unmatched -> `proxy`

### Transparent Router Policy

- traffic intercepted by `tun` or `tproxy`
- DNS path normalized
- route rules choose `direct`, `proxy`, `block`
- optional kernel-level `bypass` for Linux auto-redirect cases

## Comparison Table

| Scheme | Best For | Benefit | Risk |
|---|---|---|---|
| Direct-First | cautious environments | easy rollback | missing desired proxy coverage |
| Proxy-First | privacy/full tunnel | strong coverage | leaks if exclusions incomplete |
| Rule Set selective | large policy sets | maintainability | stale rule sets |
| Process-aware | desktops/servers | fine-grained control | platform assumptions |
| Inbound-aware | multi-service hosts | clean separation | tag drift |

## Common Mistakes

### 1. Using deprecated `geosite` or `geoip` in new configs

Result:

- immediate version debt and misleading examples.

### 2. Putting broad catch-all rules before precise exceptions

Result:

- unexpected routing behavior that looks random.

### 3. No explicit `final`

Result:

- fallback depends on first outbound ordering, which is easy to misread.

### 4. Ignoring DNS dependency of routing

Result:

- route wants domain semantics, but DNS path prevents it.

### 5. Using `bypass` outside its intended Linux auto-redirect context

Result:

- wrong mental model and ineffective policy.

## Troubleshooting

### Symptom: policy domains still go direct

Check:

- rule ordering;
- exact domain match method;
- whether DNS/path preserves domain context;
- whether `rule_set` is actually loaded.

### Symptom: local resources accidentally proxied

Check:

- `ip_is_private`;
- `.lan` / local suffix rules;
- route exclusions at TUN layer.

### Symptom: route loop or no connectivity

Check:

- `auto_detect_interface`;
- `default_interface`;
- resolver path for domain upstreams;
- TUN exclusions and direct bypass paths.

### Symptom: remote rule set policy seems stale

Check:

- update interval;
- cache behavior;
- local vs remote file source.

## Best Practices

- Always make `final` explicit.
- Prefer `rule_set` for reusable policy.
- Place narrow exceptions before broad catches.
- Keep direct path for private/local networks unless there is a strong reason not to.
- Tie routing review to DNS review.
- Document the intended scheme in words next to the JSON.

## Version Compatibility

### 1.10

- rule sets already matter;
- legacy fields still common in community configs.

### 1.11

- endpoint evolution and WireGuard deprecation affect policy design around routed peers.

### 1.12

- `default_domain_resolver` becomes strategically important;
- `geoip`/`geosite` effectively exit production path.

### 1.13 stable

- repository baseline;
- route design should now assume `rule_set` as the normal path.

### 1.14 alpha

- future additions exist in docs but should be version-gated.

## Completion Criteria

Skill считается применённым правильно, если:

- route scheme named explicitly;
- rules and final outbound shown in JSON;
- direct/proxy/block logic explained;
- rule-set and resolver dependencies acknowledged;
- OpenWrt/Linux/VPS examples present.

## Policy Design Playbooks

### Playbook: Direct-First Policy

1. Define local/private/direct-safe destinations.
2. Add narrow proxy categories.
3. Set `final: direct`.
4. Validate local services first.

### Playbook: Proxy-First Policy

1. List everything that must bypass.
2. Encode bypass as explicit rules.
3. Set `final: proxy`.
4. Validate admin access and proxy-host self-reachability.

### Playbook: Rule-Set Fleet Policy

1. Externalize reusable categories into `rule_set`.
2. Keep host- and source-specific rules local in root config.
3. Make remote policy update path explicit.
4. Tie routing review to DNS review.

## Environment Decision Matrix

### OpenWrt

Focus on:

- LAN and management bypass;
- policy that survives transparent capture;
- minimal catch-all rules until the router is proven stable.

### Linux Server

Focus on:

- process and service segmentation;
- keeping admin paths direct unless there is a strong reason not to.

### VPS

Focus on:

- making sure relay/public-service route logic does not recurse into itself;
- being explicit about resolver and upstream reachability.

## Validation Checklist

- `final` is explicit.
- Rule ordering reviewed top to bottom.
- `rule_set` declarations and references match.
- Private/local policies exist where needed.
- DNS semantics support routing semantics.

## Senior Review Questions

- If all rule sets vanish, what still works?
- Which rule protects management traffic?
- Which rule proves the proxy host can reach its own upstreams safely?
- Is this policy reusable or just a pile of exceptions?

## Field Notes

### `final`

`final` is where architectural honesty shows up. If the author avoids naming the default path, they are often avoiding a real design decision. Senior review should insist on explicit fallback intent.

### `rule_set`

A route config with `rule_set` references but no lifecycle story for those assets is incomplete. Reusable policy must have naming, ownership and update semantics.

### Source and Process Matching

These fields are powerful, but they should be introduced only when they reduce ambiguity, not when they add cleverness. If simpler domain/IP logic solves the same problem, prefer it.

## Scenario Catalog

### Scenario: Selective Streaming Proxy

External media categories go through proxy, local and generic browsing stay direct. `rule_set` is usually the cleanest long-term path.

### Scenario: Full-Tunnel With Admin Escape Hatch

Everything uses proxy except explicit private, management and rescue paths. This is where bad rule ordering most often creates operational pain.

### Scenario: Multi-Inbound Host

Different inbounds represent different trust or workload domains. Routing by `inbound` tag can keep policy explainable when process matching would be too fragile.

## Change Management Notes

Routing changes should be rolled out with explicit safety questions:

- which rule protects management traffic?
- what is the fallback if no rules match?
- can we prove local/private traffic still works?
- can the proxy host still reach its own dependencies?

On production systems, route edits often deserve isolated change windows because they redefine behavior for many otherwise-healthy layers.
