# SKILL_INDEX

Индекс production-skills по `sing-box`.

## Базовые навыки

### `sing-box-core`

Использовать когда нужно:

- понять архитектуру `sing-box`;
- разложить root JSON по секциям;
- подготовить новый проект;
- провести первичный review или migration review;
- определить stable/version baseline.

Типовые сценарии:

- “объясни, как устроен этот конфиг”
- “подготовь baseline для нового клиента или сервера”
- “после обновления перестало работать, что изменилось в структуре?”

### `sing-box-dns`

Использовать когда нужно:

- построить local DNS, DoH, DoT, split DNS;
- внедрить FakeIP;
- найти DNS leak;
- разобраться с `domain_resolver`.

Типовые сценарии:

- “часть доменов идёт мимо proxy”
- “proxy по IP работает, по домену нет”
- “нужен split DNS на роутере”

### `sing-box-inbounds`

Использовать когда нужно:

- выбрать `mixed`, `socks`, `http`, `tun`, `redirect`, `tproxy`, `direct`;
- спроектировать local proxy vs transparent capture.

Типовые сценарии:

- “что выбрать для desktop?”
- “как перехватывать трафик клиентов на роутере?”
- “нужен локальный proxy для приложений и CLI”

### `sing-box-outbounds`

Использовать когда нужно:

- выбрать proxy transport;
- построить `selector` or `urltest` group;
- сравнить VLESS, VMess, Trojan, Shadowsocks, Hysteria2, SSH;
- перейти на modern WireGuard endpoint path.

Типовые сценарии:

- “какой transport выбрать под эту сеть?”
- “нужен failover между двумя узлами”
- “как корректно оформить WireGuard в новой конфигурации?”

### `sing-box-routing`

Использовать когда нужно:

- делать selective proxying;
- делать split tunneling;
- строить policy rules by domain, ip, source, process, `rule_set`;
- искать routing loops или неверный policy match.

Типовые сценарии:

- “локальные ресурсы должны идти напрямую”
- “эти домены через proxy, остальные напрямую”
- “почему правила не срабатывают?”

### `sing-box-tun`

Использовать когда нужно:

- внедрить TUN;
- настроить `auto_route` and `auto_redirect`;
- защищать LAN/admin paths;
- диагностировать transparent capture.

Типовые сценарии:

- “нужен full-device transparent client”
- “после включения TUN пропал доступ к роутеру”
- “как сделать split tunnel через TUN?”

### `sing-box-rulesets`

Использовать когда нужно:

- мигрировать с `geosite`/`geoip`;
- использовать inline/local/remote `rule_set`;
- управлять reusable policy assets;
- проектировать cache/update strategy.

Типовые сценарии:

- “как заменить старые geosite/geoip?”
- “нужен централизованный policy file”
- “как раздать одну политику на много узлов?”

### `sing-box-security`

Использовать когда нужно:

- разобрать TLS;
- проектировать REALITY;
- проверить сертификаты;
- не попасть в deprecated ECH/uTLS assumptions.

Типовые сценарии:

- “TLS handshake не проходит”
- “как правильно собрать REALITY client/server?”
- “что делать после migration security-полей?”

### `sing-box-openwrt`

Использовать когда нужно:

- развернуть `sing-box` на OpenWrt;
- понять official `procd` path;
- выбрать router model;
- защитить admin plane и local DNS.

Типовые сценарии:

- “как поставить и запустить на OpenWrt?”
- “как сделать transparent router безопасно?”
- “почему на роутере всё ломается, а на desktop работает?”

### `sing-box-troubleshooting`

Использовать когда нужно:

- локализовать первый сломанный слой;
- пошагово диагностировать DNS, TUN, route, TLS, transport;
- сделать safe rollback.

Типовые сценарии:

- “после обновления всё сломалось”
- “подключение идёт, но трафик не работает”
- “непонятно, это DNS, маршрут или transport”

## Быстрый роутинг по запросам

Если вопрос начинается с:

- “как устроен” -> `sing-box-core`
- “почему домены” -> `sing-box-dns`
- “какой inbound” -> `sing-box-inbounds`
- “какой outbound/protocol” -> `sing-box-outbounds`
- “как маршрутизировать” -> `sing-box-routing`
- “как сделать transparent” -> `sing-box-tun`
- “как заменить geosite” -> `sing-box-rulesets`
- “TLS/REALITY/ECH” -> `sing-box-security`
- “OpenWrt/роутер” -> `sing-box-openwrt`
- “ничего не работает” -> `sing-box-troubleshooting`

## Recommended Reading Order

1. `sing-box-core`
2. `sing-box-dns`
3. `sing-box-routing`
4. `sing-box-inbounds`
5. `sing-box-outbounds`
6. `sing-box-tun`
7. `sing-box-rulesets`
8. `sing-box-security`
9. `sing-box-openwrt`
10. `sing-box-troubleshooting`

