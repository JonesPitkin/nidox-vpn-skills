# DNS: подробный аудит

## RFC и нормативная база

- RFC 1034 - Concepts and Facilities
- RFC 1035 - Implementation and Specification
- RFC 2181 - Clarifications to the DNS Specification
- RFC 2308 - Negative Caching
- RFC 7766 - DNS over TCP requirements

## Базовая схема

```text
application
  -> stub resolver
    -> recursive resolver
      -> root
      -> TLD
      -> authoritative server
    <- answer from cache or iterative lookups
```

## Recursive vs Authoritative

| Роль | Что делает | Типовой пример |
| --- | --- | --- |
| Stub resolver | Формирует запрос от имени приложения | libc/systemd-resolved |
| Recursive resolver | Ищет ответ и кэширует | `1.1.1.1`, resolver провайдера |
| Authoritative server | Хранит данные зоны | NS домена |

## Linux-команды

```sh
dig example.com
dig @1.1.1.1 example.com
dig +trace example.com
dig NS example.com
resolvectl status
tcpdump -ni any 'port 53'
```

## OpenWrt-команды

```sh
nslookup example.com 1.1.1.1
logread | grep -E 'dnsmasq|odhcpd'
uci show dhcp
ubus call network.interface.wan status
tcpdump -ni br-lan 'port 53'
/etc/init.d/dnsmasq status
```

## Практические примеры диагностики

### Проверка resolver против authoritative data

```sh
dig @1.1.1.1 example.com
dig +trace example.com
```

Если публичный resolver отвечает `SERVFAIL`, а цепочка `+trace` ломается выше authoritative уровня, проблема не у клиента.

### Проверка split DNS

Запросить имя через внутренний и внешний resolver и сравнить ответы.

## Реальные сетевые сценарии

### Сценарий 1. Есть доступ по IP, но не по имени

Это типичный DNS-инцидент: resolver timeout, broken forwarder, firewall на `53/udp`, некорректный upstream.

### Сценарий 2. Только часть клиентов получает неправильный IP

Часто причина в кэше конкретного recursive resolver или split-horizon конфигурации.

## Common Mistakes

- Путать recursive resolver и authoritative nameserver.
- Проверять DNS только через браузерный симптом без `dig`.
- Игнорировать TCP/53 fallback для больших ответов.
- Забывать о negative caching.

## Troubleshooting

1. Проверить reachability до resolver по IP.
2. Проверить запрос к конкретному resolver через `@server`.
3. При необходимости выполнить `dig +trace`.
4. Проверить локальный кэш ОС и кэш recursive resolver.
5. Проверить firewall, MTU и TCP/53 fallback при больших ответах.

## Перекрестные ссылки

- Транспорт DNS: [../tcp-vs-udp/references.md](../tcp-vs-udp/references.md)
- Базовая IP-связность: [../tcp-ip/references.md](../tcp-ip/references.md)
