---
name: network-fundamentals
description: "Фундаментальная база знаний по компьютерным сетям на русском языке: OSI, TCP/IP, TCP и UDP, MTU и MSS, NAT и CGNAT, маршрутизация, шлюз по умолчанию, DNS, IPv4, IPv6 и сетевые порты. Использовать для объяснения сетевых концепций, диагностики связности, разбора маршрутов, проблем DNS, NAT, MTU, публикации сервисов и выбора транспортных протоколов."
---

# network-fundamentals

Этот skill использовать как общий вход в сетевую тематику, когда запрос касается базовой сетевой теории, прикладной диагностики или проектирования связности.

## Как работать с этим skill

1. Определить класс проблемы: теория, диагностика, проектирование, публикация сервиса, деградация производительности.
2. Если проблема не локализована, начать с [osi-model/SKILL.md](./osi-model/SKILL.md).
3. Если нужна реальная стековая модель Интернета, перейти к [tcp-ip/SKILL.md](./tcp-ip/SKILL.md).
4. Для адресации и связности использовать разделы IPv4, IPv6, routing и gateway.
5. Для проблем приложений проверять DNS, TCP/UDP, порты, NAT/CGNAT и MTU.

## Быстрая навигация

- [README.md](./README.md) - обзор навыка, карта тем и порядок изучения
- [osi-model/SKILL.md](./osi-model/SKILL.md) - разложение проблем по слоям
- [tcp-ip/SKILL.md](./tcp-ip/SKILL.md) - практический стек Интернета
- [tcp-vs-udp/SKILL.md](./tcp-vs-udp/SKILL.md) - выбор транспорта
- [mtu/SKILL.md](./mtu/SKILL.md) - MTU, MSS, PMTUD
- [nat/SKILL.md](./nat/SKILL.md) - трансляция адресов и портов
- [cgnat/SKILL.md](./cgnat/SKILL.md) - операторский NAT
- [routing/SKILL.md](./routing/SKILL.md) - выбор пути и маршруты
- [gateway/SKILL.md](./gateway/SKILL.md) - шлюз по умолчанию
- [dns/SKILL.md](./dns/SKILL.md) - разрешение имен
- [ipv4/SKILL.md](./ipv4/SKILL.md) - адресация IPv4
- [ipv6/SKILL.md](./ipv6/SKILL.md) - адресация IPv6
- [ports/SKILL.md](./ports/SKILL.md) - транспортные порты
- [references/sources.md](./references/sources.md) - канонические источники

## Рабочий диагностический порядок

```text
link
  -> L2 adjacency
    -> IP address/prefix
      -> route/default gateway
        -> DNS
          -> TCP/UDP and port
            -> NAT/CGNAT
              -> MTU/MSS/PMTUD
                -> application behavior
```

## Правила качества

- Предпочитать объяснение от простого к техническому, не теряя смысла.
- При нормативных формулировках опираться на RFC.
- При практических примерах явно указывать протокол, адресное семейство, порт и направление трафика.
- Не считать рабочий `ping` доказательством исправности DNS, TCP, TLS или приложения.
