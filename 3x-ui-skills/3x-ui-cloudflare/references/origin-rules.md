# Origin Rules

## Возможности

Origin Rules могут изменить:

- destination hostname/IP;
- destination port;
- Host header;
- SNI.

Доступность отдельных actions зависит от Cloudflare plan.

## Когда использовать

- public edge port 443, origin service на другом supported/internal port;
- отдельный origin hostname;
- согласование Host/SNI с certificate и reverse proxy vhost.

## Пошаговая настройка

1. Сначала проверить origin напрямую.
2. Создать узкое expression по hostname/path.
3. Изменить только необходимое поле.
4. Убедиться, что origin certificate соответствует SNI после override.
5. Проверить route и Cloudflare events.
6. Документировать исходное/новое значение.

## Ошибки

- Host override ломает WebSocket virtual host.
- SNI override не совпадает с certificate: 525/526.
- Port override ведет на unsupported/закрытый listener.
- Слишком широкое expression затрагивает panel и inbound одновременно.

## Диагностика

Временно отключить rule и сравнить. Проверить origin с теми же Host/SNI:

```sh
curl --resolve <origin-host>:443:<origin-ip> https://<origin-host>/<path> -I
```

## Источники

- [Cloudflare Origin Rules](https://developers.cloudflare.com/rules/origin-rules/)
- [Origin Rules parameters](https://developers.cloudflare.com/rules/origin-rules/features/)

TODO: перед применением проверить доступность требуемого action на текущем Cloudflare plan.
