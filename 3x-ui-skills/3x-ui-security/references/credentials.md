# Credentials и 2FA

> Проверено по 3X-UI `v3.3.0`.

## Требования

- уникальный username, не `admin`;
- длинный уникальный password из password manager;
- 2FA/TOTP;
- непредсказуемый web base path;
- немедленная ротация после утечки backup/log/screenshot.

Native installer генерирует случайные credentials/path. Docker examples могут содержать `admin/admin`; их необходимо заменить сразу.

## Пошаговая процедура

1. Создать защищенный backup.
2. В UI сменить username/password.
3. Включить 2FA в Panel Settings.
4. Сохранить TOTP seed/recovery material в защищенном хранилище.
5. В отдельной private browser session проверить новый вход.
6. Через menu сбросить credentials/path, если UI недоступен:

```sh
x-ui
# Reset Username & Password
# Reset Web Base Path
```

## Секреты, которые нельзя публиковать

Добавить к списку:

- Bearer API tokens;
- MTProto FakeTLS secrets;
- outbound subscription URLs, если URL содержит credentials;
- custom subscription template data с embedded identifiers.

API token предпочтительнее scripted login для automation, но только при безопасном хранении, rotation и revoke. Endpoint specification брать из `/panel/api/openapi.json`.

Panel/API credentials, Telegram bot token/chat ID, PostgreSQL DSN, UUID/passwords клиентов, subscription URLs, Reality private key, TLS private key, Cloudflare API token.

## Типовые ошибки

- Password сменен, но browser session скрывает ошибку: проверять private session.
- TOTP time drift: синхронизировать часы VPS и телефона.
- Credentials остаются в shell history/compose file.
- Backup Telegram отправляется без учета риска доступа к bot/chat.

## Диагностика

```sh
timedatectl status
x-ui settings
journalctl -u x-ui -n 100 --no-pager
```

Не вставлять вывод `x-ui settings` в публичный issue без редактирования секретов.

## Источники

- [3X-UI README: generated credentials](https://github.com/MHSanaei/3x-ui)
- [3X-UI Wiki installation](https://github.com/MHSanaei/3x-ui/wiki/Installation)
- [x-ui reset actions](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/x-ui.sh)
- [3X-UI API controller](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/web/controller/api.go)
