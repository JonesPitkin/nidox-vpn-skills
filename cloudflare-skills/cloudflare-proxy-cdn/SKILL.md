---
name: cloudflare-proxy-cdn
description: Объяснять и применять Cloudflare Proxy/CDN: кэширование, HTTP, HTTPS, WebSocket, supported ports и заголовки CF-Connecting-IP и X-Forwarded-For.
---

# Cloudflare Proxy CDN

Используй этот skill, когда задача касается стандартного Cloudflare Proxy/CDN для веб-трафика.

## Базовая модель

- Термины `Proxied`, `DNS only`, edge и origin задаются в `cloudflare-basics`; этот модуль описывает уже поведение standard Cloudflare Proxy/CDN после выбора этой модели.
- Standard Cloudflare Proxy работает для HTTP/HTTPS-сценариев, а не для любого произвольного TCP/UDP-трафика.
- Кэширование, WAF и часть performance/security-функций применяются тогда, когда hostname действительно `Proxied`.
- Origin должен понимать, что за Cloudflare может стоять реальный клиентский IP и цепочка прокси-заголовков.

## Что проверять в первую очередь

1. Proxy status hostname.
2. Поддерживаемый порт для standard proxy.
3. Нужен ли кэш вообще или требуется bypass.
4. Есть ли WebSocket и подтверждён ли он как supported scenario.
5. Как origin восстанавливает реальный IP клиента.

## Заголовки origin-side

- `CF-Connecting-IP` — предпочтительный заголовок для получения исходного IP клиента на origin.
- `X-Forwarded-For` — цепочка IP-адресов через прокси, а не один стабильный адрес.
- `X-Forwarded-Proto` показывает, по какому протоколу клиент пришёл к Cloudflare.

## Практические правила

- Если приложение ведёт аудит, rate limiting или access control по IP, сначала определить, какой заголовок оно должно читать.
- Для origin-логов обычно полезнее `CF-Connecting-IP`, чем разбор цепочки `X-Forwarded-For`.
- Для WebSocket проверять, что приложение действительно WebSocket-based и укладывается в supported Cloudflare web path.
- Если сервис слушает нестандартный порт, сначала сверять его с официальным списком supported proxy ports.

## Кэширование

- Не считать Cloudflare cache включённым и полезным "по умолчанию для всего".
- Разделять задачи CDN, cache rules и reverse proxy connectivity.
- Если важна свежесть данных или API semantics, сначала проверить, нужен ли cache bypass или специализированные правила.

## Что не делать

- Не описывать Cloudflare Proxy как замену TCP-load balancer по умолчанию.
- Не подменять `CF-Connecting-IP` произвольным разбором `X-Forwarded-For`, если задача — получить исходный клиентский IP.
- Не обещать кэширование на любом порту или для любого протокола.

## Где брать официальные ссылки

Все официальные ссылки для этого skill перечислены в [references/sources.md](references/sources.md).
