# Hysteria и Hysteria2

> Проверено по 3X-UI `v3.3.0`, Xray Hysteria transport и official Hysteria `v2.9.2`.

## Описание

Hysteria2 — прокси-протокол поверх QUIC/UDP с обязательным TLS. Он рассчитан на сети с потерями, высокой задержкой и нестабильной пропускной способностью. Hysteria v1 — предыдущая, несовместимая версия протокола.

Различать Xray Hysteria transport, который использует 3X-UI, и standalone official Hysteria application. Xray-форма содержит auth, `udpIdleTimeout` и HTTP/3 masquerade; расширенные поля official app нельзя переносить в неё без поддержки schema.

В актуальном 3X-UI обе версии представлены внутренним protocol id `hysteria`, однако:

- новая форма inbound создаёт `version: 2`;
- transport фиксирован как `network: hysteria`;
- security фиксирован как `tls`;
- share link для v2 имеет схему `hysteria2://`, для legacy v1 — `hysteria://`;
- актуальная документация Xray требует `version: 2`.

Для новых конфигураций использовать Hysteria2. Hysteria v1 рассматривать только при обслуживании существующего inbound и клиента, которые уже подтверждённо работают.

## Когда использовать

Использовать Hysteria2, когда:

- UDP из клиентской сети доступен;
- соединение имеет потери, высокий RTT или нестабильную скорость;
- нужен полноценный TCP и UDP proxy через один inbound;
- помогает смена UDP-портов при throttling отдельного порта;
- sing-box или Podkop выступает клиентом.

Не выбирать как единственную схему, когда:

- оператор полностью блокирует UDP/QUIC;
- VPS-провайдер или LXC-хост не разрешает входящий UDP;
- доступен только TCP reverse proxy/CDN;
- клиент не поддерживает Hysteria2 или теряет параметры ссылки.

Держать TCP-based fallback, например VLESS TCP REALITY Vision.

## Преимущества

- работа поверх UDP/QUIC;
- устойчивость к потерям и нестабильным каналам;
- native UDP forwarding;
- обязательный TLS;
- Salamander obfuscation в Hysteria2;
- HTTP/3 masquerade при проверке listener;
- port hopping для сетей, ограничивающих отдельные UDP-порты;
- native Hysteria2 outbound в sing-box и поддержка в Podkop.

## Недостатки

- не работает при полном запрете UDP;
- UDP может ограничиваться провайдером, VPS firewall или CGNAT;
- обычный HTTP CDN не проксирует этот QUIC listener как TCP/WebSocket;
- требуется корректный сертификат или безопасно настроенный certificate pin;
- port hopping увеличивает поверхность firewall и сложность диагностики;
- Hysteria v1 и Hysteria2 нельзя считать взаимозаменяемыми;
- импорт URL зависит от версии клиента и parser.

## Требования

Сервер:

- актуальные 3X-UI и bundled Xray-core с Hysteria2;
- доступный UDP-порт на VPS;
- UDP разрешён в cloud security group, host firewall и LXC/Docker;
- домен, если используется публично доверенный сертификат;
- TLS certificate/key, читаемые процессом Xray;
- уникальный `auth` для каждого клиента;
- корректное время на сервере и клиенте.

Клиент:

- Hysteria2-compatible core;
- совпадающие address, UDP port, auth/password, SNI и obfs password;
- доверие к цепочке сертификата либо проверенный SHA-256 pin;
- port range и hop interval, если включён port hopping.

Зафиксировать версии 3X-UI/Xray из интерфейса панели и проверить состояние:

```sh
x-ui status
x-ui settings
journalctl -u x-ui -n 100 --no-pager
```

## Настройка в панели

1. Создать inbound и выбрать protocol `Hysteria`.
2. Оставить Version `2`. В актуальной форме поле зафиксировано на Hysteria2.
3. Выбрать UDP-порт. `443/udp` может сосуществовать с другим сервисом на `443/tcp`.
4. Добавить клиента:
   - задать уникальный email;
   - сгенерировать сильный `Auth`;
   - при необходимости настроить quota, expiry и IP limit.
5. В transport проверить:
   - Network: `Hysteria`;
   - Version: `2`;
   - UDP Idle Timeout: по умолчанию Xray использует 60 секунд;
   - Masquerade: optional.
6. В security использовать только TLS.
7. Указать certificate file и key file либо сертификат, управляемый панелью.
8. Указать SNI/server name, соответствующий SAN сертификата.
9. Для Hysteria2 оставить сгенерированный FinalMask UDP `salamander` и сохранить его password для клиента.
10. Сохранить inbound, перезапустить Xray и проверить UDP listener.

```sh
x-ui restart-xray
ss -lunp
journalctl -u x-ui -n 200 --no-pager
```

Masquerade:

- пустой type возвращает стандартную 404-страницу;
- `proxy` перенаправляет HTTP/3-запросы на URL;
- `file` отдаёт локальный каталог;
- `string` возвращает заданные status/body/headers.

Masquerade не заменяет TLS и не исправляет закрытый UDP.

## Настройка клиента

Сначала использовать share link/QR из 3X-UI:

```text
hysteria2://AUTH@media.example.com:443?security=tls&sni=media.example.com&obfs=salamander&obfs-password=SECRET#hy2
```

Это иллюстрация формата. Использовать ссылку, созданную своей панелью, и не публиковать `AUTH`/obfs password.

Минимальный sing-box outbound:

```json
{
  "type": "hysteria2",
  "tag": "hy2-out",
  "server": "media.example.com",
  "server_port": 443,
  "password": "AUTH_FROM_3X_UI",
  "obfs": {
    "type": "salamander",
    "password": "OBFS_PASSWORD_FROM_3X_UI"
  },
  "tls": {
    "enabled": true,
    "server_name": "media.example.com"
  }
}
```

Если используется публичный домен, не генерировать hostnames вроде `vpn.*`, `proxy.*`, `ws.*`, `panel.*` или `admin.*` без отдельной причины и явного предупреждения о детектируемости.

Проверить конфигурацию:

```sh
sing-box check -c config.json
```

Для Hysteria v1 sing-box использует отдельный `type: "hysteria"` и другие auth fields. Не преобразовывать v1 в v2 простой заменой URL scheme.

## UDP

Hysteria2 transport использует UDP. Открывать протокол явно:

```sh
ufw allow 443/udp
ss -lunp | grep ':443'
```

Docker Compose:

```yaml
ports:
  - "443:443/udp"
```

Для LXC проверить firewall гипервизора, bridge и контейнера. Наличие `443/tcp` ничего не говорит о `443/udp`.

### Port hopping

Port hopping документирован official Hysteria и sing-box Hysteria2 outbound. В текущей Xray Hysteria stream schema 3X-UI отдельного поля port hopping нет; использовать только механизм, который фактически генерирует установленная версия панели/client.

Перед включением:

1. Выбрать небольшой обоснованный UDP range.
2. Разрешить весь range в security group/firewall.
3. Настроить перенаправление range на основной Hysteria2 listener согласно используемой реализации.
4. Проверить, что клиент импортировал range.
5. Проверить несколько переподключений.

Не предполагать, что Linux redirect или official Hysteria port-range автоматически применяется Xray/3X-UI.

## Hysteria 2.9.2

`v2.9.2` содержит важные security fixes: UDP ACL bypass, trailing-dot ACL bypass, потенциальный OOM при HTTP sniff, SOCKS5 UDP destination и DoH fixes.

Standalone official Hysteria также поддерживает:

- экспериментальный Gecko obfuscation для фрагментации QUIC handshake;
- BBR/Reno congestion control и BBR profiles;
- QUIC idle, keepalive и PMTU settings;
- Realms/NAT traversal.

Эти возможности требуют поддержки на обеих сторонах и не означают автоматическую поддержку в Xray/3X-UI.

## Сертификаты

Предпочтительный вариант:

- домен указывает на VPS;
- сертификат выдан публичным CA;
- certificate содержит домен в SAN;
- клиент использует тот же домен как SNI;
- key доступен только root/Xray service.

Проверка:

```sh
openssl x509 -in /path/to/fullchain.pem -noout -subject -issuer -dates -ext subjectAltName
openssl pkey -in /path/to/privkey.pem -check -noout
```

Для self-signed сертификата не оставлять `insecure` единственной защитой. Использовать certificate pin, если клиент его поддерживает. 3X-UI генерирует Hysteria `pinSHA256` в hex; не подменять его base64-значением.

После renewal убедиться, что путь не изменился, Xray читает новый key/cert, а pin обновлён у клиентов, если pinning используется.

## Совместимость с sing-box

sing-box официально имеет отдельные `hysteria` и `hysteria2` outbounds.

Для актуального 3X-UI Hysteria2 сопоставлять:

| 3X-UI/Xray | sing-box |
|---|---|
| client `auth` | `password` |
| inbound address/port | `server` / `server_port` |
| port hopping | `server_ports`, `hop_interval` |
| Salamander password | `obfs.type`, `obfs.password` |
| TLS server name | `tls.server_name` |
| certificate pin/CA | соответствующие TLS verification fields |

Официальная документация sing-box указывает, что оба network types, TCP и UDP, разрешены по умолчанию через Hysteria2 outbound. Это относится к проксируемому трафику; соединение с сервером всё равно идёт через QUIC/UDP.

## Совместимость с Podkop

Актуальная документация Podkop перечисляет Hysteria2 среди поддерживаемых Proxy protocols.

Порядок:

1. Создать Proxy section.
2. Выбрать Connection URL.
3. Вставить `hysteria2://` или `hy2://` ссылку из 3X-UI.
4. Применить настройки и очистить cache после обновления.
5. Запустить Podkop Diagnostics.
6. Проверить версию sing-box и фактический generated outbound.

Если URL parser потерял SNI, obfs или port range, выбрать Outbound Config и вставить проверенный sing-box `hysteria2` outbound.

Endpoint IP/домен должен выходить напрямую, а не маршрутизироваться через тот же Hysteria2 outbound, иначе возникает routing loop.

Глобальная настройка Podkop `Disable QUIC` предназначена для управления QUIC-трафиком через правила. Её влияние на Hysteria2 проверять на конкретной версии Podkop; не делать вывод только по названию переключателя.

## Типовые ошибки

- открыт TCP, но закрыт UDP;
- Docker публикует порт без `/udp`;
- LXC host firewall не пропускает UDP;
- security group разрешает не тот port/range;
- auth/password различаются;
- Salamander включён только с одной стороны;
- SNI отсутствует в certificate SAN;
- certificate expired или chain неполна;
- key/certificate path недоступен внутри Docker;
- клиент импортировал `hysteria://` вместо `hysteria2://`;
- Hysteria v1 client подключается к v2 inbound;
- `pinSHA256` имеет неверный формат или устарел после renewal;
- port hopping range есть в ссылке, но не открыт/не перенаправляется;
- UDP блокируется текущей клиентской сетью;
- endpoint попал в routing loop Podkop.

## Диагностика

1. Проверить принятие конфигурации:

```sh
x-ui restart-xray
journalctl -u x-ui -n 250 --no-pager | grep -iE 'hysteria|quic|udp|tls|certificate|failed|error'
```

2. Проверить listener и firewall:

```sh
ss -lunp
ufw status verbose 2>/dev/null || true
nft list ruleset 2>/dev/null | grep -iE 'udp|dport|redirect'
```

3. Проверить certificate:

```sh
openssl x509 -in /path/to/fullchain.pem -noout -dates -ext subjectAltName
```

4. Сверить client fields:

- server и UDP port;
- auth/password;
- TLS SNI;
- certificate trust/pin;
- Salamander type/password;
- port range/hop interval.

5. Запустить client с debug logs. Для sing-box:

```sh
sing-box check -c config.json
sing-box run -c config.json
```

6. Сравнить:

- другая клиентская сеть;
- обычный single UDP port без hopping;
- без optional masquerade;
- другой Hysteria2-compatible client;
- TCP fallback на том же VPS.

Если Hysteria2 работает через одну сеть и не работает через другую при одинаковом config, вероятна фильтрация/throttling UDP. Это не исправляется изменением TLS SNI без сетевых доказательств.

## Источники

- [3X-UI README](https://github.com/MHSanaei/3x-ui)
- [3X-UI Hysteria inbound schema](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/schemas/protocols/inbound/hysteria.ts)
- [3X-UI Hysteria form](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/pages/inbounds/form/protocols/hysteria.tsx)
- [3X-UI share-link generator](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/sub/subService.go)
- [Xray Hysteria inbound](https://xtls.github.io/en/config/inbounds/hysteria.html)
- [Xray Hysteria transport](https://xtls.github.io/en/config/transports/hysteria.html)
- [sing-box Hysteria2 outbound](https://sing-box.sagernet.org/configuration/outbound/hysteria2/)
- [Hysteria2 server](https://v2.hysteria.network/docs/getting-started/Server/)
- [Hysteria2 client configuration](https://v2.hysteria.network/docs/advanced/Full-Client-Config/)
- [Hysteria2 port hopping](https://v2.hysteria.network/docs/advanced/Port-Hopping/)
- [Podkop sections](https://podkop.net/docs/sections/)
- [Podkop diagnostics](https://podkop.net/docs/diagnostics/)
- [Hysteria v2.9.2 release](https://github.com/apernet/hysteria/releases/tag/app/v2.9.2)
