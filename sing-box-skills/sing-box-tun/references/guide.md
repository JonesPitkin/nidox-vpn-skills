# TUN Guide

## Теория

`tun` inbound создаёт виртуальный интерфейс и перехватывает трафик без настройки proxy в приложениях.

Ключевые поля по актуальной документации:

- `interface_name`
- `address`
- `mtu`
- `auto_route`
- `iproute2_table_index`
- `iproute2_rule_index`
- `auto_redirect`
- `auto_redirect_input_mark`
- `auto_redirect_output_mark`
- `auto_redirect_reset_mark`
- `auto_redirect_nfqueue`
- `auto_redirect_iproute2_fallback_rule_index`
- `loopback_address`
- `strict_route`
- `route_address`
- `route_exclude_address`
- `route_address_set`
- `route_exclude_address_set`
- `stack`

Замечание по версии:

- официальный `main` уже показывает некоторые будущие TUN-поля `1.14.0`;
- baseline этого репозитория ориентирован на stable `1.13.13`.

## auto_route

Назначение:

- автоматически добавить маршруты для TUN;
- избавить от ручной настройки значительной части routing table.

Когда полезно:

- desktop client;
- VPS;
- router prototypes.

Риск:

- если локальная сеть, Docker bridge или management subnets не исключены, можно получить loop или потерю доступа.

## auto_redirect

Назначение:

- Linux-level transparent redirect для TUN-схем.

Когда полезно:

- маршрутизатор;
- Linux gateway;
- сложные split/full tunnel схемы.

Важно:

- официальная документация и changelog отдельно отмечают Linux-специфику;
- с `auto_redirect` связаны `bypass` action, fallback iproute2 rule и часть platform caveats.

## mtu

Практика:

- начинать с умеренного значения;
- увеличивать только если понимается path MTU;
- при QUIC, Hysteria2 и туннелях поверх туннелей проблемы MTU проявляются быстро.

## route_address и route_exclude_address

Идея:

- `route_address`: что обязательно пойдёт через TUN;
- `route_exclude_address`: что обязательно исключается.

Типовой split пример:

```json
{
  "type": "tun",
  "tag": "tun-in",
  "address": [
    "172.19.0.1/30"
  ],
  "auto_route": true,
  "route_address": [
    "0.0.0.0/1",
    "128.0.0.0/1"
  ],
  "route_exclude_address": [
    "192.168.0.0/16",
    "10.0.0.0/8"
  ],
  "stack": "system"
}
```

## Linux

Рекомендации:

- сначала проверить, создаётся ли интерфейс;
- затем проверить routes и policy routing;
- затем DNS interception;
- только потом transport-level проблемы.

## OpenWrt

Практический смысл:

- `tun` подходит для client-router сценариев;
- на роутере особенно важны исключения для LAN и management access;
- при нехватке ресурсов `tproxy` или более узкая selective схема может быть лучше.

## VPS

Обычно TUN на VPS нужен для:

- transit/proxy-router;
- привязки трафика сервисов;
- лабораторных transparent setups.

Проверять:

- права;
- ip forwarding;
- конфликты с Docker и другими policy rules.

## Маршрутизаторы

Главные риски:

- routing loop;
- потеря доступа к web/ssh management;
- DNS leak;
- неверный обход локальных сервисов.

## Типовые ошибки

- отсутствуют `address`;
- указаны старые `inet4_*` поля;
- `auto_route` есть, но забыты исключения локальной сети;
- включён `auto_redirect`, но не согласованы firewall marks;
- FakeIP включён, а DNS не заведен в TUN path.

## Рекомендации

- начинать с минимального TUN-конфига;
- добавлять `auto_redirect` только после рабочей базовой маршрутизации;
- на роутерах сначала защитить LAN и management traffic exclusions.
