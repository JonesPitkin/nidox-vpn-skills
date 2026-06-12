# XHTTP через Cloudflare

## Совместимость

XHTTP использует HTTP semantics, но его modes предъявляют разные требования к upload/download streams. Cloudflare compatibility нельзя выводить только из факта поддержки HTTPS.

Проверять:

- mode: `packet-up`, `stream-up`, `stream-one` или `auto`;
- HTTP version на client-edge и edge-origin legs;
- request method, body-size limits и buffering;
- SSE/streaming response behavior;
- path, Host/SNI и cache bypass;
- поддержку `extra` fields клиентом.

## Практический baseline

1. Проверить Xray-to-Xray direct origin.
2. Настроить origin TLS и `Full (strict)`.
3. Использовать port 443 и отдельный hostname/path.
4. Отключить cache для transport path.
5. Начать с минимальных host/path/mode fields.
6. Проверить фактическую передачу данных, а не ICMP ping или `curl -I`.

`packet-up` требует корректной передачи request bodies; `stream-one` требует надёжного streaming/HTTP2 path. При нестабильности держать DNS-only XHTTP или REALITY/WS fallback.

## Диагностика

- `404`: неверный path/origin routing;
- `405`: method не принят;
- `413`: body-size limit;
- `520/524`: origin/stream timeout;
- download работает, upload нет: buffering/method/body path;
- запрос не виден origin: edge rule/WAF/client import.

## Источники

- [Cloudflare network ports](https://developers.cloudflare.com/fundamentals/reference/network-ports/)
- [Cloudflare cache rules](https://developers.cloudflare.com/cache/how-to/cache-rules/)
- [3X-UI XHTTP schema](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/schemas/protocols/stream/xhttp.ts)
- [Xray XHTTP discussion](https://github.com/XTLS/Xray-core/discussions/4113)
