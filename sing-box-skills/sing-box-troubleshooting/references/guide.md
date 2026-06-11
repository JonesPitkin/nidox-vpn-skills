# Troubleshooting Guide

## 1. DNS не работает

Симптомы:

- домены не резолвятся;
- приложение видит timeout;
- IP работает, домен нет.

Причины:

- неверный `dns.final`;
- `dns.rules` отправляют запрос не в тот server tag;
- не задан `domain_resolver` для доменного outbound;
- legacy DNS server format после обновления.

Диагностика:

- проверить `dns.servers`;
- проверить `dns.rules`;
- проверить `domain_resolver`;
- проверить deprecated и migration notes.

Решение:

- упростить DNS topology;
- задать явный `final`;
- мигрировать старый формат.

## 2. FakeIP работает неправильно

Симптомы:

- домены выглядят как synthetic IP, но routing не срабатывает;
- часть приложений ломается;
- доменные правила не дают ожидаемого маршрута.

Причины:

- нет `reverse_mapping`;
- DNS не проходит через `sing-box`;
- FakeIP ranges конфликтуют;
- route rules не согласованы с FakeIP-схемой.

Диагностика:

- проверить server type `fakeip`;
- проверить `reverse_mapping`;
- проверить TUN/transparent DNS path.

Решение:

- привести DNS и route к одной модели;
- изолировать локальные домены и исключения.

## 3. TUN не запускается

Симптомы:

- интерфейс не появляется;
- сервис падает при старте;
- трафик не идёт через туннель.

Причины:

- нет прав;
- deprecated `inet4_*` поля;
- конфликт маршрутов;
- невалидные `address`.

Диагностика:

- проверить `sing-box check`;
- проверить права;
- проверить `address`, `auto_route`, `route_exclude_address`.

Решение:

- перейти на актуальные `address`/`route_address` поля;
- упростить маршрутную схему.

## 4. Routing loops

Симптомы:

- трафик зависает;
- соединения уходят в себя;
- direct outbound не выходит в сеть.

Причины:

- нет `auto_detect_interface` или `default_interface`, когда они нужны;
- доменный upstream резолвится по тому же пути, который ещё не поднят;
- отсутствуют exclude routes.

Диагностика:

- проверить `route.final`;
- проверить `default_domain_resolver`;
- проверить TUN exclusions.

Решение:

- задать правильный interface binding;
- выделить bypass path для управления и локальной сети.

## 5. DNS leak

Симптомы:

- часть запросов идёт мимо proxy path;
- split DNS работает не полностью.

Причины:

- системный DNS не перехвачен;
- TUN не контролирует DNS path;
- приложения используют отдельный resolver path.

Диагностика:

- проверить DNS interception strategy;
- проверить `hijack-dns`, DNS rules и то, проходит ли клиентский DNS через `sing-box`.

Решение:

- провести DNS через `sing-box`;
- убрать случайные внешние system resolvers из критичной схемы.

## 6. Rule Sets не применяются

Симптомы:

- match по `rule_set` не работает;
- remote набор не обновляется.

Причины:

- неверный `tag`;
- не включён cache file, когда он ожидается;
- deprecated `download_detour`;
- формат/путь не совпадают.

Диагностика:

- проверить `type`, `format`, `url` или `path`;
- проверить ссылку правила на `tag`.

Решение:

- упростить до одного local или remote rule set и перепроверить.

## 7. TLS ошибки

Симптомы:

- handshake failure;
- certificate verify failed;
- connection reset immediately after connect.

Причины:

- `server_name` не совпадает;
- неподходящий сертификат;
- включены неподдерживаемые или неактуальные для stable options.

Диагностика:

- отделить DNS и TCP reachability от TLS;
- проверить TLS role fields.

Решение:

- привести SNI и certificate к минимальной рабочей конфигурации.

## 8. REALITY ошибки

Симптомы:

- соединение не устанавливается, хотя TCP reachability есть.

Причины:

- перепутаны `public_key` и `private_key`;
- short ID не совпадает;
- mismatch между server-side handshake target и client-side TLS expectations.

Диагностика:

- сравнить ключи и short ID;
- проверить inbound/outbound role mapping.

Решение:

- вернуть минимальный REALITY-конфиг без лишних transport усложнений.

## 9. Hysteria2 ошибки

Симптомы:

- TCP доступность есть, но Hysteria2 не поднимается;
- нестабильный throughput;
- UDP path не работает.

Причины:

- сеть режет UDP;
- неверный TLS/SNI;
- ошибка в `obfs` или password.

Диагностика:

- проверить UDP path;
- проверить server/server_port и TLS.

Решение:

- сначала поднять минимальную Hysteria2 схему без hopping и realm;
- затем добавлять расширения.

## 10. WireGuard ошибки

Симптомы:

- handshake не идёт;
- нет трафика после подъёма endpoint.

Причины:

- неверные ключи;
- неверный `allowed_ips`;
- конфликт маршрутов;
- legacy outbound-модель вместо endpoint-пути.

Диагностика:

- проверить endpoint schema;
- проверить `address`, peer `public_key`, `allowed_ips`.

Решение:

- вернуться к минимальному `endpoint/wireguard` примеру из официальной документации.
