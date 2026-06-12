# VMess

## Описание

VMess — UUID-based протокол V2Ray/Xray. 3X-UI поддерживает VMess как полноценный inbound с клиентами, лимитами и share links.

## Когда использовать

- для совместимости со старыми V2Ray-клиентами;
- при миграции существующих VMess deployment;
- когда целевой клиент не поддерживает VLESS.

Для новой direct-конфигурации обычно предпочтительнее VLESS REALITY Vision: VMess не поддерживает REALITY или Vision.

## Преимущества

- широкая поддержка V2Ray/Xray-клиентов;
- множество stream transports;
- удобен для миграции legacy deployment.

## Недостатки

- нет REALITY и Vision;
- больше legacy baggage, чем у VLESS;
- новые transports требуют актуального client core.

## Требования

- UUID для каждого клиента;
- transport TCP/mKCP/WS/gRPC/HTTPUpgrade/XHTTP;
- TLS для публичного WS/gRPC/HTTPUpgrade/XHTTP deployment;
- совпадающие address, port, UUID, transport, host/path и TLS fields.

## Настройка в панели

1. Выбрать protocol `VMess`.
2. Добавить клиента, сгенерировать UUID, оставить security `auto`, если нет требования клиента.
3. Выбрать transport и security.
4. Для TLS указать certificate, key и SNI.
5. Сохранить и проверить Xray logs/listener.

REALITY и `xtls-rprx-vision` для VMess не выбирать: capability model 3X-UI их не разрешает.

## Настройка клиента

- v2rayNG и Shadowrocket: импортировать VMess URL/subscription и проверить transport/TLS.
- sing-box: использовать native `type: vmess` outbound.
- Podkop: VMess отсутствует в списке URL-протоколов Proxy section; не обещать импорт. Использовать другой поддержанный протокол. Custom outbound проверять на конкретной версии.

## Типовые ошибки

- UUID или address неверны;
- TLS включён только на одной стороне;
- потеряны host/path/serviceName;
- выбран REALITY/Vision, которые VMess не поддерживает;
- старый клиент не понимает новый transport;
- subscription содержит устаревшую запись.

## Диагностика

Сверить VMess link после импорта, временно отключить mux/TUN и проверить простую TCP/TLS либо WS/TLS схему. На сервере:

```sh
journalctl -u x-ui -n 200 --no-pager | grep -iE 'vmess|failed|error'
ss -lntup
```

## Источники

- [3X-UI Wiki Home](https://github.com/MHSanaei/3x-ui/wiki)
- [3X-UI VMess schema](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/schemas/protocols/inbound/vmess.ts)
- [Xray VMess inbound](https://xtls.github.io/en/config/inbounds/vmess.html)
- [sing-box VMess outbound](https://sing-box.sagernet.org/configuration/outbound/vmess/)
- [v2rayNG](https://github.com/2dust/v2rayNG)
