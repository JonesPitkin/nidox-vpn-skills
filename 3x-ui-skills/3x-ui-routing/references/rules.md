# Routing Rules

## Поддерживаемые поля 3X-UI

Текущая schema включает: `domain`, `ip`, `port`, `sourcePort`, `localPort`, `network`, `sourceIP`, `localIP`, `user`, `vlessRoute`, `inboundTag`, `protocol`, `attrs`, `process`, `outboundTag`, `balancerTag`, `ruleTag`, `webhook`.

Не каждое поле применимо на сервере и каждой ОС. Например, process matching обычно относится к локальным outbound-сценариям, а не удаленному клиентскому процессу.

## Порядок

1. Служебные правила панели/API, если они присутствуют.
2. Явные исключения.
3. DNS/internal/private policy.
4. Узкие domain/IP/inbound/user rules.
5. Широкие geosite/geoip rules.
6. Catch-all.

Wiki предупреждает: API routing rule должен оставаться первым, иначе статистика/API могут работать некорректно.

## Пошаговый пример

1. Создать outbound `warp`.
2. Добавить rule:

```json
{
  "type": "field",
  "domain": [
    "domain:example.com",
    "geosite:google"
  ],
  "network": "tcp,udp",
  "outboundTag": "warp",
  "ruleTag": "selected-via-warp"
}
```

3. Ниже добавить block rule:

```json
{
  "type": "field",
  "protocol": ["bittorrent"],
  "outboundTag": "blocked"
}
```

4. Проверить порядок и существование tags.

## Ошибки

- Пустое поле принимается за wildcard без проверки.
- `network` исключает UDP, хотя приложение использует QUIC.
- `protocol=bittorrent` требует sniffing/распознавания; не гарантировать блокировку любого зашифрованного трафика.
- `outboundTag` и `balancerTag` заданы вместе.
- Rule относится к client email/user, которого нет в inbound.

## Диагностика

Временно повысить Xray loglevel до `info`/`debug` только на короткий тест, затем вернуть `warning`. Сопоставить один тестовый client, один domain и один rule.

## Источники

- [3X-UI routing schema](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/schemas/routing.ts)
- [3X-UI Wiki FAQ: WARP and API rule](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems)
- [Xray routing rules](https://xtls.github.io/en/config/routing.html)
