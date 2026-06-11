---
name: 3x-ui
description: Route operator requests to the correct 3x-ui skill for VPS deployment, installation, inbound design, routing, security hardening, or Cloudflare publishing.
---

# 3X-UI Repository Router

Use this skill when the task mentions `3x-ui` broadly but the correct operating surface is not yet chosen.

## Routing Rules

- Use `3x-ui-vps` for opinionated VPS deployment, nginx publishing, loopback-only panel exposure, and scripted maintenance.
- Use `3x-ui-install` for install, update, backup, restore, and migration workflows.
- Use `3x-ui-inbounds` for protocol, transport, REALITY, XHTTP, WebSocket, gRPC, Hysteria2, and client compatibility.
- Use `3x-ui-routing` for Xray DNS, routing rules, direct/proxy/block policy, WARP, and balancers.
- Use `3x-ui-security` for panel hardening, TLS, firewall, SSH, Fail2Ban, and backup protection.
- Use `3x-ui-cloudflare` for DNS, proxied publication, Tunnel, SSL modes, and edge-to-origin compatibility.

## Escalation Rules

- if the task mutates a live server, verify that the operator controls the host
- if the change involves current release-specific behavior, verify the official repository and wiki first
- if the task crosses multiple domains, start with the smallest safe change and then branch into the specialist skill
