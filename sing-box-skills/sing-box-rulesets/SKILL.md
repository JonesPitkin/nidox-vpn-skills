---
name: sing-box-rulesets
description: "Production skill по rule sets в sing-box: inline, local, remote, source и binary форматы, migration с GeoSite/GeoIP, caching, update strategy и эксплуатация reusable policy sets на клиентах, серверах и роутерах."
---

# sing-box Rule Sets

`rule_set` — это один из главных признаков mature `sing-box` architecture. Как только policy становится больше нескольких ручных `domain_suffix` правил, инженер почти неизбежно приходит к необходимости вынести её в переиспользуемые наборы правил. В `sing-box` это не костыль и не внешняя надстройка, а официальный современный путь, который пришёл на смену устаревающим `GeoSite` и `GeoIP`.

Этот skill нужен, когда требуется:

- мигрировать старые geosite/geoip-конфиги;
- организовать reusable policy layers;
- выбрать между `inline`, `local` и `remote` rule sets;
- понимать разницу `source` и `binary`;
- настроить update/caching strategy;
- проектировать policy for OpenWrt, Linux, VPS and sing-box-compatible consumers.

## Official Source Map

- Rule Set index: `https://sing-box.sagernet.org/configuration/rule-set/`
- Headless Rule: `https://sing-box.sagernet.org/configuration/rule-set/headless-rule/`
- Source Format: `https://sing-box.sagernet.org/configuration/rule-set/source-format/`
- Migration: `https://sing-box.sagernet.org/migration/`
- Deprecated: `https://sing-box.sagernet.org/deprecated/`
- sing-geosite repository: `https://github.com/SagerNet/sing-geosite`
- sing-box repository: `https://github.com/SagerNet/sing-box`

## Why Rule Sets Matter

Production reasons:

- policy is reusable;
- rules become auditable;
- update cadence can be separated from core config;
- router and client fleets can share a policy source;
- migration from old geo-oriented mechanisms gets a supported path.

В official docs `rule_set` появляется как полноценный path с `1.8.0`. Дальнейшие deprecated notes прямо подталкивают инженера уходить от `GeoIP` и `Geosite`.

## Stable Baseline

Для stable `1.13.13` supported patterns:

- `inline`
- `local`
- `remote`
- `format: source`
- `format: binary`
- `download_detour` для remote in stable line
- `experimental.cache_file.enabled` для useful cache behavior

Важно:

- official mainline already documents future `http_client` path for remote rule sets in `1.14`;
- production baseline для этой базы остаётся stable `1.13.13`.

## Rule Set Types

### Inline

Rule set живёт внутри root config.

Пример:

```json
{
  "route": {
    "rule_set": [
      {
        "type": "inline",
        "tag": "corp-inline",
        "rules": [
          {
            "domain_suffix": [
              ".corp.example"
            ]
          }
        ]
      }
    ]
  }
}
```

Best for:

- small embedded policies;
- test configs;
- tightly coupled one-off logic.

Risk:

- scaling pain;
- poor reuse across environments.

### Local

Rule set хранится в локальном файле.

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
    ]
  }
}
```

Best for:

- Git-managed infrastructure;
- OpenWrt and Linux server deployments;
- audited static policies.

### Remote

Rule set загружается по URL.

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "policy",
        "format": "binary",
        "url": "https://example.invalid/policy.srs",
        "download_detour": "proxy",
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

Best for:

- central policy distribution;
- fleet updates;
- consistent client/router policy without manually copying files.

## Source vs Binary

### `source`

Плюсы:

- human-readable;
- easier review and diffing;
- better for authoring.

Минусы:

- not always the smallest or simplest distribution artifact.

### `binary`

Плюсы:

- distribution-friendly;
- often cleaner for production consumption.

Минусы:

- not human-readable during incident response;
- usually requires separate source-of-truth elsewhere.

## Real Production Configurations

### Local Source Rule Set

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

### Local Binary Rule Set

```json
{
  "route": {
    "rule_set": [
      {
        "type": "local",
        "tag": "policy",
        "format": "binary",
        "path": "/etc/sing-box/rules/policy.srs"
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
    ]
  }
}
```

### Remote Rule Set with Cache

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "policy",
        "format": "binary",
        "url": "https://example.invalid/policy.srs",
        "download_detour": "proxy",
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
  },
  "experimental": {
    "cache_file": {
      "enabled": true
    }
  }
}
```

## Migration from GeoSite and GeoIP

Официальные migration docs дают прямые ориентиры:

- `geosite` -> `rule_set`
- `geoip` -> `rule_set`
- custom conversion can involve sing-box tooling and official rule-set artifacts

Production rule:

- new config must not introduce `geosite`/`geoip`;
- legacy config may reference them only as migration context;
- operational docs should point engineers toward rule-set-native design.

### Example Migration Concept

Old mental model:

- “route this domain category via `geosite`”

New mental model:

- “route this reusable policy tag via `rule_set`”

This shift matters because it moves the system from hardcoded legacy categories to explicit policy assets.

## OpenWrt Examples

### OpenWrt Local Rule Set

```json
{
  "route": {
    "rule_set": [
      {
        "type": "local",
        "tag": "router-policy",
        "format": "source",
        "path": "/etc/sing-box/router-policy.json"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "router-policy"
        ],
        "action": "route",
        "outbound": "proxy"
      }
    ],
    "final": "direct"
  }
}
```

### OpenWrt Remote Rule Set

Useful when a fleet of routers shares one maintained policy source.

## Linux Server Examples

### Server-Local Managed Policy

```json
{
  "route": {
    "rule_set": [
      {
        "type": "local",
        "tag": "corp",
        "format": "source",
        "path": "/srv/sing-box/rules/corp.json"
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
    ],
    "final": "proxy"
  }
}
```

## VPS Examples

### VPS Remote Policy Distribution

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
        "outbound": "relay"
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

## Podkop-Compatible Examples

Only sing-box-native logic may be described.

### Custom Policy Set Template

```json
{
  "route": {
    "rule_set": [
      {
        "type": "local",
        "tag": "custom",
        "format": "source",
        "path": "/etc/sing-box/custom.json"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "custom"
        ],
        "action": "route",
        "outbound": "proxy"
      }
    ],
    "final": "direct"
  }
}
```

## 3x-ui-Compatible Examples

Again, only sing-box-side examples are valid here. A 3x-ui-provisioned outbound can be paired with rule-set based routing exactly like any other outbound:

```json
{
  "route": {
    "rule_set": [
      {
        "type": "local",
        "tag": "bypass",
        "format": "source",
        "path": "/etc/sing-box/bypass.json"
      }
    ],
    "rules": [
      {
        "rule_set": [
          "bypass"
        ],
        "action": "route",
        "outbound": "direct"
      }
    ],
    "final": "proxy"
  }
}
```

## Routing Schemes with Rule Sets

### Domain Category Routing

- `rule_set` stores domains or other policy elements
- route rules consume only tag references

### Source/Policy Hybrid

- base route uses process/source/private rules
- reusable categories live in `rule_set`

### Fleet Policy Model

- remote rule set distributed to routers/clients/servers
- one policy source, many consumers

## Comparison Table

| Type | Best For | Benefit | Risk |
|---|---|---|---|
| Inline | tiny policies | no external file | poor scalability |
| Local source | audited infra | readable and versioned | file distribution overhead |
| Local binary | compact production asset | deployment simplicity | not human-readable |
| Remote binary | fleet policy | centralized updates | cache/update dependency |

## Common Mistakes

### 1. New configs still use `geosite`/`geoip`

Result:

- immediate architecture debt.

### 2. Rule set declared but never referenced correctly

Result:

- policy silently absent.

### 3. Remote sets without cache strategy

Result:

- unexpected runtime behavior or brittle updates.

### 4. Binary-only policy without a readable source of truth

Result:

- painful incident response.

### 5. Naming rule-set tags inconsistently

Result:

- hard-to-review configurations and copy/paste mistakes.

## Troubleshooting

### Symptom: route rule referencing rule set never matches

Check:

- tag spelling;
- path/url correctness;
- whether the rule-set file format matches declared `format`.

### Symptom: remote policy updates inconsistently

Check:

- `update_interval`;
- `download_detour`;
- `experimental.cache_file.enabled`;
- network reachability to the source.

### Symptom: migration from geosite seems incomplete

Check:

- whether route rules still contain old fields;
- whether policy semantics were translated or merely renamed.

## Best Practices

- Treat rule sets as policy assets, not random helper files.
- Prefer local source format for authoring, binary for controlled distribution if needed.
- Standardize tag naming.
- Keep a clear source of truth for generated binary sets.
- Explicitly document update cadence for remote sets.
- Use rule sets for stable reusable policy, not for every tiny one-off rule.

## Version Compatibility

### 1.10

- inline rule sets already relevant in modern design.

### 1.11

- legacy geo fields already clearly on the way out.

### 1.12

- migration pressure is strong; modern design should be rule-set-first.

### 1.13 stable

- baseline for this repository;
- `download_detour` remains the stable remote distribution path.

### 1.14 alpha

- official future docs show `http_client` direction, but stable consumers should remain on validated `1.13` semantics unless explicitly upgraded.

## Completion Criteria

Skill применён правильно, если:

- policy asset type chosen explicitly;
- geosite/geoip legacy path avoided in new config;
- route integration shown with real JSON;
- update and cache behavior explained.

## Policy Lifecycle Playbooks

### Playbook: Author in Source, Distribute in Binary

1. Maintain source-format policy in version control.
2. Review and test it locally.
3. Publish binary artifacts for consumers if distribution simplicity matters.
4. Keep source-of-truth references documented.

### Playbook: Router Fleet Policy

1. Keep one shared policy source.
2. Use remote binary sets only after cache behavior is understood.
3. Keep local direct-safe exceptions outside huge shared sets where appropriate.

### Playbook: Migration from Legacy Geo

1. Identify every `geosite` and `geoip` usage.
2. Map semantics to `rule_set`.
3. Replace legacy root sections and rule fields.
4. Validate behavior category by category rather than all at once.

## Validation Checklist

- Rule-set type chosen intentionally.
- `format` matches artifact reality.
- Tag naming is consistent.
- Remote sets have update and cache strategy.
- Legacy geo fields removed from new design.
- There is a readable policy source somewhere.

## Senior Review Questions

- Is this policy asset reusable across hosts?
- Can an on-call engineer understand it during an incident?
- What happens if the remote source is unavailable?
- Which categories belong in reusable sets, and which belong in host-local rules?

## Field Notes

### `tag`

Rule-set tags are not cosmetic. They become the vocabulary of your policy system. Weak naming produces configs that nobody can review confidently during an outage.

### `update_interval`

This field is an operational contract. If remote policy changes too often, the fleet becomes unpredictable. If it changes too slowly, the policy becomes stale. Senior design ties update cadence to actual policy ownership.

### `download_detour`

In stable `1.13`, this is still a meaningful remote acquisition control. It should be treated as part of supply-path design, not as a random knob.

## Scenario Catalog

### Scenario: Corporate Policy Distribution

Many clients share one domain/IP policy source. Remote binary sets with cache can work well, but only if the organization accepts centralized policy change risk.

### Scenario: Home Router with Personal Allow/Block Lists

Local source sets are often superior here because readability and deterministic control beat remote automation.

### Scenario: Migration Cleanup Project

When a repo contains years of `geosite` and `geoip` cargo-culting, the cleanest approach is to define a modern rule-set vocabulary first, then migrate categories into it deliberately.

## Change Management Notes

Rule-set changes are policy publication events. Senior teams treat them as content deploys:

- source of truth updated;
- artifact format known;
- update cadence controlled;
- consumer cache behavior understood;
- rollback asset available.

This prevents a central rule-set source from becoming an unreviewed global blast radius.
