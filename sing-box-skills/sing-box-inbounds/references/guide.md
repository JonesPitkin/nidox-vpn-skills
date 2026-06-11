# Inbounds Guide

## Mixed

Назначение: единая локальная точка входа для `socks4`, `socks4a`, `socks5` и `http`.

Когда использовать:

- desktop-клиент;
- тестовый локальный прокси;
- приложения, где удобнее один порт вместо двух.

Пример:

```json
{
  "type": "mixed",
  "tag": "mixed-in",
  "listen": "127.0.0.1",
  "listen_port": 2080,
  "users": [
    {
      "username": "agent",
      "password": "strong-password"
    }
  ]
}
```

Типовые ошибки:

- слушает на `0.0.0.0` без необходимости;
- забыта авторизация в небезопасной сети;
- ожидается transparent behavior, которого mixed не даёт.

## SOCKS

Назначение: только SOCKS server.

Плюсы:

- минимальная совместимость;
- проще клиентская интеграция для CLI и системных приложений.

Минусы:

- HTTP-клиенты без SOCKS-поддержки не подключатся напрямую.

## HTTP

Назначение: HTTP proxy, опционально с TLS.

Пример:

```json
{
  "type": "http",
  "tag": "http-in",
  "listen": "127.0.0.1",
  "listen_port": 8080,
  "users": [
    {
      "username": "agent",
      "password": "strong-password"
    }
  ]
}
```

Типовые ошибки:

- ожидание, что HTTP proxy покрывает все non-HTTP сценарии;
- включение TLS без корректного сертификата;
- путаница между `set_system_proxy` и TUN/transparent proxy.

## TUN

Назначение: виртуальный сетевой интерфейс для захвата трафика на уровне IP.

Когда использовать:

- full-tunnel или split-tunnel на клиенте;
- шлюз, router, VPS-маршрутизация;
- transparent UX без настройки proxy в приложениях.

Ключевые поля:

- `interface_name`
- `address`
- `mtu`
- `auto_route`
- `auto_redirect`
- `route_address`
- `route_exclude_address`
- `stack`

Типовые ошибки:

- использование deprecated `inet4_*` и `inet6_*` полей;
- конфликт маршрутов с Docker/bridge;
- отсутствие прав на поднятие интерфейса;
- DNS проходит мимо `sing-box`.

## Redirect

Назначение: transparent redirect inbound для Linux/macOS.

Когда использовать:

- трафик уже перенаправлен firewall/NAT на локальный порт;
- нужен простой TCP redirect без TProxy semantics.

Ошибка:

- попытка использовать его как полноценную замену `tproxy` для всех UDP/TCP сценариев.

## TProxy

Назначение: Linux transparent proxy inbound с сохранением оригинального назначения.

Когда использовать:

- маршрутизатор;
- OpenWrt/Linux gateway;
- сложная прозрачная маршрутизация с TCP и UDP.

Пример:

```json
{
  "type": "tproxy",
  "tag": "tproxy-in",
  "listen": "::",
  "listen_port": 60080,
  "network": "tcp"
}
```

Типовые ошибки:

- забыты policy routing и marks;
- firewall rules отправляют трафик не в тот inbound;
- UDP не перехватывается, хотя inbound создан только для TCP.

## Direct inbound

Назначение: tunnel server.

Использование:

- приёмы трафика с опциональным `override_address` и `override_port`;
- server-side service tunneling.

Пример:

```json
{
  "type": "direct",
  "tag": "direct-in",
  "listen": "0.0.0.0",
  "listen_port": 5353,
  "network": "udp",
  "override_address": "1.1.1.1",
  "override_port": 53
}
```

## Рекомендации по выбору

- локальный агент/браузер: `mixed`
- SOCKS-only экосистема: `socks`
- HTTP proxy deployment: `http`
- user-transparent client mode: `tun`
- router transparent interception: `tproxy` или `tun + auto_redirect`
- service-level redirect: `redirect`
