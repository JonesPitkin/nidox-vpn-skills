# Диагностика Routing

## Безопасный порядок

1. Зафиксировать симптом: domain, client, inbound, TCP/UDP, время.
2. Проверить Xray config/load.
3. Проверить DNS result.
4. Найти первое matching rule.
5. Проверить target outbound напрямую.
6. Проверить geofile/category.
7. Проверить egress IP и приложение.

## Команды

```sh
x-ui status
journalctl -u x-ui -n 300 --no-pager
ss -lntup
getent ahosts <domain>
dig A <domain>
dig AAAA <domain>
curl -4 https://api.ipify.org
curl -6 https://api64.ipify.org
```

## Симптомы

### Xray не запускается

Искать invalid tag, отсутствующий geosite category, malformed DNS object, несовместимое поле bundled core. Откатить последнее одно изменение.

### Все идет direct

Проверить порядок, spelling tags, domain form и `domainStrategy`. Убедиться, что тест идет через нужный inbound.

### Все идет proxy

Искать ранний catch-all. Поднять direct/block exceptions выше.

### Domain rule работает не всегда

Проверить CDN IP, IPv4/IPv6, DNS cache, QUIC/UDP и наличие доменного имени после sniffing. Не полагаться на IP rule для быстро меняющегося CDN.

### Geosite/GeoIP не загружается

Проверить файл, alias, category и permissions каталога Xray. Сверить с logs после restart.

### Podkop ведет себя иначе

Собрать Podkop/sing-box route и DNS отдельно. Правило на VPS видит только трафик, уже отправленный клиентом.

## Временное логирование

Повышать loglevel на короткий интервал и не публиковать логи без очистки UUID, domains и client IP. После теста вернуть обычный уровень.

## UI Version Check

Если требуется точный walkthrough, сверить установленную версию и текущий frontend source: Wiki не фиксирует каждую кнопку routing editor.

## Источники

- [3X-UI Wiki FAQ](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems)
- [3X-UI routing source](https://github.com/MHSanaei/3x-ui/tree/v3.3.0/frontend/src/pages/xray/routing)
- [Xray routing](https://xtls.github.io/en/config/routing.html)
