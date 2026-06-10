# Порты и сокеты: подробный аудит

## RFC и нормативная база

- RFC 6335 - Service Name and Transport Protocol Port Number Registry
- RFC 6056 - Recommendations for Transport Port Randomization

## Диапазоны портов

| Диапазон | Название | Назначение |
| --- | --- | --- |
| 0-1023 | Well-known | Стандартизованные системные сервисы |
| 1024-49151 | Registered | Прикладные сервисы |
| 49152-65535 | Dynamic/Ephemeral | Временные клиентские порты |

## ASCII-схема сокета

```text
client 192.168.1.10:53124/tcp
  -> server 93.184.216.34:443/tcp
```

## Linux-команды

```sh
ss -lntup
lsof -i
nc -vz <host> <port>
tcpdump -ni any 'port 443'
nft list ruleset
```

## OpenWrt-команды

```sh
ss -lntup
tcpdump -ni br-lan 'port 53 or port 443'
fw4 print
nft list ruleset
logread | tail -n 100
```

## Практические примеры диагностики

### Проверка bind/listen

Если сервис слушает только `127.0.0.1:443`, он недоступен извне, даже если firewall и routing корректны.

### Проверка transport-specific порта

`53/udp` и `53/tcp` - не одно и то же. Нужно явно проверять нужный протокол.

## Реальные сетевые сценарии

### Сценарий 1. DNS отвечает не всегда

Часть запросов проходит по UDP, а большие ответы требуют TCP/53 и ломаются на firewall.

### Сценарий 2. PAT на границе

Эфемерные порты клиента становятся критичны для NAT и conntrack: именно ими различаются одновременные исходящие сессии.

## Common Mistakes

- Проверять только номер порта без указания TCP/UDP.
- Считать "порт открыт" гарантией исправности приложения.
- Игнорировать bind-address.
- Забывать про ephemeral ports клиента и NAT.

## Troubleshooting

1. Проверить, слушает ли процесс нужный IP:port/proto.
2. Проверить reachability к порту с клиента.
3. Проверить firewall/NAT правила.
4. Проверить transport-специфику и packet capture.

## Перекрестные ссылки

- TCP и UDP: [../tcp-vs-udp/references.md](../tcp-vs-udp/references.md)
- NAT и PAT: [../nat/references.md](../nat/references.md)
