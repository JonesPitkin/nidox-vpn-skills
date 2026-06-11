# Outbounds Guide

## Служебные outbounds

### direct

Назначение: отправить трафик напрямую.

Плюсы:

- минимальная сложность;
- нужен для bypass и split tunneling.

Минусы:

- не скрывает трафик;
- чувствителен к локальной маршрутизации и DNS-схеме.

### block

Назначение: отвергать трафик.

Подходит для:

- ad/tracker блокировки;
- блокировки нежелательных портов;
- защиты от утечек.

### dns

Назначение: отправка трафика в DNS-модуль.

Подходит для:

- маршрутов, где DNS нужно обрабатывать как отдельный outbound path.

### socks и http

Назначение: использовать upstream proxy.

Типовой случай:

- `sing-box` работает как локальный router, а upstream уже существует.

### selector

Назначение: ручной выбор одного из нескольких outbounds.

Подходит для:

- UI/CLI выбора active node;
- сценариев "proxy-a" или "proxy-b" без автоматического health check.

### urltest

Назначение: авто-выбор лучшего outbound по проверке URL.

Подходит для:

- failover;
- выбор наименьшей задержки;
- группы однотипных прокси.

## Прокси-протоколы

### VLESS

Сильные стороны:

- современный распространённый протокол;
- поддержка `flow: xtls-rprx-vision`;
- сочетается с TLS и V2Ray transports.

Слабые стороны:

- требует точного совпадения transport/TLS параметров;
- ошибки в `flow` или REALITY-полях ломают соединение полностью.

Пример:

```json
{
  "type": "vless",
  "tag": "vless-out",
  "server": "example.com",
  "server_port": 443,
  "uuid": "11111111-1111-1111-1111-111111111111",
  "flow": "xtls-rprx-vision",
  "tls": {
    "enabled": true,
    "server_name": "example.com"
  }
}
```

### VMess

Плюсы:

- широкая совместимость со старым стеком;
- поддержка transport-путей.

Минусы:

- больше legacy-наследия;
- в новых развёртываниях часто уступает VLESS по простоте и ожидаемому future path.

### Trojan

Плюсы:

- понятная TLS-модель;
- часто удобен для reverse proxy/TLS deployment.

Минусы:

- пароль и TLS должны совпадать абсолютно точно;
- при рассинхроне выглядит как generic TLS failure.

### Shadowsocks

Плюсы:

- простота;
- хороший fit для lightweight-сценариев;
- есть AEAD и 2022 methods.

Минусы:

- plugin compatibility надо проверять отдельно;
- `udp_over_tcp` конфликтует с `multiplex`.

### Hysteria2

Плюсы:

- сильный QUIC/UDP-oriented transport;
- поддержка port hopping и realm;
- хорош для сетей, где UDP реально проходит.

Минусы:

- бесполезен там, где UDP режется;
- требует аккуратной TLS и QUIC настройки.

Пример:

```json
{
  "type": "hysteria2",
  "tag": "hy2-out",
  "server": "hy2.example.com",
  "server_port": 8443,
  "password": "strong-password",
  "tls": {
    "enabled": true,
    "server_name": "hy2.example.com"
  }
}
```

### WireGuard

Актуальный путь: `endpoint/wireguard`.

Практический вывод:

- при новых конфигурациях сначала проектировать WireGuard как endpoint;
- старые WireGuard outbound схемы проверять по `deprecated` и `migration`.

Минимальный endpoint-пример:

```json
{
  "type": "wireguard",
  "tag": "wg-ep",
  "address": [
    "10.7.0.2/32"
  ],
  "private_key": "BASE64_PRIVATE_KEY",
  "peers": [
    {
      "address": "203.0.113.10",
      "port": 51820,
      "public_key": "BASE64_PUBLIC_KEY",
      "allowed_ips": [
        "0.0.0.0/0",
        "::/0"
      ]
    }
  ]
}
```

### SSH

Подходит для:

- environments, где SSH допустим как транспорт;
- операционных сценариев с known host key policy.

Минусы:

- не замена массовым high-throughput proxy transport;
- host key verification надо проектировать явно.

## Transport-подсказки

- `ws`, `grpc`, `httpupgrade`, `http` использовать только у протоколов, где это документировано.
- официальная документация отдельно предупреждает о различиях `sing-box` и `v2ray-core` transport semantics.
- `mKCP` и TCP transport как в v2ray-core здесь не являются прямым путём.

## Типовые ошибки

- забыт `domain_resolver` для доменного `server`.
- смешаны `packet_encoding`, `multiplex` и `udp_over_tcp` без проверки конфликтов.
- Hysteria2 поставлен в сеть без UDP.
- VLESS/REALITY fields перепутаны между inbound и outbound ролями.
- WireGuard настроен по старому outbound-пути вместо endpoint-пути.

## Рекомендации

- для группы серверов использовать `selector` или `urltest`;
- для domain-based server addresses задавать resolver осознанно;
- для новых схем избегать deprecated transport и migration-only patterns.
