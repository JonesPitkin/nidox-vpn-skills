# XTLS Vision

## Описание

Vision — VLESS flow `xtls-rprx-vision`. В текущей форме 3X-UI он допустим только при VLESS + TCP + TLS или REALITY.

## Когда использовать

- direct VLESS TCP REALITY;
- direct VLESS TCP TLS;
- когда клиентский core явно поддерживает Vision/XUDP.

## Преимущества

- рекомендованный Wiki baseline вместе с TCP REALITY;
- снижает лишнее encapsulation для подходящего TLS traffic;
- поддержан Xray и официальным VLESS outbound sing-box.

## Недостатки

- не является transport и не применяется к WS/gRPC/XHTTP;
- старые клиенты теряют или не понимают `flow`;
- multiplex/custom wrapping может конфликтовать;
- не заменяет REALITY/TLS.

## Требования

- protocol `vless`;
- `network=tcp`;
- `security=tls` или `reality`;
- client `flow=xtls-rprx-vision`;
- актуальный core.

## Настройка в панели

1. Создать VLESS inbound.
2. TCP (Raw).
3. TLS или REALITY.
4. В client row выбрать `xtls-rprx-vision`.
5. `testseed` оставлять default, если нет подтвержденной причины менять. Schema требует четыре positive integers; fixture/default UI показывает `900,500,900,256`.

Не добавлять Vision к клиентам другого transport: panel link generator включает `flow` только для TCP.

## Настройка клиента

В URL/JSON должно быть:

```text
flow=xtls-rprx-vision
```

sing-box:

```json
"flow": "xtls-rprx-vision"
```

Для v2rayNG/Shadowrocket проверить field после импорта. В Podkop VLESS REALITY example содержит тот же flow.

## Типовые ошибки

- connection closes immediately: flow mismatch;
- flow отсутствует после subscription conversion;
- попытка Vision + gRPC/WS/XHTTP;
- старый client core;
- включенный mux вызывает нестабильность.

## Диагностика

Сначала удалить mux/fragment/custom packet encoding. Сравнить работу того же client:

1. TCP REALITY без Vision.
2. TCP REALITY с Vision.

Если ломается только второй вариант, обновить client core и проверить импорт `flow`.

## Источники

- [3X-UI capability predicates](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/lib/xray/protocol-capabilities.ts)
- [3X-UI VLESS form](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/pages/inbounds/form/protocols/vless.tsx)
- [VLESS REALITY Vision fixture](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/test/golden/fixtures/inbound-full/vless-tcp-reality.json)
- [sing-box VLESS flow](https://sing-box.sagernet.org/configuration/outbound/vless/)
- [Podkop custom outbound](https://podkop.net/docs/own-outbound/)
