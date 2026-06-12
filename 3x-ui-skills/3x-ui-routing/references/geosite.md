# Geosite

## Описание

`geosite.dat` содержит категории доменов. Примеры из Wiki: `geosite:cn`, `geosite:google`. Содержимое зависит от выбранного поставщика geofiles и даты обновления.

## Встроенные и дополнительные файлы

3X-UI умеет управлять стандартными и дополнительными geofiles. Wiki перечисляет наборы Loyalsoldier, Iran и Russia. Дополнительный файл получает детерминированное имя `geosite_<alias>.dat` в каталоге Xray.

Ссылка на категорию дополнительного файла:

```text
ext:geosite_myalias.dat:category
```

Alias должен соответствовать `^[a-z0-9_-]+$`. Не создавать aliases, которые нормализуются в одно имя.

## Пошаговая процедура

1. Выбрать доверенный официальный/общеизвестный источник `.dat`.
2. Проверить release/hash и лицензию.
3. В панели добавить geofile URL и уникальный alias.
4. Обновить файл и убедиться, что он появился в Xray bin directory.
5. Проверить наличие нужной категории средствами поставщика файла.
6. Добавить routing rule ниже исключений.
7. Перезапустить Xray и проверить журнал.

## Сценарии

- `geosite:category-ads-all` -> block, если категория есть в текущем файле.
- `geosite:google` -> WARP/proxy.
- локальная категория дополнительного файла -> специальный outbound.

## Ошибки и диагностика

- `failed to load geosite`: файл отсутствует/поврежден или category не существует.
- Список устарел: обновить geofile, затем повторно проверить.
- Domain не совпал: проверить тип записи (`domain:`, `full:`, `regexp:` внутри dataset) и порядок rules.

```sh
find / -name 'geosite*.dat' 2>/dev/null
journalctl -u x-ui -n 200 --no-pager | grep -i geosite
```

## Совместимость

sing-box 1.12 удалил legacy geosite database и rule fields; в 1.13 использовать SRS/remote/inline rule-set. Podkop использует собственные rule-sets: серверный `geosite.dat` автоматически не переносится.

## Источники

- [3X-UI Wiki: Geosites](https://github.com/MHSanaei/3x-ui/wiki/Configuration#geosites)
- [Xray routing domain rules](https://xtls.github.io/en/config/routing.html)
- [sing-box migration from geosite](https://sing-box.sagernet.org/migration/#migrate-geosite-to-rule-sets)
