# Cloudflare Tunnel

## Описание

`cloudflared` устанавливает исходящие соединения к Cloudflare, поэтому panel origin не требует public inbound port. Public hostname route обычно проксирует HTTP service.

## Когда использовать

- скрыть panel/subscription origin;
- не открывать panel port в firewall;
- добавить Cloudflare Access policy перед admin UI.

Не использовать как автоматически прозрачный transport для REALITY, raw VLESS/Trojan или Hysteria2.
Не публиковать panel на очевидных hostname вроде `panel.*` или `admin.*`.

## Пошаговая схема

1. Создать Tunnel в Cloudflare Zero Trust.
2. Установить `cloudflared` из официального package/source.
3. Запустить connector как system service.
4. Создать public hostname:

```text
content.example.com -> http://127.0.0.1:<panel-port>
```

5. Сохранить hidden admin path, не похожий на VPN transport path.
6. Добавить Access policy, если требуется.
7. Закрыть public panel port только после внешней проверки Tunnel.

## Проверка

```sh
systemctl status cloudflared --no-pager
journalctl -u cloudflared -n 200 --no-pager
curl -I http://127.0.0.1:<panel-port>/<path>/
curl -I https://content.example.com/<hidden-panel-path>/
```

## Ошибки

- Service URL использует HTTPS, но local panel HTTP, или наоборот.
- Path/redirect не учитывает public hostname.
- Access blocks API/subscription clients.
- Tunnel token/config leaked.
- Public panel port остался открыт.
- Hostname выглядит как публичная admin surface и лишний раз маркирует панель.

## Источники

- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/)
- [Tunnel routing to services](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/routing-to-tunnel/)
- [3X-UI reverse proxy guidance](https://github.com/MHSanaei/3x-ui/wiki/Configuration)
