# Политика репозиториев NIDOX

## Назначение nidox-vpn-skills

Этот репозиторий является главным сборником VPN Skills.

В него входят навыки для:

- 3x-ui
- Podkop
- OpenWrt
- Cudy WR3000S
- sing-box
- Xray
- Cloudflare
- Remnawave

Все навыки внутри данного репозитория должны проходить аудит через `nidox-vpn-detection-defense-skill`.

## Самостоятельные репозитории

Отдельные репозитории:

- `3x-ui-skills`
- `podkop-skills`
- `openwrt-cudy-wr3000s-skill`
- `sing-box-skill`
- `remnawave-skill`

могут использоваться независимо и не требуют обязательного аудита.

## Правило включения

После переноса любого skill в `nidox-vpn-skills` он автоматически становится частью общей VPN-инфраструктуры и должен проходить аудит.
