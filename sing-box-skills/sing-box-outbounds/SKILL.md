---
name: sing-box-outbounds
description: "Production skill по outbounds sing-box: direct, block, dns, socks, http, selector, urltest, VLESS, VMess, Trojan, Shadowsocks, Hysteria2, SSH и актуальный WireGuard endpoint path. Использовать при выборе transport, fallback, proxy groups и клиентских/server-side peer схем."
---

# sing-box Outbounds

`outbounds` — это слой, который чаще всего получает больше всего внимания у начинающих инженеров и меньше всего дисциплины. Все спорят про VLESS, Trojan, Hysteria2 и WireGuard, но production-качество зависит не от названия протокола, а от того, насколько осознанно выбран тип выхода, как он сочетается с DNS, routing, TLS и целевым окружением.

Этот skill нужен, когда требуется:

- выбрать между `direct`, `block`, `dns`, `socks`, `http`, `selector`, `urltest` и proxy protocols;
- построить fallback-группу;
- правильно оформить VLESS/VMess/Trojan/Shadowsocks/Hysteria2/SSH outbound;
- понять, что WireGuard в современном official path связан с `endpoint/wireguard`, а не со старым outbound-first мышлением;
- подготовить sing-box-compatible client side для OpenWrt, Linux server, VPS, Podkop-like и 3x-ui-like environments.

## Official Source Map

- Outbound index: `https://sing-box.sagernet.org/configuration/outbound/`
- Direct: `https://sing-box.sagernet.org/configuration/outbound/direct/`
- Block: `https://sing-box.sagernet.org/configuration/outbound/block/`
- DNS outbound: `https://sing-box.sagernet.org/configuration/outbound/dns/`
- SOCKS outbound: `https://sing-box.sagernet.org/configuration/outbound/socks/`
- HTTP outbound: `https://sing-box.sagernet.org/configuration/outbound/http/`
- Selector: `https://sing-box.sagernet.org/configuration/outbound/selector/`
- URLTest: `https://sing-box.sagernet.org/configuration/outbound/urltest/`
- VLESS: `https://sing-box.sagernet.org/configuration/outbound/vless/`
- VMess: `https://sing-box.sagernet.org/configuration/outbound/vmess/`
- Trojan: `https://sing-box.sagernet.org/configuration/outbound/trojan/`
- Shadowsocks: `https://sing-box.sagernet.org/configuration/outbound/shadowsocks/`
- Hysteria2: `https://sing-box.sagernet.org/configuration/outbound/hysteria2/`
- SSH: `https://sing-box.sagernet.org/configuration/outbound/ssh/`
- WireGuard endpoint: `https://sing-box.sagernet.org/configuration/endpoint/wireguard/`
- Dial fields: `https://sing-box.sagernet.org/configuration/shared/dial/`
- V2Ray transport: `https://sing-box.sagernet.org/configuration/shared/v2ray-transport/`
- Deprecated: `https://sing-box.sagernet.org/deprecated/`

## Production Selection Model

Прежде чем выбрать outbound, ответить:

- нужен direct bypass, reject path или реальный proxy transport?
- это одиночный proxy или группа?
- важна ли автоматическая деградация/failover?
- upstream server задан IP или доменом?
- нужна ли TLS-обвязка?
- есть ли QUIC/UDP constraints?
- это endpoint-like transport such as WireGuard or traditional proxy transport?

С точки зрения design выбор идёт сверху вниз:

1. special utility outbounds;
2. grouping/failover layer;
3. actual transport layer;
4. dial/tls/transport fields;
5. route integration.

## Utility Outbounds

### `direct`

Назначение: отправить трафик напрямую.

Пример:

```json
{
  "type": "direct",
  "tag": "direct"
}
```

Production use:

- bypass local/LAN/corp targets;
- default path for server-side responses;
- fallback in split-tunnel designs.

Main risk:

- если `direct` резолвит доменные upstreams не тем resolver path, можно получить loops or leaks.

### `block`

Назначение: блокировать трафик.

```json
{
  "type": "block",
  "tag": "block"
}
```

Use cases:

- ad/tracker segments;
- denylist paths;
- safety guardrail for prohibited destinations.

### `dns`

Назначение: специальный outbound в DNS module path.

Production use:

- когда routing explicitly wants to hand off DNS traffic to the DNS module.

### `socks` and `http`

Используются как upstream proxy adapters.

SOCKS example:

```json
{
  "type": "socks",
  "tag": "upstream-socks",
  "server": "127.0.0.1",
  "server_port": 1080
}
```

HTTP example:

```json
{
  "type": "http",
  "tag": "upstream-http",
  "server": "127.0.0.1",
  "server_port": 8080
}
```

## Group Outbounds

### `selector`

Manual choice group.

```json
{
  "type": "selector",
  "tag": "manual-group",
  "outbounds": [
    "proxy-a",
    "proxy-b",
    "direct"
  ],
  "default": "proxy-a"
}
```

Use cases:

- operator-controlled switching;
- UI/manual profile selection;
- staged migration between servers.

### `urltest`

Automatic health and latency-based choice.

```json
{
  "type": "urltest",
  "tag": "auto-group",
  "outbounds": [
    "proxy-a",
    "proxy-b"
  ],
  "url": "https://www.gstatic.com/generate_204",
  "interval": "10m"
}
```

Production use:

- multiple similar nodes;
- resilient edge fleet;
- automatic failover preference.

## Proxy Protocol Outbounds

### VLESS

Один из самых production-important transports в modern sing-box ecosystems.

Base example:

```json
{
  "type": "vless",
  "tag": "vless-out",
  "server": "example.com",
  "server_port": 443,
  "uuid": "11111111-1111-1111-1111-111111111111",
  "flow": "xtls-rprx-vision",
  "tls": {
    "enabled": true,
    "server_name": "example.com"
  }
}
```

Advantages:

- modern protocol path;
- `xtls-rprx-vision` available;
- integrates with TLS and documented V2Ray transport options.

Disadvantages:

- transport and TLS mismatch kills connectivity hard;
- domain resolver oversight common when server uses hostname.

### VMess

Base example:

```json
{
  "type": "vmess",
  "tag": "vmess-out",
  "server": "example.com",
  "server_port": 443,
  "uuid": "11111111-1111-1111-1111-111111111111",
  "security": "auto",
  "tls": {
    "enabled": true,
    "server_name": "example.com"
  }
}
```

Advantages:

- compatibility with older stacks;
- transport flexibility.

Disadvantages:

- more legacy baggage;
- in new designs often less attractive than VLESS unless compatibility is the main goal.

### Trojan

Base example:

```json
{
  "type": "trojan",
  "tag": "trojan-out",
  "server": "edge.example.com",
  "server_port": 443,
  "password": "strong-password",
  "tls": {
    "enabled": true,
    "server_name": "edge.example.com"
  }
}
```

Advantages:

- simple mental model;
- good TLS-centric deployments.

Disadvantages:

- very sensitive to password/TLS mismatch;
- easy to misdiagnose as generic TLS failure.

### Shadowsocks

Base example:

```json
{
  "type": "shadowsocks",
  "tag": "ss-out",
  "server": "198.51.100.10",
  "server_port": 8388,
  "method": "2022-blake3-aes-128-gcm",
  "password": "strong-password"
}
```

Advantages:

- lightweight;
- broad operational familiarity;
- documented support for modern 2022 methods.

Disadvantages:

- plugin path must be treated carefully;
- `udp_over_tcp` conflicts with `multiplex`.

### Hysteria2

Base example:

```json
{
  "type": "hysteria2",
  "tag": "hy2-out",
  "server": "hy2.example.com",
  "server_port": 8443,
  "password": "strong-password",
  "tls": {
    "enabled": true,
    "server_name": "hy2.example.com"
  }
}
```

Advantages:

- UDP/QUIC-oriented high-performance path;
- supports hopping and more advanced scenarios.

Disadvantages:

- not suitable where UDP is blocked or unstable;
- TLS and QUIC misalignment quickly breaks the session.

### SSH

Base example:

```json
{
  "type": "ssh",
  "tag": "ssh-out",
  "server": "198.51.100.10",
  "server_port": 22,
  "user": "proxy",
  "private_key_path": "/root/.ssh/id_ed25519"
}
```

Advantages:

- useful in constrained or admin-centric scenarios;
- host key policy can be controlled.

Disadvantages:

- not a universal high-throughput replacement for mainstream proxy transports;
- operational posture depends heavily on SSH server policy.

## WireGuard in Modern sing-box

Production note номер один: official deprecated docs explicitly say WireGuard outbound is deprecated and can be replaced by endpoint.

Это значит:

- новый design не должен строить mental model “WireGuard is just another outbound”;
- нужно мыслить через `endpoint/wireguard` как modern path.

Base endpoint example:

```json
{
  "type": "wireguard",
  "tag": "wg-ep",
  "address": [
    "10.7.0.2/32"
  ],
  "private_key": "BASE64_PRIVATE_KEY",
  "peers": [
    {
      "address": "203.0.113.10",
      "port": 51820,
      "public_key": "BASE64_PUBLIC_KEY",
      "allowed_ips": [
        "0.0.0.0/0",
        "::/0"
      ]
    }
  ]
}
```

## OpenWrt Examples

### OpenWrt Direct + Proxy Group

```json
{
  "outbounds": [
    {
      "type": "direct",
      "tag": "direct"
    },
    {
      "type": "trojan",
      "tag": "proxy-a",
      "server": "edge-a.example.com",
      "server_port": 443,
      "password": "password-a",
      "tls": {
        "enabled": true,
        "server_name": "edge-a.example.com"
      }
    },
    {
      "type": "trojan",
      "tag": "proxy-b",
      "server": "edge-b.example.com",
      "server_port": 443,
      "password": "password-b",
      "tls": {
        "enabled": true,
        "server_name": "edge-b.example.com"
      }
    },
    {
      "type": "urltest",
      "tag": "proxy",
      "outbounds": [
        "proxy-a",
        "proxy-b"
      ],
      "url": "https://www.gstatic.com/generate_204",
      "interval": "10m"
    }
  ]
}
```

## Linux Server Examples

### Linux Server as Egress Policy Engine

```json
{
  "outbounds": [
    {
      "type": "direct",
      "tag": "direct"
    },
    {
      "type": "socks",
      "tag": "corp-upstream",
      "server": "127.0.0.1",
      "server_port": 1080
    }
  ]
}
```

### Linux Server with VLESS Egress

```json
{
  "outbounds": [
    {
      "type": "vless",
      "tag": "proxy",
      "server": "edge.example.com",
      "server_port": 443,
      "uuid": "11111111-1111-1111-1111-111111111111",
      "flow": "xtls-rprx-vision",
      "tls": {
        "enabled": true,
        "server_name": "edge.example.com"
      }
    }
  ]
}
```

## VPS Examples

### VPS Egress Relay Using Trojan

```json
{
  "outbounds": [
    {
      "type": "trojan",
      "tag": "relay",
      "server": "upstream.example.com",
      "server_port": 443,
      "password": "strong-password",
      "tls": {
        "enabled": true,
        "server_name": "upstream.example.com"
      }
    }
  ]
}
```

### VPS with WireGuard Endpoint

Useful for infra-like peer connectivity and routed egress, using the modern endpoint model.

## Podkop-Compatible Examples

Под official-only ограничением допустим только sing-box-side custom outbound pattern.

### Podkop-Compatible VLESS

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
  ]
}
```

### Podkop-Compatible Hysteria2

```json
{
  "outbounds": [
    {
      "type": "hysteria2",
      "tag": "proxy",
      "server": "hy2.example.com",
      "server_port": 8443,
      "password": "strong-password",
      "tls": {
        "enabled": true,
        "server_name": "hy2.example.com"
      }
    }
  ]
}
```

## 3x-ui-Compatible Examples

Тут снова допустим only sing-box-side counterpart.

### 3x-ui-Compatible Trojan Client

```json
{
  "outbounds": [
    {
      "type": "trojan",
      "tag": "proxy",
      "server": "content.example.com",
      "server_port": 443,
      "password": "panel-password",
      "tls": {
        "enabled": true,
        "server_name": "content.example.com"
      }
    }
  ]
}
```

### 3x-ui-Compatible VMess Client

```json
{
  "outbounds": [
    {
      "type": "vmess",
      "tag": "proxy",
      "server": "content.example.com",
      "server_port": 443,
      "uuid": "11111111-1111-1111-1111-111111111111",
      "security": "auto",
      "tls": {
        "enabled": true,
        "server_name": "content.example.com"
      }
    }
  ]
}
```

## Routing Schemes for Outbounds

### Direct Bypass

- local/private destinations -> `direct`
- everything else -> proxy group

### Manual Operator Choice

- `selector` decides active node

### Automatic Failover

- `urltest` sits above multiple real transports

### Protocol Segmentation

- UDP-friendly targets -> Hysteria2
- generic TLS/proxy targets -> VLESS or Trojan
- legacy compatibility -> VMess or Shadowsocks when justified

## Protocol Comparison Table

| Protocol | Strength | Weakness | Best Fit |
|---|---|---|---|
| VLESS | modern flexible path | exact transport/TLS matching required | modern client egress |
| VMess | compatibility | more legacy baggage | older ecosystems |
| Trojan | simple TLS mental model | easy TLS/password mismatch | TLS-centric deployments |
| Shadowsocks | lightweight | plugin/legacy confusion | simple egress |
| Hysteria2 | strong UDP/QUIC path | weak fit in blocked UDP networks | high-performance UDP-friendly paths |
| SSH | admin-friendly transport | not universal proxy replacement | constrained/operator scenarios |
| WireGuard endpoint | routed peer model | different mental model than proxy transports | infra/routed connectivity |

## Common Mistakes

### 1. Choosing protocol before route and DNS design

Result:

- beautiful outbound, broken system.

### 2. Forgetting `domain_resolver` for domain-based servers

Result:

- proxy host fails to resolve consistently.

### 3. Building new WireGuard logic on deprecated outbound assumptions

Result:

- outdated design and migration pain.

### 4. Using Hysteria2 where UDP is not realistically available

Result:

- unstable or nonfunctional sessions.

### 5. Mixing transport knobs from different protocol families

Result:

- config may validate poorly or behave unexpectedly.

## Troubleshooting

### Symptom: TCP connect works, session fails immediately

Check:

- TLS parameters;
- auth material;
- protocol-specific fields.

### Symptom: domain-based proxy host is flaky

Check:

- `domain_resolver`;
- upstream DNS path;
- route rules that affect proxy host resolution.

### Symptom: failover group behaves strangely

Check:

- whether the problem is in underlying outbounds or the group;
- `urltest` interval and health URL;
- manual vs automatic group semantics.

### Symptom: Hysteria2 fails while TCP-based transports work

Check:

- UDP reachability;
- QUIC/TLS path;
- password and obfuscation fields.

## Best Practices

- Keep utility outbounds explicit: `direct`, `block`, `dns`.
- Put real transports under clear tags and group names.
- For domain server names, review DNS ownership explicitly.
- Use `urltest` for homogeneous fleets; use `selector` when operator intent matters.
- Prefer modern official WireGuard endpoint path.
- Keep one low-complexity fallback transport for diagnostics.

## Version Compatibility

### 1.10

- traditional outbound-centric mindset still common.

### 1.11

- endpoint model becomes more important;
- WireGuard outbound already deprecated.

### 1.12

- broader migration pressure affects resolver and TLS assumptions around outbounds.

### 1.13 stable

- production baseline for this skill;
- modern protocol set and endpoint awareness should be default.

### 1.14 alpha

- future config structures appear in docs but are not to be forced into `1.13` production.

## Completion Criteria

Skill применён корректно, если:

- chosen outbound matches environment constraints;
- direct/block/grouping/transport layers separated conceptually;
- real JSON examples are provided;
- version-aware WireGuard and resolver guidance is followed.

## Deployment Playbooks

### Playbook: Single Reliable Egress

1. Start with one real transport plus `direct`.
2. Make DNS ownership explicit for the proxy host.
3. Validate handshake and route path.
4. Only then introduce grouping.

### Playbook: Failover Group

1. Validate every member outbound independently.
2. Add `urltest` or `selector`.
3. Confirm the health URL makes sense in the target network.
4. Keep one simple fallback transport for diagnostics.

### Playbook: Modern WireGuard Design

1. Decide whether the use case is really routed endpoint connectivity.
2. Use official endpoint path, not legacy outbound mental model.
3. Validate peer keys and allowed IPs before layering route complexity.

## Environment Decision Matrix

### OpenWrt

Prefer:

- simple direct + one proxy baseline first;
- groups only after router policy is stable;
- UDP-heavy transports only when the network and hardware justify them.

### Linux Server

Prefer:

- explicit direct bypass and one controlled egress transport;
- process/inbound segmentation when multiple workloads share the host.

### VPS

Prefer:

- clear server/relay role;
- avoid clever multi-protocol groups until the basic egress path is proven.

## Validation Checklist

- Transport matches network constraints.
- Proxy host resolver path defined.
- Group members validated individually.
- WireGuard designs use endpoint terminology and structure.
- Direct/block utility outbounds present where policy requires them.

## Senior Review Questions

- Why is this protocol better here than a simpler one?
- If the network blocks UDP, what is the fallback?
- Is the grouping layer hiding a broken member?
- Are we debugging transport, DNS or policy?

## Field Notes

### `server` and `server_port`

When a production issue says “proxy is down”, the first question is whether it is really down or merely unresolved. Domain-based `server` values should always trigger a resolver ownership review.

### `tls`

For most modern transports, TLS is not an optional ornament but part of the actual protocol contract. Therefore, outbound review must verify TLS semantics together with transport, not later.

### `transport`

Official V2Ray transport docs warn about behavioral differences from other ecosystems. Senior review should not assume community transport names imply identical runtime behavior.

## Scenario Catalog

### Scenario: Single Node Client

Use one transport, one direct fallback and explicit route policy. Avoid groups until the single-node path is stable.

### Scenario: Two-Node Resilient Client

Validate both transports independently, then add `urltest` or `selector`. Do not use group success as proof that each member is healthy.

### Scenario: Router Egress Policy

On OpenWrt or Linux gateway, outbounds are part of a resource budget. High-complexity transport choice should be justified not only by protocol capability, but by CPU, DNS and policy cost.

## Change Management Notes

Outbound changes should be sequenced from simple to complex:

1. validate one transport;
2. validate TLS and resolver path;
3. validate route integration;
4. only then add groups, failover or alternate protocols.

A surprisingly large number of “protocol problems” are actually group-design or resolver-ownership problems introduced during overly broad changes.
