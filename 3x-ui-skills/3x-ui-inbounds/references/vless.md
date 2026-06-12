# VLESS

## Описание

VLESS — основной lightweight protocol Xray без встроенного шифрования payload. Защиту предоставляет TLS или REALITY. В 3X-UI client идентифицируется UUID; основные inbound fields: `clients`, `decryption`, `encryption`, `fallbacks`.

## Когда использовать

- базовый выбор для новых Xray deployments;
- REALITY/Vision direct endpoint;
- TLS transport через reverse proxy/CDN;
- подписки для Xray-based клиентов;
- Podkop через VLESS URL или sing-box outbound.

## Преимущества

- поддерживает REALITY и Vision;
- широкий выбор transports;
- UUID clients, quotas, expiry, IP limits и subscriptions в панели;
- актуальный 3X-UI генерирует VLESS share links и JSON/Clash subscriptions.

## Недостатки

- без TLS/REALITY не обеспечивает confidentiality;
- новые encryption/XHTTP/ML-KEM/ML-DSA fields могут не поддерживаться старыми клиентами;
- неправильный flow/security вызывает handshake failure.

## Требования

- уникальный UUID;
- совпадающие address/port/security/transport;
- для Vision: TCP + TLS/REALITY;
- для REALITY: public key, SNI, short ID, fingerprint;
- открытый inbound port или корректный reverse proxy.

## Настройка в панели

`Inbounds -> Add Inbound`:

1. Protocol: `VLESS`.
2. Listen: пусто для всех interfaces или конкретный address.
3. Port: свободный.
4. Client: UUID, email, optional flow, quota, expiry, IP limit.
5. `decryption`: `none`.
6. `encryption`: сохранять `none`, если не используется явно сгенерированный panel VLESS encryption profile.
7. Transport/security выбрать по отдельным references.
8. Сохранить и restart Xray.

Golden fixture baseline:

```json
{
  "protocol": "vless",
  "settings": {
    "clients": [{
      "id": "<uuid>",
      "email": "client@example",
      "flow": ""
    }],
    "decryption": "none",
    "encryption": "none",
    "fallbacks": []
  }
}
```

## Настройка клиента

Предпочитать QR/share link/subscription 3X-UI. Проверить query:

- `type`: `tcp`, `ws`, `grpc`, `httpupgrade`, `xhttp`;
- `security`: `none`, `tls`, `reality`;
- `flow=xtls-rprx-vision` только для TCP;
- `sni`, `fp`, `pbk`, `sid`, `spx` для REALITY;
- transport-specific fields.

sing-box outbound baseline:

```json
{
  "type": "vless",
  "tag": "vless-out",
  "server": "<host>",
  "server_port": 443,
  "uuid": "<uuid>",
  "flow": "xtls-rprx-vision",
  "network": "tcp",
  "tls": {}
}
```

## Клиенты

- v2rayNG: предпочтителен актуальный Xray core; импортировать VLESS URL.
- Shadowrocket: импортировать URL/QR и сверять flow, REALITY и XHTTP fields.
- sing-box: VLESS/Vision подтверждены официальной документацией; transports ограничены его schema.
- Podkop: VLESS URL поддержан; при parser failure использовать custom sing-box outbound.

## Типовые ошибки

- `invalid UUID`: поврежден UUID.
- подключение есть, трафика нет: routing/DNS/UDP или client disabled/quota.
- `flow` потерян при импорте: клиент не поддерживает Vision или link parser устарел.
- VLESS plain TCP заблокирован: добавить TLS/REALITY, а не случайные headers.

## Диагностика

```sh
ss -lntp | grep ':<port> '
journalctl -u x-ui -n 200 --no-pager | grep -iE 'vless|inbound|failed|error'
```

Создать test client без quota/expiry/IP limit. Сначала проверить TCP+REALITY+Vision, затем усложнять transport.

## Источники

- [3X-UI VLESS schema](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/schemas/protocols/inbound/vless.ts)
- [3X-UI VLESS REALITY fixture](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/test/golden/fixtures/inbound-full/vless-tcp-reality.json)
- [3X-UI link generator](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/sub/subService.go)
- [sing-box VLESS](https://sing-box.sagernet.org/configuration/outbound/vless/)
