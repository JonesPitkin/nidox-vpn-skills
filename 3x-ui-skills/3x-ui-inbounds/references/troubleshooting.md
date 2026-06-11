# Диагностика inbounds

## Содержание

1. Слои проверки
2. Матрица совместимости
3. Server checks
4. Handshake
5. Reverse proxy/CDN
6. Clients
7. Podkop
8. Hysteria2/UDP
9. Источники

## 1. Слои проверки

1. Config accepted.
2. Listener открыт.
3. TCP/UDP reachability.
4. TLS/REALITY handshake.
5. Protocol auth.
6. Transport path.
7. DNS/routing.
8. Client TUN/system integration.

## 2. Матрица совместимости

| Схема | v2rayNG | sing-box | Shadowrocket | Podkop |
|---|---|---|---|---|
| VLESS TCP REALITY Vision | Да, актуальный Xray | Да | Да, проверить версию | Да URL/custom outbound |
| VLESS WS TLS | Да | Да | Да | Обычно через VLESS parser/custom outbound |
| VLESS gRPC TLS/REALITY | Да | Да | Версионно | Custom outbound/version check |
| VLESS HTTPUpgrade TLS | Версионно | Да | Версионно | Custom outbound/version check |
| VLESS XHTTP | Актуальный Xray, version-sensitive | Не заявлен в official transport docs | Да, активно меняется | Не считать поддержанным |
| Trojan | Да | Да | Да | Перечислен в docs |
| Shadowsocks/SS2022 | method-dependent | Да | method-dependent | Да |
| Hysteria2 TLS | Зависит от bundled Xray и UI | Да, native outbound | Проверять версию | Да, URL/custom outbound |
| VMess | Да | Да | Да | Не перечислен в Proxy URL protocols |
| WireGuard | Не гарантировать без version check | Version-sensitive | Да, version check | VPN interface section |
| HTTP/SOCKS Mixed | Custom/local profile | Да | Да | SOCKS4/5 |
| Tunnel/TUN | Не client profile | Не client profile | Не client profile | Не client profile |

“Да” не отменяет проверку версии и импортированных полей.
Полная матрица: [clients.md](clients.md). Сравнение рекомендуемых схем: [comparison.md](comparison.md).

## 3. Server checks

```sh
x-ui status
x-ui settings
x-ui restart-xray
journalctl -u x-ui -n 250 --no-pager
ss -lntup
ufw status verbose 2>/dev/null || true
```

Docker: убедиться, что inbound port опубликован или используется host network. Для Hysteria2 публиковать UDP, например `443:443/udp`; TCP mapping не заменяет UDP.

Config error искать до сетевой диагностики:

```sh
journalctl -u x-ui -n 300 --no-pager | grep -iE 'failed|error|invalid|inbound|stream'
```

## 4. Handshake

**Timeout:** firewall, provider security group, IP block, wrong port.

**Connection refused:** нет listener/wrong address/container port.

**TLS error:** SNI, certificate chain, ALPN, client clock.

**REALITY invalid:** public/private key mismatch, short ID, SNI, fingerprint, time, unsupported optional ML-DSA.

**Auth error:** UUID/password/flow mismatch.

**Hysteria2 timeout:** UDP закрыт в host firewall, security group, Docker/LXC или сети клиента; неверен port hopping range.

**Hysteria2 TLS error:** SNI не входит в SAN сертификата, цепочка неполна, файл ключа недоступен процессу Xray или неверен pin.

## 5. Reverse proxy/CDN

Проверить:

- DNS указывает на edge/origin как задумано;
- TLS certificate соответствует public host;
- path/location совпадает;
- WS Upgrade/gRPC HTTP2/HTTPUpgrade/XHTTP method разрешены;
- origin port доступен proxy, но не обязательно всему интернету;
- REALITY не помещен за TLS-terminating CDN.

Status hints:

- 404: path;
- 400/426: Upgrade;
- 405: XHTTP method;
- 502/504: backend;
- 521/522: CDN-origin.

## 6. Clients

После импорта открыть config editor и сравнить:

- server/port;
- UUID/password;
- security/SNI/fingerprint;
- Reality public key/short ID;
- flow;
- transport/path/host/service/mode.

v2rayNG: записать app и Xray core version. Отключить TUN/mux/fragment для baseline.

Shadowrocket: записать App Store version; XHTTP release notes меняются часто. Проверить mode/padding.

sing-box:

```sh
sing-box check -c config.json
```

Не создавать XHTTP outbound, если installed sing-box docs/schema его не поддерживают.

## 7. Podkop

Проверить версию Podkop/sing-box и global diagnostics. URL mode принимает VLESS/Shadowsocks/Trojan/Hysteria2 по актуальной документации.

Если VLESS URL не разбирается:

1. Удалить secrets из diagnostic copy.
2. Сравнить URL query с supported sing-box fields.
3. Использовать custom outbound.
4. Для REALITY Vision взять официальный Podkop example.
5. Не конвертировать XHTTP в WS/gRPC автоматически: это другой transport.

Отдельно проверить routing loop: endpoint IP не должен уходить в тот же proxy.

Для Hysteria2:

1. Импортировать `hysteria2://`/`hy2://` URL и проверить password, SNI, obfs и port range.
2. Если parser теряет параметры, использовать `type: "hysteria2"` custom outbound.
3. Влияние глобальной настройки Podkop `Disable QUIC` проверять на установленной версии Podkop/sing-box, а не определять только по названию.
4. Исключить IP/домен Hysteria2 endpoint из маршрута через этот же proxy.

## 8. Hysteria2/UDP

Проверять по слоям:

```sh
ss -lunp
ufw status verbose 2>/dev/null || true
nft list ruleset 2>/dev/null | grep -iE 'udp|dport|redirect'
journalctl -u x-ui -n 250 --no-pager | grep -iE 'hysteria|quic|udp|tls|certificate|failed|error'
```

С внешнего Linux-хоста базовая UDP-проверка не доказывает handshake, но может обнаружить явный reject:

```sh
nc -uvz SERVER 443
```

Далее проверять реальным Hysteria2/sing-box клиентом. Для port hopping убедиться, что весь диапазон разрешён как UDP и перенаправляется на listener. В Docker опубликовать диапазон с `/udp`; в LXC проверить firewall хоста и контейнера.

Если TCP inbound работает на `443/tcp`, это не подтверждает доступность Hysteria2 на `443/udp`: протоколы могут использовать одинаковый номер порта независимо.

## Типовые ошибки 3X-UI

- link address равен listen address/неверному subscription host;
- random Reality SNI меняется между generated links;
- client email содержит spaces;
- CDN скрывает real IP и ломает IP limit;
- port есть в panel, но не Docker `ports`;
- открыт `443/tcp`, но закрыт `443/udp` для Hysteria2;
- certificate path существует на host, но не виден внутри контейнера;
- Salamander password или `mport` потеряны при импорте ссылки;
- subscription cached старую конфигурацию.

## Минимальный отчет

Скрыть secrets и приложить:

- 3X-UI/Xray/client versions;
- protocol/network/security/flow;
- redacted link query;
- server listener/firewall;
- последние relevant log lines;
- direct/CDN и разные ISP results.

## Источники

- [3X-UI Wiki FAQ](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems)
- [3X-UI protocol capabilities](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/lib/xray/protocol-capabilities.ts)
- [3X-UI link generator](https://github.com/MHSanaei/3x-ui/blob/main/sub/subService.go)
- [v2rayNG](https://github.com/2dust/v2rayNG)
- [sing-box VLESS](https://sing-box.sagernet.org/configuration/outbound/vless/)
- [sing-box transports](https://sing-box.sagernet.org/configuration/shared/v2ray-transport/)
- [Xray Hysteria inbound](https://xtls.github.io/en/config/inbounds/hysteria.html)
- [Xray Hysteria transport](https://xtls.github.io/en/config/transports/hysteria.html)
- [sing-box Hysteria2 outbound](https://sing-box.sagernet.org/configuration/outbound/hysteria2/)
- [Hysteria2 port hopping](https://v2.hysteria.network/docs/advanced/Port-Hopping/)
- [Shadowrocket App Store](https://apps.apple.com/us/app/shadowrocket/id932747118)
- [Podkop sections](https://podkop.net/docs/sections/)
- [Podkop custom outbound](https://podkop.net/docs/own-outbound/)
