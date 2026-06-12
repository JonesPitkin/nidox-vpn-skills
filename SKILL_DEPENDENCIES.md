# SKILL_DEPENDENCIES

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
