# API и OpenAPI

## 3X-UI v3.3.0

Панель содержит Swagger UI и генерируемую OpenAPI 3 specification:

```text
<panel-base>/panel/api/openapi.json
```

API поддерживает panel session cookie и Bearer API token, созданный в Settings.

## Breaking Change

| До v3.3.0 | v3.3.0+ |
|---|---|
| `/panel/setting/*` | `/panel/api/setting/*` |
| `/panel/xray/*` | `/panel/api/xray/*` |

Inbounds, clients, server, nodes и custom-geo также находятся под `/panel/api`.

## Рабочий процесс

1. Получить фактический panel base path.
2. Открыть API Docs и выгрузить текущий `openapi.json`.
3. Создать API token вместо автоматизации логина, если это подходит задаче.
4. Перед mutation сохранить backup и протестировать отдельный объект.
5. Проверять HTTP status и JSON envelope.

```sh
curl -fsS \
  -H "Authorization: Bearer $XUI_API_TOKEN" \
  "https://panel.example/panel/api/server/status"
```

Не помещать token в shell history, query string или публичный лог.

## Custom Subscription Pages

`v3.3.0` позволяет указать абсолютный каталог с `index.html` или `sub.html`. Каталог должен принадлежать доверенному администратору, не содержать secrets и быть доступен процессу панели только на чтение.

## Источники

- [3X-UI v3.3.0 release](https://github.com/MHSanaei/3x-ui/releases/tag/v3.3.0)
- [3X-UI API controller](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/web/controller/api.go)
- [Wiki API Documentation](https://github.com/MHSanaei/3x-ui/wiki/Configuration#api-documentation)
- [Custom subscription templates](https://github.com/MHSanaei/3x-ui/tree/v3.3.0/sub_templates)
