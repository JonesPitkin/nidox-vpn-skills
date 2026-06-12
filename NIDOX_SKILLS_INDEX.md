# NIDOX Skills Index

`NIDOX_SKILLS_INDEX.md` — главный навигационный центр репозитория `nidox-vpn-skills`. Это первая точка входа для Codex и для человека, который впервые открывает проект.

## Что Такое `nidox-vpn-skills`

`nidox-vpn-skills` — это мета-репозиторий skill-пакетов NIDOX для проектирования, развёртывания, настройки, проверки и сопровождения VPN- и сетевой инфраструктуры. Репозиторий собирает в одном месте базовые сетевые знания, платформенные пакеты и прикладные VPN-навыки, чтобы ими можно было пользоваться как по отдельности, так и как единой системой.

Репозиторий нужен для того, чтобы:

- дать единый вход в skill-пакеты проекта NIDOX;
- зафиксировать зависимости между пакетами;
- задать общий стандарт структуры, источников и проверки;
- ускорить навигацию между фундаментальными, платформенными и прикладными навыками;
- снизить риск вымышленных конфигураций и несогласованных рекомендаций.

Практически skill-пакеты используются совместно так:

- `network-fundamentals` даёт базу по сетям и диагностике;
- `cloudflare-skills` и `openwrt-cudy-wr3000s-skills` добавляют платформенный контекст;
- `sing-box-skills` даёт основной транспортный и конфигурационный слой;
- `3x-ui-skills`, `remnawave-skills` и `podkop-skills` накладывают панельные и продуктовые сценарии;
- `censorship-resistant-networking` собирает несколько пакетов в архитектурные и troubleshooting-сценарии для сложных сетевых условий.

## Архитектура Навыков

Ниже приведено актуализированное дерево верхнеуровневых зависимостей по текущей структуре репозитория.

```text
network-fundamentals
├── cloudflare-skills
├── openwrt-cudy-wr3000s-skills
├── sing-box-skills
│   ├── 3x-ui-skills
│   ├── remnawave-skills
│   └── podkop-skills
└── censorship-resistant-networking
```

Перекрёстные зависимости, которые не помещаются в простое дерево:

- `3x-ui-skills` также опирается на `cloudflare-skills` для публикации и edge-сценариев.
- `podkop-skills` также опирается на `openwrt-cudy-wr3000s-skills` для роутерного и OpenWrt-контекста.
- `censorship-resistant-networking` использует знания из `cloudflare-skills`, `openwrt-cudy-wr3000s-skills`, `sing-box-skills`, `3x-ui-skills` и `podkop-skills`.

## Базовые Навыки

### `network-fundamentals`

- Назначение: фундаментальная база по OSI, TCP/IP, DNS, NAT, маршрутизации, IPv4/IPv6, MTU и портам.
- Обязательность: обязательный базовый слой для всех VPN skill-пакетов репозитория.
- Зависимости: отсутствуют на верхнем уровне; это исходная опорная база.

### `cloudflare-skills`

- Назначение: домены, DNS, proxy/CDN, SSL/TLS, Tunnel, Zero Trust и Cloudflare-side интеграция с VPN-сценариями.
- Обязательность: обязательный базовый платформенный пакет для edge-публикации и доменной инфраструктуры.
- Зависимости: `network-fundamentals`.

### `openwrt-cudy-wr3000s-skills`

- Назначение: аппаратная платформа `Cudy WR3000S v1`, установка OpenWrt, recovery, DSA/VLAN и запуск сетевых сервисов на роутере.
- Обязательность: обязательный базовый платформенный пакет для роутерных и OpenWrt-сценариев.
- Зависимости: `network-fundamentals`.

## Основные VPN-Навыки

### `sing-box-skills`

- Назначение: основной пакет по архитектуре `sing-box`, DNS, inbounds/outbounds, маршрутизации, TUN, rulesets, security и troubleshooting.
- Что изучает: transport-модели, policy routing, DNS design, transparent proxying, OpenWrt-развёртывания и миграции.
- На какие навыки опирается: `network-fundamentals`.

### `3x-ui-skills`

- Назначение: пакет по эксплуатации `3x-ui`, VPS bootstrap, install/update, inbound-дизайну, Xray routing, hardening и Cloudflare-публикации.
- Что изучает: панельный слой управления Xray/VLESS-инфраструктурой и связанный operational lifecycle.
- На какие навыки опирается: `network-fundamentals`, `sing-box-skills`, `cloudflare-skills`.

### `remnawave-skills`

- Назначение: пакет по Remnawave для deployment planning, panel operations, node integration и source-backed validation.
- Что изучает: роль панели, operational baseline, интеграцию узлов и проверку production-изменений по официальным источникам.
- На какие навыки опирается: `network-fundamentals`, `sing-box-skills`.

### `podkop-skills`

- Назначение: пакет по Podkop на OpenWrt для install/update, DNS и FakeIP, routing, diagnostics и minimal-change troubleshooting.
- Что изучает: роутерный proxy/VPN-клиентский контур на базе `sing-box`, `dnsmasq` и OpenWrt.
- На какие навыки опирается: `network-fundamentals`, `sing-box-skills`, `openwrt-cudy-wr3000s-skills`.

## Дополнительные Навыки

### `censorship-resistant-networking`

- Назначение: проектирование и диагностика устойчивых к блокировкам сетевых топологий, selective routing, CDN-path, WARP, cascades и transparent OpenWrt-схем.
- Роль в репозитории: надстройка над базовыми и основными VPN skill-пакетами для более сложных и составных сценариев.
- Зависимости: `network-fundamentals`, `cloudflare-skills`, `openwrt-cudy-wr3000s-skills`, `sing-box-skills`, `3x-ui-skills`, `podkop-skills`.

### Будущие Skill-Пакеты

Список дополнительных навыков будет расширяться. Новые пакеты будут включаться в этот индекс после появления в репозитории и после проверки их места в общей dependency-модели.

## Рекомендуемый Порядок Изучения

1. `network-fundamentals`
2. `cloudflare-skills`
3. `openwrt-cudy-wr3000s-skills`
4. `sing-box-skills`
5. `3x-ui-skills`
6. `remnawave-skills`
7. `podkop-skills`
8. `censorship-resistant-networking`

## Skill Dependency Matrix

| Skill | Depends On |
| --- | --- |
| `network-fundamentals` | none |
| `cloudflare-skills` | `network-fundamentals` |
| `openwrt-cudy-wr3000s-skills` | `network-fundamentals` |
| `sing-box-skills` | `network-fundamentals` |
| `3x-ui-skills` | `network-fundamentals`, `sing-box-skills`, `cloudflare-skills` |
| `remnawave-skills` | `network-fundamentals`, `sing-box-skills` |
| `podkop-skills` | `network-fundamentals`, `sing-box-skills`, `openwrt-cudy-wr3000s-skills` |
| `censorship-resistant-networking` | `network-fundamentals`, `cloudflare-skills`, `openwrt-cudy-wr3000s-skills`, `sing-box-skills`, `3x-ui-skills`, `podkop-skills` |

## Стандарты Проекта

Для production-style skill-пакетов репозитория принят следующий стандарт:

- каждый skill-модуль использует `SKILL.md` как entrypoint;
- каждый skill-модуль должен иметь `references/`;
- каждый skill-модуль должен иметь `agents/`;
- в качестве источников используются только официальные документы, репозитории и vendor-maintained materials;
- запрещено выдумывать конфигурации, команды, поля UI, версии, режимы работы и unsupported compatibility claims.

Текущая оговорка по структуре:

- `network-fundamentals` уже соответствует общей идее entrypoint-first структуры, но хранит значительную часть материалов в плоском формате `references.md`, `glossary.md` и `examples.md` внутри тематических разделов; это нужно учитывать как совместимое историческое исключение текущего репозитория.

## План Развития

Текущие и будущие направления расширения:

- `happ-skills`;
- новые OpenWrt skills;
- новые Cloudflare skills;
- новые панели управления VPN;
- новые сетевые технологии.

## Навигация По Репозиторию

- [README.md](./README.md) — общий обзор репозитория.
- [SKILL_INDEX.md](./SKILL_INDEX.md) — текущий краткий каталог skill-пакетов верхнего уровня.
- [network-fundamentals/README.md](./network-fundamentals/README.md) — фундаментальный сетевой пакет.
- [cloudflare-skills/README.md](./cloudflare-skills/README.md) — пакет по Cloudflare.
- [openwrt-cudy-wr3000s-skills/README.md](./openwrt-cudy-wr3000s-skills/README.md) — пакет по OpenWrt/Cudy WR3000S.
- [sing-box-skills/README.md](./sing-box-skills/README.md) — пакет по `sing-box`.
- [3x-ui-skills/README.md](./3x-ui-skills/README.md) — пакет по `3x-ui`.
- [remnawave-skills/README.md](./remnawave-skills/README.md) — пакет по Remnawave.
- [podkop-skills/README.md](./podkop-skills/README.md) — пакет по Podkop.
- [censorship-resistant-networking/SKILL.md](./censorship-resistant-networking/SKILL.md) — дополнительный skill по устойчивым сетевым архитектурам.
