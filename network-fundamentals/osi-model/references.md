# OSI: подробный аудит

## Роль раздела

Этот раздел нужен не для описания конкретного интернет-стандарта, а для методического разложения неисправности по слоям. Детали TCP/IP, DNS, MTU, NAT и routing вынесены в профильные разделы.

## RFC и нормативная база

- Прямого RFC для модели OSI нет: это эталонная модель ISO.
- RFC 1122 - Host Requirements и практическая модель уровней в стеке TCP/IP.
- RFC 1123 - дополнительные требования к хостам и прикладным протоколам.

## Соотношение OSI и TCP/IP

| OSI | TCP/IP | Что реально диагностируется |
| --- | --- | --- |
| L7-L5 | Application | DNS, HTTP, TLS, SSH |
| L4 | Transport | TCP, UDP, порты, retransmission |
| L3 | Internet | IPv4, IPv6, routing, ICMP |
| L2-L1 | Link | Ethernet, Wi-Fi, VLAN, carrier |

## ASCII-схема

```text
L7  Application   -> HTTP, DNS, SMTP
L6  Presentation  -> TLS, кодирование данных
L5  Session       -> управление логикой обмена
L4  Transport     -> TCP, UDP, ports
L3  Network       -> IPv4, IPv6, routing
L2  Data Link     -> Ethernet, Wi-Fi, MAC, VLAN
L1  Physical      -> кабель, оптика, радио
```

## Практическая схема диагностики

```text
нет доступа к сервису
  -> есть ли carrier/L1
  -> есть ли соседство и VLAN/L2
  -> есть ли адрес, маршрут и gateway/L3
  -> есть ли TCP/UDP обмен/L4
  -> работает ли DNS/TLS/HTTP/L7
```

## Linux-команды

```sh
ip link
ip addr
bridge link
ip route
ping -c 3 8.8.8.8
traceroute 8.8.8.8
ss -lntup
tcpdump -ni any
curl -I https://example.com
dig example.com
```

## OpenWrt-команды

```sh
ubus call network.interface dump
ifstatus lan
ifstatus wan
ip link show
bridge vlan show
logread | tail -n 100
tcpdump -ni br-lan
nslookup openwrt.org 1.1.1.1
```

## Реальные сценарии

### Сценарий 1. "Wi-Fi есть, сайты не открываются"

- L1/L2: ассоциация есть.
- L3: клиент получил адрес, но нет default route.
- Вывод: проблема уровня L3, а не "сломанный Интернет вообще".

### Сценарий 2. "IP пингуется, имя не резолвится"

- L3 исправен.
- L7 для DNS сломан.
- Вывод: не нужно начинать с кабеля или маршрута.

### Сценарий 3. "Сервис слушает локально, но недоступен извне"

- L4 на хосте может быть исправен.
- Проблема может быть на L3/L4 границе: firewall, NAT, route back.

## Common Mistakes

- Пытаться объяснить любой сбой только одним слоем.
- Считать OSI буквальной картой современного Интернета.
- Делать вывод "сеть исправна" только по `ping`.
- Разбирать DNS раньше проверки IP-адреса и маршрута.

## Troubleshooting

1. Проверить физическое состояние интерфейса и carrier.
2. Проверить L2-смежность: MAC, bridge, VLAN, ARP/NDP.
3. Проверить L3: адрес, prefix, route lookup, gateway.
4. Проверить L4: SYN/SYN-ACK, UDP request/reply, listen socket.
5. Проверить L7 конкретным клиентом: `curl`, `dig`, `openssl s_client`.

## Перекрестные ссылки

- Реальный стек Интернета: [../tcp-ip/references.md](../tcp-ip/references.md)
- Транспорт: [../tcp-vs-udp/references.md](../tcp-vs-udp/references.md)
- Адресация и маршрут: [../ipv4/references.md](../ipv4/references.md), [../ipv6/references.md](../ipv6/references.md), [../routing/references.md](../routing/references.md)
