# REALITY

> Проверено по 3X-UI `v3.3.0` и bundled Xray-core `v26.6.1`.

## Описание

REALITY — Xray security layer, использующий X25519 keypair, SNI/target, short ID и uTLS fingerprint. Он предназначен для direct client-to-Xray connection и не требует собственного публичного certificate на inbound.

## Когда использовать

- прямой VPS endpoint без CDN;
- VLESS + TCP + Vision как основной baseline;
- сети с TLS/SNI/DPI filtering, после диагностики;
- когда домен и certificate для обычного TLS нежелательны.

## Преимущества

- не требует server certificate;
- handshake похож на выбранный target;
- работает с Vision;
- panel генерирует keypair, target/SNI и short IDs.

## Недостатки

- не работает за conventional TLS-terminating CDN;
- target/SNI должен быть достижим и подходить по TLS behavior;
- чувствителен к clock/version/fingerprint и client support;
- public key/short ID/SNI mismatch полностью ломает handshake.

## Требования

REALITY разрешен для VLESS/Trojan с Raw/TCP, gRPC и XHTTP. Для WS и HTTPUpgrade форма его не предлагает. Старое имя server-side поля `dest` заменено на `target` и остаётся alias.

Поля:

- `target`: `host:port`;
- `serverNames`: один или несколько SNI;
- `privateKey`/client `publicKey`;
- `shortIds`;
- `fingerprint`, default `chrome`;
- `spiderX`, default `/`;
- optional `minClientVer`, `maxClientVer`, `maxTimediff`;
- optional `mldsa65Seed`/`mldsa65Verify`;
- optional fallback upload/download rate limits.

Если target поддерживает X25519MLKEM768, актуальный Xray использует post-quantum key exchange автоматически. Проверять через `xray tls ping <target>`.

## Настройка в панели

1. Protocol `VLESS`.
2. Transport `TCP (Raw)` для baseline.
3. Security `REALITY`.
4. Нажать generate keypair и short IDs.
5. Указать target `example.com:443` и SNI из certificate target.
6. Fingerprint `chrome`.
7. Client flow `xtls-rprx-vision`.
8. Сохранить и restart Xray.

Не копировать private key клиенту. Share link должен содержать `pbk`, `sid`, `sni`, `fp`, `spx`.

## Выбор target/SNI

Wiki рекомендует TLS 1.3/H2-capable SNI и ссылается на RealiTLScanner. Не использовать чужой target как гарантию обхода. Проверить с VPS:

```sh
openssl s_client -connect <target>:443 -servername <sni> </dev/null
```

Неаутентифицированный трафик пересылается к `target`. Target за публичным CDN может превратить VPS в нежелательный port forward после сканирования. Предпочитать target в том же ASN. Fallback rate limiting применять только после оценки: он создаёт собственный fingerprint.

## Настройка клиента

Проверить:

- VLESS UUID;
- endpoint — IP/domain VPS, не target;
- SNI — один из `serverNames`;
- public key — из `settings.publicKey`;
- short ID — один из `shortIds`;
- fingerprint;
- flow Vision для TCP;
- transport fields.

Podkop official custom outbound example:

```json
{
  "type": "vless",
  "server": "<server>",
  "server_port": 443,
  "uuid": "<uuid>",
  "flow": "xtls-rprx-vision",
  "tls": {
    "enabled": true,
    "server_name": "<sni>",
    "utls": {"enabled": true, "fingerprint": "chrome"},
    "reality": {
      "enabled": true,
      "public_key": "<public-key>",
      "short_id": "<short-id>"
    }
  }
}
```

## Обход блокировок

REALITY снижает очевидность Xray handshake, но IP может быть заблокирован, TCP shaped, target fingerprint выделен или client traffic fingerprinted. Держать запасной IP/port/transport. Не совмещать REALITY и CDN.

## Типовые ошибки

- `REALITY: processed invalid connection`: mismatch SNI/key/sid/time/client.
- timeout до handshake: firewall/IP block/routing.
- работает на одном ISP: фильтрация сети, а не server config.
- ML-DSA error: старый client; очистить optional ML-DSA fields или обновить обе стороны.

## Диагностика

```sh
date -u
timedatectl status
ss -lntp | grep ':<port> '
journalctl -u x-ui -n 250 --no-pager | grep -iE 'reality|tls|handshake|failed'
```

Сравнить URL parameters с panel fields посимвольно. Проверить connection без TUN/mux/custom fragment.

## Источники

- [Wiki FAQ: recommended REALITY settings](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems#6-what-settings-do-you-recommend-for-reality)
- [3X-UI REALITY schema](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/schemas/protocols/security/reality.ts)
- [3X-UI REALITY form](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/pages/inbounds/form/security/reality.tsx)
- [3X-UI golden fixture](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/test/golden/fixtures/inbound-full/vless-tcp-reality.json)
- [Podkop custom outbound](https://podkop.net/docs/own-outbound/)
- [Xray REALITY](https://xtls.github.io/en/config/transports/reality.html)
