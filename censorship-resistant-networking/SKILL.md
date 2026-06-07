---
name: configure-censorship-resistant-networking
description: Diagnose restricted or shaped Internet access and design, configure, review, or troubleshoot resilient personal networking based on Xray-core/VLESS, Reality, XHTTP, WebSocket, VPS cascades, HAProxy, selective Cloudflare WARP routing, Cloudflare CDN, OpenWrt TPROXY split tunneling, nftables, dnsmasq, and dnscrypt-proxy. Use for requests about bypassing network blocking or DPI, choosing a direct/cascade/CDN topology, preparing server or router configs, securing 3X-UI, generating client links, or debugging connectivity, routing, DNS, SNI, TLS, firewall, and performance problems.
---

# Configure Censorship-Resistant Networking

Build the smallest topology that satisfies the user's observed network constraints. Treat product versions, installation commands, provider behavior, censorship methods, and client compatibility as time-sensitive.

## Core Workflow

1. Establish the environment:
   - Client OS and application or router model/OpenWrt version.
   - Access network: fixed, mobile, or both.
   - VPS locations, operating systems, public IPs, domains, and administrative access.
   - Required behavior: full tunnel, selected domains, selected devices, failover, or regional egress.
   - Current symptoms and tests already performed.

2. Diagnose before selecting a topology:
   - Separate DNS failure, IP blocking, SNI/TLS filtering, protocol fingerprinting, TCP shaping, UDP/QUIC blocking, and server-side geolocation restrictions.
   - Compare direct access, access by IP, encrypted DNS, TCP versus UDP, and the same endpoint from another ISP.
   - Preserve exact commands, timestamps, client versions, and error messages.

3. Select the minimum sufficient architecture:
   - Direct foreign VPS for the simplest baseline.
   - Local/intermediate VPS plus foreign VPS when foreign destinations are shaped or inaccessible.
   - Selective WARP egress only for destinations that reject or misclassify the VPS address.
   - OpenWrt split tunneling when multiple devices or managed devices need transparent routing.
   - CDN path when a domain, valid TLS, and CDN-reachable edge provide a useful alternate route.
   - Prefer a documented backup path such as SSH-based tunneling when practical.

4. Verify current facts before producing commands:
   - Check official release pages and documentation for Xray-core, 3X-UI, OpenWrt, Cloudflare WARP, Podkop, HAProxy, and nginx.
   - Never reuse version numbers, package repositories, certificate behavior, UI labels, or protocol defaults from the reference without verification.
   - Prefer official documentation and upstream repositories. State when a conclusion is inferred from community reports.

5. Prepare changes safely:
   - Back up current configs and record a rollback command.
   - Keep the active SSH port allowed before changing firewall policy.
   - Validate configs before restart.
   - Apply one layer at a time: endpoint, intermediate hop, routing, DNS, then client automation.
   - Never expose UUIDs, private keys, subscription URLs, panel credentials, or certificates in output.

6. Test each layer:
   - Service state and listening sockets.
   - Config syntax.
   - TLS/SNI and transport handshake.
   - Direct and proxied public IP.
   - DNS resolution path and leak behavior.
   - TCP and UDP/QUIC where required.
   - Reboot persistence, failover, and rollback.

7. Deliver an operational runbook:
   - Assumptions and selected topology.
   - Placeholders and secrets the user must provide.
   - Ordered commands/configs.
   - Validation after every destructive or state-changing step.
   - Rollback steps and known limitations.

## Decision Rules

- Prefer raw Xray-core for transparent, auditable, minimal installations.
- Use 3X-UI when subscription management and UI operation matter; require random credentials, HTTPS, a non-default path, restricted panel access, and 2FA when supported.
- Use iptables DNAT/MASQUERADE for a minimal fixed L4 relay.
- Use HAProxy for health checks, multiple backends, or controlled balancing.
- Use Xray on the intermediate VPS only when domain-aware routing justifies TLS termination and extra CPU/latency.
- Use Reality only on direct endpoint paths. Do not place Reality behind a conventional CDN that must see the real SNI.
- For CDN paths, use a real domain, valid TLS, nginx or equivalent termination, and WS/XHTTP supported by the CDN.
- For OpenWrt, prefer an established maintained package such as Podkop when it meets requirements; use manual TPROXY only when the user needs explicit control.
- Route through WARP selectively rather than globally unless the user explicitly needs global WARP egress.

## Configuration Discipline

- Use valid JSON in final Xray configs; remove comments and substitute all placeholders.
- Keep inbound/outbound tags unique and routing rules ordered from specific to fallback.
- Enable sniffing only when domain-based routing requires it and explain its privacy implications.
- Bind internal Xray/CDN backends to loopback or a Unix socket.
- Restrict dashboard and statistics listeners; do not expose them publicly by default.
- Match firewall rules to the actual SSH, panel, inbound, HTTP challenge, and transport ports.
- On OpenWrt, confirm CPU architecture, storage, RAM, interface names, firewall generation, and package compatibility before installation.
- Prevent routing loops by excluding the proxy endpoint, local networks, router addresses, and management paths from transparent proxying.

## Reference

Read [references/architecture-guide.md](references/architecture-guide.md) for the topology matrix, implementation notes, tests, failure modes, and provenance distilled from the source instruction.

## Boundaries

- Support lawful personal privacy, access, resilience, research, and administration.
- Do not help compromise third-party infrastructure, steal credentials, conceal malware, perform unauthorized scanning, or evade controls on systems the user does not own or administer.
- Warn that local law, provider terms, hosting policy, and workplace policy may apply.
