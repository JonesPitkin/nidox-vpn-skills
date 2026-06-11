# Обновление и миграция

## Содержание

1. Подготовка
2. Native update
3. Docker update
4. Перенос на новый сервер
5. SQLite и PostgreSQL
6. Rollback
7. Ошибки
8. Источники

## 1. Подготовка

Перед обновлением:

```sh
x-ui settings
/usr/local/x-ui/x-ui -v
systemctl status x-ui --no-pager -l
cp -a /etc/x-ui "/root/x-ui-backup-$(date +%F-%H%M%S)"
```

Сохранить также `/etc/default/x-ui` на Ubuntu/Debian, сертификаты, Docker compose/env и список ports. Для PostgreSQL создать `pg_dump`, см. `backup.md`.

Проверить latest release и release notes:

```sh
curl -fsSL https://api.github.com/repos/MHSanaei/3x-ui/releases/latest
```

## 2. Native update

Штатная команда:

```sh
x-ui update
```

Management script предупреждает, что обновляет все компоненты и сохраняет данные. `update.sh`:

- получает latest tag;
- скачивает release archive;
- останавливает и временно удаляет старую service unit;
- заменяет binaries/scripts;
- восстанавливает unit и autostart;
- запускает panel migration;
- проверяет settings и TLS.

Не считать фразу “data will not be lost” заменой backup.

Проверка:

```sh
/usr/local/x-ui/x-ui -v
x-ui status
x-ui settings
journalctl -u x-ui -n 150 --no-pager
```

Затем проверить panel login, Xray state, clients/inbounds и фактический трафик.

Обновление только management menu:

```sh
x-ui
```

Выбрать `Update Menu`. Не использовать как замену обновлению panel binary.

## 3. Docker update

Compose:

```sh
cd /opt/3x-ui
docker compose config
docker compose down
docker compose pull
docker compose up -d
docker compose ps
docker compose logs --tail=150 3xui
```

Проверить, что bind mounts остались теми же:

```sh
docker inspect 3xui_app --format '{{json .Mounts}}'
```

Для PostgreSQL profile:

```sh
docker compose --profile postgres up -d
```

CLI container:

```sh
docker stop 3x-ui
docker rm 3x-ui
docker pull ghcr.io/mhsanaei/3x-ui:latest
# Повторить исходный docker run с теми же volumes, env, caps и network.
```

Не выполнять `docker system prune -a` как обязательный шаг обновления. Он удаляет неиспользуемые images/cache и может затронуть другие workloads.

Для воспроизводимости можно pin image tag вместо `latest`, но актуальный поддерживаемый tag сначала сверять в Releases. TODO: Wiki показывает `latest` и не описывает официальный pin/rollback policy.

## 4. Перенос на новый сервер

### SQLite native → native

1. На старом сервере записать version и settings.
2. Остановить панель:
   ```sh
   x-ui stop
   ```
3. Скопировать `/etc/x-ui/x-ui.db`, env file и необходимые cert files.
4. Установить на новом сервере ту же или более новую поддерживаемую версию.
5. Остановить новую панель.
6. Поместить DB в `/etc/x-ui/x-ui.db`, проверить owner/mode по созданному installer файлу.
7. Запустить и выполнить update/migration:
   ```sh
   x-ui start
   x-ui update
   ```
8. Проверить настройки, TLS paths, public IP/domain и все listeners.

Wiki FAQ советует после переноса DB обновить panel, если traffic counters стали нулевыми.

### Docker → Docker

Переносить compose/env и persistent directories `db`, `cert`; для PostgreSQL также `pgdata` или логический dump. На destination сначала не публиковать panel наружу, пока credentials/TLS не проверены.

## 5. SQLite и PostgreSQL

### SQLite → PostgreSQL

README показывает `x-ui migrate-db`, но текущий management wrapper `x-ui.sh` не
маршрутизирует lowercase subcommand к binary. Использовать binary напрямую:

```sh
/usr/local/x-ui/x-ui migrate-db \
  --dsn "postgres://USER:PASSWORD@HOST:5432/DB?sslmode=disable"
```

Она копирует данные из configured SQLite source в PostgreSQL и оставляет source file нетронутым. Затем на Ubuntu/Debian:

Сохранить `XUI_DB_TYPE=postgres` и `XUI_DB_DSN=...` в
`/etc/default/x-ui`, не удаляя другие существующие переменные, установить mode
`600` и перезапустить:

```sh
chmod 600 /etc/default/x-ui
systemctl restart x-ui
```

Не выводить реальный DSN в отчеты. Перед миграцией destination DB должна быть выделена панели: реализация очищает panel tables в destination.

Проверить:

```sh
x-ui settings
systemctl status x-ui --no-pager -l
journalctl -u x-ui -n 150 --no-pager
```

### SQLite portable dump

Management script:

```sh
x-ui migrateDB /etc/x-ui/x-ui.db /root/x-ui.dump
```

Restore в отдельный путь:

```sh
x-ui migrateDB /root/x-ui.dump /root/restored-x-ui.db
```

Wrapper определяет направление по extension/header. Restore в live `/etc/x-ui/x-ui.db` отклоняется, пока panel запущена.

Binary equivalents:

```sh
/usr/local/x-ui/x-ui migrate-db --src /etc/x-ui/x-ui.db --dump /root/x-ui.dump
/usr/local/x-ui/x-ui migrate-db --restore /root/x-ui.dump --out /root/restored-x-ui.db
```

### PostgreSQL backup/restore

Panel использует `pg_dump` и `pg_restore`; на Ubuntu/Debian нужен `postgresql-client`. Проверять:

```sh
command -v pg_dump
command -v pg_restore
```

UI `Backup & Restore` скачивает `.dump`; restore загружает его через `pg_restore`.

## 6. Rollback

Native:

1. Остановить service.
2. Вернуть проверенный DB backup и env/cert paths.
3. Установить конкретный старый release только если он доступен и совместим с уже мигрированной schema.
4. Запустить и проверить logs.

Официальная Wiki показывает legacy installation, но предупреждает, что она не рекомендуется. Автоматическая обратная совместимость DB не обещана.

TODO: проверить, исправил ли upstream расхождение README `x-ui migrate-db` и
dispatch в `x-ui.sh` после зафиксированного commit.

Docker:

```sh
docker compose down
# Вернуть прежний image tag и backup volumes/data.
docker compose up -d
```

Нельзя считать rollback безопасным без pre-update backup: новая версия могла мигрировать schema.

## 7. Ошибки

**Не скачивается GitHub:** проверить DNS/IPv4, использовать installer/update retry по IPv4; не использовать случайные mirrors.

**После update panel не открывается:** `x-ui status`, `x-ui settings`, `journalctl`; Wiki рекомендует `Reset Settings` при Xray/panel SSL issue, но сначала записать текущие settings и backup.

**После migration counters нулевые:** обновить panel, проверить Xray config и что API routing rule стоит первой, согласно FAQ.

**PostgreSQL backup недоступен:** установить `postgresql-client`, проверить PATH и совместимость client/server versions.

## 8. Источники

- [README: database migration](https://github.com/MHSanaei/3x-ui/blob/main/README.md#database-options)
- [Official update.sh](https://github.com/MHSanaei/3x-ui/blob/main/update.sh)
- [Official x-ui.sh](https://github.com/MHSanaei/3x-ui/blob/main/x-ui.sh)
- [Wiki: Docker update and legacy install](https://github.com/MHSanaei/3x-ui/wiki/Installation)
- [Wiki: Common Questions & Problems](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems)
- [Database migration implementation](https://github.com/MHSanaei/3x-ui/blob/main/database/migrate_data.go)
- [SQLite dump implementation](https://github.com/MHSanaei/3x-ui/blob/main/database/dump_sqlite.go)
