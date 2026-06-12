# Xray Routing в 3X-UI

## Описание

Routing Xray выбирает outbound или balancer по полям входящего соединения: domain/IP назначения, port, network, protocol, source, user и inbound tag. Правила применяются сверху вниз; побеждает первое совпадение.

## Когда использовать

- отправлять отдельные сервисы через WARP/VPN/proxy;
- блокировать private ranges или BitTorrent;
- разделять маршруты клиентов/inbounds;
- строить server-side split tunneling;
- выбирать группу outbounds через balancer.

## `domainStrategy`

Актуальный Xray поддерживает стратегии, описанные в официальной документации routing. Практический выбор:

- `AsIs`: сопоставлять исходное доменное имя без дополнительного DNS resolution для IP-rules;
- `IPIfNonMatch`: если domain rules не совпали, разрешить домен и проверить IP-rules;
- `IPOnDemand`: разрешать домен, когда для проверки правила нужен IP.

`IPIfNonMatch`/`IPOnDemand` увеличивают роль DNS и могут изменить задержку и наблюдаемое поведение. Проверять названия в UI текущей версии.

## Пошаговая настройка

1. `Xray Configs -> Routing`.
2. Зафиксировать текущий `domainStrategy`.
3. Создать/проверить требуемые outbounds.
4. Добавить узкие rules: API/panel, DNS, специальные domains/IP.
5. Ниже добавить широкие geosite/geoip и catch-all rules.
6. Сохранить, перезапустить Xray.
7. Проверить каждый маршрут отдельным доменом и ожидаемым egress IP.

Пример логики:

```json
{
  "domainStrategy": "IPIfNonMatch",
  "rules": [
    {
      "type": "field",
      "domain": ["domain:example.com"],
      "outboundTag": "warp"
    },
    {
      "type": "field",
      "ip": ["geoip:private"],
      "outboundTag": "blocked"
    }
  ]
}
```

Это фрагмент модели, не готовый полный config: теги должны существовать локально.

## Проверка

```sh
journalctl -u x-ui -n 200 --no-pager | grep -iE 'routing|outbound|config|error'
curl -4 https://api.ipify.org
```

Для отдельного маршрута запускать запрос через соответствующего тестового клиента, а не с VPS напрямую.

## Типовые ошибки

- Общее правило расположено выше исключения.
- Rule ссылается на удаленный outbound.
- `domainStrategy=AsIs`, но ожидается совпадение только по `geoip`.
- Проверяется DNS address, а не фактический egress.
- Серверные rules ошибочно считают правилами Podkop.

## Источники

- [3X-UI README: routing/outbounds](https://github.com/MHSanaei/3x-ui)
- [3X-UI routing schema](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/schemas/routing.ts)
- [Xray routing](https://xtls.github.io/en/config/routing.html)
