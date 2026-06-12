# SKILL_DEPENDENCIES

## Зависимости между модулями

### `cloudflare-basics`

Базовый модуль для:

- `cloudflare-dns`
- `cloudflare-ssl-tls`
- `cloudflare-proxy-cdn`
- `cloudflare-tunnel`
- `cloudflare-zero-trust`
- `cloudflare-security`
- `cloudflare-vpn-integration`

### `cloudflare-dns`

Зависит от:

- `cloudflare-basics`

Используется вместе с:

- `cloudflare-proxy-cdn`
- `cloudflare-ssl-tls`
- `cloudflare-vpn-integration`

### `cloudflare-ssl-tls`

Зависит от:

- `cloudflare-basics`
- `cloudflare-dns`

Используется вместе с:

- `cloudflare-proxy-cdn`
- `cloudflare-vpn-integration`

### `cloudflare-proxy-cdn`

Зависит от:

- `cloudflare-basics`
- `cloudflare-dns`
- `cloudflare-ssl-tls`

Используется вместе с:

- `cloudflare-vpn-integration`

### `cloudflare-tunnel`

Зависит от:

- `cloudflare-basics`

Используется вместе с:

- `cloudflare-zero-trust`
- `cloudflare-vpn-integration`

### `cloudflare-zero-trust`

Зависит от:

- `cloudflare-basics`
- `cloudflare-tunnel`

Используется вместе с:

- `cloudflare-vpn-integration`

### `cloudflare-security`

Зависит от:

- `cloudflare-basics`

Используется вместе с:

- `cloudflare-vpn-integration`

### `cloudflare-vpn-integration`

Интеграционный модуль, который собирает решения из:

- `cloudflare-basics`
- `cloudflare-dns`
- `cloudflare-ssl-tls`
- `cloudflare-proxy-cdn`
- `cloudflare-tunnel`
- `cloudflare-zero-trust`
- `cloudflare-security`
