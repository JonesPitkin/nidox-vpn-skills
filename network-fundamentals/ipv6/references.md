# IPv6: подробный аудит

## RFC и нормативная база

- RFC 4291 - IPv6 Addressing Architecture
- RFC 4443 - ICMPv6
- RFC 4861 - Neighbor Discovery for IPv6
- RFC 4862 - Stateless Address Autoconfiguration
- RFC 8200 - IPv6
- RFC 8201 - PMTUD for IPv6
- RFC 8504 - IPv6 Node Requirements

## Типы адресов

| Тип | Пример | Назначение |
| --- | --- | --- |
| Global Unicast | `2001:db8::1` | Глобальная маршрутизация |
| Link-local | `fe80::1` | Служебная локальная связность |
| Unique Local | `fd00::/8` style | Локальная маршрутизация |
| Multicast | `ff02::1` | Групповая доставка |

## ASCII-схема

```text
host
  -> receives RA
  -> builds SLAAC address
  -> learns default router via link-local
  -> sends traffic using IPv6 routing
```

## Linux-команды

```sh
ip -6 addr
ip -6 route
ip -6 neigh
ping6 2606:4700:4700::1111
traceroute6 2606:4700:4700::1111
tcpdump -ni any 'icmp6'
```

## OpenWrt-команды

```sh
ifstatus lan
ifstatus wan6
ip -6 addr
ip -6 route
logread | grep -E 'odhcpd|odhcp6c'
tcpdump -ni br-lan 'icmp6'
uci show network
```

## Практические примеры диагностики

### Проверка Router Advertisement и default route

Проверить наличие глобального адреса, link-local next hop и маршрута `::/0`.

### Проверка ICMPv6 `Packet Too Big`

Если часть соединений зависает, нужно искать фильтрацию критичных ICMPv6 сообщений.

## Реальные сетевые сценарии

### Сценарий 1. Dual-stack с broken IPv6

Если клиент предпочитает AAAA и IPv6-path частично сломан, пользователь видит "сайт долго думает", хотя IPv4-path здоров.

### Сценарий 2. Домашний провайдер выдает /56

OpenWrt может раздать разные /64 по VLAN или LAN-сегментам без NAT66.

## Common Mistakes

- Блокировать ICMPv6 как "лишний шум".
- Пытаться мыслить broadcast-моделью IPv4.
- Считать NAT обязательной частью IPv6.
- Игнорировать link-local адреса как служебные и неважные.

## Troubleshooting

1. Проверить наличие GUA/ULA/link-local адресов.
2. Проверить `::/0` и next hop.
3. Проверить NDP и ICMPv6.
4. Проверить MTU/PMTUD.
5. Сравнить IPv4 и IPv6 пути отдельно.

## Перекрестные ссылки

- MTU и PMTUD: [../mtu/references.md](../mtu/references.md)
- Gateway и routing: [../gateway/references.md](../gateway/references.md), [../routing/references.md](../routing/references.md)
