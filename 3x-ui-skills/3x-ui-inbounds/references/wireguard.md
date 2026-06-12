# WireGuard

> Проверено по 3X-UI `v3.3.0` и sing-box `v1.13.13`.

## Описание

WireGuard inbound в 3X-UI создаётся средствами Xray и принимает peer-based VPN traffic по UDP. Это не VLESS transport и не WARP outbound.

## Когда использовать

- нужен обычный IP-layer VPN;
- клиент поддерживает WireGuard config;
- UDP доступен;
- важнее простота VPN, чем маскировка proxy-протокола.

WireGuard имеет узнаваемый UDP pattern и не является базовым выбором при жёсткой фильтрации протоколов.

## Преимущества

- простой IP-layer VPN;
- высокая производительность;
- зрелые native clients;
- TCP и UDP приложения работают через tunnel.

## Недостатки

- зависит от UDP;
- не маскируется под обычный HTTPS;
- требует аккуратной адресации, routes и key management.

## Требования

- UDP listener и firewall;
- server private key;
- public/private keypair каждого peer;
- уникальные `allowedIPs`;
- согласованные MTU, routes и optional PSK;
- исключение endpoint из маршрута через сам tunnel.

## Настройка в панели

1. Выбрать `WireGuard`.
2. Сгенерировать server Secret Key; public key вычисляется панелью.
3. Выбрать MTU, baseline `1420`.
4. Добавить peer и сгенерировать его keypair.
5. Назначить уникальный peer address, например `10.0.0.2/32`.
6. При NAT использовать keepalive по требованиям сети.
7. Открыть inbound port как UDP.

`noKernelTun` включать только при подтверждённой необходимости.

## Настройка клиента

Использовать QR/config, созданный 3X-UI. Сверить endpoint, server public key, client private key, allowed IPs, DNS и MTU.

- Shadowrocket: WireGuard поддерживается, но импорт и routing options зависят от версии.
- v2rayNG: не считать универсальным WireGuard-клиентом без проверки конкретной версии/core.
- sing-box `1.13`: legacy WireGuard outbound удалён; использовать top-level WireGuard endpoint и routing к нему.
- Podkop: использовать VPN section с предварительно созданным WireGuard interface, а не Proxy URL.

## Типовые ошибки

- открыт TCP вместо UDP;
- peer addresses пересекаются;
- перепутаны private/public keys;
- одинаковый private key у нескольких peers;
- endpoint попал в tunnel route;
- MTU вызывает зависания больших пакетов;
- Docker/LXC не пропускает UDP.

## Диагностика

```sh
ss -lunp
journalctl -u x-ui -n 200 --no-pager | grep -iE 'wireguard|udp|failed|error'
ip route
```

Проверить handshake реальным клиентом, затем ping tunnel address, DNS и external IP.

## Источники

- [3X-UI WireGuard schema](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/schemas/protocols/inbound/wireguard.ts)
- [3X-UI WireGuard form](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/pages/inbounds/form/protocols/wireguard.tsx)
- [Xray WireGuard inbound](https://xtls.github.io/en/config/inbounds/wireguard.html)
- [Podkop WireGuard](https://podkop.net/docs/tunnels/wg_settings/)
- [sing-box WireGuard endpoint](https://sing-box.sagernet.org/configuration/endpoint/wireguard/)
- [sing-box WireGuard migration](https://sing-box.sagernet.org/migration/#migrate-wireguard-outbound-to-endpoint)
