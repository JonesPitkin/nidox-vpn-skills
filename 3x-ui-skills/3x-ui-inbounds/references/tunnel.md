# Tunnel / Dokodemo-door

## Описание

`Tunnel` в 3X-UI — panel abstraction для Xray `dokodemo-door`-style forwarding. Он принимает TCP/UDP и перенаправляет на `rewriteAddress`/`rewritePort` или по `portMap`.

## Когда использовать

- L4 forwarding между собственными узлами;
- перенаправление fixed service;
- transparent redirect с `followRedirect`;
- panel-to-panel/tunnel architecture.

Это не клиентский протокол и не генерирует универсальную share link.

## Преимущества

- простой TCP/UDP forwarding;
- port mapping и transparent redirect;
- не требует специального profile у конечного приложения.

## Недостатки

- не добавляет encryption/auth сам по себе;
- легко создать routing loop;
- destination может видеть только адрес промежуточного узла.

## Требования

- точный destination и network;
- firewall/NAT rules;
- loop prevention;
- для `followRedirect` — заранее настроенный transparent redirect;
- понимание того, какой source IP увидит destination.

## Настройка в панели

1. Выбрать `Tunnel`.
2. Задать `rewriteAddress` и `rewritePort` либо `portMap`.
3. Выбрать `tcp`, `udp` или `tcp,udp`.
4. `followRedirect` включать только для transparent interception.
5. Ограничить listener firewall.

## Настройка клиента

Отдельной настройки v2rayNG, Shadowrocket, sing-box или Podkop нет: клиент подключается к сервису, который опубликован tunnel listener. Совместимость определяется внешним протоколом сервиса.

## Типовые ошибки

- forwarding loop;
- destination слушает только loopback;
- UDP разрешён только на одном узле;
- неверный port map;
- `followRedirect` включён без redirect metadata;
- IP limit на дальнем узле видит только промежуточный сервер.

## Диагностика

```sh
ss -lntup
ip route get DESTINATION_IP
journalctl -u x-ui -n 200 --no-pager | grep -iE 'dokodemo|tunnel|failed|error'
```

Проверить listener, destination отдельно и затем end-to-end.

## Источники

- [3X-UI Tunnel schema](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/schemas/protocols/inbound/tunnel.ts)
- [Xray Dokodemo-door](https://xtls.github.io/en/config/inbounds/dokodemo.html)
- [3X-UI Wiki FAQ](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems)
