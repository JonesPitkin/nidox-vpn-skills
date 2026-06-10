# Routing: подробный аудит

## RFC и нормативная база

- RFC 791 - IPv4 forwarding context
- RFC 1812 - Requirements for IP Version 4 Routers
- RFC 8200 - IPv6 forwarding context
- RFC 2328 - OSPFv2
- RFC 4271 - BGP-4

## Как принимается решение

```text
packet arrives
  -> inspect destination IP
  -> longest prefix match
  -> choose next hop or connected interface
  -> decrement TTL/Hop Limit
  -> forward
```

## Статическая и динамическая маршрутизация

| Тип | Плюсы | Минусы | Где использовать |
| --- | --- | --- | --- |
| Static | Простота, предсказуемость | Нет автоадаптации | Дом, small office, stub network |
| Dynamic | Сходимость, масштабирование | Сложность | Enterprise, ISP, multiple paths |

## ASCII-схема

```text
host A
  -> router R1
    -> router R2
      -> remote subnet
```

## Linux-команды

```sh
ip route
ip -6 route
ip route get 8.8.8.8
ip rule
traceroute 8.8.8.8
tracepath 1.1.1.1
```

## OpenWrt-команды

```sh
ip route show table all
ip -6 route show table all
uci show network
ifstatus wan
traceroute 8.8.8.8
logread | grep -i netifd
```

## Практические примеры диагностики

### Проверка longest prefix match

```sh
ip route get 10.20.30.40
```

Команда покажет, какой маршрут и какой `via` реально выбраны ядром.

### Проверка asymmetry

Снять `tcpdump` на обоих uplink и посмотреть, не уходит ли запрос через один интерфейс, а ответ через другой.

## Реальные сетевые сценарии

### Сценарий 1. Site-to-site VPN к филиалу

Нужен статический маршрут в удаленный префикс через tunnel interface или peer address.

### Сценарий 2. Два провайдера на edge-router

Без policy routing или корректных metric часть трафика может возвращаться не тем WAN и ломать stateful firewall/NAT.

## Common Mistakes

- Смотреть только наличие маршрута, а не конкретный route lookup.
- Игнорировать более специфичные префиксы.
- Забывать про маршрут возврата.
- Путать default route и route-policy.

## Troubleshooting

1. Проверить таблицу маршрутов.
2. Выполнить `ip route get` для конкретной цели.
3. Проверить next hop и доступность соседнего роутера.
4. Проверить возвратный маршрут.
5. При multi-WAN проверить policy routing и асимметрию.

## Перекрестные ссылки

- Шлюз по умолчанию: [../gateway/references.md](../gateway/references.md)
- IPv4/IPv6 адресация: [../ipv4/references.md](../ipv4/references.md), [../ipv6/references.md](../ipv6/references.md)
