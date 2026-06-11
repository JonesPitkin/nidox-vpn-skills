---
name: sing-box-inbounds
description: "Production skill по inbounds sing-box: mixed, socks, http, tun, redirect, tproxy и direct. Использовать для локального прокси, transparent gateway, router deployment, Linux server и sing-box-совместимых интеграций."
---

# sing-box Inbounds

`inbounds` — это точка, где абстрактная конфигурация `sing-box` встречается с реальным трафиком. На production-уровне inbound нельзя выбирать по принципу “какой тут моднее”. Нужно понимать, какой тип трафика приходит, на каком уровне OSI его нужно захватить, нужен ли user-space proxy semantics или transparent interception, кто будет инициатором соединений и как inbound вписывается в DNS/routing model.

Неверный inbound — одна из самых дорогих архитектурных ошибок. Многие проблемы, которые потом кажутся TLS-, DNS- или transport-сбоями, на самом деле начинаются с неправильного выбора точки входа.

## Official Source Map

- Inbound index: `https://sing-box.sagernet.org/configuration/inbound/`
- Mixed: `https://sing-box.sagernet.org/configuration/inbound/mixed/`
- SOCKS: `https://sing-box.sagernet.org/configuration/inbound/socks/`
- HTTP: `https://sing-box.sagernet.org/configuration/inbound/http/`
- TUN: `https://sing-box.sagernet.org/configuration/inbound/tun/`
- Redirect: `https://sing-box.sagernet.org/configuration/inbound/redirect/`
- TProxy: `https://sing-box.sagernet.org/configuration/inbound/tproxy/`
- Direct inbound: `https://sing-box.sagernet.org/configuration/inbound/direct/`
- Shared listen fields: `https://sing-box.sagernet.org/configuration/shared/listen/`

## Production Decision Model

Перед выбором inbound задать вопросы:

- клиент будет сам явно использовать proxy port?
- нужен full-device capture without app config?
- это router/gateway scenario?
- важны ли оригинальные destination IP/port?
- нужен ли UDP capture?
- есть ли firewall/NAT rules outside `sing-box`?

После этого inbound обычно выбирается естественно:

- локальный user proxy: `mixed`, `socks`, `http`
- full-device or app-transparent local capture: `tun`
- transparent interception with preserved semantics: `tproxy`
- simple redirected TCP interception: `redirect`
- service tunnel / override destination: `direct`

## `mixed`

`mixed` inbound объединяет socks4, socks4a, socks5 и http server в одном listener.

### Когда использовать

- desktop setup;
- localhost proxy for many applications;
- temporary diagnostics;
- environments, где один unified proxy port удобнее нескольких.

### Базовый пример

```json
{
  "type": "mixed",
  "tag": "mixed-in",
  "listen": "127.0.0.1",
  "listen_port": 2080
}
```

### С авторизацией

```json
{
  "type": "mixed",
  "tag": "mixed-in",
  "listen": "127.0.0.1",
  "listen_port": 2080,
  "users": [
    {
      "username": "agent",
      "password": "strong-password"
    }
  ]
}
```

### Operational Notes

- отлично подходит для локальной разработки и ручного тестирования;
- не является transparent proxy;
- если его слушать на `0.0.0.0`, безопасность становится отдельной задачей.

## `socks`

SOCKS-only inbound.

### Когда использовать

- приложения и клиенты, которые хорошо умеют SOCKS5;
- серверные environments, где HTTP proxy не нужен;
- более строгое и предсказуемое proxy semantics.

### Пример

```json
{
  "type": "socks",
  "tag": "socks-in",
  "listen": "127.0.0.1",
  "listen_port": 1080
}
```

### Production Observations

- прост и предсказуем;
- легко сочетается с CLI tooling;
- часто полезен как debug fallback даже в TUN-based проектах.

## `http`

HTTP proxy inbound с optional TLS support.

### Когда использовать

- приложения с native HTTP proxy support;
- enterprise-like client environments;
- cases, где CONNECT semantics expected explicitly.

### Пример

```json
{
  "type": "http",
  "tag": "http-in",
  "listen": "127.0.0.1",
  "listen_port": 8080
}
```

### Пример с пользователями

```json
{
  "type": "http",
  "tag": "http-in",
  "listen": "127.0.0.1",
  "listen_port": 8080,
  "users": [
    {
      "username": "agent",
      "password": "strong-password"
    }
  ]
}
```

### Production Notes

- useful in controlled desktop/server environments;
- не решает transparent capture;
- при TLS-enabled HTTP proxy нужно особенно внимательно относиться к cert path.

## `tun`

Это самый стратегически важный inbound для client-side transparent experience.

### Когда использовать

- нужен full-device capture;
- нельзя или неудобно настраивать proxy per application;
- нужен router-side или host-side transparent workflow;
- нужны route-based policies на весь трафик.

### Базовый пример

```json
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
```

### Production TUN Example for Split Traffic

```json
{
  "type": "tun",
  "tag": "tun-in",
  "interface_name": "tun0",
  "address": [
    "172.19.0.1/30",
    "fdfe:dcba:9876::1/126"
  ],
  "mtu": 1500,
  "auto_route": true,
  "route_address": [
    "0.0.0.0/1",
    "128.0.0.0/1"
  ],
  "route_exclude_address": [
    "192.168.0.0/16",
    "10.0.0.0/8",
    "fc00::/7"
  ],
  "stack": "system"
}
```

### Production Notes

- `tun` изменяет routing reality host or router;
- нужно заранее защитить management access;
- в `1.10+` использовать только merged address fields, а не старые `inet4_*`.

## `redirect`

Inbound для redirected traffic. Supported on Linux and macOS.

### Когда использовать

- external firewall/NAT already redirects traffic to local port;
- нужен относительно простой transparent TCP path;
- не нужен полный TProxy semantics.

### Пример

```json
{
  "type": "redirect",
  "tag": "redirect-in",
  "listen": "0.0.0.0",
  "listen_port": 60080
}
```

### Operational Caveat

`redirect` нельзя считать полной заменой `tproxy`, особенно если важны UDP semantics и original destination handling на production gateway.

## `tproxy`

Linux-only inbound для transparent proxy interception.

### Когда использовать

- router/gateway deployment;
- policy routing with preserved original destination;
- mixed TCP/UDP interception;
- advanced Linux network stack control.

### TCP Example

```json
{
  "type": "tproxy",
  "tag": "tproxy-tcp",
  "listen": "::",
  "listen_port": 60080,
  "network": "tcp"
}
```

### UDP Example

```json
{
  "type": "tproxy",
  "tag": "tproxy-udp",
  "listen": "::",
  "listen_port": 60080,
  "network": "udp"
}
```

### Production Notes

- `tproxy` сам по себе ничего магического не делает без firewall/policy routing;
- отлично подходит для OpenWrt and Linux router scenarios;
- очень легко получить “порт слушает, но трафика нет” из-за несогласованных marks и rules.

## `direct` inbound

По официальной документации это tunnel server.

### Когда использовать

- когда входящий трафик нужно принять и перенаправить на заданный destination;
- сервисные tunnel patterns;
- специфические server-side overrides.

### Пример

```json
{
  "type": "direct",
  "tag": "dns-tunnel",
  "listen": "0.0.0.0",
  "listen_port": 5353,
  "network": "udp",
  "override_address": "1.1.1.1",
  "override_port": 53
}
```

### Production Notes

- это не “обычный direct proxy listener”;
- особенно полезен в service-like tunnel cases.

## OpenWrt Examples

### OpenWrt TUN Inbound

```json
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
```

Смысл:

- трафик LAN-клиентов может проходить через policy model;
- management subnet лучше исключать явно.

### OpenWrt TProxy Pattern

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

## Linux Server Examples

### Server Admin Proxy

```json
{
  "type": "socks",
  "tag": "admin-socks",
  "listen": "127.0.0.1",
  "listen_port": 1080
}
```

### Multi-App Local Proxy

```json
{
  "type": "mixed",
  "tag": "mixed-in",
  "listen": "127.0.0.1",
  "listen_port": 2080,
  "users": [
    {
      "username": "svc",
      "password": "svc-password"
    }
  ]
}
```

## VPS Examples

### Minimal Admin Inbound on VPS

```json
{
  "type": "http",
  "tag": "local-http",
  "listen": "127.0.0.1",
  "listen_port": 8080
}
```

Это полезно как utility inbound для админских задач и проверок, но не должно путаться с public protocol inbounds.

## Podkop-Compatible Examples

Так как здесь разрешены только official sing-box facts, Podkop examples должны быть выражены как sing-box-compatible inbound choices.

### Podkop-Like Transparent Client Core

```json
{
  "type": "tun",
  "tag": "tun-in",
  "address": [
    "172.19.0.1/30"
  ],
  "auto_route": true,
  "stack": "system"
}
```

Это не инструкция по Podkop UI, а canonical sing-box TUN shape, которую подобная система может порождать или импортировать.

## 3x-ui-Compatible Examples

3x-ui сам по себе не документируется официальными sing-box sources, поэтому здесь допустим только client-side counterpart logic:

- если 3x-ui выдаёт proxy profile, sing-box может принимать трафик локально через `mixed`/`socks`/`http` или полностью через `tun`;
- inbound-side на клиенте не зависит от UI 3x-ui, а зависит от того, как локальные приложения будут отправлять трафик.

### 3x-ui Companion Client Using Mixed Inbound

```json
{
  "type": "mixed",
  "tag": "mixed-in",
  "listen": "127.0.0.1",
  "listen_port": 2080
}
```

## Routing Schemes for Inbounds

### Local Proxy Scheme

- App -> `mixed`/`socks`/`http` -> route rules -> outbound

### Transparent Host Scheme

- App -> OS stack -> `tun` -> DNS + route -> outbound

### Transparent Gateway Scheme

- Client device -> firewall interception -> `tproxy`/`redirect` -> route -> outbound

### Service Tunnel Scheme

- External packet -> `direct` inbound -> overridden destination

## Comparison Table

| Inbound | Best For | Strength | Main Risk |
|---|---|---|---|
| `mixed` | local workstation | universal local proxy | accidentally exposed listener |
| `socks` | CLI/services | simplicity | limited client compatibility |
| `http` | apps with HTTP proxy | explicit proxy semantics | not transparent |
| `tun` | full-device capture | transparent user experience | routing complexity |
| `redirect` | simple redirected flows | lightweight transparent TCP | limited semantics |
| `tproxy` | router/gateway | full transparent policy control | firewall complexity |
| `direct` | service tunnel | destination override | misuse as generic proxy |

## Common Mistakes

### 1. Using `mixed` when transparent capture is needed

Result:

- apps that do not support proxies bypass the system.

### 2. Using `tun` on a router without protecting management access

Result:

- lockout from SSH/LuCI/admin plane.

### 3. Treating `redirect` as equivalent to `tproxy`

Result:

- UDP and original destination semantics fail unexpectedly.

### 4. Forgetting auth on non-local proxy listener

Result:

- accidental exposure of proxy service.

### 5. Using deprecated TUN address fields from old guides

Result:

- migration pain and broken configs across versions.

## Troubleshooting

### Symptom: local app cannot connect to proxy

Check:

- correct listener address and port;
- app protocol matches inbound type;
- auth requirements.

### Symptom: TUN starts but traffic bypasses policy

Check:

- route exclusions;
- DNS path;
- `auto_route` effect;
- platform privileges.

### Symptom: TProxy port listens but nothing is intercepted

Check:

- firewall redirection;
- Linux marks and policy routing;
- TCP vs UDP inbound separation.

### Symptom: router loses internet or admin access after enabling TUN

Check:

- `route_exclude_address`;
- local subnets;
- upstream interface detection;
- management plane bypass.

## Best Practices

- Pick inbound based on traffic acquisition model, not protocol preference.
- Start with the smallest inbound that solves the problem.
- For routers, design admin/network exclusions first.
- Keep one diagnostic local proxy inbound even in TUN-heavy systems.
- Separate TCP and UDP transparent logic when operationally helpful.
- Never reuse desktop assumptions on OpenWrt without review.

## Version Compatibility

### 1.10

- merged TUN address fields become the right path;
- legacy TUN fields already heading out.

### 1.11

- endpoint evolution affects some deployment patterns around routing and transport.

### 1.12

- broader migration pressure around DNS and WireGuard indirectly changes how inbounds fit system design.

### 1.13 stable

- recommended production target for this repository;
- `tun`, `tproxy`, `mixed`, `http`, `socks`, `direct`, `redirect` remain core choices.

### 1.14 alpha

- future fields exist in official docs but should not be assumed in `1.13` production.

## Completion Criteria

Skill применён корректно, если:

- выбран inbound, соответствующий traffic acquisition model;
- даны working JSON examples;
- clarified relation to DNS and route;
- risks for OpenWrt/Linux/VPS transparent environments are named before deployment.

## Deployment Playbooks

### Playbook: Desktop Local Proxy

1. Start with `mixed` or `socks`.
2. Bind only to `127.0.0.1`.
3. Add auth only if the exposure model requires it.
4. Validate app compatibility.
5. Only move to TUN if proxy-aware apps are not enough.

### Playbook: Router Transparent Proxy

1. Decide between `tun` and `tproxy`.
2. Protect management and local subnets.
3. Add DNS policy before broad routing policy.
4. Validate TCP path first, then UDP.
5. Add complex rule sets last.

### Playbook: Service Tunnel

1. Confirm the use case really needs `direct` inbound.
2. Make override destination explicit.
3. Validate port and protocol behavior.
4. Document why ordinary local proxy inbounds are not sufficient.

## Environment Decision Matrix

### OpenWrt

Prefer:

- `tun` when you want client-transparent behavior with an interface-centric design;
- `tproxy` when you already control firewall/policy routing and want deeper transparent semantics;
- `mixed` or `socks` only for admin/debug scenarios.

### Linux Server

Prefer:

- `socks` or `http` for operator and service-level tooling;
- `tun` only when the whole host should be policy-routed or captured transparently.

### VPS

Prefer:

- server protocol inbounds for public service roles;
- local utility proxy inbounds for maintenance, not as a substitute for public protocol design.

## Validation Checklist

- Listener address is intentionally scoped.
- Inbound type matches traffic acquisition model.
- Auth exposure reviewed where applicable.
- TUN/TProxy choice justified, not accidental.
- DNS and route implications documented.
- Transparent deployments include rollback path.

## Senior Review Questions

- Does this inbound require the application to cooperate?
- Can this inbound preserve original destination semantics?
- What happens to UDP under this choice?
- How would we recover if the router locks us out?

## Field Notes

### Listen Scope

Senior review should always inspect `listen` and `listen_port` as exposure decisions, not as random defaults. A `mixed` inbound on `0.0.0.0` is a security event, not merely a convenience choice.

### Users and Auth

Authentication on local-only admin proxy differs from authentication on a LAN-visible listener. The same JSON field has radically different operational meaning depending on bind scope.

### Transparent Capture Semantics

`tun`, `redirect` and `tproxy` all feel “transparent”, but they solve different problems. A good skill application explains which layer captures traffic, whether the app must cooperate, and whether original destination information is preserved.

## Scenario Catalog

### Scenario: Developer Workstation

Start with `mixed` or `socks`. Only escalate to TUN if app diversity or user experience actually requires transparent capture.

### Scenario: Home or Office Router

Choose between `tun` and `tproxy` based on available firewall control, desired policy depth and tolerance for complexity. Router contexts should never inherit workstation assumptions uncritically.

### Scenario: Multi-Service Linux Host

Use multiple local inbounds with clear tags and different route policies rather than overloading one listener with conflicting expectations.

## Change Management Notes

Inbound changes are exposure changes. A senior rollout asks:

- who can reach this listener before and after the change;
- whether the app/user must be reconfigured;
- whether transparent capture scope is expanding;
- what rollback looks like if the chosen acquisition model is wrong.

This is why changing from `mixed` to `tun` or from local proxy to `tproxy` should be treated as an architecture change, not a tuning tweak.
