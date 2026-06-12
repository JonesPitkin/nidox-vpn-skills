---
name: cloudflare-security
description: Проектировать и проверять Cloudflare security controls: WAF, custom rules, firewall rules migration, rate limiting, bot protection и DDoS protection.
---

# Cloudflare Security

Используй этот skill, когда задача касается защиты веб-приложения, API или origin на стороне Cloudflare.

## Актуальная терминология

- В текущей документации Cloudflare исторические `Firewall Rules` считаются deprecated и переведены в `WAF custom rules`.
- Для новых решений ориентируйся на `WAF`, `Custom rules`, `Managed rules`, `Rate limiting rules` и `DDoS Protection`.

## Базовые компоненты

- `WAF`: проверяет входящий HTTP/API-трафик и применяет rulesets.
- `Custom rules`: кастомная логика фильтрации с действиями вроде `Block` и `Managed Challenge`.
- `Managed rules`: преднастроенные rulesets Cloudflare.
- `Rate limiting rules`: ограничение частоты запросов по выражению и характеристикам клиента.
- `Bot protection`: средства защиты от нежелательных ботов и связанные с ними правила.
- `DDoS Protection`: автоматическая защита L3/L4/L7 на стороне Cloudflare.

## Рабочий процесс

1. Определи тип угрозы: exploit, brute force, scraping, bad bots, volumetric flood, abuse API.
2. Раздели managed protection и custom logic.
3. Для новых HTTP-политик сначала думай в терминах custom rules и rules language.
4. Для abuse-паттернов по частоте запросов используй rate limiting rules.
5. Для origin-sensitive сценариев проверяй, доходит ли вредный трафик до origin или отсекается на edge.

## Практические правила

- Если пользователь просит "firewall rules", объясняй через современную модель `WAF custom rules`, но можешь отметить legacy-термин.
- Для ботов сначала проверять встроенные bot-management или bot-related возможности и только затем усложнять custom logic.
- Для brute force и abuse API rate limiting обычно является отдельным слоем, а не заменой WAF.
- DDoS-защиту не описывать как ручной toggle "включить защиту вообще"; у Cloudflare значительная часть защиты автоматическая.

## Что не делать

- Не строить новые рекомендации на deprecated Firewall Rules как на primary API/UI-модели.
- Не обещать, что один custom rule заменит все managed protections.
- Не придумывать пороги rate limiting без явного обозначения, что это пример, а не правило из документации.

## Где брать официальные ссылки

Все официальные ссылки для этого skill перечислены в [references/sources.md](references/sources.md).
