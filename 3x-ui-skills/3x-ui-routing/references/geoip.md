# GeoIP

## Описание

`geoip.dat` сопоставляет IP-адреса категориям, например `geoip:cn` и `geoip:private`. Совпадение относится к адресу назначения после доступного routing engine IP resolution.

## Дополнительные файлы

3X-UI сохраняет дополнительный файл как `geoip_<alias>.dat`. Формат rule:

```text
ext:geoip_myalias.dat:category
```

Требования к alias такие же, как для geosite: lowercase `a-z`, цифры, `_`, `-`.

## Пошаговая настройка

1. Уточнить, нужен ли IP-rule или достаточно domain-rule.
2. Выбрать и проверить источник `geoip.dat`.
3. Добавить файл/alias в панели.
4. Проверить download и наличие категории.
5. Добавить rule с `ip`.
6. Выбрать `domainStrategy`, если доменные назначения тоже должны проверяться по IP.
7. Перезапустить и проверить на известных test IP.

## Сценарии

- `geoip:private` -> block для публичного proxy inbound, если private destinations не нужны.
- country IP category -> direct/proxy.
- отдельный corporate prefix в CIDR -> специальный outbound.

## Ошибки

- Динамический/CDN IP не соответствует ожидаемой стране.
- `AsIs` не разрешает домен для IP-rule.
- IPv6 забыта, и часть трафика обходится.
- Private ranges блокируют нужный internal service.

## Диагностика

```sh
getent ahosts example.com
ip route get <resolved-ip>
journalctl -u x-ui -n 200 --no-pager | grep -iE 'geoip|routing|error'
```

Не использовать country GeoIP как точную юридическую или физическую геолокацию.

## Источники

- [3X-UI Wiki: Geosites/GeoIP](https://github.com/MHSanaei/3x-ui/wiki/Configuration#geosites)
- [Xray routing IP rules](https://xtls.github.io/en/config/routing.html)
