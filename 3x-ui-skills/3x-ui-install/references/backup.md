# Резервное копирование и восстановление

## Содержание

1. Что сохранять
2. SQLite
3. PostgreSQL
4. Docker
5. Панель и Telegram
6. Проверка восстановления
7. Ошибки
8. Источники

## 1. Что сохранять

Минимум:

- SQLite: `/etc/x-ui/x-ui.db`;
- PostgreSQL: logical dump и DSN отдельно;
- Ubuntu/Debian env: `/etc/default/x-ui`;
- certificates: фактические paths из `x-ui settings`/certificate settings;
- Docker: compose file, env/secrets и bind volumes `db`, `cert`, при PostgreSQL `pgdata` или dump;
- версия panel и management settings;
- firewall/reverse proxy configs, если они нужны для восстановления доступа.

Не включать backups в публичные репозитории. Они содержат credentials, client IDs, API tokens и connection data.

## 2. SQLite

### Штатный UI backup

На dashboard открыть `Backup & Restore` и скачать `x-ui.db`. README/Wiki заявляют export/import database.

### Консистентная файловая копия

Самый простой безопасный runbook:

```sh
install -d -m 700 /root/backup-3x-ui
x-ui stop
cp -a /etc/x-ui/x-ui.db "/root/backup-3x-ui/x-ui-$(date +%F-%H%M%S).db"
x-ui start
```

Проверка:

```sh
test -s /root/backup-3x-ui/x-ui-*.db
file /root/backup-3x-ui/x-ui-*.db
sha256sum /root/backup-3x-ui/x-ui-*.db
```

### Portable SQL dump

```sh
x-ui migrateDB /etc/x-ui/x-ui.db "/root/backup-3x-ui/x-ui-$(date +%F-%H%M%S).dump"
```

Проверить восстановлением в новый файл:

```sh
x-ui migrateDB /root/backup-3x-ui/x-ui-YYYY-MM-DD-HHMMSS.dump /root/backup-3x-ui/test-restore.db
file /root/backup-3x-ui/test-restore.db
```

### Restore SQLite

1. Сделать backup текущего состояния.
2. Остановить panel:
   ```sh
   x-ui stop
   ```
3. Восстановить в отдельный файл и проверить.
4. Заменить live DB:
   ```sh
   cp -a /etc/x-ui/x-ui.db /etc/x-ui/x-ui.db.before-restore
   cp /root/backup-3x-ui/test-restore.db /etc/x-ui/x-ui.db
   ```
5. Сохранить owner/mode прежнего файла.
6. Запустить:
   ```sh
   x-ui start
   journalctl -u x-ui -n 150 --no-pager
   ```

## 3. PostgreSQL

Installer устанавливает `postgresql-client` для in-panel backup/restore. Проверить:

```sh
command -v pg_dump
command -v pg_restore
```

UI backup скачивает `x-ui.dump`, restore использует `pg_restore`.

CLI example:

```sh
PGPASSWORD='<password>' pg_dump \
  -h <host> -p 5432 -U <user> -d <database> \
  -Fc -f "/root/backup-3x-ui/x-ui-$(date +%F-%H%M%S).dump"
```

Не помещать password в командную строку в реальном automation: использовать `.pgpass`, environment с ограниченным scope или secret manager.

Проверка архива:

```sh
pg_restore --list /root/backup-3x-ui/x-ui-*.dump | sed -n '1,40p'
```

Restore выполнять в тестовую/пустую database либо через panel UI. Реализация panel останавливает Xray/DB operations и пытается не менять database при failed restore, но backup перед restore обязателен.

Ограничение источников: официальный Wiki не дает отдельного полного CLI runbook для PostgreSQL restore и гарантии совместимости версий. Перед production restore сверить PostgreSQL docs для установленных server/client и актуальную реализацию `web/service/server.go`.

## 4. Docker

SQLite compose:

```sh
cd /opt/3x-ui
docker compose stop 3xui
tar -C /opt/3x-ui -czf "/root/3x-ui-docker-$(date +%F-%H%M%S).tar.gz" \
  docker-compose.yml db cert
docker compose start 3xui
```

Проверить:

```sh
tar tzf /root/3x-ui-docker-*.tar.gz | sed -n '1,80p'
docker compose ps
```

PostgreSQL container: предпочтительнее logical `pg_dump` через container, а не копирование live `pgdata`:

```sh
docker exec 3xui_postgres pg_dump -U xui -d xui -Fc \
  > "/root/x-ui-postgres-$(date +%F-%H%M%S).dump"
```

Пароли и имена заменить фактическими. Проверить ненулевой размер и `pg_restore --list` в совместимом client container/host.

## 5. Панель и Telegram

Dashboard `Backup & Restore`:

- SQLite backup: `.db`;
- PostgreSQL backup: `pg_dump .dump`;
- migration download предоставляет cross-engine artifact;
- import является destructive restore.

Telegram bot может отправлять database backup с periodic report: включить `Database Backup` и задать `Notification Time`. Это дополнительная копия, не единственная стратегия. Доступ к Telegram chat/token защищать как секрет.

## 6. Проверка восстановления

Backup не считается проверенным, пока:

- файл читается и checksum записан;
- SQLite dump разворачивается в отдельный `.db` или PostgreSQL dump проходит `pg_restore --list`;
- test instance запускается;
- присутствуют users, settings, inbounds, clients и traffic data;
- Xray config формируется без ошибки;
- credentials и TLS paths понятны после переноса.

## 7. Ошибки

**`database is locked`:** FAQ связывает это со слабым/медленным диском и рекомендует отключить access log. Для backup сначала остановить panel и повторить.

**Restore live DB при запущенной панели:** `x-ui migrateDB` специально отказывает. Остановить panel или восстановить в другой output.

**Пустой Docker backup:** проверить bind mounts через `docker inspect`; возможно данные находятся не в ожидаемом host directory.

**`pg_dump not found`:**

```sh
apt-get update
apt-get install -y postgresql-client
```

## 8. Источники

- [README: export/import and database options](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/README.md)
- [Wiki: Telegram database backup](https://github.com/MHSanaei/3x-ui/wiki/Advanced)
- [Wiki FAQ: backup schedule and database errors](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems)
- [x-ui.sh migrateDB implementation](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/x-ui.sh)
- [Server backup/restore implementation](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/web/service/server.go)
- [Backup controller](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/web/controller/server.go)
- [SQLite dump/restore](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/database/dump_sqlite.go)
