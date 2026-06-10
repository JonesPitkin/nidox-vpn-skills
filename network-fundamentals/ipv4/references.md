# IPv4: подробный аудит

## RFC и нормативная база

- RFC 791 - IPv4
- RFC 919 - Broadcasting Internet Datagrams
- RFC 922 - Broadcasting Internet Datagrams in the Presence of Subnets
- RFC 1519 - CIDR strategy
- RFC 1918 - private addressing
- RFC 4632 - Classless Inter-domain Routing

## Структура адреса

```text
192.168.1.10/24
network   192.168.1.0
host      10
broadcast 192.168.1.255
```

## Частные диапазоны

| Диапазон | Назначение |
| --- | --- |
| 10.0.0.0/8 | Private |
| 172.16.0.0/12 | Private |
| 192.168.0.0/16 | Private |

## ASCII-схема

```text
host 192.168.1.10/24
  -> local 192.168.1.20 direct
  -> remote 8.8.8.8 via gateway 192.168.1.1
```

## Linux-команды

```sh
ip addr
ip route
ipcalc 192.168.1.10/24
arp -an
ping -c 3 192.168.1.1
```

## OpenWrt-команды

```sh
ifstatus lan
ip addr show br-lan
ip route
uci show network
arp -an
```

## Практические примеры диагностики

### Неверная маска сети

Если хост считает удаленный адрес локальным из-за слишком широкого prefix, он будет ARP-запрашивать то, что должно идти через gateway.

### Перекрытие подсетей при VPN

Две площадки используют `192.168.1.0/24`, и route selection становится неоднозначным.

## Реальные сетевые сценарии

### Сценарий 1. Домашняя сеть и NAT

Клиент получает RFC 1918-адрес по DHCP и выходит в Интернет через NAT на edge-router.

### Сценарий 2. Site-to-site VPN двух офисов

Нельзя бездумно выбирать одинаковые private prefixes, иначе маршрутизация между площадками станет конфликтной.

## Common Mistakes

- Думать классовой адресацией вместо CIDR.
- Игнорировать overlap частных сетей.
- Путать broadcast и network address.
- Считать private IPv4 пригодным для прямой публикации в Интернет.

## Troubleshooting

1. Проверить адрес и prefix.
2. Проверить, какой адрес считается локальным, а какой удаленным.
3. Проверить default gateway и ARP.
4. Проверить overlap с VPN и другими сетями.

## Перекрестные ссылки

- NAT: [../nat/references.md](../nat/references.md)
- Gateway и routing: [../gateway/references.md](../gateway/references.md), [../routing/references.md](../routing/references.md)
