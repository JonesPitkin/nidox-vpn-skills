# MTProto FakeTLS

## Модель 3X-UI

Начиная с `v3.3.0`, 3X-UI управляет MTProto inbound через отдельный процесс `mtg`. Это не Xray inbound: Xray stream settings, VLESS clients, REALITY и обычные transport-поля к нему не применяются.

Основные поля:

- `fakeTlsDomain` — домен, кодируемый в FakeTLS secret;
- `secret` — credential с префиксом `ee`;
- listener port и enable state inbound.

Backend нормализует secret при сохранении так, чтобы доменная часть соответствовала `fakeTlsDomain`.

## Рабочий процесс

1. Обновить 3X-UI до `v3.3.0+`.
2. Создать MTProto inbound и выбрать доступный FakeTLS domain.
3. Сохранить inbound и убедиться, что managed `mtg` process запущен.
4. Использовать сгенерированную Telegram proxy link; обычные Xray-клиенты её не импортируют.
5. Проверить listener, журнал 3X-UI/mtg и реальное подключение Telegram.

## Ограничения

- MTProto не заменяет системный VPN или универсальный proxy.
- Не добавлять TLS/REALITY/XHTTP fields вручную.
- Secret считать паролем; не публиковать его.
- После обновления проверять, что orphaned `mtg` процессы завершены.

## Источники

- [3X-UI v3.3.0 release](https://github.com/MHSanaei/3x-ui/releases/tag/v3.3.0)
- [MTProto schema](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/schemas/protocols/inbound/mtproto.ts)
- [MTProto manager](https://github.com/MHSanaei/3x-ui/tree/v3.3.0/mtproto)
