# network-fundamentals

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status: Ready for Publication](https://img.shields.io/badge/status-ready%20for%20publication-2ea44f)

`network-fundamentals` — фундаментальный сетевой skill и справочник для Codex на русском языке. Пакет предназначен для объяснения базовых сетевых концепций, диагностики реальных проблем в Linux и OpenWrt, а также для использования как долговременная база знаний по адресации, маршрутизации, транспорту и сетевой эксплуатации.

## Project Overview

Этот skill покрывает:

- модель OSI и практическое разложение проблем по слоям;
- реальный стек TCP/IP;
- TCP, UDP и различия между ними;
- MTU, MSS, PMTUD и проблемы фрагментации;
- NAT, PAT и CGNAT;
- маршрутизацию и шлюз по умолчанию;
- DNS, recursive resolver и authoritative DNS;
- IPv4, IPv6 и сетевые порты.

## Repository Map

| Раздел | Назначение |
| --- | --- |
| [SKILL.md](./SKILL.md) | Корневой entrypoint skill для Codex |
| [README.md](./README.md) | Обзор проекта, структура и источники |
| [AUDIT.md](./AUDIT.md) | История внесенных улучшений после аудита |
| [QUALITY_REPORT.md](./QUALITY_REPORT.md) | Финальная оценка качества разделов |
| [references/sources.md](./references/sources.md) | Канонический список источников и RFC |
| [osi-model/](./osi-model/) | Диагностика и объяснение по модели OSI |
| [tcp-ip/](./tcp-ip/) | Практический Internet protocol suite |
| [tcp-vs-udp/](./tcp-vs-udp/) | TCP, UDP и транспортное поведение |
| [mtu/](./mtu/) | MTU, MSS, PMTUD |
| [nat/](./nat/) | NAT, PAT, SNAT, DNAT |
| [cgnat/](./cgnat/) | Carrier-Grade NAT |
| [routing/](./routing/) | Статическая и динамическая маршрутизация |
| [gateway/](./gateway/) | Шлюз по умолчанию и next hop |
| [dns/](./dns/) | DNS и серверные роли |
| [ipv4/](./ipv4/) | Адресация IPv4 |
| [ipv6/](./ipv6/) | Адресация IPv6 |
| [ports/](./ports/) | Сетевые порты и сокеты |

## Recommended Reading Order

1. [osi-model](./osi-model/SKILL.md)
2. [tcp-ip](./tcp-ip/SKILL.md)
3. [ipv4](./ipv4/SKILL.md)
4. [ipv6](./ipv6/SKILL.md)
5. [routing](./routing/SKILL.md)
6. [gateway](./gateway/SKILL.md)
7. [tcp-vs-udp](./tcp-vs-udp/SKILL.md)
8. [ports](./ports/SKILL.md)
9. [dns](./dns/SKILL.md)
10. [nat](./nat/SKILL.md)
11. [cgnat](./cgnat/SKILL.md)
12. [mtu](./mtu/SKILL.md)

## Topic Map

```text
OSI
  -> задает диагностическую модель
  -> ведет к TCP/IP как к реальной реализации

TCP/IP
  -> использует IPv4 и IPv6
  -> использует TCP и UDP

IPv4
  -> тесно связан с NAT и дефицитом адресов

IPv6
  -> опирается на ICMPv6, NDP, SLAAC и PMTUD

Routing + Gateway
  -> определяют выбор пути и выход за пределы локальной подсети

DNS
  -> зависит от IP-связности, маршрута и транспорта

Ports + TCP/UDP
  -> определяют доставку данных приложению

MTU/MSS
  -> влияют на стабильность передачи и туннели
```

## Sources

Основные авторитетные источники:

- Cloudflare Learning Center
- Cisco Networking Academy
- OpenWrt Networking Docs
- MDN Networking
- RFC Editor

Полный список ссылок и RFC: [references/sources.md](./references/sources.md)

## Quality Report

Финальный аудит качества и оценки разделов доступны в [QUALITY_REPORT.md](./QUALITY_REPORT.md).

Ключевые результаты:

- структура пакета целостна;
- все тематические разделы содержат `SKILL.md`, `references.md`, `glossary.md`, `examples.md`;
- во всех `references.md` есть `Common Mistakes` и `Troubleshooting`;
- RFC привязаны к темам корректно;
- команды Linux/OpenWrt и диагностические сценарии приведены к единому operational-формату.

## Audit History

История углубленного аудита и список внесенных улучшений зафиксированы в [AUDIT.md](./AUDIT.md).

## License

Проект лицензирован по лицензии MIT. Материалы можно свободно использовать, изменять и распространять в соответствии с условиями лицензии MIT.

Полный текст лицензии: [LICENSE](./LICENSE)
