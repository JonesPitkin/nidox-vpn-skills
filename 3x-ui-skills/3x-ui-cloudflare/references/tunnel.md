# Cloudflare Tunnel

## Описание

`cloudflared` устанавливает исходящие соединения к Cloudflare, поэтому panel origin не требует public inbound port. Public hostname route обычно проксирует HTTP service.

## Когда использовать

- скрыть panel/subscription origin;
- не открывать panel port в firewall;
- добавить Cloudflare Access policy перед admin UI.

Не использовать как автоматически прозрачный transport для REALITY, raw VLESS/Trojan или Hysteria2.

## Пошаговая схема

1. Создать Tunnel в Cloudflare Zero Trust.
2. Установить `cloudflared` из официального package/source.
3. Запустить connector как system service.
4. Создать public hostname:

```text
panel.example.com -> http://127.0.0.1:<panel-port>
```

5. Сохранить custom web path.
6. Добавить Access policy, если требуется.
7. Закрыть public panel port только после внешней проверки Tunnel.

## Проверка

```sh
systemctl status cloudflared --no-pager
journalctl -u cloudflared -n 200 --no-pager
curl -I http://127.0.0.1:<panel-port>/<path>/
curl -I https://panel.example.com/<path>/
```

## Ошибки

- Service URL использует HTTPS, но local panel HTTP, или наоборот.
- Path/redirect не учитывает public hostname.
- Access blocks API/subscription clients.
- Tunnel token/config leaked.
- Public panel port остался открыт.

## Источники

- [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- [Tunnel routing to services](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/routing-to-tunnel/)
- [3X-UI reverse proxy guidance](https://github.com/MHSanaei/3x-ui/wiki/Configuration)
