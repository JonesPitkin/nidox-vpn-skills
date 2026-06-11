# SplitHTTP / XHTTP

## Описание

В актуальном 3X-UI transport называется `XHTTP`, wire field — `network: "xhttp"`, settings — `xhttpSettings`. В исходниках он описан как modern `SplitHTTPConfig`; старые инструкции могут называть его SplitHTTP.

## Когда использовать

- актуальный Xray client/server;
- HTTP-aware paths, CDN/reverse proxy experiments;
- packet/stream modes для сетей, где TCP REALITY нестабилен;
- только после проверки client version.

## Преимущества

- modes `auto`, `packet-up`, `stream-up`, `stream-one`;
- path/host/headers и padding;
- REALITY и TLS разрешены в 3X-UI;
- 3X-UI генерирует URL extra fields и Clash `xhttp-opts`.

## Недостатки

- быстро меняющийся transport;
- большая матрица options и несовместимость parsers;
- официальный sing-box V2Ray transport список XHTTP не содержит;
- Podkop/sing-box path не считать поддержанным;
- CDN/WAF может блокировать methods/body/SSE.

## Требования

- актуальный Xray core на обеих сторонах;
- совпадающие mode/path/host и extra options;
- HTTP infrastructure, пропускающая выбранный mode/method;
- отдельная проверка client parser.

## Настройка в панели

Начать минимально:

- host/path;
- mode `auto` или явно подтвержденный client mode;
- default padding `100-1000`;
- не включать obfs placement/XMUX/custom GET до baseline.

Mode fields:

- `packet-up`: max buffered posts, post bytes, optional GET;
- `stream-up`: server seconds;
- `stream-one`: single stream behavior;
- `auto`: core decides, но некоторые client versions требовали explicit mode.

Security:

- direct: REALITY;
- CDN/reverse proxy: TLS;
- Vision не применяется.

## Настройка клиента

- v2rayNG: VLESS+XHTTP подтверждается upstream issues, но behavior менялся между core versions; обновлять и явно сверять mode.
- Shadowrocket: release notes 2026 подтверждают XHTTP fixes/options; использовать текущую версию и минимальные fields.
- sing-box: официальная transport schema не перечисляет XHTTP. TODO: повторно проверить при обновлении sing-box.
- Podkop: URL/custom outbound основан на sing-box; XHTTP не рекомендовать без подтвержденного parser/core support.

## Типовые ошибки

- config импортирован как TCP/unknown;
- `mode=auto` не определился;
- 405 от CDN из-за HTTP method;
- upload работает плохо, download работает;
- extra JSON fields потеряны subscription converter;
- path/padding/session placement mismatch.

## Диагностика

1. Xray-to-Xray client, без CDN.
2. Explicit mode.
3. Default padding/options.
4. Затем reverse proxy/CDN.
5. Сравнить generated URL `type=xhttp`, `mode`, `path`, `host`, `extra`.

Проверить HTTP status/access logs и Xray logs. Не отлаживать XHTTP через sing-box, если его версия официально не заявляет transport.

## Источники

- [XHTTP schema](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/schemas/protocols/stream/xhttp.ts)
- [XHTTP form](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/pages/inbounds/form/transport/xhttp.tsx)
- [3X-UI URL generator](https://github.com/MHSanaei/3x-ui/blob/main/sub/subService.go)
- [3X-UI Clash generator](https://github.com/MHSanaei/3x-ui/blob/main/sub/subClashService.go)
- [v2rayNG repository](https://github.com/2dust/v2rayNG)
- [Shadowrocket App Store](https://apps.apple.com/us/app/shadowrocket/id932747118)
- [sing-box transports](https://sing-box.sagernet.org/configuration/shared/v2ray-transport/)
