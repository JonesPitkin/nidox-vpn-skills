# Защита базы и резервных копий

> Проверено по 3X-UI `v3.3.0`.

## Что содержит backup

Новые модели могут включать outbound subscriptions, API tokens/settings, multi-node metadata и MTProto inbound secrets. После upgrade проверять, что backup/restore переносит их вместе с inbounds и clients.

SQLite/PostgreSQL backup может содержать panel users, client UUID/passwords, subscription data, routing, Telegram settings и другие секреты. Certificate archive может содержать private keys.

## SQLite

Default path в официальной установке: `/etc/x-ui/x-ui.db`.

Безопасная файловая копия:

```sh
systemctl stop x-ui
install -d -m 700 /root/3x-ui-backups
cp --preserve=mode,ownership /etc/x-ui/x-ui.db /root/3x-ui-backups/x-ui-$(date +%F).db
chmod 600 /root/3x-ui-backups/x-ui-*.db
systemctl start x-ui
```

Либо использовать SQLite backup API/command при подтвержденной доступности. Не копировать actively changing DB без консистентной процедуры.

## PostgreSQL

```sh
umask 077
pg_dump --format=custom "$XUI_DB_DSN" > /root/3x-ui-backups/x-ui-$(date +%F).dump
```

Не помещать DSN в command history/process list. Предпочитать `.pgpass` с mode `0600` или controlled environment.

## Хранение

- owner root/service account, mode `0600`, directory `0700`;
- encryption before off-host upload;
- отдельные credentials для backup storage;
- retention и удаление старых copies;
- периодический restore test в изолированную среду;
- не коммитить DB/certs/.env.

## Проверка

```sh
stat /etc/x-ui/x-ui.db /root/3x-ui-backups/*
sha256sum /root/3x-ui-backups/<file>
```

Hash проверяет целостность, не конфиденциальность.

## Ошибки

- Backup отправлен в публичный чат/issue.
- Restore выполнен поверх live DB без остановки.
- Archive содержит readable private key.
- Backup есть, но не тестировался и поврежден.

## Источники

- [3X-UI database source/config](https://github.com/MHSanaei/3x-ui/tree/v3.3.0/database)
- [3X-UI Wiki installation/database](https://github.com/MHSanaei/3x-ui/wiki/Installation)
- [PostgreSQL pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html)
- [SQLite backup](https://www.sqlite.org/backup.html)
