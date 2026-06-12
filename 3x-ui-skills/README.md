# 3x-ui-skills

Comprehensive AI Skill Repository for `3x-ui`.

Official-source-oriented skill collection for `3x-ui` installation, VPS operations, inbound design, routing, security hardening, API automation, and Cloudflare edge publishing.

Documentation baseline: `3x-ui v3.3.0`, bundled Xray-core `v26.6.1`, sing-box `v1.13.13`, and Hysteria `v2.9.2`. See [`VERSION_MATRIX.md`](VERSION_MATRIX.md).

## Skill Tree

- [`3x-ui`](3x-ui/SKILL.md)
- [`3x-ui-vps`](3x-ui-vps/SKILL.md)
- [`3x-ui-install`](3x-ui-install/SKILL.md)
- [`3x-ui-inbounds`](3x-ui-inbounds/SKILL.md)
- [`3x-ui-routing`](3x-ui-routing/SKILL.md)
- [`3x-ui-security`](3x-ui-security/SKILL.md)
- [`3x-ui-cloudflare`](3x-ui-cloudflare/SKILL.md)

## Dependency Map

- `3x-ui` is the entrypoint skill for repository-level triage and routing.
- `3x-ui-vps` covers host bootstrap, loopback-only panel exposure, nginx, Docker Compose, and maintenance scripts.
- `3x-ui-install` handles package, image, database, backup, migration, and rollback workflows.
- `3x-ui-inbounds` owns protocol and transport design.
- `3x-ui-routing` owns Xray-side policy, split tunneling, DNS strategy, and balancers.
- `3x-ui-security` owns panel hardening, TLS, firewall, SSH, and backup protection.
- `3x-ui-cloudflare` owns DNS, CDN, TLS mode, Tunnel, and proxied endpoint compatibility.

## Quick Start

1. Start with [`3x-ui/SKILL.md`](3x-ui/SKILL.md) to classify the operator task.
2. Jump into the domain skill that owns the change.
3. Use the linked `references/` files for runbooks, edge cases, and validation commands.
4. If the material is embedded into `nidox-vpn-skills`, apply the audit policy from the meta-repository.

## Repository Structure

```text
3x-ui-skills/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SKILL_INDEX.md
├── VERSION_MATRIX.md
├── MIGRATION_GUIDE.md
├── GITHUB_REPOSITORY.md
├── RELEASE_v1.0.0.md
├── RELEASE_v1.1.0.md
├── scripts/
├── 3x-ui/
├── 3x-ui-vps/
├── 3x-ui-install/
├── 3x-ui-inbounds/
├── 3x-ui-routing/
├── 3x-ui-security/
└── 3x-ui-cloudflare/
```

## Supported Scope

- Ubuntu and Debian hosts
- VPS and loopback-only panel publishing
- Docker Compose and native install flows
- Xray inbounds and transports inside `3x-ui`
- MTProto FakeTLS through the managed `mtg` sidecar
- typed panel API/OpenAPI, subscription outbounds, WARP rotation, and custom subscription pages
- current sing-box endpoint/rule-set migration guidance
- current Hysteria2 security and transport guidance
- Cloudflare-backed publication patterns for supported HTTP(S) transports
- Security hardening and maintenance operations

## Official Sources

- `3x-ui` official repository and wiki
- official `3x-ui` release artifacts and bundled scripts
- official Xray-core, sing-box, and Hysteria documentation and release notes
- official Cloudflare Developers documentation for DNS, Proxy, SSL/TLS, and Tunnel

See [`3x-ui/references/official-links.md`](3x-ui/references/official-links.md).

## Version Policy

This repository is prepared for release `v1.1.0`, but has not been tagged or published. Upstream `3x-ui`, Xray-core, sing-box, Hysteria, and Cloudflare behavior can change quickly. Validate current release notes and compatibility before production mutations.

See [`VERSION_MATRIX.md`](VERSION_MATRIX.md) and [`MIGRATION_GUIDE.md`](MIGRATION_GUIDE.md).

## Validation

Run the repository structural audit:

```sh
python3 scripts/audit_repository.py
```

Each skill must also pass the `quick_validate.py` supplied by the Codex
`skill-creator` skill.

## License

Released under the MIT License. See [`LICENSE`](LICENSE).

## Contribution Guide

Contributions should preserve official-source attribution, avoid storing secrets, and keep each skill internally consistent.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Changelog

Repository-level release notes are tracked in [`CHANGELOG.md`](CHANGELOG.md).
