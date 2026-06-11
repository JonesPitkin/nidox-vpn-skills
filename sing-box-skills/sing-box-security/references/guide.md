# Security Guide

## TLS

Официальная TLS-модель делит поля на inbound и outbound роли.

Что важно помнить:

- server-side и client-side TLS fields не симметричны;
- `handshake_timeout`, `spoof`, `curve_preferences`, pinning и fragment options зависят от версии.

Замечание по версии:

- официальный `main` уже показывает alpha-поля `1.14.0`;
- stable baseline для этой базы знаний: `1.13.13`;
- если поле видно только в mainline notes `1.14.0`, не считать его обязательным для production.

## Базовый TLS client пример

```json
{
  "tls": {
    "enabled": true,
    "server_name": "example.com",
    "alpn": [
      "h2",
      "http/1.1"
    ],
    "min_version": "1.2",
    "max_version": "1.3"
  }
}
```

## Базовый TLS server пример

```json
{
  "tls": {
    "enabled": true,
    "certificate_path": "/etc/sing-box/cert.pem",
    "key_path": "/etc/sing-box/key.pem"
  }
}
```

## REALITY

Server-side включает:

- `enabled`
- `handshake.server`
- `handshake.server_port`
- `private_key`
- `short_id`
- `max_time_difference`

Client-side включает:

- `enabled`
- `public_key`
- `short_id`

Практика:

- сервер и клиент должны совпадать по public/private key pair semantics;
- `short_id` должен совпадать;
- `server_name` и handshake target не стоит путать между собой.

## ECH

Официальная документация отмечает, что ECH migrated to stdlib path начиная с `1.12.0`, а legacy ECH fields deprecated.

Практический вывод:

- не использовать старые ECH-поля из старых гайдов;
- если конфиг старый, проверять `migration` и `deprecated`.

## Сертификаты

Текущая база знаний должна учитывать:

- inline `certificate` / `key`
- `certificate_path` / `key_path`

Рекомендации:

- в production предпочитать file-based или provider-based хранение;
- пути и права файлов проверять до сетевой диагностики.

## Fingerprint и uTLS

`utls.fingerprint` документирован как client-side возможность, но официальные changelog notes предупреждают:

- у uTLS есть фундаментальные архитектурные ограничения;
- его не следует подавать как надёжное средство обхода серьёзной цензуры.

## Типовые ошибки

- перепутаны inbound и outbound TLS fields;
- REALITY public/private keys поставлены не по ролям;
- `server_name` не совпадает с сертификатом;
- legacy ACME/ECH поля остались после обновления;
- слишком агрессивно включены fragment options без понимания цели.

## Рекомендации по безопасности

- держать минимум TLS 1.2 или выше, если совместимость не требует иного;
- использовать pinning только когда понимается operational impact;
- не включать `insecure` без чёткой причины;
- при миграции проверять официальные `migration` и `deprecated` notes перед обновлением схемы сертификатов.
