# TCP/IP: подробный аудит

## Роль раздела

Этот раздел описывает реальный Internet protocol suite. Поведение конкретных транспортных протоколов, MTU и DNS вынесено в отдельные разделы, чтобы не дублировать детали.

## RFC и нормативная база

- RFC 791 - IPv4
- RFC 792 - ICMP for IPv4
- RFC 1122 - Host Requirements
- RFC 1123 - Host Requirements for Internet applications
- RFC 8200 - IPv6
- RFC 9293 - TCP
- RFC 768 - UDP

## Архитектура стека

| Уровень TCP/IP | Назначение | Примеры |
| --- | --- | --- |
| Application | Прикладная логика | DNS, HTTP, SSH |
| Transport | Доставка приложению | TCP, UDP |
| Internet | Межсетевая доставка | IPv4, IPv6, ICMP |
| Link | Локальная доставка | Ethernet, Wi-Fi |

## ASCII-схема инкапсуляции

```text
application payload
  -> TCP/UDP header
    -> IP header
      -> Ethernet/Wi-Fi frame
```

## ASCII-схема пути пакета

```text
client
  -> local switch/ap
  -> router/default gateway
  -> upstream routers
  -> destination server
```

## Linux-команды

```sh
ip addr
ip route
ip route get 1.1.1.1
ping -c 3 1.1.1.1
traceroute 1.1.1.1
ss -lntup
tcpdump -ni any host 1.1.1.1
curl -v https://example.com
dig example.com
```

## OpenWrt-команды

```sh
ubus call network.interface dump
ifstatus wan
ip route show table all
ping -c 3 1.1.1.1
traceroute 1.1.1.1
logread | tail -n 100
tcpdump -ni pppoe-wan
```

## Практические примеры диагностики

### Проверка IP-связности без DNS

```sh
ping -c 3 1.1.1.1
curl -vk --connect-timeout 5 https://1.1.1.1
```

### Проверка выбора маршрута

```sh
ip route get 8.8.8.8
ip -6 route get 2606:4700:4700::1111
```

## Реальные сетевые сценарии

### Сценарий 1. Веб работает по IPv4, но не по IPv6

Это не "поломка TCP/IP вообще", а частичный отказ Internet layer для одного семейства адресов.

### Сценарий 2. VPN поднят, но часть приложений не выходит наружу

Нужно разделять:

- IP-маршрут через туннель;
- DNS-путь;
- TCP/UDP-поведение приложения;
- MTU в туннеле.

## Common Mistakes

- Путать стек TCP/IP с одним TCP.
- Считать IP надежным транспортом.
- Игнорировать различие между адресацией, маршрутизацией и приложением.
- Пытаться диагностировать HTTP, не проверив IP-route и transport.

## Troubleshooting

1. Проверить IP-адреса на интерфейсах.
2. Проверить таблицу маршрутов и route lookup.
3. Проверить reachability до IP без участия DNS.
4. Проверить нужный transport и порт.
5. Проверить прикладной протокол.

## Перекрестные ссылки

- Модель диагностики: [../osi-model/references.md](../osi-model/references.md)
- Транспорт: [../tcp-vs-udp/references.md](../tcp-vs-udp/references.md)
- Адресные семейства: [../ipv4/references.md](../ipv4/references.md), [../ipv6/references.md](../ipv6/references.md)
