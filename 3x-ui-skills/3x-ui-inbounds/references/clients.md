# Совместимость клиентов

Проверять точную версию приложения и core. “Поддерживается” означает наличие protocol/transport в upstream, но не гарантирует корректный импорт каждой 3X-UI share link.

## Матрица proxy-схем

| Схема | sing-box | v2rayNG | Shadowrocket | Podkop |
|---|---|---|---|---|
| VLESS TCP REALITY Vision | Да | Да, Xray core | Да, version check | Да, URL/custom outbound |
| VLESS WS TLS | Да | Да | Да | Да через VLESS URL/custom outbound |
| VLESS gRPC TLS/REALITY | Да | Да | Да, version check | Custom outbound/version check |
| VLESS HTTPUpgrade TLS | Да | Да, version check | Да, version check | Custom outbound/version check |
| VLESS XHTTP/SplitHTTP | Не заявлен в official transport schema | Да, актуальный Xray | Да, активно развивается | Не считать поддержанным |
| VMess | Да | Да | Да | Не перечислен в Proxy URL protocols |
| Trojan | Да | Да | Да | Да |
| Shadowsocks/SS2022 | Да | Method-dependent | Method-dependent | Да |
| Hysteria2 | Да, native | Не основной гарантированный путь | Да, version check | Да |
| mKCP | Не заявлен как V2Ray transport | Да, Xray core | Version check | Не считать поддержанным |

## Все inbounds 3X-UI

| Inbound панели | Удалённый client profile | Комментарий |
|---|---|---|
| VLESS | Да | Основной современный Xray protocol |
| VMess | Да | Legacy compatibility, без REALITY/Vision |
| Trojan | Да | Password + TLS/REALITY |
| Shadowsocks | Да | Проверять cipher/method |
| Hysteria2 | Да | QUIC/UDP + TLS |
| WireGuard | Да, через endpoint в 1.13 | VPN peer, не proxy URL |
| HTTP | Да, HTTP proxy settings | Обычно private/local use |
| SOCKS/Mixed | Да, SOCKS/HTTP settings | Podkop поддерживает SOCKS4/5 |
| Tunnel/Dokodemo-door | Нет отдельного profile | Server-side forwarding |
| TUN | Нет отдельного profile | Local system interface |

## sing-box

- Native outbounds: VLESS, VMess, Trojan, Shadowsocks, Hysteria2, HTTP, SOCKS.
- VLESS поддерживает `xtls-rprx-vision`.
- V2Ray transports: HTTP, WebSocket, QUIC, gRPC и HTTPUpgrade согласно текущей schema; XHTTP и mKCP в ней не заявлены.
- В sing-box `1.13` использовать WireGuard endpoint; legacy outbound удалён.
- Legacy inbound sniff fields удалены; sniffing задавать route action.
- Перед запуском выполнять `sing-box check -c config.json`.

## Podkop

Текущая документация Proxy section перечисляет VLESS, Shadowsocks, Trojan, Hysteria2 и SOCKS4/5. WireGuard используется через VPN section с предварительно настроенным interface.

- Для VLESS REALITY Vision сначала использовать URL.
- При потере fields использовать custom sing-box outbound.
- VMess и XHTTP не считать поддержанными UI/importer без отдельного подтверждения.
- Endpoint исключать из transparent proxy, чтобы не создать routing loop.

## v2rayNG

v2rayNG использует Xray/v2fly core. Для VLESS, VMess, Trojan и Xray transports фиксировать app/core version. REALITY, Vision, XHTTP и новые optional fields требуют актуального Xray core.

Hysteria2 и WireGuard не считать гарантированными только из факта использования Xray: проверять наличие profile parser и core support в конкретном release.

## Shadowrocket

App Store release notes подтверждают развитие VLESS/Vision, REALITY, XHTTP, Hysteria и WireGuard. Проверять:

- версию приложения;
- импортированные `flow`, SNI, Reality keys;
- XHTTP mode/path/padding;
- Hysteria auth/obfs/port range;
- WireGuard routes/MTU.

## Проверка импорта

После QR/subscription открыть профиль и вручную сравнить:

1. address/port;
2. UUID/password/auth;
3. protocol version;
4. TLS/REALITY/SNI/fingerprint;
5. flow;
6. transport/path/host/serviceName/mode;
7. UDP, obfs и port hopping;
8. DNS/TUN/routing.

## Источники

- [sing-box outbounds](https://sing-box.sagernet.org/configuration/outbound/)
- [sing-box V2Ray transports](https://sing-box.sagernet.org/configuration/shared/v2ray-transport/)
- [v2rayNG](https://github.com/2dust/v2rayNG)
- [Shadowrocket App Store](https://apps.apple.com/us/app/shadowrocket/id932747118)
- [Podkop sections](https://podkop.net/docs/sections/)
- [Podkop custom outbound](https://podkop.net/docs/own-outbound/)
