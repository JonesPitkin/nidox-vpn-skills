# mKCP

## Описание

mKCP — UDP transport Xray с configurable header camouflage. Wiki 3X-UI перечисляет его среди современных transports.

## Когда использовать

- UDP доступен и требуется transport Xray поверх KCP;
- поддержка mKCP подтверждена у клиента;
- тесты показывают преимущество на конкретной lossy network.

Для новых deployment чаще сначала сравнивать Hysteria2: у него отдельная современная QUIC/TLS модель. mKCP без дополнительной security не считать маскировкой уровня TLS/REALITY.

## Преимущества

- UDP transport;
- настройка MTU/TTI/capacity/congestion;
- поддержка Xray-based clients.

## Недостатки

- может создавать высокий overhead;
- UDP часто блокируется или throttled;
- параметры обеих сторон должны совпадать;
- нет обычной CDN/reverse-proxy совместимости.

## Требования

- открыть UDP;
- совпадающие seed/header и KCP parameters;
- проверить MTU;
- использовать только допустимую для protocol security combination.

## Настройка в панели

1. Выбрать transport `mKCP`.
2. Начать с defaults.
3. Выбрать header type только при поддержке клиента.
4. Не завышать uplink/downlink capacity без измерений.
5. Открыть port как UDP.

## Настройка клиента

- v2rayNG: Xray core поддерживает mKCP; сверить imported seed/header.
- Shadowrocket: поддержка зависит от версии/профиля; проверять до deployment.
- sing-box: official V2Ray transport list не включает mKCP; не конвертировать автоматически.
- Podkop/sing-box: не считать поддержанным через обычный VLESS URL без подтверждения используемого core.

## Типовые ошибки

- открыт TCP вместо UDP;
- seed/header отличаются;
- MTU вызывает fragmentation;
- параметры capacity/TTI ухудшают сеть;
- клиент не поддерживает mKCP.

## Диагностика

Проверить UDP listener/firewall, затем baseline defaults одним Xray-based клиентом. Сравнить single port из другой сети.

## Источники

- [3X-UI Wiki Home](https://github.com/MHSanaei/3x-ui/wiki)
- [Xray mKCP transport](https://xtls.github.io/en/config/transports/mkcp.html)
- [3X-UI stream form](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/pages/inbounds/form/InboundFormModal.tsx)
