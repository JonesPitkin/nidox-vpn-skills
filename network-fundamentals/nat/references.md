# NAT и PAT: подробный аудит

## RFC и нормативная база

- RFC 1918 - private IPv4
- RFC 2663 - NAT terminology
- RFC 3022 - Traditional NAT
- RFC 4787 - NAT behavioral requirements for UDP
- RFC 5382 - NAT behavioral requirements for TCP

## Ключевые формы NAT

| Термин | Что меняется | Типичный кейс |
| --- | --- | --- |
| SNAT | Source address | Выход LAN в Интернет |
| DNAT | Destination address | Публикация внутреннего сервиса |
| PAT/NAPT | Source/destination port + address | Много клиентов за одним IPv4 |

## ASCII-схема PAT

```text
192.168.1.10:51514
  -> router NAT
203.0.113.5:40001
  -> 93.184.216.34:443

reply:
93.184.216.34:443
  -> 203.0.113.5:40001
  -> router translates back
  -> 192.168.1.10:51514
```

## ASCII-схема DNAT

```text
internet client -> 203.0.113.5:443
  -> DNAT on edge router
  -> 192.168.1.20:443
```

## Linux-команды

```sh
ip addr
ip route
ss -lntup
tcpdump -ni any host <public-ip>
nft list ruleset
conntrack -L
```

## OpenWrt-команды

```sh
ifstatus wan
uci show firewall
nft list ruleset
fw4 print
logread | grep -i firewall
tcpdump -ni wan host <remote-ip>
cat /proc/net/nf_conntrack | head
```

## Практические примеры диагностики

### Исходящее соединение работает, входящее нет

Проверять:

1. есть ли DNAT;
2. разрешен ли forward/input firewall;
3. слушает ли сервис нужный адрес/порт;
4. правильный ли путь возврата.

### Hairpin NAT

Клиент из LAN обращается к сервису по публичному адресу. Если reflection не настроен, извне сервис работает, а изнутри по публичному IP - нет.

## Реальные сетевые сценарии

### Сценарий 1. Домашний роутер публикует NAS

Нужны одновременно:

- публичный IPv4;
- DNAT;
- разрешающий firewall;
- сервис, слушающий нужный адрес;
- корректный route back.

### Сценарий 2. Корпоративный outbound через SNAT

Внутренние серверы выходят наружу под общим адресом firewall, и внешняя система видит не реальные хосты, а адрес границы.

## Common Mistakes

- Считать NAT и firewall одним и тем же.
- Забывать про обратный маршрут.
- Путать DNAT публикации и SNAT выхода.
- Искать причину только на сервере, игнорируя границу NAT.

## Troubleshooting

1. Определить, где именно выполняется NAT.
2. Сопоставить private/public address и порт.
3. Проверить правила SNAT/DNAT.
4. Проверить conntrack/state.
5. Проверить маршрут возврата и bind/listen приложения.

## Перекрестные ссылки

- IPv4 и частные диапазоны: [../ipv4/references.md](../ipv4/references.md)
- Провайдерский NAT: [../cgnat/references.md](../cgnat/references.md)
- Порты и сервисы: [../ports/references.md](../ports/references.md)
