# Default Gateway: подробный аудит

## RFC и нормативная база

- RFC 1122 - Host Requirements
- RFC 1812 - Router Requirements
- RFC 4861 - Neighbor Discovery for IPv6

## Базовый принцип

Хост сам не знает все сети мира. Для не-локальных адресов он отправляет пакет на default gateway.

## ASCII-схема

```text
host 192.168.1.10/24
  -> destination 8.8.8.8 not local
  -> send frame to gateway 192.168.1.1 MAC
  -> router forwards further
```

## Отличия терминов

| Термин | Значение |
| --- | --- |
| Default gateway | Шлюз хоста для не-локальных сетей |
| Next hop | Следующий узел в конкретном маршруте |
| Default route | Маршрут `0.0.0.0/0` или `::/0` |

## Linux-команды

```sh
ip addr
ip route
ip route get 8.8.8.8
arp -an
ip neigh
ping -c 3 <gateway-ip>
```

## OpenWrt-команды

```sh
ifstatus lan
ifstatus wan
ip route
ip neigh
ubus call network.interface dump
ping -c 3 <gateway-ip>
```

## Практические примеры диагностики

### Неверный gateway от DHCP

```sh
ip route
ping -c 3 <gateway-ip>
```

Если gateway находится вне подсети хоста, трафик за пределы LAN не выйдет.

### IPv6 default route не получен

Проверить Router Advertisement, `ip -6 route`, `ip -6 neigh`.

## Реальные сетевые сценарии

### Сценарий 1. Домашний клиент видит соседей, но не Интернет

Обычно локальный L2 исправен, а default gateway не получен, неверен или недоступен.

### Сценарий 2. Сервер с двумя интерфейсами

Неправильный default route уводит ответы не тем интерфейсом, и соединение выглядит "плавающим".

## Common Mistakes

- Ставить gateway не из своей подсети IPv4.
- Предполагать, что один working `ping` к соседу проверяет default route.
- Игнорировать отдельную проверку IPv6 default route.

## Troubleshooting

1. Проверить адрес и префикс интерфейса.
2. Проверить default route.
3. Проверить ARP/NDP до gateway.
4. Проверить, что сам gateway имеет путь дальше.
5. Для multi-homed систем проверить policy routing.

## Перекрестные ссылки

- Принятие маршрута: [../routing/references.md](../routing/references.md)
- IPv6 соседство: [../ipv6/references.md](../ipv6/references.md)
