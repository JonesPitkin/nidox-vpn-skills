# Version Matrix

| Area | Coverage Policy | Source of Truth |
|---|---|---|
| `3x-ui` panel features | follow current official repository and wiki before making production changes | official `3x-ui` repository, wiki, release notes |
| bundled Xray behavior | verify transport and routing semantics against the currently shipped upstream build | `3x-ui` release artifacts and source tree |
| Cloudflare edge behavior | treat ports, product limits, and transport compatibility as changeable | Cloudflare Developers documentation |
| repository release | current standalone repository release is `v1.0.0` | this repository |

## Compatibility Notes

- `3x-ui-vps` assumes Ubuntu or Debian with root-managed Docker and nginx.
- `3x-ui-cloudflare` assumes standard Cloudflare products, not unsupported arbitrary TCP or UDP proxying.
- `3x-ui-inbounds` should be checked against current client release notes when XHTTP, REALITY, or other fast-moving transports are involved.
