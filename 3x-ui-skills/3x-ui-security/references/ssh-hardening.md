# SSH Hardening

## Цель

SSH остается аварийным каналом управления. Смена port уменьшает шум, но основная защита — keys, ограничение users/sources, отключение password/root login и актуальный OpenSSH.

## Безопасная последовательность

1. Открыть вторую SSH/console session.
2. Создать отдельного sudo user.
3. Установить public key и проверить вход.
4. Проверить effective config:

```sh
sshd -t
sshd -T | grep -E 'passwordauthentication|permitrootlogin|pubkeyauthentication'
```

5. В drop-in, соответствующем distro policy, задать:

```text
PubkeyAuthentication yes
PasswordAuthentication no
PermitRootLogin no
```

6. При смене port сначала разрешить новый в firewall.
7. Reload SSH, открыть новую session, затем закрывать старую.

```sh
systemctl reload ssh
```

На некоторых системах service называется `sshd`; проверить локально.

## Дополнительные меры

- `AllowUsers`/`AllowGroups`;
- source allowlist/VPN;
- короткий `LoginGraceTime`, разумный `MaxAuthTries`;
- защита ключа passphrase и ротация.

## Ошибки

- Отключен root/password до проверки sudo key user.
- Изменен не тот config/drop-in.
- Firewall не разрешает новый port.
- Cloud-init/provider перезаписывает настройки.

## Источники

- [OpenSSH sshd_config](https://man.openbsd.org/sshd_config)
- [3X-UI Wiki FAQ: SSH port](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems)

Ограничение источников: distro-specific drop-in precedence проверять по установленному Ubuntu/Debian OpenSSH package, а не переносить путь между версиями.
