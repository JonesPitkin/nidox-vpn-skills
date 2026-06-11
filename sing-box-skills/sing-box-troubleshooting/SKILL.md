---
name: sing-box-troubleshooting
description: "Production troubleshooting skill по sing-box: запуск, DNS, FakeIP, TUN, route rules, rule sets, TLS, REALITY, Hysteria2, WireGuard, OpenWrt and VPS incidents. Использовать для пошаговой локализации первопричины и безопасного восстановления."
---

# sing-box Troubleshooting

Production troubleshooting в `sing-box` начинается не с догадки и не с любимого протокола инженера, а с дисциплины. Любая проблема должна быть локализована по слоям. Это особенно важно в `sing-box`, потому что один и тот же пользовательский симптом — “не открывается сайт” или “не подключается proxy” — может быть вызван:

- синтаксической ошибкой конфига;
- неправильным listener;
- broken DNS path;
- route mismatch;
- deprecated field;
- TUN loop;
- TLS verify failure;
- transport-specific mismatch;
- policy cache/update issue.

Этот skill должен сделать агент спокойным, последовательным и инженерно аккуратным.

## Official Source Map

- Configuration index: `https://sing-box.sagernet.org/configuration/`
- DNS: `https://sing-box.sagernet.org/configuration/dns/`
- Inbounds: `https://sing-box.sagernet.org/configuration/inbound/`
- Outbounds: `https://sing-box.sagernet.org/configuration/outbound/`
- Route: `https://sing-box.sagernet.org/configuration/route/`
- Rule Set: `https://sing-box.sagernet.org/configuration/rule-set/`
- TLS: `https://sing-box.sagernet.org/configuration/shared/tls/`
- Migration: `https://sing-box.sagernet.org/migration/`
- Deprecated: `https://sing-box.sagernet.org/deprecated/`
- Releases: `https://github.com/SagerNet/sing-box/releases`

## Golden Troubleshooting Order

Всегда идти в таком порядке:

1. version and syntax
2. process and service lifecycle
3. listener/inbound reachability
4. DNS
5. routing and rule-set policy
6. outbound reachability
7. TLS/REALITY/security
8. transport-specific features
9. performance and optimization issues

Если этот порядок нарушить, инженер почти всегда начинает лечить симптомы, а не причину.

## Universal First Steps

### 1. Confirm Version

Убедиться, что обсуждаемая конфигурация соответствует target version:

- `1.10`
- `1.11`
- `1.12`
- `1.13 stable`
- `1.14 alpha/mainline`

### 2. Format and Check

```bash
sing-box format -w -c config.json -D config_directory
sing-box check -c config.json -D config_directory
```

Это обязательный этап. Если инженер не сделал этого, вся дальнейшая диагностика может идти по ложному следу.

### 3. Review Deprecated and Migration Notes

Особенно при симптомах “раньше работало, после обновления нет”.

## Case 1: Service Does Not Start

### Symptoms

- process immediately exits;
- systemd/procd restarts repeatedly;
- no listener appears.

### Causes

- invalid JSON;
- unsupported or deprecated fields;
- wrong root structure for version;
- missing referenced files or wrong paths.

### Diagnostics

- run `format` and `check`;
- verify path semantics with `-D config_directory`;
- compare config against target version docs;
- inspect deprecated notes for DNS, WireGuard, TUN, ECH, geosite/geoip.

### Fix

- remove invalid fields;
- migrate old syntax;
- reduce to minimal baseline and add sections back gradually.

## Case 2: DNS Fails

### Symptoms

- domains fail, IPs work;
- some domains work, some hang;
- proxy host with domain name is unstable.

### Causes

- wrong `dns.final`;
- wrong server selected by DNS rules;
- missing `domain_resolver`;
- secure DNS TLS mismatch;
- old DNS formats after version upgrade.

### Diagnostics

- inspect `dns.servers`, `dns.rules`, `dns.final`;
- verify whether app/client DNS really enters `sing-box`;
- verify upstream proxy hostname resolution path;
- compare with stable DNS docs and migration notes.

### Fix

- simplify DNS topology;
- make `final` explicit;
- add `domain_resolver` where needed;
- re-check `server_name` and path for DoH/DoT.

## Case 3: FakeIP Problems

### Symptoms

- synthetic IP answers appear, but policy does not work;
- apps break unexpectedly;
- domain-based routing seems lost after resolution.

### Causes

- FakeIP enabled without route alignment;
- no `reverse_mapping`;
- DNS path bypasses `sing-box`;
- fake ranges conflict or assumptions are incomplete.

### Diagnostics

- verify `type: fakeip`;
- verify reverse mapping;
- verify route rules depend on domain-aware logic appropriately;
- test without FakeIP to isolate behavior.

### Fix

- reintroduce FakeIP only where transparent/domain-restoration semantics are required;
- align TUN, DNS and route together.

## Case 4: TUN Starts but Traffic Does Not Work

### Symptoms

- TUN interface exists;
- some traffic works, some not;
- internet or local resources disappear.

### Causes

- missing exclusions;
- wrong `route.final`;
- DNS leak or DNS bypass;
- loop through wrong interface;
- auto-redirect complexity.

### Diagnostics

- validate `address`, `route_address`, `route_exclude_address`;
- verify admin/local subnets;
- test minimal TUN config without advanced route rules;
- disable `auto_redirect` temporarily if needed to isolate.

### Fix

- simplify to minimal TUN;
- add exclusions first;
- restore DNS control;
- reintroduce route complexity gradually.

## Case 5: Routing Loops or Wrong Policy

### Symptoms

- local traffic unexpectedly proxied;
- proxy host cannot be reached consistently;
- requests take wrong path or hang.

### Causes

- catch-all rules before exceptions;
- missing `final`;
- wrong assumption about private ranges;
- `rule_set` tag mismatch;
- proxy host DNS resolving into the same policy trap.

### Diagnostics

- review rule order;
- inspect `rule_set` declarations and references;
- verify `final`;
- review whether route and DNS are aligned.

### Fix

- narrow exceptions first;
- explicit `final`;
- isolate rule sets and test them one by one.

## Case 6: Remote Rule Set Issues

### Symptoms

- category policy never matches;
- updates seem stale;
- deployment works once then drifts.

### Causes

- wrong `format`;
- wrong `path` or `url`;
- missing or misunderstood cache behavior;
- version mismatch around remote rule-set options.

### Diagnostics

- verify stable `1.13` remote semantics;
- confirm `download_detour` and `update_interval`;
- confirm `experimental.cache_file.enabled`;
- test with a local static replacement to isolate network/update issues.

### Fix

- move to a local tested set first;
- then restore remote distribution with explicit cache policy.

## Case 7: TLS Failures

### Symptoms

- TCP connects but proxy session dies;
- certificate verify fails;
- handshake resets immediately.

### Causes

- wrong `server_name`;
- wrong cert or key path;
- inbound/outbound TLS role confusion;
- old ECH fields or future-only assumptions.

### Diagnostics

- verify DNS and route first;
- check cert identity;
- verify TLS block placement;
- compare config with stable target docs.

### Fix

- return to minimal TLS config;
- remove optional features until the base handshake works.

## Case 8: REALITY Fails

### Symptoms

- direct TCP reachability exists, but proxy does not connect;
- failure persists despite seemingly valid TLS settings.

### Causes

- client/server role mismatch;
- wrong public/private key usage;
- short ID mismatch;
- unrelated DNS or route problem misread as REALITY.

### Diagnostics

- verify client has `public_key`, server has `private_key`;
- verify short ID alignment;
- verify route and DNS path for the proxy host.

### Fix

- reapply minimal documented REALITY blocks;
- add no other advanced features until it works.

## Case 9: Hysteria2 Fails

### Symptoms

- transport fails while TCP-based alternatives work;
- severe instability;
- timeout patterns inconsistent with other protocols.

### Causes

- blocked or degraded UDP;
- wrong TLS/SNI;
- wrong password;
- too many advanced features introduced at once.

### Diagnostics

- test a minimal Hysteria2 config;
- compare against a TCP transport baseline;
- validate QUIC/UDP environment assumptions.

### Fix

- strip back to minimal config;
- use TCP-based fallback if the network clearly punishes UDP.

## Case 10: WireGuard Path Issues

### Symptoms

- handshake never becomes useful traffic;
- routed traffic blackholes.

### Causes

- outdated outbound mental model;
- wrong endpoint keys;
- wrong allowed IPs;
- route conflicts.

### Diagnostics

- verify official endpoint path, not legacy outbound assumptions;
- inspect addresses and peer settings;
- verify routing expectations around allowed IPs.

### Fix

- return to minimal endpoint example from official docs;
- rebuild route policy around it.

## OpenWrt-Specific Troubleshooting

### Symptoms

- all LAN clients lose connectivity;
- LuCI/SSH inaccessible;
- router resolves names but clients do not.

### Causes

- admin subnet not excluded;
- DNS path not adapted to router role;
- TUN/TProxy rollout too aggressive;
- rule sets or proxy host path break the router’s own control plane.

### Diagnostics

- verify official `procd` service path;
- test router-local connectivity separately from client connectivity;
- keep rollback access ready;
- verify that local/private domains stay local.

### Fix

- strip to direct baseline;
- reintroduce DNS;
- reintroduce transparent capture;
- reintroduce policy last.

## Linux Server and VPS Troubleshooting

Linux and VPS problems often look similar, but priorities differ:

- Linux server: process, user, local service and interface issues common;
- VPS: public TLS, upstream reachability and policy recursion more common.

Troubleshooting should reflect that context rather than applying generic fixes.

## Podkop-Compatible Troubleshooting

Because only official sing-box facts are allowed, Podkop troubleshooting here means:

- validate the underlying sing-box-compatible JSON;
- isolate whether the issue exists in plain sing-box semantics before attributing it to a higher-level system.

## 3x-ui-Compatible Troubleshooting

Same principle:

- validate the sing-box-side counterpart against official protocol docs;
- do not infer panel behavior that is not in official sing-box sources.

## Comparison Table

| Symptom Class | First Layer to Check | Common Root Cause |
|---|---|---|
| service exits | syntax/version | deprecated or invalid config |
| domains fail | DNS | wrong final/rule/resolver |
| transparent path broken | TUN/routing | exclusions or loops |
| proxy connects then dies | TLS/security | name/cert/role mismatch |
| category routing wrong | route/rule set | tag/order mismatch |
| router-wide outage | OpenWrt/TUN | unsafe rollout |

## Common Mistakes

### 1. Jumping straight to the transport layer

### 2. Ignoring version and deprecated notes

### 3. Changing too many variables at once

### 4. Treating app symptom as proof of network-layer cause

### 5. No minimal reproducible baseline

Each of these turns routine troubleshooting into guesswork.

## Best Practices

- Troubleshoot one layer at a time.
- Always keep a minimal known-good baseline.
- Version-gate every fix.
- Use official docs to confirm whether the issue is syntax, migration or runtime.
- On routers, preserve rollback access before experimentation.
- Document the first broken layer, not just the final fix.

## Version Compatibility

### 1.10

- old community snippets often originate here or around here; migration drift is common.

### 1.11

- endpoint-related misunderstandings appear more often.

### 1.12

- DNS and ECH migration issues become much more common.

### 1.13 stable

- baseline for this repository;
- most production troubleshooting should validate against this stable semantics.

### 1.14 alpha

- do not diagnose a stable deployment using alpha-only assumptions unless the target is explicitly alpha.

## Completion Criteria

Skill применён правильно, если:

- first broken layer identified;
- fix proposal tied to version-aware official semantics;
- issue separated from neighboring layers;
- rollback-safe remediation path proposed.

## Incident Playbooks

### Playbook: After Upgrade Failure

1. Identify previous and current version.
2. Re-run `format` and `check`.
3. Open `deprecated` and `migration` for the target stable.
4. Isolate removed or legacy fields.
5. Reduce to minimal baseline if necessary.

### Playbook: Router-Wide Outage

1. Verify router-local admin access.
2. Validate service state.
3. Disable or reduce transparent capture if needed.
4. Restore direct path.
5. Reintroduce DNS and route incrementally.

### Playbook: Proxy Hostname Problem

1. Test with IP if possible.
2. Inspect `domain_resolver`.
3. Inspect DNS rules and final server.
4. Only after that inspect transport details.

## Validation Checklist

- Broken layer identified explicitly.
- Version mismatch ruled out.
- Minimal baseline available.
- Router/admin rollback path considered where relevant.
- No simultaneous multi-layer changes proposed without isolation.

## Senior Review Questions

- What is the first thing that is definitely broken, not just visibly broken?
- What would still fail if we swapped the transport for `direct`?
- Are we seeing a config bug, a version bug or a topology bug?
- What is the smallest safe rollback?

## Troubleshooting Heuristics

### Heuristic: Prefer Baselines Over Beliefs

If the engineer says “this part must be fine”, but there is no minimal baseline proving it, treat the statement as unverified. `sing-box` failures often hide behind confident but wrong assumptions.

### Heuristic: DNS and Route Masquerade as Transport

Whenever a domain-based outbound fails, assume DNS or route may be guilty until proven otherwise. This one habit prevents a large amount of wasted TLS and protocol debugging.

### Heuristic: Router Incidents Are Different

On OpenWrt, the question is not merely “why does traffic fail?” but also “what still allows recovery?” That changes fix ordering and rollback priorities.

## Scenario Catalog

### Scenario: Works on Desktop, Fails on Router

Assume topology difference first: DNS ownership, local subnet treatment, transparent capture and admin-path exclusions usually differ more than the protocol itself.

### Scenario: Works with IP, Fails with Domain

This is a DNS/resolver ownership investigation until proven otherwise.

### Scenario: Works Until Version Upgrade

This is a migration/deprecated investigation until proven otherwise.

## Change Management Notes

The best troubleshooting often happens before the incident:

- keep a known-good baseline;
- record target version;
- separate transport changes from DNS changes;
- keep rollback artifacts for router and server deployments.

When those habits are absent, troubleshooting becomes archaeology instead of engineering.
