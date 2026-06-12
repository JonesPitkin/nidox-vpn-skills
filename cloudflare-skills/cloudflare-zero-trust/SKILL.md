---
name: cloudflare-zero-trust
description: Настраивать и объяснять Cloudflare Zero Trust: Access, policies, identity provider, WARP / Cloudflare One Client, Access applications и service tokens.
---

# Cloudflare Zero Trust

Используй этот skill, когда нужно дать доступ к приложению или private resource не "по открытому URL для всех", а по identity- и policy-driven модели.

## Базовая модель

- `Cloudflare Access` определяет, кто может reach приложение, через Access policies.
- `Identity Provider` даёт источник identity.
- `Cloudflare One Client` (бывший WARP) подключает устройство к Cloudflare network и даёт device-context для политик.
- `Service Tokens` нужны для machine-to-machine и service auth сценариев.
- Сетевой путь до private resource или local service сам по себе обычно задаётся через `cloudflare-tunnel`; этот модуль не заменяет Tunnel и не описывает connector-level publication.

## Что проектировать

- Кто субъект доступа: пользователь, группа, сервис, устройство.
- Какой объект защищается: Access application, automation endpoint или иной private resource.
- Нужен ли IdP login, mTLS, service token или требование WARP/device posture.

## Рабочий процесс

1. Определи ресурс и способ доступа: browser app, private hostname, private IP/CIDR, automation.
2. Выбери тип Access application и policy model.
3. Подключи IdP, если доступ user-centric.
4. Для device-aware доступа реши, нужен ли Cloudflare One Client / WARP.
5. Для automation реши, подходит ли service token.
6. На origin-side не забывай о token validation, если это требуется по модели приложения.

## Практические правила

- Для внутренней панели, homelab UI или admin endpoint сначала рассматривать Access, а не публичный unauthenticated URL.
- Для private network доступа учитывать отдельно сетевой путь, identity-слой и клиентский путь Cloudflare One Client / WARP.
- Для B2B, подрядчиков и нескольких identity domains учитывать, что Cloudflare поддерживает multiple identity providers.
- Для сервисов без интерактивного логина рассматривать `Service Auth` / `Service Tokens`.

## Что не делать

- Не считать Zero Trust просто "ещё одной VPN".
- Не путать public hostname через Tunnel и приватный доступ через WARP как один и тот же UX.
- Не выдавать service token как аналог пользовательской сессии.
- Не пропускать origin/token validation там, где официальная документация требует её.

## Где брать официальные ссылки

Все официальные ссылки для этого skill перечислены в [references/sources.md](references/sources.md).
