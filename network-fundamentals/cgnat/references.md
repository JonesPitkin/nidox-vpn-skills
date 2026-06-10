# CGNAT: подробный аудит

## RFC и нормативная база

- RFC 6598 - Shared Address Space `100.64.0.0/10`
- RFC 6888 - Common Requirements for Carrier-Grade NATs

## Как распознать CGNAT

- WAN-адрес роутера не совпадает с внешним IP.
- WAN получает RFC 1918 адрес или `100.64.0.0/10`.
- Port forward на домашнем роутере не дает входящей доступности.

## ASCII-схема

```text
LAN host 192.168.1.10
  -> home NAT
100.64.10.5
  -> ISP CGNAT
198.51.100.25
  -> Internet
```

## Linux-команды

```sh
ip addr
ip route
curl -4 ifconfig.me
traceroute 1.1.1.1
```

## OpenWrt-команды

```sh
ifstatus wan
ip addr show $(ifstatus wan | jsonfilter -e '@.device')
ubus call network.interface.wan status
ping -c 3 1.1.1.1
traceroute 1.1.1.1
```

## Практические примеры диагностики

### Сравнение WAN IP и внешнего IP

```sh
curl -4 ifconfig.me
```

Если внешний IP отличается от WAN на роутере, велика вероятность промежуточного NAT.

### Проверка недоступного port forward

Если сервис внутри LAN слушает, локальный DNAT настроен, но извне недоступен и WAN не публичный - это типичный CGNAT.

## Реальные сетевые сценарии

### Сценарий 1. Домашний VPN-сервер не доступен с мобильной сети

Причина может быть не в WireGuard-конфиге, а в отсутствии собственного публичного IPv4.

### Сценарий 2. Жалобы на репутацию внешнего IP

Под одним IP могут жить десятки или сотни абонентов, поэтому блок-листы и rate limits иногда затрагивают невиновных пользователей.

## Common Mistakes

- Пытаться исправить CGNAT обычным port forward на своем роутере.
- Путать частный WAN-адрес со "статическим публичным".
- Искать причину только в firewall LAN-сервера.

## Troubleshooting

1. Проверить WAN IP.
2. Сравнить его с внешним IP, видимым из Интернета.
3. Уточнить у провайдера наличие CGNAT и услуги публичного IPv4.
4. При необходимости перейти на IPv6, reverse tunnel или VPS.

## Перекрестные ссылки

- Базовый NAT: [../nat/references.md](../nat/references.md)
- IPv6 как альтернатива inbound IPv4: [../ipv6/references.md](../ipv6/references.md)
