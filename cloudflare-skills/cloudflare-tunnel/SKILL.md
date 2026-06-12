---
name: cloudflare-tunnel
description: Настраивать и объяснять Cloudflare Tunnel и cloudflared: public hostnames, ingress-модель, private network routing, local services и homelab-публикацию без inbound-портов.
---

# Cloudflare Tunnel

Используй этот skill, когда нужно подключить сервис к Cloudflare без прямой публикации origin IP и без входящего порта на маршрутизаторе или межсетевом экране.

## Базовая модель

- `cloudflared` поднимает outbound-only соединение от origin к Cloudflare.
- Tunnel отвечает за сетевой путь между origin и Cloudflare.
- Вопросы identity, Access policies, Cloudflare One Client и service tokens относятся к `cloudflare-zero-trust`, а не к этому модулю.
- Tunnel не надо описывать как "обычный A record на домашний IP"; это отдельная модель подключения.

## Типовые сценарии

- Публикация self-hosted веб-приложения по public hostname.
- Публикация homelab dashboard или panel без открытия inbound-порта.
- Подключение private network / CIDR к Cloudflare через Tunnel.
- Сетевое подключение локального сервиса к Cloudflare без прямого входящего доступа на origin.

## Рабочий процесс

1. Определи, нужен public hostname или private network route.
2. Если сервис должен быть доступен из Интернета как веб-приложение, проектируй public hostname поверх Tunnel.
3. Если сервис должен быть доступен только авторизованным пользователям или устройствам, сначала проектируй Tunnel-path, а затем при необходимости передавай задачу в `cloudflare-zero-trust`.
4. Зафиксируй, какой local service публикуется и по какому протоколу.
5. Проверяй Tunnel отдельно от DNS, Access policy и origin application.

## Практические правила

- Для homelab Tunnel часто безопаснее прямой публикации origin IP.
- Для private access через Cloudflare Zero Trust нужно проектировать не только Tunnel, но и отдельный policy-слой из `cloudflare-zero-trust`.
- Если задача сводится к "спрятать домашний origin и не открывать порт", Tunnel должен быть первым кандидатом.
- Не смешивай public hostname для браузерного доступа и private CIDR routing для внутренней сети как одну и ту же функцию Cloudflare Tunnel.

## Что не делать

- Не описывать Tunnel как требующий публичный routable IP на origin.
- Не путать standard proxied DNS и Tunnel как один и тот же механизм.
- Не выдумывать ingress-настройки, которых нет в официальной документации.

## Где брать официальные ссылки

Все официальные ссылки для этого skill перечислены в [references/sources.md](references/sources.md).
