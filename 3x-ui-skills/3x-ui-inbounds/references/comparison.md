# Сравнение рекомендуемых схем

Оценки относительные и зависят от ISP, IP VPS, SNI, CDN, клиента и версии core. “Устойчивость” нельзя трактовать как гарантию обхода блокировок.

| Вариант | Устойчивость к блокировкам | Скорость | Сложность настройки | Поддержка клиентов | Рекомендации по применению |
|---|---|---|---|---|---|
| VLESS + Reality | Высокая на direct TCP path при удачном target/SNI; не для обычного CDN | Высокая | Средняя | Xray, sing-box, v2rayNG, Shadowrocket, Podkop | Базовый direct-вариант без собственного TLS-сертификата |
| VLESS + Vision | Высокая при TCP + TLS/REALITY; flow уменьшает характерные признаки TLS-in-TLS | Очень высокая, низкий overhead | Средняя | Xray, sing-box, v2rayNG, Shadowrocket, Podkop | Предпочтительный flow для VLESS TCP TLS/REALITY |
| VLESS + WS | Средняя; может использовать CDN, но WS/path/IP CDN фильтруются | Средняя, выше overhead | Средняя/высокая с reverse proxy | Очень широкая | CDN/reverse-proxy fallback и сети, где direct endpoint недоступен |
| VLESS + gRPC | Средняя/высокая при рабочем HTTP/2 path; зависит от proxy/CDN | Высокая | Высокая | Xray, sing-box, v2rayNG; Shadowrocket/Podkop version-sensitive | HTTP/2 infrastructure, multiplexed streams, controlled reverse proxy |
| Trojan | Средняя/высокая с корректным TLS/REALITY; зависит от transport | Высокая | Средняя | Очень широкая, включая sing-box, v2rayNG, Shadowrocket, Podkop | Совместимость и password-based access; TLS deployment |
| Hysteria2 | Высокая в lossy networks при доступном UDP; низкая при блокировке QUIC/UDP | Очень высокая на подходящей сети | Средняя/высокая | sing-box, Shadowrocket, Podkop; другие клиенты проверять | Мобильные/дальние/потерянные каналы; обязательно иметь TCP fallback |

## Важное различие

REALITY и Vision не являются взаимоисключающими вариантами:

- REALITY — security/handshake;
- Vision — VLESS flow `xtls-rprx-vision`;
- распространённая схема объединяет их: VLESS + TCP + REALITY + Vision.

Строки разделены, чтобы сравнить роль каждого механизма, как требуется при выборе конфигурации.

## Практический выбор

1. Начать с VLESS TCP REALITY Vision для direct VPS.
2. Добавить Hysteria2 как UDP path, если целевые сети его пропускают.
3. Добавить VLESS WS TLS через CDN/reverse proxy, если нужен независимый edge path.
4. Использовать gRPC при подтверждённой HTTP/2 совместимости всей цепочки.
5. Выбрать Trojan, когда важнее password-based compatibility.
6. Не менять сразу transport, security и client core: сравнивать по одному фактору.

## Проверка результата

- подключение минимум из двух целевых сетей;
- latency, throughput и packet loss в одинаковое время;
- DNS и UDP behavior;
- reconnect после смены сети;
- импорт профиля без потери fields;
- работа после reboot/restart;
- документированный TCP fallback для Hysteria2.

## Источники

- [3X-UI Wiki FAQ](https://github.com/MHSanaei/3x-ui/wiki/Common-questions-and-problems)
- [3X-UI Wiki Home](https://github.com/MHSanaei/3x-ui/wiki)
- [Xray REALITY](https://xtls.github.io/en/config/transport.html#realityobject)
- [Xray VLESS](https://xtls.github.io/en/config/inbounds/vless.html)
- [Hysteria2 documentation](https://v2.hysteria.network/docs/)
