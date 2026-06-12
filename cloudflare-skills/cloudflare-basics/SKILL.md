---
name: cloudflare-basics
description: Объяснять и применять базовую архитектуру Cloudflare: edge network, Anycast, CDN, reverse proxy, orange cloud и grey cloud. Использовать, когда нужно правильно классифицировать, как Cloudflare публикует и обслуживает трафик.
---

# Cloudflare Basics

Используй этот skill, когда задача начинается с вопроса "как именно Cloudflare стоит между клиентом и origin" и без этой модели легко ошибиться в DNS, SSL/TLS, Tunnel или Zero Trust.

## Что считать базовой моделью

- Cloudflare для веб-трафика работает как reverse proxy на edge network, а не как "универсальный TCP/UDP прокси по умолчанию".
- Anycast нужен для того, чтобы запрос попадал в ближайшую или доступную edge-точку Cloudflare.
- CDN, кэширование, WAF и часть security-функций доступны только там, где трафик действительно проходит через edge Cloudflare.
- `Proxied` и `DNS only` — это не косметическая разница, а выбор архитектуры потока трафика.

## Ключевые термины

- `Orange Cloud` / `Proxied`: Cloudflare принимает веб-трафик на своей edge-сети, может кэшировать, фильтровать и скрывать origin IP.
- `Grey Cloud` / `DNS only`: Cloudflare только отвечает DNS-записью, а клиент идёт напрямую в origin.
- `Edge Network`: глобальная сеть точек присутствия Cloudflare, где применяются сертификаты edge, CDN и security-функции.
- `Origin`: ваш сервер или промежуточный reverse proxy, например Nginx Proxy Manager.

## Границы модулей

- `cloudflare-dns` отвечает за record types, proxy status и DNSSEC.
- `cloudflare-ssl-tls` отвечает за SSL/TLS modes, edge certificates и Origin CA.
- `cloudflare-proxy-cdn` отвечает за standard Cloudflare Proxy/CDN, cache behavior, ports и headers.
- `cloudflare-tunnel` отвечает за `cloudflared`, public hostnames и private network publication через Tunnel.
- `cloudflare-zero-trust` отвечает за Access, identity, policies, Cloudflare One Client и service tokens.
- `cloudflare-security` отвечает за WAF, custom rules, rate limiting и DDoS-related controls.
- `cloudflare-vpn-integration` собирает решения из остальных модулей для VPN- и homelab-контекста.

## Рабочий процесс

1. Сначала определить тип сервиса: публичный веб-сервис, верификационная запись, почта, private resource, Tunnel или нестандартный transport.
2. Затем определить, должен ли трафик идти через Cloudflare edge или напрямую на origin.
3. Только после этого выбирать DNS record type, proxy status и SSL/TLS mode.
4. Если задача касается VPN, panel, API, self-hosted приложения или homelab, не считать автоматически, что standard Cloudflare Proxy подходит для любого протокола.

## Практические правила

- Если цель — CDN, WAF, скрытие origin IP и edge certificates, нужен `Proxied` веб-трафик.
- Если цель — почта, domain verification, часть SRV/MX/TXT-сценариев или неподдерживаемый transport, чаще нужен `DNS only`.
- Если нужен доступ к private resource без inbound-порта, сначала рассматривать Tunnel, а затем отдельно решать, нужен ли сверху Zero Trust-доступ.
- Если Cloudflare-документация говорит про продуктовые ограничения, не замещать их предположениями "обычно должно работать".

## Что не делать

- Не описывать Cloudflare как замену любого VPN или любого L4-прокси без проверки конкретного продукта.
- Не обещать преимущества CDN или WAF для `DNS only` записей.
- Не путать origin certificate и edge certificate.
- Не выдумывать поведение orange cloud для протоколов, которые в документации не подтверждены.

## Где брать официальные ссылки

Все официальные ссылки для этого skill перечислены в [references/sources.md](references/sources.md).
