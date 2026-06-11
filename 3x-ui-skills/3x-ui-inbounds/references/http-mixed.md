# HTTP и SOCKS/Mixed

## Описание

3X-UI предоставляет:

- `HTTP` — forward HTTP proxy с accounts и `allowTransparent`;
- `Mixed` — единый listener для SOCKS и HTTP, с password/noauth и optional UDP.

Это access inbounds, а не маскирующие публичные proxy-протоколы.

## Когда использовать

- локальный proxy на `127.0.0.1` или защищённой LAN;
- upstream для приложения/reverse SSH tunnel;
- controlled access внутри private network;
- Mixed как SOCKS5/HTTP endpoint для Podkop или другого router.

Не публиковать `noauth` listener в интернет.

## Преимущества

- поддерживаются обычными приложениями без Xray profile;
- удобны как local/LAN access proxy;
- Mixed объединяет HTTP и SOCKS на одном listener.

## Недостатки

- сами по себе не дают современную transport masking;
- public exposure создаёт open-proxy risk;
- обычный HTTP proxy не шифрует proxy handshake.

## Требования

- bind на loopback/private address;
- firewall allowlist;
- сильные username/password;
- для Mixed UDP указать корректный reachable `ip`;
- отдельный TLS/VPN layer, если трафик проходит недоверенную сеть.

## Настройка в панели

HTTP:

1. Выбрать `HTTP`.
2. Добавить account.
3. `allowTransparent` включать только для специально построенной transparent-схемы.

Mixed:

1. Выбрать `Mixed`.
2. Оставить auth `password`.
3. Добавить account.
4. Включить UDP только при необходимости и указать UDP IP.

## Настройка клиента

- sing-box поддерживает HTTP и SOCKS outbounds;
- Shadowrocket поддерживает HTTP/SOCKS proxy;
- v2rayNG может работать с локальными/custom configs, но 3X-UI не выдаёт для этих inbounds обычную tracked-client subscription;
- Podkop Proxy section официально поддерживает SOCKS4/5, поэтому использовать SOCKS side Mixed и проверять auth/UDP.

## Типовые ошибки

- listener открыт на `0.0.0.0` без firewall;
- `noauth` доступен извне;
- HTTP proxy принимают за HTTPS tunnel;
- Mixed UDP IP недоступен клиенту;
- приложение использует HTTP credentials как SOCKS credentials неверного формата.

## Диагностика

```sh
curl -x http://USER:PASS@127.0.0.1:PORT https://ifconfig.me
curl --socks5-hostname USER:PASS@127.0.0.1:PORT https://ifconfig.me
ss -lntup
```

## Источники

- [3X-UI HTTP schema](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/schemas/protocols/inbound/http.ts)
- [3X-UI Mixed schema](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/schemas/protocols/inbound/mixed.ts)
- [Xray HTTP inbound](https://xtls.github.io/en/config/inbounds/http.html)
- [Xray SOCKS inbound](https://xtls.github.io/en/config/inbounds/socks.html)
- [Podkop sections](https://podkop.net/docs/sections/)
