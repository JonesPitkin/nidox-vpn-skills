# Direct, Proxy и Block

## Модель

- `direct`: Freedom outbound отправляет трафик с VPS напрямую.
- `proxy`: конкретный outbound, например WireGuard/WARP, SOCKS или другой Xray proxy.
- `block`: Blackhole outbound прекращает соединение выбранным способом.

Названия tags произвольны; правила должны ссылаться на реальные tags.

## Настройка direct

1. Создать/проверить Freedom outbound.
2. Назначить уникальный tag, обычно `direct`.
3. При необходимости настроить domainStrategy/redirect согласно Xray docs.
4. Добавить rule для доменов/IP.
5. Проверить внешний IP: он должен быть IP VPS.

## Настройка proxy

1. Создать outbound и отдельно проверить его connectivity.
2. Не добавлять routing rule, пока outbound не работает.
3. Добавить узкое правило.
4. Проверить egress через целевой endpoint.
5. Только затем расширять список.

Wiki приводит WARP route как штатный сценарий 3X-UI.

## Настройка block

1. Создать Blackhole outbound, например `blocked`.
2. Добавить private/BitTorrent/domain rules.
3. Проверить, что нужный legitimate traffic не затронут.
4. Проверить TCP и UDP отдельно.

## Split tunneling

Server-side split tunneling делит трафик уже после подключения клиента к inbound. Client-side split tunneling в sing-box/Podkop решает, какой трафик вообще отправлять на 3X-UI. Эти policies могут дополнять друг друга.

## Ошибки

- Proxy outbound зависит от DNS, который routing отправляет в тот же неработающий outbound.
- Catch-all proxy вызывает неожиданный рост трафика/стоимости.
- Block private отключает доступ к нужному private upstream.
- Direct rule раскрывает VPS IP сервису, хотя ожидался proxy.

## Источники

- [3X-UI README: custom routing/WARP](https://github.com/MHSanaei/3x-ui)
- [Xray Freedom](https://xtls.github.io/en/config/outbounds/freedom.html)
- [Xray Blackhole](https://xtls.github.io/en/config/outbounds/blackhole.html)
- [Podkop sections](https://podkop.net/docs/sections/)
