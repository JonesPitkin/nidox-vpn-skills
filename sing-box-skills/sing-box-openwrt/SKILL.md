---
name: sing-box-openwrt
description: "Production skill по использованию sing-box на OpenWrt: установка, procd, config paths, DNS, TUN/TProxy patterns, performance, router policy design и safe integration with sing-box-compatible environments."
---

# sing-box OpenWrt

OpenWrt — одна из самых demanding сред для `sing-box`. На desktop можно пережить лишний route loop или ручной restart. На роутере цена ошибки выше: пропадает интернет у всех клиентов, теряется доступ к панели управления, ломаются DHCP/DNS assumptions и становится трудно даже собрать диагностику. Поэтому production skill по OpenWrt должен быть особенно дисциплинированным: никакой магии, только официальные paths и network-aware reasoning.

Этот skill нужен, когда надо:

- установить и запустить `sing-box` на OpenWrt;
- понять официальный procd lifecycle;
- выбрать между TUN and TProxy router models;
- связать DNS, route rules, policy sets и proxy transports;
- подготовить safe rollout на домашнем или edge router;
- объяснить, как OpenWrt-hosted `sing-box` соотносится с Podkop-like, 3x-ui-like and other sing-box-compatible ecosystems без выхода за рамки official-only фактов.

## Official Source Map

- Package manager install: `https://sing-box.sagernet.org/installation/package-manager/`
- Main repository: `https://github.com/SagerNet/sing-box`
- Releases: `https://github.com/SagerNet/sing-box/releases`
- TUN inbound: `https://sing-box.sagernet.org/configuration/inbound/tun/`
- Route: `https://sing-box.sagernet.org/configuration/route/`
- DNS: `https://sing-box.sagernet.org/configuration/dns/`
- release config `openwrt.conf` and `openwrt.init` from official repo

## Official OpenWrt Packaging Model

Official repository contains OpenWrt-specific runtime assets.

### `openwrt.conf`

```uci
config sing-box 'main'
	option enabled '1'
	option conffile '/etc/sing-box/config.json'
	option workdir '/usr/share/sing-box'
	option log_stderr '1'
```

### `openwrt.init`

Production meaning of the official init script:

- service managed by `procd`
- runtime command is `sing-box run -c "$config_file" -D "$working_directory"`
- config file watched for reload
- stderr logging controllable
- `nofile` limit raised significantly
- service respawns

Это даёт инженеру официальную operational модель, а не community folklore.

## Installation Paths

Официальная документация по package manager отмечает OpenWrt support и install script path.

Практически полезно различать:

- package/release-based installation;
- config deployment;
- service enablement;
- later policy/rule-set updates.

## OpenWrt Deployment Models

### 1. Local Router Utility Proxy

Роутер сам использует локальный outbound path для своих сервисов и admin tasks.

### 2. Client Router Transparent Mode

Клиенты LAN используют роутер как transparent gateway.

### 3. Policy Router

Часть трафика идёт напрямую, часть через proxy group based on route rules.

### 4. Transit/Relay Role

Менее типично для OpenWrt, но возможно на мощных устройствах.

## Real OpenWrt Configurations

### Minimal Managed Config

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

Это service baseline, useful before any transparent capture.

### OpenWrt TUN Router Baseline

```json
{
  "log": {
    "level": "info"
  },
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
    "reverse_mapping": true
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
    },
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

### OpenWrt TProxy Skeleton

```json
{
  "inbounds": [
    {
      "type": "tproxy",
      "tag": "tproxy-tcp",
      "listen": "::",
      "listen_port": 60080,
      "network": "tcp"
    },
    {
      "type": "tproxy",
      "tag": "tproxy-udp",
      "listen": "::",
      "listen_port": 60080,
      "network": "udp"
    }
  ]
}
```

This is useful when router policy is built around Linux transparent interception rather than TUN semantics.

## DNS on OpenWrt

OpenWrt makes DNS especially delicate because the router often already acts as:

- DHCP server;
- local DNS forwarder;
- default gateway;
- management host.

Production implications:

- local domains must remain resolvable;
- management-plane DNS should not disappear into a proxy path accidentally;
- `reverse_mapping` and FakeIP must be introduced with full awareness of client impact.

### OpenWrt Split DNS Example

```json
{
  "dns": {
    "servers": [
      {
        "tag": "local",
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
          ".lan"
        ],
        "action": "route",
        "server": "local"
      }
    ],
    "final": "remote"
  }
}
```

## Performance Considerations

OpenWrt hardware varies wildly. Even without using non-official hardware-specific sources, the general production considerations are clear:

- TUN is usually heavier than simple local proxy modes;
- Hysteria2/QUIC paths may stress CPU differently from TCP-based transports;
- remote rule sets and large DNS policy tables increase memory and I/O pressure;
- verbose logging is expensive on constrained flash/storage.

Production rule:

- start with the smallest working design;
- only then add transparent capture, large rule sets and advanced routing.

## Linux Server and VPS Relevance

Этот skill открыт про OpenWrt, но полезно уметь сравнить его с Linux Server and VPS models:

- OpenWrt is a router-first environment;
- Linux server is service-first;
- VPS is remote-edge-first.

Это помогает не переносить server assumptions на router, например не считать, что management access can always be recovered later.

## Podkop-Compatible Examples

Only sing-box-native logic may be documented.

### Podkop-Like Router TUN Core

```json
{
  "inbounds": [
    {
      "type": "tun",
      "tag": "tun-in",
      "address": [
        "172.19.0.1/30"
      ],
      "auto_route": true,
      "stack": "system"
    }
  ]
}
```

This is valid as a conceptual sing-box router core that a higher-level system may generate.

## 3x-ui-Compatible Examples

Again, only sing-box-side compatibility logic is valid.

### OpenWrt Client for 3x-ui-Provisioned Server

```json
{
  "outbounds": [
    {
      "type": "vless",
      "tag": "proxy",
      "server": "content.example.com",
      "server_port": 443,
      "uuid": "11111111-1111-1111-1111-111111111111",
      "tls": {
        "enabled": true,
        "server_name": "content.example.com"
      }
    }
  ],
  "route": {
    "final": "proxy"
  }
}
```

## Routing Schemes on OpenWrt

### Direct-First Router

- private and local domains direct
- chosen categories via proxy
- safer starting point

### Proxy-First Router

- everything through proxy except explicit bypass
- higher leak protection but higher deployment risk

### Rule-Set Driven Router

- reusable policy tags determine egress
- best for repeatable fleet configurations

## Comparison Table

| OpenWrt Mode | Benefit | Main Risk | Best Fit |
|---|---|---|---|
| Simple local proxy | low complexity | no transparent coverage | admin/testing |
| TUN router | clean transparent UX | route/DNS/admin complexity | client-router deployments |
| TProxy router | strong transparent control | firewall complexity | advanced gateway |
| Rule-set router | reusable policy | update/caching dependencies | managed fleets |

## Common Mistakes

### 1. Deploying TUN before mapping management paths

Result:

- SSH/LuCI lockout.

### 2. Using router-wide proxy path without LAN/private bypass

Result:

- broken local service discovery and internal access.

### 3. Forgetting OpenWrt service lifecycle

Result:

- config copied into place but not aligned with official `procd` path.

### 4. Treating router DNS like desktop DNS

Result:

- client-facing failures and local name resolution breakage.

### 5. Overbuilding on weak hardware

Result:

- unstable throughput and difficult diagnostics.

## Troubleshooting

### Symptom: service starts but clients lose internet

Check:

- route.final;
- excluded local networks;
- DNS final server;
- whether transparent capture exceeds the intended scope.

### Symptom: LuCI/SSH lost after rollout

Check:

- `route_exclude_address`;
- admin subnet placement;
- direct bypass rules.

### Symptom: WAN works on router, clients fail

Check:

- client traffic actually enters `sing-box`;
- DNS path for LAN clients;
- route rules based on inbound or source assumptions.

### Symptom: remote policy or proxy seems intermittently unavailable

Check:

- cache and rule-set updates;
- resolver path for proxy host;
- whether the router itself can still resolve and reach the upstream.

## Best Practices

- Validate the official `procd` path before adding policy complexity.
- Start with non-transparent baseline.
- Add DNS control before adding aggressive routing.
- Protect admin and local subnets first.
- Keep one rollback path outside the proxied topology.
- Prefer explicit rule sets and explicit direct exceptions.

## Version Compatibility

### 1.10

- simpler root model, but already not the right target for new production designs.

### 1.11

- endpoints appear, which matters for modern router connectivity patterns.

### 1.12

- root model broadens with certificates/services;
- migrations around DNS and WireGuard become more important.

### 1.13 stable

- baseline for this repository;
- strongest practical target for production OpenWrt guidance here.

### 1.14 alpha

- future docs exist, but router deployments should stay version-disciplined.

## Completion Criteria

Skill применён правильно, если:

- OpenWrt deployment model is identified clearly;
- official service path acknowledged;
- DNS/routing/admin safety all covered before transparent rollout;
- working JSON examples included.

## Router Rollout Playbooks

### Playbook: Safe First Deployment

1. Install service and validate official procd lifecycle.
2. Run non-transparent direct baseline.
3. Confirm router keeps WAN, DNS and admin access.
4. Add one proxy outbound.
5. Add route policy.
6. Add transparent capture last.

### Playbook: TUN Router Rollout

1. Map management plane.
2. Add TUN with exclusions only.
3. Validate router-local behavior.
4. Validate one client.
5. Scale policy gradually.

### Playbook: TProxy Router Rollout

1. Confirm firewall/policy routing control exists.
2. Add TCP interception.
3. Add UDP interception.
4. Integrate DNS.
5. Only then add complex categories and remote sets.

## Validation Checklist

- Official service files understood.
- Router-local admin path protected.
- Local DNS and local domains preserved intentionally.
- Transparent scope documented.
- Hardware/performance constraints acknowledged.

## Senior Review Questions

- If the proxy upstream dies, does the router still remain manageable?
- Which traffic keeps the router itself alive?
- What is the cheapest recovery path if the rollout fails?
- Are we designing for this router, or importing a desktop pattern blindly?

## Field Notes

### `conffile` and `workdir`

On OpenWrt these are not mere paths. They define the contract between config, rule-set files and the managed service lifecycle. A router rollout that ignores this contract invites brittle updates.

### `log_stderr`

This option matters because router debugging is often service-centric. If logs are not where the operator expects them, every later incident gets harder.

### Resource Budget

Even without hardware-specific sources, senior practice assumes routers are constrained by default. Every added feature — TUN, large rule sets, secure DNS, heavy transports — should justify its operational cost.

## Scenario Catalog

### Scenario: First Home Router Proxy

Start with router-local direct baseline, then one outbound, then DNS, then policy, then transparent capture. Reversing this order is the fastest path to a self-inflicted outage.

### Scenario: Fleet of Managed Routers

The value of official procd management and explicit rule-set policy grows with fleet size. Local hacks that “work on one device” become unacceptable.

### Scenario: Emergency Recovery

A senior OpenWrt design always answers: if the new rollout breaks traffic, how do we get back in? The answer should not depend on remembering a clever command under stress.

## Pre-Deploy Checklist

- Config path and workdir match official service contract.
- Router management IP and access method documented.
- Local/private subnets identified.
- DNS behavior for local domains defined.
- One non-transparent rollback profile available.
- Remote upstream hostname resolution path understood.

## Post-Deploy Checklist

- `sing-box` service is healthy under `procd`.
- Router itself still has control-plane connectivity.
- One LAN client has the expected policy path.
- Local domains and admin interfaces still work.
- Rollback can still be executed if later policy layers fail.
