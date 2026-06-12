# Changelog

## v1.1.1 — 3x-ui-skills v1.1.0 synchronization

### Changed

- synchronized the embedded `3x-ui-skills` directory with standalone release
  `v1.1.0` at commit `27eef38884407145bd0f3289848c64dbba080296`
- added current 3X-UI `v3.3.0`, Xray-core, sing-box, Hysteria2, MTProto,
  OpenAPI, XHTTP, WARP rotation and outbound subscription guidance
- added the root `VERSION_MATRIX.md`
- updated `SKILL_DEPENDENCIES.md` with package versions and cross-package
  dependencies
- updated README release metadata and 3X-UI package status
- audited the synchronized `3x-ui-skills` package and root release metadata:
  structure, Markdown links, empty files and duplicate headings

## v1.0.0 — NIDOX VPN Skills Foundation

Первый стабильный релиз базовой архитектуры `nidox-vpn-skills`.

### Added

- Root `NIDOX_SKILLS_INDEX.md`
- Base skill architecture
- `network-fundamentals` as mandatory base dependency
- `cloudflare-skills` integration
- `sing-box-skills` integration
- `3x-ui-skills` integration
- `podkop-skills` integration
- `remnawave-skills` integration
- `openwrt-cudy-wr3000s-skills` integration
- `censorship-resistant-networking` layer
- audit policy
- contribution guide

### Changed

- Repository structure normalized
- Legacy skills directory removed
- `README.md` updated with current architecture
