---
name: sing-box-tun
description: "Production skill по TUN-режиму sing-box: auto_route, auto_redirect, route_address, route_exclude_address, stack, MTU, Linux/OpenWrt/VPS deployment и troubleshooting transparent capture."
---

# sing-box TUN

`tun` в `sing-box` — это не просто ещё один inbound и не “волшебная кнопка transparent proxy”. Это механизм, который меняет саму сетевую реальность хоста или роутера. Именно поэтому TUN-сценарии часто дают лучший user experience и самую сложную эксплуатацию одновременно. Production TUN deployment требует думать не только о самом `sing-box`, но и о таблицах маршрутизации, интерфейсах, исключениях, доступе к management plane, DNS и взаимодействии с Docker, bridges и локальными сервисами.

Этот skill нужен, когда нужно:

- развернуть full-device или router-side transparent capture;
- понять, нужен ли `tun`, `tproxy` или обычный локальный proxy;
- настроить `auto_route`, `auto_redirect`, `route_address`, `route_exclude_address`;
- избежать routing loops;
- сделать TUN workable на Linux, OpenWrt, VPS и sing-box-compatible client stacks.

## Official Source Map

- TUN inbound: `https://sing-box.sagernet.org/configuration/inbound/tun/`
- Route index: `https://sing-box.sagernet.org/configuration/route/`
- Route actions: `https://sing-box.sagernet.org/configuration/route/rule_action/`
- Dial fields: `https://sing-box.sagernet.org/configuration/shared/dial/`
- Deprecated: `https://sing-box.sagernet.org/deprecated/`
- Changelog: `https://sing-box.sagernet.org/changelog/`

## Stable TUN Baseline

Для stable `1.13.13` production TUN базируется на merged address model и на следующих ключевых полях:

- `interface_name`
- `address`
- `mtu`
- `auto_route`
- `iproute2_table_index`
- `iproute2_rule_index`
- `auto_redirect`
- `auto_redirect_input_mark`
- `auto_redirect_output_mark`
- `auto_redirect_reset_mark`
- `auto_redirect_nfqueue`
- `auto_redirect_iproute2_fallback_rule_index`
- `exclude_mptcp`
- `loopback_address`
- `strict_route`
- `route_address`
- `route_exclude_address`
- `route_address_set`
- `route_exclude_address_set`
- `stack`
- include/exclude interface and uid selectors

Важно: старые `inet4_address`, `inet6_address`, `inet4_route_address`, `inet6_route_address` и related fields относятся к migration-пути и не должны использоваться в новых production-конфигах.

## What TUN Changes

Когда включается `tun`, меняется не только точка входа трафика, но и сеть вокруг него:

- появляется виртуальный интерфейс;
- часть или весь трафик начинает идти через него;
- может включаться auto-added routing;
- может включаться kernel-level redirect semantics;
- DNS policy должна соответствовать новой модели;
- direct path для управления и локальной сети должен быть осознанным.

Отсюда главный production принцип: TUN нужно вводить только после того, как понятна карта сети и существует safe rollback path.

## Core Fields

### `address`

Список IPv4/IPv6 prefix для TUN interface.

Пример:

```json
{
  "type": "tun",
  "tag": "tun-in",
  "address": [
    "172.19.0.1/30",
    "fdfe:dcba:9876::1/126"
  ]
}
```

Практика:

- не использовать legacy split address fields;
- задавать только те prefixes, которые реально нужны;
- на роутере помнить о конфликтах с существующими private ranges.

### `mtu`

MTU влияет на throughput, fragmentation и стабильность transport-слоя.

Пример:

```json
{
  "mtu": 1500
}
```

Практика:

- начинать с консервативного значения;
- повышать только при контролируемом тестировании;
- помнить, что QUIC and tunnel-over-tunnel setups чувствительны к MTU.

### `auto_route`

Автоматически добавляет нужные маршруты.

Production смысл:

- снижает ручную сложность;
- облегчает desktop deployment;
- на роутере и VPS всё равно требует осмысленных исключений.

### `auto_redirect`

Linux-oriented transparent redirect logic для TUN path.

Production смысл:

- позволяет глубже интегрировать TUN с kernel routing;
- нужен для некоторых bypass semantics через route action `bypass`;
- требует ещё более аккуратного понимания marks, fallback rules и исключений.

### `route_address`

Что должно быть отправлено в TUN path.

### `route_exclude_address`

Что должно остаться вне TUN path.

Именно это поле часто спасает:

- management access;
- LAN;
- upstream gateway communication;
- local service networks.

### `stack`

Влияет на реализацию TUN stack.

Production практика:

- начинать со stable documented path;
- не менять stack ради моды или слухов;
- любое отклонение подтверждать тестами.

## Real TUN Configurations

### Minimal Desktop TUN

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

Use case:

- quick transparent capture baseline;
- initial local validation before full routing policy.

### Split-Tunnel TUN

```json
{
  "inbounds": [
    {
      "type": "tun",
      "tag": "tun-in",
      "interface_name": "tun0",
      "address": [
        "172.19.0.1/30"
      ],
      "mtu": 1500,
      "auto_route": true,
      "route_address": [
        "0.0.0.0/1",
        "128.0.0.0/1"
      ],
      "route_exclude_address": [
        "192.168.0.0/16",
        "10.0.0.0/8"
      ],
      "stack": "system"
    }
  ]
}
```

### Linux Auto-Redirect TUN

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
      "auto_redirect": true,
      "auto_redirect_input_mark": "0x2023",
      "auto_redirect_output_mark": "0x2024",
      "auto_redirect_reset_mark": "0x2025",
      "iproute2_table_index": 2022,
      "iproute2_rule_index": 9000,
      "route_exclude_address": [
        "192.168.0.0/16"
      ],
      "stack": "system"
    }
  ]
}
```

Production note:

- такой конфиг нельзя рассматривать отдельно от route rules и host networking;
- это kernel-integrated pattern, а не просто “ещё одна опция”.

## Linux Server Examples

### Linux Workstation/Server Transparent Client

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
      "route_exclude_address": [
        "192.168.0.0/16",
        "10.0.0.0/8"
      ],
      "stack": "system"
    }
  ]
}
```

### Linux Server with UID Scope

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
      "include_uid_range": [
        "1000:65535"
      ],
      "exclude_uid": [
        0
      ],
      "stack": "system"
    }
  ]
}
```

Use case:

- transparent policy only for user workloads, while root/admin operations stay safer.

## OpenWrt Examples

### OpenWrt Basic TUN

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
      "route_exclude_address": [
        "192.168.0.0/16"
      ],
      "stack": "system"
    }
  ]
}
```

### OpenWrt Router with Extra Exclusions

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
      "route_exclude_address": [
        "192.168.0.0/16",
        "10.0.0.0/8",
        "172.16.0.0/12"
      ],
      "stack": "system"
    }
  ]
}
```

Production router insight:

- exclusions should reflect management IPs, WAN edge dependencies and any side-service networks;
- do not trust a generic one-size-fits-all private-network exclusion without mapping the actual router role.

## VPS Examples

### VPS Transit TUN Skeleton

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

### VPS with Safe Exclusion

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
      "route_exclude_address": [
        "127.0.0.0/8"
      ],
      "stack": "system"
    }
  ]
}
```

VPS note:

- TUN on VPS is powerful but can disrupt management or peer network flows if exclusions are careless.

## Podkop-Compatible Examples

Only sing-box-native patterns are allowed here.

### Podkop-Like Transparent Client Core

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

This is a conceptual template for systems that generate or import sing-box-compatible TUN logic.

## 3x-ui-Compatible Examples

3x-ui itself is outside official sing-box scope, but a sing-box client consuming a 3x-ui-generated transport can still rely on TUN locally:

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
      "route_exclude_address": [
        "192.168.0.0/16"
      ],
      "stack": "system"
    }
  ]
}
```

## Routing Schemes

### Full Tunnel

- `auto_route: true`
- route/final sends most traffic to proxy
- only management and private paths excluded

### Split Tunnel

- `route_address` narrows captured prefixes
- `route_exclude_address` protects local dependencies

### Transparent Router

- TUN acts as system interception point
- route rules and DNS determine final policy

## Comparison Table

| Mode | Benefit | Risk | Best Fit |
|---|---|---|---|
| Basic TUN | easy transparent baseline | hidden routing assumptions | workstation test |
| Split TUN | precise coverage | exclusion mistakes | privacy + LAN coexistence |
| Auto-Redirect TUN | deep Linux integration | kernel complexity | advanced Linux gateway |
| UID-scoped TUN | safer host segmentation | host policy complexity | Linux multi-user systems |

## Common Mistakes

### 1. Using old `inet4_*`/`inet6_*` fields

Result:

- migration debt;
- broken future compatibility.

### 2. No `route_exclude_address` on router deployments

Result:

- loss of access to local resources or management plane.

### 3. Enabling `auto_redirect` without understanding the host networking

Result:

- opaque failures;
- loops;
- broken Docker/bridge interaction.

### 4. Treating TUN as a DNS-independent feature

Result:

- leaks or broken routing semantics.

### 5. Tuning MTU blindly

Result:

- fragmentation issues and unstable performance.

## Troubleshooting

### Symptom: TUN interface does not appear

Check:

- privileges;
- target platform support;
- `address` values;
- whether runtime is sandboxed or restricted.

### Symptom: interface appears, but no traffic passes

Check:

- route/final outbound;
- DNS path;
- excluded routes;
- actual chosen interface and upstream connectivity.

### Symptom: management access lost after enabling TUN

Check:

- `route_exclude_address`;
- private ranges;
- SSH/LuCI/admin networks;
- upstream interface path.

### Symptom: some apps work, others fail

Check:

- MTU;
- DNS interception;
- protocol differences;
- whether some traffic is intentionally excluded.

### Symptom: Linux auto-redirect behaves inconsistently

Check:

- marks;
- policy routing indices;
- interaction with route actions and host firewall;
- whether problem exists without `auto_redirect`.

## Best Practices

- Start from the smallest TUN baseline and grow gradually.
- Protect management plane before proxying user traffic.
- Treat DNS and routing as mandatory companions to TUN.
- Use stable merged address fields only.
- For routers, document every excluded network explicitly.
- For Linux, keep a recovery shell and rollback path outside the TUN-dependent workflow.

## Version Compatibility

### 1.10

- merged TUN address fields become the correct path;
- legacy fields already on the way out.

### 1.11

- TUN still central to transparent deployments;
- broader route/endpoint ecosystem evolves around it.

### 1.12

- loopback and newer transparent-related options expand design possibilities.

### 1.13 stable

- repository baseline;
- `auto_redirect` and strict route related options are mature enough for careful production use.

### 1.14 alpha

- official future docs show more fields;
- do not backport assumptions blindly to stable `1.13`.

## Completion Criteria

Skill применён правильно, если:

- chosen TUN mode matches the target environment;
- exclusion logic documented;
- DNS and routing dependencies acknowledged;
- rollback and admin-plane safety considered before deployment.

## Rollout Playbooks

### Playbook: Workstation TUN

1. Start with minimal `tun` and `direct` baseline.
2. Confirm the interface appears.
3. Confirm DNS path.
4. Add route exclusions.
5. Only then add proxy-first or split policy.

### Playbook: Router TUN

1. Document management IPs and subnets.
2. Add exclusions for local/private/admin paths.
3. Validate router-local access.
4. Validate one LAN client.
5. Expand to wider policy only after safe behavior is proven.

### Playbook: Linux Auto-Redirect

1. Prove basic TUN works without `auto_redirect`.
2. Introduce `auto_redirect` and related marks.
3. Validate no loop with direct traffic.
4. Validate bypass behavior only after core path works.

## Validation Checklist

- Minimal TUN works before advanced options.
- Exclusions include local/admin paths.
- Transparent capture scope documented.
- DNS ownership is explicit.
- Auto-redirect is justified, not habitual.

## Senior Review Questions

- What traffic must never enter the TUN?
- Can we recover if route policy breaks?
- Are we using TUN because we need transparency, or because it seems powerful?
- What is the cost of this TUN design on constrained hardware?

## Field Notes

### `auto_route`

This field is easy to love and easy to misunderstand. It saves manual routing work, but it does not remove the need to reason about which routes should exist at all.

### `route_exclude_address`

This is often the true life-support section of a production TUN config. Senior review should read these exclusions not as a list of subnets, but as a story about what must remain reachable when everything else is captured.

### `stack`

Changing stack should be treated as changing part of the runtime model. It needs a reason, a test plan and a rollback story.

## Scenario Catalog

### Scenario: Transparent Laptop

User wants all traffic proxied without per-app setup. TUN is appropriate, but only if local network access and DNS ownership remain explainable.

### Scenario: Edge Router

TUN on a router provides elegant policy control but raises the cost of mistakes. This is why management and LAN safety must be explicit before performance tuning begins.

### Scenario: Service Host With Partial Capture

UID-scoped or selective route-address patterns can work, but only if the engineer can still explain which workloads stay outside the tunnel and why.
