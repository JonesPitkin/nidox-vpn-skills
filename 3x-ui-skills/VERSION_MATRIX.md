# Version Matrix

Verified June 12, 2026.

| Component | Verified baseline | Source of truth |
|---|---|---|
| `3x-ui` | `v3.3.0`, commit `f8e89cc848b908d8507f30e0e35a0a74d6fe983c` | official repository, Wiki, release notes, generated schemas |
| bundled Xray-core | artifact `v26.6.1`; module revision `94ffd50060f1` | `3x-ui` release workflow and Xray-core source |
| Xray-core stable channel | `v26.3.27`; `v26.6.1` is prerelease upstream but bundled by 3X-UI | Xray-core releases |
| sing-box | stable `v1.13.13`; `1.14` is alpha | official docs, changelog, migration guide |
| Hysteria | `v2.9.2` | official docs and release notes |
| Cloudflare | checked June 12, 2026 | Cloudflare Developers; plan limits remain dynamic |
| this repository | prepared `v1.1.0`, not tagged or published | this repository |

## Compatibility Notes

- `3x-ui-vps` assumes Ubuntu or Debian with root-managed Docker and nginx.
- `3x-ui-cloudflare` assumes standard Cloudflare products, not unsupported arbitrary TCP or UDP proxying.
- `3x-ui-inbounds` should be checked against current client release notes when XHTTP, REALITY, or other fast-moving transports are involved.
- `3x-ui v3.3.0` moves settings and Xray API routes under `/panel/api`; migrate integrations using `/panel/setting` or `/panel/xray`.
- sing-box `1.13` removes the legacy WireGuard outbound, legacy special outbounds, legacy inbound sniff fields, and legacy GeoIP/Geosite.
- Hysteria `2.9.2` is a security update. Gecko and Realms belong to the official Hysteria application and are not automatically available in the Xray Hysteria transport exposed by 3X-UI.
