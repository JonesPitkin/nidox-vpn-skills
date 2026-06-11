# Защита панели

## Модель доступа

Предпочтительный порядок:

1. panel слушает `127.0.0.1`, доступ через SSH tunnel;
2. panel за TLS reverse proxy с source/VPN/Access restriction;
3. panel с собственным TLS и firewall allowlist;
4. публичная panel без ограничения — наименее предпочтительно.

## Пошаговая настройка

1. Записать текущие URL, port и path.
2. Открыть резервную SSH/console сессию.
3. Сменить web base path через menu:

```sh
x-ui
# Reset Web Base Path
```

4. Сменить panel port на свободный непубличный/разрешенный port.
5. Включить TLS или reverse proxy.
6. Ограничить source IP/firewall.
7. Проверить новый URL с завершающим `/`, затем закрыть старый rule.

Для loopback + SSH tunnel:

```sh
ssh -L 2222:127.0.0.1:<panel-port> <user>@<server>
```

Открыть `http://127.0.0.1:2222/<web-base-path>/` либо HTTPS согласно panel config.

## Сценарии

- Один администратор со стабильным IP: UFW allow from admin IP.
- Динамический IP: WireGuard/Tailscale/Cloudflare Access/reverse proxy, после отдельной оценки.
- Docker: не публиковать panel port на `0.0.0.0`, если нужен только local reverse proxy.

## Ошибки

- Reverse proxy path не совпадает с base path.
- URL без trailing slash ломает redirects/assets.
- Panel bind изменен до проверки tunnel.
- Firewall закрыт раньше, чем разрешен новый port.

## Проверка

```sh
ss -lntp | grep ':<panel-port> '
curl -I http://127.0.0.1:<panel-port>/<path>/
```

## Источники

- [3X-UI Wiki FAQ: brute force and restricted access](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems)
- [3X-UI Wiki: reverse proxy](https://github.com/MHSanaei/3x-ui/wiki/Configuration)
- [x-ui management script](https://github.com/MHSanaei/3x-ui/blob/main/x-ui.sh)
