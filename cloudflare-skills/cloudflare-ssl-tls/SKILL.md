---
name: cloudflare-ssl-tls
description: Настраивать и объяснять Cloudflare SSL/TLS: Flexible, Full, Full Strict, edge certificates, Origin CA, Universal SSL и origin reverse proxy сценарии, включая Nginx Proxy Manager.
---

# Cloudflare SSL/TLS

Используй этот skill, когда задача касается режима шифрования между клиентом, Cloudflare edge и origin.

## Базовая модель

- Edge certificate — сертификат, который Cloudflare показывает посетителю.
- Origin certificate — сертификат, который origin показывает Cloudflare.
- Режим SSL/TLS определяет, как Cloudflare соединяется с origin, а не только то, что видит браузер пользователя.

## Режимы SSL/TLS

- `Flexible`: HTTPS только между клиентом и Cloudflare; от Cloudflare до origin идёт HTTP. Использовать крайне осторожно и не рекомендовать как нормальную целевую конфигурацию.
- `Full`: HTTPS между Cloudflare и origin есть, но сертификат origin может быть self-signed, Cloudflare Origin CA или публичный.
- `Full (strict)`: как `Full`, но сертификат origin должен соответствовать строгим требованиям Cloudflare.

## Предпочтительный подход

- По умолчанию рекомендовать `Full (strict)`.
- Для origin использовать Cloudflare Origin CA или корректный публичный сертификат.
- Если origin — это Nginx Proxy Manager, считать его обычным origin reverse proxy: Cloudflare edge завершает внешнее TLS, а Nginx Proxy Manager должен корректно обслуживать TLS до origin-уровня согласно выбранному mode.

## Edge certificates

- `Universal SSL` — автоматические edge-сертификаты Cloudflare для активированных доменов.
- Нужно помнить про ограничения покрытия Universal SSL, особенно для глубоких subdomain в full setup.
- Если нужны дополнительные hostname, контроль CA или иные edge-параметры, проверять Advanced Certificate Manager или Custom certificate path в официальной документации.

## Origin certificates

- `Cloudflare Origin CA` предназначен для соединения Cloudflare-to-origin.
- Origin CA не надо описывать как сертификат для прямых клиентских подключений в обход Cloudflare.
- Если запись `DNS only`, клиент идёт прямо к origin, значит сертификат должен подходить уже для прямого клиентского сценария, а не только для Cloudflare edge.

## Рабочий процесс

1. Определи, идёт ли трафик через `Proxied` hostname или напрямую.
2. Определи, кто завершает TLS на origin: само приложение, Nginx, Nginx Proxy Manager или иной reverse proxy.
3. Выбери SSL/TLS mode.
4. Проверь edge certificate coverage и origin certificate validity отдельно.
5. Если origin защищается сильнее, рассмотри Authenticated Origin Pulls как дополнительный слой.

## Что не делать

- Не рекомендовать `Flexible` как долгосрочную безопасную схему.
- Не путать Universal SSL с сертификатом на origin.
- Не считать Origin CA валидным ответом для прямого `DNS only` доступа посетителя.
- Не выдумывать отдельные Nginx Proxy Manager toggle-имена, если они не подтверждены документацией Cloudflare.

## Где брать официальные ссылки

Все официальные ссылки для этого skill перечислены в [references/sources.md](references/sources.md).
