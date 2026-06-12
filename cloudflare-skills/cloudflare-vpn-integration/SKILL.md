---
name: cloudflare-vpn-integration
description: Интегрировать Cloudflare с OpenWrt, sing-box, 3x-ui, Nginx Proxy Manager и homelab-сценариями, не выходя за пределы официально подтверждённого поведения Cloudflare.
---

# Cloudflare VPN Integration

Используй этот skill, когда Cloudflare надо встроить в VPN- или homelab-инфраструктуру, но рекомендации должны оставаться строго на Cloudflare-side и без выдумывания настроек внешних систем.

## Границы этого skill

- Этот skill описывает, как Cloudflare ведёт себя рядом с `OpenWrt`, `sing-box`, `3x-ui`, `Nginx Proxy Manager` и homelab-сервисами.
- Если для внешнего продукта нет подтверждённой Cloudflare-side схемы, это нужно прямо сказать.
- Приоритет у архитектурных решений Cloudflare: `DNS only`, `Proxied`, `Tunnel`, `Access`, `WARP`, `Origin CA`, `WAF`.
- За базовой терминологией и деталями модулей сначала обращаться в `cloudflare-basics`, `cloudflare-dns`, `cloudflare-ssl-tls`, `cloudflare-proxy-cdn`, `cloudflare-tunnel` и `cloudflare-zero-trust`.

## Ментальная модель

- `OpenWrt` и homelab часто выступают как origin network или private LAN behind Tunnel.
- `Nginx Proxy Manager` выступает как origin reverse proxy, а не как Cloudflare feature.
- `3x-ui` и `sing-box` нельзя автоматически считать совместимыми со standard Cloudflare Proxy на любом transport.
- Если transport не является подтверждённым HTTP/HTTPS web path, сначала проверяй, не нужен ли `DNS only` или альтернативная Cloudflare product path.

## Рабочий процесс

1. Зафиксируй сервис: panel, subscription endpoint, internal dashboard, API, private app, raw transport.
2. Определи, веб-трафик это или нет.
3. Выбери модель публикации: `Proxied` для supported web-сценариев; `DNS only` для direct-сценариев и неподдерживаемых standard proxy transport; `Tunnel` для безопасной публикации без origin IP; `Access` / `WARP` для private или admin-only доступа.
4. Отдельно выбери SSL/TLS mode и origin certificate strategy.
5. Для origin hardening учитывай allowlisting Cloudflare IPs, Authenticated Origin Pulls или Tunnel.

## Практические правила интеграции

- Для `Nginx Proxy Manager` описывай Cloudflare как edge/front door, а Nginx Proxy Manager как origin reverse proxy.
- Для `OpenWrt` и homelab сначала решай, нужен ли public hostname или private access.
- Для `3x-ui` и `sing-box` не выдавай blanket-утверждение, что любой inbound/transport можно пустить через orange cloud.
- Для admin panel и self-hosted dashboard чаще сначала проверяй Tunnel + Access, а не публичный direct exposure.

## Что не делать

- Не выдумывать совместимость нестандартного VPN transport со standard Cloudflare Proxy.
- Не давать NPM-, OpenWrt- или 3x-ui-специфичные шаги как "официальные Cloudflare", если они такими не являются.
- Не превращать Cloudflare в универсальный ответ на задачи L4/L7 без проверки продукта и transport.

## Где брать официальные ссылки

Все официальные ссылки для этого skill перечислены в [references/sources.md](references/sources.md).
