# TUN

## Описание

TUN inbound создаёт виртуальный интерфейс Xray и принимает IP traffic через системную маршрутизацию. Это локальный системный ingress, а не удалённый proxy listener.

## Когда использовать

- весь трафик VPS/container должен поступать в Xray routing;
- требуется transparent IP routing;
- приложение невозможно настроить на SOCKS/HTTP proxy.

## Преимущества

- принимает traffic приложений без proxy support;
- работает на IP layer;
- позволяет централизовать routing внутри Xray.

## Недостатки

- требует повышенных privileges;
- ошибка routes может отрезать SSH/panel;
- сложнее DNS, IPv6, MTU и loop diagnostics.

## Требования

- Linux TUN support и `/dev/net/tun`;
- root/CAP_NET_ADMIN;
- уникальное имя interface;
- gateway CIDRs, DNS и routes без конфликтов;
- исключение management/endpoint routes;
- Docker device/capabilities или разрешения LXC.

## Настройка в панели

1. Выбрать `TUN`.
2. Задать interface name, например `xray0`.
3. Указать MTU и gateway IPv4/IPv6.
4. Добавить DNS.
5. Настроить `autoSystemRoutingTable` только после исключения SSH, panel и proxy endpoints.
6. Проверить `autoOutboundsInterface`.

## Настройка клиента

Удалённого клиента нет. v2rayNG/Shadowrocket/Podkop/sing-box не импортируют этот inbound как server profile. Они могут иметь собственный локальный TUN mode, но это другая сторона архитектуры.

## Типовые ошибки

- отсутствует `/dev/net/tun`;
- нет CAP_NET_ADMIN;
- default route уводит SSH/panel в Xray;
- routing loop;
- конфликт gateway CIDR;
- MTU/IPv6/DNS настроены частично;
- container interface исчезает после restart.

## Диагностика

```sh
test -c /dev/net/tun
ip link show
ip address show dev xray0
ip rule
ip route show table all
journalctl -u x-ui -n 250 --no-pager | grep -iE 'tun|route|permission|failed|error'
```

Иметь out-of-band console и rollback до изменения default routes.

## Источники

- [3X-UI TUN schema](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/schemas/protocols/inbound/tun.ts)
- [3X-UI TUN form](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/pages/inbounds/form/protocols/tun.tsx)
- [Xray TUN inbound](https://xtls.github.io/en/config/inbounds/tun.html)
