# MTU, MSS и PMTUD: подробный аудит

## RFC и нормативная база

- RFC 879 - TCP MSS
- RFC 1191 - Path MTU Discovery for IPv4
- RFC 4821 - Packetization Layer Path MTU Discovery
- RFC 8201 - Path MTU Discovery for IPv6

## Базовая логика

| Термин | Смысл |
| --- | --- |
| MTU | Максимальный размер IP-пакета на интерфейсе/канале |
| MSS | Максимальный размер полезной нагрузки TCP |
| PMTU | Наименьший MTU по пути |
| PMTUD | Механизм обнаружения PMTU |

## ASCII-схема

```text
host A MTU 1500
  -> router
  -> tunnel segment effective MTU 1420
  -> router sends ICMP too big / fragmentation needed
  -> host reduces packet size or MSS
```

## Практические вычисления

```text
Ethernet MTU 1500
IPv4 + TCP: MSS 1460
IPv6 + TCP: MSS 1440
```

## Linux-команды

```sh
ip link show
tracepath 1.1.1.1
tracepath6 2606:4700:4700::1111
ping -M do -s 1472 1.1.1.1
ping6 -s 1440 2606:4700:4700::1111
tcpdump -ni any 'icmp or icmp6'
```

## OpenWrt-команды

```sh
ip link show
ifstatus wan
tracepath 1.1.1.1
ping -M do -s 1472 1.1.1.1
tcpdump -ni wan 'icmp or icmp6'
uci show network | grep mtu
logread | tail -n 100
```

## Практические примеры диагностики

### Проверка black hole MTU

```sh
ping -M do -s 1472 8.8.8.8
ping -M do -s 1400 8.8.8.8
```

Если большой пакет не проходит, а меньший проходит, по пути есть более узкий MTU или сломан PMTUD.

### Проверка TCP MSS косвенно

Снять `tcpdump` на SYN и посмотреть negotiated MSS.

## Реальные сетевые сценарии

### Сценарий 1. PPPoE + VPN

Наружный канал уже уменьшает доступный payload, а поверх него добавляется overhead туннеля. Без корректного MTU/MSS часть сайтов зависает на TLS или загрузке крупных объектов.

### Сценарий 2. IPv6 работает хуже IPv4

Часто причина не в "плохом IPv6", а в фильтрации ICMPv6 `Packet Too Big`.

## Common Mistakes

- Полностью блокировать ICMP/ICMPv6.
- Путать MTU и MSS.
- Изменять MTU на клиенте, не проверив bottleneck по пути.
- Игнорировать overhead PPPoE, GRE, VXLAN, WireGuard, OpenVPN, IPsec.

## Troubleshooting

1. Проверить MTU интерфейсов.
2. Проверить реальный PMTU через `tracepath`.
3. Проверить ICMP/ICMPv6 сообщения `too big`.
4. Сравнить поведение малых и больших пакетов.
5. Для TCP оценить negotiated MSS и возможный MSS clamp.

## Перекрестные ссылки

- Транспорт и MSS: [../tcp-vs-udp/references.md](../tcp-vs-udp/references.md)
- IPv6 и ICMPv6: [../ipv6/references.md](../ipv6/references.md)
