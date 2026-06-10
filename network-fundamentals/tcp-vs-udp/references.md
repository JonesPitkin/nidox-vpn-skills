# TCP и UDP: подробный аудит

## RFC и нормативная база

- RFC 768 - UDP
- RFC 8085 - UDP Usage Guidelines
- RFC 9293 - TCP

## Сравнение

| Свойство | TCP | UDP |
| --- | --- | --- |
| Тип | Connection-oriented | Connectionless |
| Гарантия порядка | Да | Нет |
| Повтор потерянных данных | Да | Нет |
| Контроль перегрузки | Встроен | На уровне приложения или отсутствует |
| Типичное использование | HTTPS, SSH, SMTP | DNS, VoIP, telemetry, media |

## ASCII-схема TCP

```text
client SYN
  -> server SYN-ACK
    -> client ACK
      -> data
        -> ACK/retransmission/window control
```

## ASCII-схема UDP

```text
client datagram
  -> network
    -> server datagram receive or loss
```

## Linux-команды

```sh
ss -tn
ss -un
tcpdump -ni any 'tcp port 443'
tcpdump -ni any 'udp port 53'
nc -vz example.com 443
dig @1.1.1.1 example.com
```

## OpenWrt-команды

```sh
ss -tn
ss -un
tcpdump -ni br-lan 'tcp port 443'
tcpdump -ni wan 'udp port 53'
nslookup example.com 1.1.1.1
logread | tail -n 100
```

## Практические примеры диагностики

### TCP: SYN уходит, SYN-ACK не приходит

```sh
tcpdump -ni any 'tcp[tcpflags] & (tcp-syn|tcp-ack) != 0 and host <server-ip>'
```

Возможные причины:

- firewall;
- неверный DNAT;
- маршрут возврата;
- сервис не слушает.

### UDP: запрос ушел, ответа нет

```sh
tcpdump -ni any 'udp and host <server-ip>'
dig @<server-ip> example.com
```

Возможные причины:

- packet loss;
- фрагментация;
- ACL/firewall;
- приложение не отвечает.

## Реальные сетевые сценарии

### Сценарий 1. DNS работает нестабильно только по UDP

Маленькие ответы проходят, большие режутся из-за MTU/firewall, а TCP fallback спасает часть запросов.

### Сценарий 2. Голос в звонке рвется, хотя HTTPS работает

UDP-медиатрафик чувствителен к jitter и loss, а TCP-веб-трафик компенсирует потери повторами.

## Common Mistakes

- Называть UDP "сломанным TCP без handshake".
- Считать, что отсутствие handshake означает отсутствие портов и состояния в приложении.
- Ожидать от UDP встроенной надежности.
- Оценивать real-time трафик только по throughput.

## Troubleshooting

1. Уточнить, какой transport использует сервис.
2. Проверить listen socket или факт генерации датаграмм.
3. Снять capture и увидеть направление обмена.
4. Для TCP искать handshake/retransmission/reset.
5. Для UDP искать потерю, ACL, MTU и логи приложения.

## Перекрестные ссылки

- Порты и сокеты: [../ports/references.md](../ports/references.md)
- Размер пакета и PMTUD: [../mtu/references.md](../mtu/references.md)
