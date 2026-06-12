# Shadowsocks

## Описание

3X-UI поддерживает Shadowsocks classic AEAD и Shadowsocks 2022. Inbound fields: method, password, `network` (`tcp`, `udp`, `tcp,udp`), clients, `ivCheck`.

## Когда использовать

- простые клиенты и Podkop;
- TCP+UDP с минимальной конфигурацией;
- совместимость с существующим Shadowsocks ecosystem.

## Преимущества

- простые `ss://` links;
- Podkop URL mode поддерживает Shadowsocks;
- UDP доступен;
- SS2022 multi-user model поддержан 3X-UI.

## Недостатки

- plain Shadowsocks легче fingerprint/block;
- method/password format сильно влияет на совместимость;
- SS2022 поддерживается не всеми clients;
- TLS/transport wrapping 3X-UI может не импортироваться обычным SS client.

## Требования

- одинаковый method и корректный key format;
- UDP listener/firewall, если нужен UDP;
- client support выбранного SS2022 method;
- generated share link для multi-user SS2022.

## Настройка в панели

1. Protocol Shadowsocks.
2. Method выбрать по client support.
3. `network=tcp,udp`, если нужен UDP.
4. Password сгенерировать панелью.
5. Для SS2022 учитывать server password и per-client password.
6. Начать с TCP stream/security none.

Golden fixture:

```json
{
  "method": "2022-blake3-aes-256-gcm",
  "password": "<server-key>",
  "network": "tcp,udp",
  "clients": [{"password": "<client-key>", "email": "client"}],
  "ivCheck": false
}
```

3X-UI генерирует ключи нужной длины для SS2022 methods.

## Настройка клиента

Импортировать `ss://`. Для SS2022 multi-user generated credential может объединять server/client material; не собирать URL вручную.

- Podkop: поддержан URL и custom outbound.
- sing-box: имеет native Shadowsocks outbound.
- v2rayNG/Shadowrocket: проверить конкретный method, особенно SS2022.

## Типовые ошибки

- invalid key length/base64;
- classic client не понимает SS2022;
- UDP disabled на server/client/firewall;
- server/client password перепутаны;
- обычный client игнорирует extra Xray transport/TLS.

## Диагностика

Сначала TCP-only. Затем UDP:

```sh
ss -lntup | grep ':<port> '
journalctl -u x-ui -n 150 --no-pager | grep -i shadowsocks
```

Проверить method и generated URL, не редактируя key.

## Источники

- [Shadowsocks schema](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/schemas/protocols/inbound/shadowsocks.ts)
- [SS2022 fixture](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/test/golden/fixtures/inbound-full/shadowsocks-tcp-2022.json)
- [Client key validation](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/web/service/client.go)
- [Podkop sections](https://podkop.net/docs/sections/)
