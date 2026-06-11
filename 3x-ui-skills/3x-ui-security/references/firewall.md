# Firewall

## Принцип

Разрешать только текущий SSH, TLS/reverse proxy и реально используемые inbound ports. Panel port открывать только trusted source либо не открывать публично.

## UFW procedure

1. Узнать текущий SSH port:

```sh
ss -lntp
```

2. Сначала разрешить его:

```sh
ufw allow <ssh-port>/tcp
```

3. Разрешить нужные services:

```sh
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow <inbound-port>/tcp
ufw allow <hysteria-port>/udp
ufw allow from <admin-ip> to any port <panel-port> proto tcp
```

4. Проверить и только затем enable:

```sh
ufw status numbered
ufw enable
```

## Docker/LXC

Docker может управлять iptables/nftables вне ожидаемой UFW policy; проверять опубликованные ports и полный ruleset. В unprivileged LXC firewall/NET_ADMIN может контролироваться host.

```sh
docker ps --format 'table {{.Names}}\t{{.Ports}}'
nft list ruleset
```

## Ошибки

- Разрешен TCP, но inbound использует UDP.
- Docker port остается public несмотря на UFW expectation.
- Cloudflare proxied origin разрешает весь Internet вместо Cloudflare IP ranges.
- Старый panel port остается открыт.

## Проверка

С внешней разрешенной и запрещенной сети проверить конкретные ports. Не полагаться только на локальный `ss`.

## Источники

- [3X-UI Wiki FAQ: firewall](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems)
- [x-ui firewall management](https://github.com/MHSanaei/3x-ui/blob/main/x-ui.sh)
- [Ubuntu UFW](https://documentation.ubuntu.com/server/how-to/security/firewalls/)
