# openwrt-cudy-wr3000s-skills

Comprehensive AI Skill Repository for `Cudy WR3000S v1` on OpenWrt.

Official-source-based repository for hardware understanding, installation, recovery, networking, and Podkop or sing-box operation on `Cudy WR3000S v1`.

## Skill Tree

- [`openwrt-cudy-wr3000s`](openwrt-cudy-wr3000s/SKILL.md)
- [`openwrt-cudy-wr3000s-hardware`](openwrt-cudy-wr3000s-hardware/SKILL.md)
- [`openwrt-cudy-wr3000s-install`](openwrt-cudy-wr3000s-install/SKILL.md)
- [`openwrt-cudy-wr3000s-recovery`](openwrt-cudy-wr3000s-recovery/SKILL.md)
- [`openwrt-cudy-wr3000s-networking`](openwrt-cudy-wr3000s-networking/SKILL.md)
- [`openwrt-cudy-wr3000s-services`](openwrt-cudy-wr3000s-services/SKILL.md)

## Dependency Map

- `openwrt-cudy-wr3000s` is the repository router for broad WR3000S tasks.
- `openwrt-cudy-wr3000s-hardware` covers SoC, NAND revisions, LEDs, and platform constraints.
- `openwrt-cudy-wr3000s-install` covers installation and normal upgrade flow.
- `openwrt-cudy-wr3000s-recovery` covers reset, failsafe, OEM TFTP recovery, and UART access.
- `openwrt-cudy-wr3000s-networking` covers DSA ports, VLAN design, and interface mapping.
- `openwrt-cudy-wr3000s-services` covers Podkop, sing-box, DNS, FakeIP, and performance boundaries.

## Quick Start

1. Start with [`openwrt-cudy-wr3000s/SKILL.md`](openwrt-cudy-wr3000s/SKILL.md) for broad device requests.
2. Use `openwrt-cudy-wr3000s-install` before changing firmware.
3. Use `openwrt-cudy-wr3000s-recovery` if the device is already impaired or inaccessible.
4. Use `openwrt-cudy-wr3000s-services` for Podkop or sing-box planning on this hardware.

## Repository Structure

```text
openwrt-cudy-wr3000s-skills/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── VERSION_MATRIX.md
├── SKILL_INDEX.md
├── MIGRATION_GUIDE.md
├── RELEASE_v1.0.0.md
├── openwrt-cudy-wr3000s/
├── openwrt-cudy-wr3000s-hardware/
├── openwrt-cudy-wr3000s-install/
├── openwrt-cudy-wr3000s-recovery/
├── openwrt-cudy-wr3000s-networking/
└── openwrt-cudy-wr3000s-services/
```

## Official Sources

- OpenWrt device page and Techdata
- OpenWrt release notes and Firmware Selector
- official OpenWrt source commits and pull requests for device support
- official Cudy recovery guidance

See [`openwrt-cudy-wr3000s/references/official-links.md`](openwrt-cudy-wr3000s/references/official-links.md).

## Version Policy

Release numbers, NAND support, and OpenWrt layout transitions are version-sensitive. Validate current OpenWrt stable and old-stable state before production changes.

## License

Released under the MIT License. See [`LICENSE`](LICENSE).
