---
name: cloudflare
description: Design, configure, validate, and troubleshoot Cloudflare DNS, Proxy, SSL/TLS, Origin CA, and Tunnel for VPN and proxy publication patterns.
---

# Cloudflare VPN Publishing

Use this skill when the task centers on Cloudflare as the public edge for VPN-related services.

## Core Workflow

1. classify the endpoint as `DNS only`, proxied through the standard edge, or published via Tunnel
2. verify whether the transport is actually supported behind standard Cloudflare Proxy
3. select the correct SSL mode and origin certificate strategy
4. validate DNS, edge response, and origin response independently

## Key Rules

- do not assume standard Cloudflare Proxy supports arbitrary TCP or UDP protocols
- prefer `Full (strict)` when a certificate is present on the origin
- keep origin credentials and private keys off shared systems
- treat transport compatibility as a first-class design decision, not a post-incident fix
