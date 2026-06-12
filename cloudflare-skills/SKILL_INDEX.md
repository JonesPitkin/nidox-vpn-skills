# SKILL_INDEX

Индекс production-skills по `cloudflare-skills`.

## Модули

### `cloudflare-basics`

Использовать когда нужно:

- понять, как Cloudflare стоит между клиентом и origin;
- различить `Proxied`, `DNS only`, Tunnel и Zero Trust;
- объяснить edge network, Anycast, reverse proxy и CDN;
- выбрать правильную базовую архитектуру до детальной настройки.

Краткое описание:

Базовый модуль, который задаёт терминологию, архитектурные границы и модель трафика для всех остальных разделов.

### `cloudflare-dns`

Использовать когда нужно:

- выбрать `A`, `AAAA`, `CNAME`, `MX`, `TXT`, `NS` или `SRV`;
- определить `Proxied` или `DNS only`;
- разобраться с DNSSEC;
- спроектировать публикацию домена через Cloudflare DNS.

Краткое описание:

Модуль по DNS-записям, proxy status и доменной публикации.

### `cloudflare-ssl-tls`

Использовать когда нужно:

- выбрать `Flexible`, `Full` или `Full (strict)`;
- объяснить разницу между edge certificate и origin certificate;
- использовать `Universal SSL` и `Origin CA`;
- построить корректную TLS-схему для origin reverse proxy.

Краткое описание:

Модуль по SSL/TLS-архитектуре между клиентом, Cloudflare и origin.

### `cloudflare-proxy-cdn`

Использовать когда нужно:

- проверить standard Cloudflare Proxy/CDN;
- понять кэширование и поведение заголовков;
- проверить WebSocket и supported ports;
- восстановить реальный клиентский IP на origin.

Краткое описание:

Модуль по HTTP/HTTPS reverse proxy, кэшу, заголовкам и edge-поведению.

### `cloudflare-tunnel`

Использовать когда нужно:

- опубликовать сервис без inbound-порта;
- использовать `cloudflared`;
- настроить public hostname;
- подключить private network routing через Tunnel.

Краткое описание:

Модуль по Cloudflare Tunnel как connector-модели между origin и Cloudflare.

### `cloudflare-zero-trust`

Использовать когда нужно:

- защитить приложение через Access;
- выбрать policy-модель;
- подключить identity provider;
- использовать Cloudflare One Client, WARP и service tokens.

Краткое описание:

Модуль по identity-driven доступу и Zero Trust-политикам.

### `cloudflare-security`

Использовать когда нужно:

- включить или проверить WAF;
- проектировать custom rules;
- применять rate limiting;
- разобрать bot-related controls и DDoS protection.

Краткое описание:

Модуль по security-контролям Cloudflare на edge-уровне.

### `cloudflare-vpn-integration`

Использовать когда нужно:

- встроить Cloudflare в VPN- или homelab-схему;
- определить допустимую Cloudflare-side архитектуру для OpenWrt, sing-box, 3x-ui или Nginx Proxy Manager;
- разделить supported web publication и direct transport;
- выбрать между `Proxied`, `DNS only`, Tunnel и Zero Trust в интеграционном сценарии.

Краткое описание:

Интеграционный модуль, который собирает решения из остальных разделов и применяет их к VPN- и homelab-контексту.

## Зависимости между модулями

```text
cloudflare-basics
  -> cloudflare-dns
  -> cloudflare-ssl-tls
  -> cloudflare-proxy-cdn
  -> cloudflare-tunnel
  -> cloudflare-zero-trust
  -> cloudflare-security
  -> cloudflare-vpn-integration

cloudflare-dns
  -> cloudflare-proxy-cdn
  -> cloudflare-ssl-tls
  -> cloudflare-vpn-integration

cloudflare-ssl-tls
  -> cloudflare-proxy-cdn
  -> cloudflare-vpn-integration

cloudflare-tunnel
  -> cloudflare-zero-trust
  -> cloudflare-vpn-integration

cloudflare-zero-trust
  -> cloudflare-vpn-integration

cloudflare-security
  -> cloudflare-vpn-integration
```

## Рекомендуемый порядок изучения

1. `cloudflare-basics`
2. `cloudflare-dns`
3. `cloudflare-ssl-tls`
4. `cloudflare-proxy-cdn`
5. `cloudflare-tunnel`
6. `cloudflare-zero-trust`
7. `cloudflare-security`
8. `cloudflare-vpn-integration`

## Быстрый роутинг по запросам

Если вопрос начинается с:

- "как устроен Cloudflare" -> `cloudflare-basics`
- "какую DNS-запись выбрать" -> `cloudflare-dns`
- "какой SSL/TLS mode нужен" -> `cloudflare-ssl-tls`
- "что делает orange cloud / proxy / cache" -> `cloudflare-proxy-cdn`
- "как опубликовать без открытого порта" -> `cloudflare-tunnel`
- "как ограничить доступ по identity" -> `cloudflare-zero-trust`
- "как защитить сервис на edge" -> `cloudflare-security`
- "как встроить это в VPN или homelab" -> `cloudflare-vpn-integration`
