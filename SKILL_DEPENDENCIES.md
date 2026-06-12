# SKILL_DEPENDENCIES

Verified for `nidox-vpn-skills v1.1.1`.

```text
network-fundamentals-skill
│
├── sing-box-skills
├── podkop-skills
├── 3x-ui-skills
├── remnawave-skills
├── cloudflare-skills
├── openwrt-cudy-wr3000s-skills
└── nidox-vpn-detection-defense-skill
```

## Notes

- `network-fundamentals-skill` is the mandatory conceptual and operational base layer.
- `sing-box-skills`, `podkop-skills`, `3x-ui-skills`, `remnawave-skills`, `cloudflare-skills` and `openwrt-cudy-wr3000s-skills` all depend on this shared network base.
- `nidox-vpn-detection-defense-skill` also depends on `network-fundamentals-skill`, because audit conclusions require common grounding in routing, DNS, MTU, NAT, TLS, firewall and Internet delivery concepts.

## Cross-package Dependencies

| Package | Embedded version | Depends on |
|---|---|---|
| `network-fundamentals` | unversioned snapshot | none |
| `cloudflare-skills` | `v1.0.0` | `network-fundamentals` |
| `openwrt-cudy-wr3000s-skills` | `v1.0.0` | `network-fundamentals` |
| `sing-box-skills` | `v1.0.0` | `network-fundamentals` |
| `3x-ui-skills` | `v1.1.0` | `network-fundamentals`, `sing-box-skills`, `cloudflare-skills` |
| `remnawave-skills` | `v1.0.0` | `network-fundamentals`, `sing-box-skills` |
| `podkop-skills` | `v1.0.0` | `network-fundamentals`, `sing-box-skills`, `openwrt-cudy-wr3000s-skills` |
| `censorship-resistant-networking` | unversioned snapshot | all relevant networking, edge, proxy, panel and OpenWrt packages |

The embedded `3x-ui-skills` directory is a full copy of standalone tag
`v1.1.0`, commit `27eef38884407145bd0f3289848c64dbba080296`.
