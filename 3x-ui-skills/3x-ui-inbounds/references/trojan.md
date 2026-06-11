# Trojan

## Описание

Trojan использует password clients и обычно TLS-like deployment. 3X-UI поддерживает fallbacks и transports TCP, WS, gRPC, HTTPUpgrade, XHTTP; REALITY разрешен для TCP/gRPC/XHTTP.

## Когда использовать

- TLS/reverse proxy deployments;
- клиенты с хорошей Trojan support;
- fallbacks на одном TLS port;
- альтернатива VLESS без UUID/flow.

## Преимущества

- простая password authentication;
- TLS и fallbacks;
- широкая client compatibility;
- 3X-UI subscriptions/share links.

## Недостатки

- нет VLESS Vision flow в panel client schema;
- TLS certificate/reverse proxy complexity;
- password leakage компрометирует client;
- Reality+Trojan client support уже, чем VLESS REALITY.

## Требования

- unique password;
- TLS certificate/SNI либо поддержанный REALITY client;
- transport support на client и proxy;
- корректный fallback destination, если fallbacks включены.

## Настройка в панели

1. Protocol Trojan.
2. Client password и unique email.
3. Security TLS для стандартной схемы.
4. Transport TCP или WS/gRPC/HTTPUpgrade/XHTTP.
5. Fallbacks настраивать только при понимании `name`, `alpn`, `path`, `dest`, `xver`.

Golden fixture Trojan WS TLS доступен в repository.

## Настройка клиента

`trojan://<percent-encoded-password>@host:port?...`. 3X-UI percent-encodes `/` и `=` для parser compatibility.

- sing-box имеет native Trojan outbound и V2Ray transports.
- v2rayNG/Shadowrocket поддерживают Trojan, но новые transports требуют актуальной версии.
- Podkop текущая документация sections перечисляет Trojan; при URL parse failure использовать custom outbound.

## Типовые ошибки

- password содержит символы и был скопирован без URL decoding;
- certificate/SNI mismatch;
- fallback loop/wrong dest;
- transport path/service mismatch;
- client не поддерживает Trojan REALITY.

## Диагностика

Начать Trojan TCP TLS без fallback. Проверить certificate, password и SNI. Затем добавлять transport/fallback по одному.

```sh
openssl s_client -connect <host>:443 -servername <sni> </dev/null
journalctl -u x-ui -n 200 --no-pager | grep -iE 'trojan|tls|fallback'
```

## Источники

- [Trojan schema](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/schemas/protocols/inbound/trojan.ts)
- [Trojan WS TLS fixture](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/test/golden/fixtures/inbound-full/trojan-ws-tls.json)
- [3X-UI Trojan link generator](https://github.com/MHSanaei/3x-ui/blob/main/sub/subService.go)
- [Podkop sections](https://podkop.net/docs/sections/)
