# HTTPUpgrade

## Описание

`network=httpupgrade` использует HTTP Upgrade с path, host и headers. По форме похож на WebSocket, но без WS framing/heartbeat.

## Когда использовать

- reverse proxy/CDN явно поддерживает generic HTTP Upgrade;
- WS нежелателен, а XHTTP не поддерживается клиентом;
- sing-box клиент с HTTPUpgrade.

## Преимущества

- path/host routing;
- меньше WS-specific полей;
- официально поддержан sing-box V2Ray transport.

## Недостатки

- поддержка proxy/CDN менее предсказуема, чем WS;
- REALITY не разрешен текущей 3X-UI формой;
- старые clients могут не знать `httpupgrade`.

## Требования

- proxy/CDN должен пропускать HTTP Upgrade;
- одинаковые host/path;
- TLS для public deployment;
- клиент с HTTPUpgrade transport.

## Настройка в панели

- Transport HTTPUpgrade;
- path `/upgrade`;
- host public domain;
- TLS для public endpoint;
- `acceptProxyProtocol=false` без L4 proxy.

## Настройка клиента

Share link: `type=httpupgrade`, `path`, `host`.

sing-box:

```json
"transport": {
  "type": "httpupgrade",
  "host": "<domain>",
  "path": "/upgrade",
  "headers": {}
}
```

v2rayNG/Shadowrocket: обновить до версии с HTTPUpgrade и проверить импорт. Podkop зависит от sing-box parser/custom outbound.

## Типовые ошибки

- 404/405 от proxy;
- Upgrade header удален;
- path отличается trailing slash;
- клиент интерпретирует как WS.

## Диагностика

Проверить proxy access log/status codes, backend listener и точные headers. Временно обходить proxy и подключаться к origin.

## Источники

- [HTTPUpgrade schema](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/schemas/protocols/stream/httpupgrade.ts)
- [HTTPUpgrade form](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/pages/inbounds/form/transport/httpupgrade.tsx)
- [sing-box HTTPUpgrade](https://sing-box.sagernet.org/configuration/shared/v2ray-transport/)
