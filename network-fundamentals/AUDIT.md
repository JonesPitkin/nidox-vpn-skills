# AUDIT

## Цель аудита

Проведен полный аудит skill-пакета `network-fundamentals` с акцентом на:

- полноту RFC;
- практическую диагностику;
- Linux и OpenWrt команды;
- ASCII-схемы;
- реальные эксплуатационные сценарии;
- унификацию терминологии;
- устранение лишнего дублирования между разделами.

## Внесенные улучшения по всему пакету

### 1. Добавлены недостающие RFC

Расширен нормативный слой по разделам:

- `osi-model`: RFC 1122, RFC 1123 как реальная стековая опора TCP/IP рядом с OSI.
- `tcp-ip`: RFC 792, RFC 1122, RFC 1123.
- `tcp-vs-udp`: RFC 8085.
- `mtu`: RFC 4821.
- `nat`: RFC 2663, RFC 4787, RFC 5382.
- `cgnat`: RFC 6598.
- `routing`: RFC 1812, RFC 2328, RFC 4271.
- `gateway`: RFC 4861 в контексте IPv6 next hop.
- `dns`: RFC 2181, RFC 2308, RFC 7766.
- `ipv4`: RFC 919, RFC 922, RFC 1519, RFC 4632.
- `ipv6`: RFC 4291, RFC 4861, RFC 4862, RFC 8504.
- `ports`: RFC 6056.

### 2. Добавлены практические примеры диагностики

Во все `references.md` добавлены отдельные секции с реальными диагностическими паттернами:

- route lookup через `ip route get`;
- DNS-проверки через `dig @server` и `dig +trace`;
- black hole MTU через `ping -M do` и `tracepath`;
- TCP handshake и UDP-request/response через `tcpdump`;
- NAT/DNAT/PAT и CGNAT-разбор;
- IPv6 RA/NDP/ICMPv6-проверки.

### 3. Добавлены Linux-команды

Во все тематические `references.md` добавлены целевые Linux-команды:

- `ip`, `ss`, `bridge`, `tcpdump`, `curl`, `dig`, `tracepath`, `traceroute`, `ip neigh`, `arp`, `nft`, `conntrack`.

### 4. Добавлены OpenWrt-команды

Во все разделы добавлены практические команды OpenWrt:

- `ubus call network.interface dump`
- `ifstatus`
- `uci show network`
- `uci show firewall`
- `fw4 print`
- `logread`
- `nslookup`
- `tcpdump`

### 5. Добавлены ASCII-схемы

В каждом разделе теперь есть текстовые схемы:

- уровни OSI;
- инкапсуляция TCP/IP;
- TCP handshake и UDP datagram flow;
- PMTUD и path bottleneck;
- NAT/PAT/DNAT;
- CGNAT-цепочка;
- routing и gateway flow;
- DNS resolution path;
- IPv4 local/remote decision;
- IPv6 RA/SLAAC/NDP;
- socket tuple и роль портов.

### 6. Добавлены реальные сетевые сценарии

Во все разделы добавлены практические эксплуатационные кейсы:

- broken default route;
- dual-stack с частично сломанным IPv6;
- site-to-site VPN с overlap префиксов;
- домашний сервис за NAT/CGNAT;
- split DNS;
- PPPoE + tunnel MTU overhead;
- multi-WAN asymmetry.

### 7. Снижено дублирование между разделами

Пакет был переработан так, чтобы каждый раздел держал только свою основную область:

- `osi-model` оставлен как диагностическая метамодель;
- `tcp-ip` описывает только реальный Internet suite без повторного подробного разбора DNS/NAT/MTU;
- `tcp-vs-udp` оставлен про поведение транспорта, а не про порты вообще;
- `routing` и `gateway` разведены: первый про выбор пути роутером, второй про поведение хоста;
- `nat` и `cgnat` разведены: первый про трансляцию вообще, второй про операторскую модель;
- `ipv4` и `ipv6` очищены от лишнего повторения transport/DNS-логики.

Вместо повторов добавлены перекрестные ссылки между разделами.

### 8. Проверена и выровнена терминология

Уточнены или нормализованы термины:

- `PAT/NAPT` как частный случай NAT, а не синоним NAT "вообще";
- `default gateway` против `default route` и `next hop`;
- `recursive resolver` против `authoritative DNS`;
- `MTU` против `MSS`;
- `link-local`, `SLAAC`, `NDP`, `ICMPv6`;
- `well-known`, `registered`, `dynamic/ephemeral ports`.

### 9. Добавлены обязательные секции `Common Mistakes`

Во все `references.md` добавлены отдельные разделы `Common Mistakes`.

### 10. Добавлены обязательные секции `Troubleshooting`

Во все `references.md` добавлены пошаговые разделы `Troubleshooting`.

### 11. Исправлен реестр источников

В [references/sources.md](./references/sources.md):

- удалена некорректная Cloudflare-ссылка для NAT;
- расширен список RFC в соответствии с аудитом разделов;
- добавлен отдельный блок по маршрутизации.

## Измененные файлы

- [references/sources.md](/Users/evgeniishumilkin/Documents/Скилы/network-fundamentals/references/sources.md)
- [osi-model/references.md](/Users/evgeniishumilkin/Documents/Скилы/network-fundamentals/osi-model/references.md)
- [tcp-ip/references.md](/Users/evgeniishumilkin/Documents/Скилы/network-fundamentals/tcp-ip/references.md)
- [tcp-vs-udp/references.md](/Users/evgeniishumilkin/Documents/Скилы/network-fundamentals/tcp-vs-udp/references.md)
- [mtu/references.md](/Users/evgeniishumilkin/Documents/Скилы/network-fundamentals/mtu/references.md)
- [nat/references.md](/Users/evgeniishumilkin/Documents/Скилы/network-fundamentals/nat/references.md)
- [cgnat/references.md](/Users/evgeniishumilkin/Documents/Скилы/network-fundamentals/cgnat/references.md)
- [routing/references.md](/Users/evgeniishumilkin/Documents/Скилы/network-fundamentals/routing/references.md)
- [gateway/references.md](/Users/evgeniishumilkin/Documents/Скилы/network-fundamentals/gateway/references.md)
- [dns/references.md](/Users/evgeniishumilkin/Documents/Скилы/network-fundamentals/dns/references.md)
- [ipv4/references.md](/Users/evgeniishumilkin/Documents/Скилы/network-fundamentals/ipv4/references.md)
- [ipv6/references.md](/Users/evgeniishumilkin/Documents/Скилы/network-fundamentals/ipv6/references.md)
- [ports/references.md](/Users/evgeniishumilkin/Documents/Скилы/network-fundamentals/ports/references.md)

## Результат

После аудита `network-fundamentals` стал заметно ближе к эксплуатационной базе знаний:

- меньше теоретических повторов;
- больше практики Linux/OpenWrt;
- больше нормативной RFC-опоры;
- явная структура ошибок и диагностики для каждого раздела.
