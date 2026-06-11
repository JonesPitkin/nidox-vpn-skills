# nidox-vpn-skills

`nidox-vpn-skills` — главный сборник моих VPN Codex skills. Этот репозиторий используется как мета-уровень для навыков, связанных с проектированием, развёртыванием, настройкой и сопровождением VPN-инфраструктуры.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Сюда складываются skills, относящиеся к следующим направлениям:

- 3x-ui
- Podkop
- OpenWrt / Cudy WR3000S
- sing-box
- Xray
- Cloudflare
- Remnawave

## Skills

- network-fundamentals
- openwrt-skills
- podkop-skills
- 3x-ui-skills
- cloudflare-skills
- remnawave-skills
- sing-box-skills

Репозиторий фиксирует общую структуру VPN-навыков и задаёт единые правила аудита. При этом существующие skill-файлы и ранее созданные каталоги сохраняются и могут использоваться как часть переходного периода.

## Skill repositories

- 3x-ui-skills
- podkop-skills
- cloudflare-skills
- remnawave-skills
- sing-box-skills
- network-fundamentals
- openwrt-cudy-wr3000s

## Быстрая навигация

- [SKILL_INDEX.md](./SKILL_INDEX.md) — центральный каталог VPN Skills со статусами и требованиями к аудиту.
- [AUDIT_POLICY.md](./AUDIT_POLICY.md) — правила обязательного аудита skills внутри `nidox-vpn-skills`.
- [REPOSITORY_POLICY.md](./REPOSITORY_POLICY.md) — разграничение ролей главного репозитория и самостоятельных skill-репозиториев.
- [ROADMAP.md](./ROADMAP.md) — план развития текущих и будущих VPN Skills.
- [CONTRIBUTING.md](./CONTRIBUTING.md) — требования к структуре и включению новых Skills.
- [network-fundamentals/](./network-fundamentals/) — встроенный фундаментальный skill по сетям.

## Структура репозитория

```text
nidox-vpn-skills/
├── README.md
├── AUDIT_POLICY.md
├── REPOSITORY_POLICY.md
├── SKILL_INDEX.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore
├── network-fundamentals/
│   ├── README.md
│   ├── SKILL.md
│   ├── AUDIT.md
│   ├── QUALITY_REPORT.md
│   ├── references/
│   └── ...
├── archive/
│   ├── macOS/
│   ├── packages/
│   └── README.md
├── skills/
│   ├── 3x-ui/
│   │   └── README.md
│   ├── podkop/
│   │   └── README.md
│   ├── openwrt-cudy-wr3000s/
│   │   └── README.md
│   ├── sing-box/
│   │   └── README.md
│   ├── cloudflare/
│   │   └── README.md
│   └── remnawave/
│       └── README.md
├── 3x-ui-skills/
│   ├── README.md
│   ├── SKILL_INDEX.md
│   ├── VERSION_MATRIX.md
│   ├── MIGRATION_GUIDE.md
│   └── ...
├── podkop-skills/
│   ├── README.md
│   ├── SKILL_INDEX.md
│   ├── VERSION_MATRIX.md
│   ├── MIGRATION_GUIDE.md
│   └── ...
├── cloudflare-skills/
│   ├── README.md
│   ├── SKILL_INDEX.md
│   ├── VERSION_MATRIX.md
│   ├── MIGRATION_GUIDE.md
│   └── ...
├── remnawave-skills/
│   ├── README.md
│   ├── SKILL_INDEX.md
│   ├── VERSION_MATRIX.md
│   ├── MIGRATION_GUIDE.md
│   └── ...
├── sing-box-skills/
│   ├── README.md
│   ├── SKILL_INDEX.md
│   ├── VERSION_MATRIX.md
│   ├── MIGRATION_GUIDE.md
│   └── ...
└── audit/
    └── nidox-vpn-detection-defense-skill.md
```

Каталог `skills/` является целевой мета-структурой для VPN-навыков внутри этого репозитория. Если конкретный skill ещё не перенесён или не оформлен отдельно, внутри каталога хранится служебный `README.md`, чтобы структура оставалась явной и сохранялась в Git.

## Политика аудита

Все skills внутри `nidox-vpn-skills` должны проверяться через `nidox-vpn-detection-defense-skill`.

Это обязательное правило действует именно для данного мета-репозитория, потому что здесь навыки рассматриваются как части одной VPN-системы, а не как полностью изолированные модули. Аудит нужен для проверки:

- VPN detection risks
- network fingerprints
- routing artifacts
- GeoIP / ASN exposure
- DNS leaks
- false-positive detection scenarios

Подробные правила описаны в файле [AUDIT_POLICY.md](./AUDIT_POLICY.md).

Общая роль главного репозитория и границы между мета-репозиторием и отдельными skill-репозиториями дополнительно описаны в файле [REPOSITORY_POLICY.md](./REPOSITORY_POLICY.md).

## Network Fundamentals

В репозиторий добавлен отдельный фундаментальный skill по компьютерным сетям:

- встроенная версия: [network-fundamentals/](./network-fundamentals/)
- самостоятельный репозиторий: [network-fundamentals-skill](https://github.com/JonesPitkin/network-fundamentals-skill)

Раздел предназначен для общей сетевой теории и практической диагностики: OSI, TCP/IP, TCP и UDP, MTU и MSS, NAT и CGNAT, routing, gateway, DNS, IPv4, IPv6 и порты.

## Связанные репозитории

- `3x-ui-skills` — самостоятельный репозиторий навыков для 3x-ui.
- `podkop-skills` — самостоятельный репозиторий навыков для Podkop.
- `cloudflare-skills` — самостоятельный репозиторий навыков для Cloudflare-публикации VPN-инфраструктуры.
- `openwrt-cudy-wr3000s-skill` — самостоятельный репозиторий навыков для OpenWrt / Cudy WR3000S.
- `sing-box-skills` — самостоятельный репозиторий навыков для sing-box.
- `remnawave-skills` — самостоятельный репозиторий навыков для Remnawave.
- [`network-fundamentals-skill`](https://github.com/JonesPitkin/network-fundamentals-skill) — самостоятельный репозиторий фундаментального сетевого справочника для Codex.
- `nidox-vpn-detection-defense-skill` — отдельный аудит-модуль для проверки VPN skills.

Отдельные репозитории могут использоваться сами по себе без обязательного аудита. Обязательная проверка через `nidox-vpn-detection-defense-skill` включается в тот момент, когда skill используется внутри `nidox-vpn-skills`.

## License

Репозиторий лицензирован по лицензии MIT. Материалы можно свободно использовать, изменять и распространять в соответствии с условиями лицензии MIT.

Полный текст лицензии: [LICENSE](./LICENSE)
