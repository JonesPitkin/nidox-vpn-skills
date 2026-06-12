# Fail2Ban и IP Limit

> Проверено по 3X-UI `v3.3.0`.

## Что защищает интеграция

3X-UI использует Xray access log и Fail2Ban для ограничения числа IP, использующих client. Это помогает против sharing. Не считать этот jail полноценной защитой panel login.

## Требования

В official Docker image Fail2Ban включён по умолчанию через `XUI_ENABLE_FAIL2BAN=true`. Для применения ban rules контейнеру нужны `NET_ADMIN`, а для IPv6 также `NET_RAW`; без capabilities события могут логироваться без фактической блокировки.

В актуальной ветке panel/SSH ports исключаются из IP-limit ban logic. Это не превращает IP-limit jail в защиту panel login.

- Fail2Ban установлен/запущен;
- Xray access log включен;
- client имеет IP limit;
- firewall backend способен применять ban;
- Docker получает `NET_ADMIN`, а для IPv6 rules также `NET_RAW` согласно официальному compose/entrypoint.

Пример logging:

```json
{
  "log": {
    "access": "./access.log",
    "dnsLog": false,
    "error": "./error.log",
    "loglevel": "warning"
  }
}
```

## Настройка

```sh
x-ui
# IP Limit Management
```

В menu доступны install Fail2Ban, update geo files, view logs, ban/unban IP и service status/restart.

## Проверка

```sh
systemctl status fail2ban --no-pager
fail2ban-client status
fail2ban-client status 3x-ipl
x-ui banlog
```

Проверить test client с контролируемых IP, не блокируя собственный административный доступ.

## Ошибки

- Bans видны в log, но не применяются: нет NET_ADMIN/firewall access.
- Access log выключен или path не совпадает.
- NAT заставляет многих legit users выглядеть одним IP.
- IPv6 остается неблокированным.
- Ожидается защита `/login`, но jail анализирует Xray clients.

## Источники

- [3X-UI Wiki: Fail2Ban](https://github.com/MHSanaei/3x-ui/wiki/Configuration)
- [3X-UI Docker entrypoint](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/DockerEntrypoint.sh)
- [Fail2Ban](https://github.com/fail2ban/fail2ban)
