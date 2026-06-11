# OpenWrt Guide

## Установка

Официальная документация package manager отмечает, что install script поддерживает OpenWrt:

```sh
curl -fsSL https://sing-box.app/install.sh | sh
```

Также релизы публикуют OpenWrt packages.

## Официальный procd-конфиг

Из репозитория `release/config/openwrt.conf`:

```uci
config sing-box 'main'
	option enabled '1'
	option conffile '/etc/sing-box/config.json'
	option workdir '/usr/share/sing-box'
	option log_stderr '1'
```

Из `release/config/openwrt.init` следует operational модель:

- `sing-box run -c "$config_file" -D "$working_directory"`
- procd следит за `config.json`
- включён `respawn`
- поднят высокий `nofile` limit

## Практический базовый путь

1. Положить JSON в `/etc/sing-box/config.json`.
2. Убедиться, что rule sets и дополнительные файлы лежат внутри `workdir` или имеют корректные абсолютные пути.
3. Включить сервис через UCI/procd.
4. Проверить, что DNS и routing соответствуют роли роутера.

## DNS на OpenWrt

Практика по официальной модели sing-box:

- `dns.servers` должны отражать реальную topology роутера;
- transparent deployment почти всегда требует, чтобы DNS тоже проходил через `sing-box`-логику;
- для split DNS полезно разделять локальные домены и внешние домены.

## TUN на OpenWrt

Подходит, когда нужен router-side transparent client mode.

Риски:

- слабое железо;
- конфликт с LAN management access;
- неправильные `route_exclude_address`.

## TProxy на OpenWrt

Может быть уместнее TUN, когда:

- нужен точечный transparent interception;
- хочется меньше изменять интерфейсную модель;
- есть готовая firewall-mark схема.

## Производительность

С точки зрения официальных источников по `sing-box`, стоит внимательно смотреть на:

- `mtu`
- выбранный transport
- `auto_redirect`
- количество remote rule sets
- DNS topology

## Cudy WR3000S, Podkop, NekoBox, 3x-ui

Так как этот репозиторий ограничен официальными источниками `sing-box`, здесь допустимо говорить только следующее:

- роутер вроде Cudy WR3000S рассматривается как OpenWrt-host для `sing-box`;
- Podkop и NekoBox можно рассматривать как системы, которые используют или импортируют `sing-box`-совместимые концепции;
- 3x-ui relevant только в той части, где его серверные параметры должны совпасть с официальной схемой `sing-box` transports, TLS и routing.

Все UI-специфические советы для этих продуктов нужно верифицировать отдельно по их собственным официальным источникам.

