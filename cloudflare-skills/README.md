# cloudflare-skills

Comprehensive AI Skill Repository for Cloudflare-backed VPN publishing.

Official-source-oriented skill collection for Cloudflare DNS, Proxy/CDN, SSL/TLS, Origin CA, Tunnel, and edge publishing patterns used by VPN and proxy control planes.

## Skill Tree

- [`cloudflare`](cloudflare/SKILL.md)

## Dependency Map

- `cloudflare` is the repository entrypoint and primary operational skill.
- the skill focuses on DNS records, proxied publication, SSL modes, Tunnel, origin certificates, and edge-to-origin troubleshooting.

## Quick Start

1. open [`cloudflare/SKILL.md`](cloudflare/SKILL.md)
2. classify whether the endpoint should be `DNS only`, proxied through the standard edge, or published through Cloudflare Tunnel
3. validate certificate mode and transport compatibility before changing DNS or proxy state

## Repository Structure

```text
cloudflare-skills/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SKILL_INDEX.md
├── VERSION_MATRIX.md
├── MIGRATION_GUIDE.md
├── GITHUB_REPOSITORY.md
├── RELEASE_v1.0.0.md
└── cloudflare/
```

## Official Sources

See [`cloudflare/references/official-links.md`](cloudflare/references/official-links.md).

## Version Policy

Cloudflare product limits, supported ports, and edge behavior can change. Verify current official documentation before production rollout.

## License

Released under the MIT License. See [`LICENSE`](LICENSE).
