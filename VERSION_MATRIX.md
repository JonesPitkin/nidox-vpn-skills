# NIDOX VPN Skills Version Matrix

Verified June 12, 2026 for meta-repository release `v1.1.1`.

| Package or standalone Skill | Version/source snapshot | Skills | Status |
|---|---:|---:|---|
| `network-fundamentals` | unversioned embedded snapshot | 13 | Stable base layer |
| `cloudflare-skills` | `v1.0.0` | 8 | Embedded |
| `openwrt-cudy-wr3000s-skills` | `v1.0.0` | 6 | Embedded |
| `sing-box-skills` | `v1.0.0` | 10 | Embedded; sing-box baseline `v1.13.13` |
| `3x-ui-skills` | `v1.1.0`, commit `27eef38884407145bd0f3289848c64dbba080296` | 7 | Synchronized |
| `remnawave-skills` | `v1.0.0` | 1 | Embedded |
| `podkop-skills` | `v1.0.0` | 6 | Embedded |
| `censorship-resistant-networking` | unversioned embedded snapshot | 1 | Incubating |
| `3x-ui-vps` | unversioned standalone top-level copy | 1 | Compatibility copy |
| `openwrt-cudy-wr3000s` | unversioned standalone top-level copy | 1 | Compatibility copy |
| **Total** | `nidox-vpn-skills v1.1.1` | **54** | Release baseline |

## 3X-UI Component Baseline

The embedded `3x-ui-skills v1.1.0` snapshot documents:

| Component | Baseline |
|---|---|
| 3X-UI | `v3.3.0` |
| bundled Xray-core | `v26.6.1` |
| Xray-core stable channel | `v26.3.27` |
| sing-box | `v1.13.13` |
| Hysteria | `v2.9.2` |

Package versions are taken from each embedded package's changelog or version
matrix. `Unversioned` means the current embedded content has no standalone
release identifier in this repository; it does not imply version `v1.0.0`.
