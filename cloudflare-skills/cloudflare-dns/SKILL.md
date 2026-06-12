---
name: cloudflare-dns
description: Проектировать и проверять Cloudflare DNS: A, AAAA, CNAME, MX, TXT, NS, SRV, DNSSEC, proxied и DNS only. Использовать, когда задача связана с доменом, записями DNS, proxy status или публикацией сервиса через Cloudflare DNS.
---

# Cloudflare DNS

Используй этот skill, когда нужно спроектировать или проверить DNS-часть публикации через Cloudflare.

## Базовые правила

- Архитектурную разницу между `Proxied` и `DNS only` сначала брать из `cloudflare-basics`; этот модуль применяет её к конкретным DNS-записям.
- Для веб-публикации через standard Cloudflare Proxy проксируются только записи `A`, `AAAA` и `CNAME`.
- `MX`, `TXT`, `NS`, `SRV` и большинство служебных записей не надо описывать как proxied-веб-трафик.
- `Proxied` нужен там, где трафик должен идти через edge Cloudflare.
- `DNS only` нужен там, где Cloudflare должна только отдавать DNS-ответ и не становиться reverse proxy.

## Как выбирать запись

- `A`: имя указывает на IPv4 origin.
- `AAAA`: имя указывает на IPv6 origin.
- `CNAME`: имя указывает на другое canonical hostname.
- `MX`: почтовая маршрутизация.
- `TXT`: верификация, SPF/DKIM/DMARC и другие текстовые данные.
- `NS`: делегирование поддомена или особые authoritative-сценарии.
- `SRV`: discovery сервисов по имени, порту и приоритету.

## Рабочий процесс

1. Определи, является ли hostname веб-ресурсом, почтовым сервисом, verification-записью или private-resource маршрутом.
2. Выбери record type по функции, а не по привычке.
3. Для `A` / `AAAA` / `CNAME` реши, нужен `Proxied` или `DNS only`.
4. Если домен должен быть защищён от DNS spoofing, проверь DNSSEC-сценарий.
5. Если сервис зависит от прямого IP, нестандартного транспорта или сторонней проверки домена, особенно внимательно проверяй, допустим ли `DNS only`.

## Практические правила

- Для публичных HTTP(S) hostname обычно сначала рассматривать `A`, `AAAA` или `CNAME` с `Proxied`.
- Для third-party domain verification и части SaaS-интеграций не включай proxy без явного подтверждения из документации.
- Для почты `MX` должен описываться как почтовая запись, а не как Cloudflare CDN endpoint.
- Для делегирования поддомена `NS` применяй только там, где действительно нужна delegation boundary.
- Для DNSSEC опирайся на текущий setup: full setup, subdomain setup или migration path.

## Проверка и диагностика

- Проверяй record type, name, content, TTL и proxy status отдельно.
- Не смешивай на одном и том же имени ручные HTTPS records с proxied-записями без проверки официальных ограничений.
- Если есть сомнение по поддержке конкретной записи в proxied-режиме, сначала смотри официальные ограничения Cloudflare DNS.

## Что не делать

- Не называть `MX`, `TXT`, `SRV` или `NS` "orange-clouded" веб-записями.
- Не обещать, что любой `CNAME` можно безопасно проксировать.
- Не выдумывать DNSSEC-шаги; использовать только documented setup path.

## Где брать официальные ссылки

Все официальные ссылки для этого skill перечислены в [references/sources.md](references/sources.md).
