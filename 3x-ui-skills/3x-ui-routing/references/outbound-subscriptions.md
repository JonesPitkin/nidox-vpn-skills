# Subscription Outbounds

## Возможность v3.3.0

3X-UI может импортировать outbounds из remote subscription URL, сохранять стабильные tags и автоматически обновлять содержимое. Полученные outbounds объединяются с manual template outbounds до запуска Xray.

Основные controls:

- URL и remark;
- tag prefix;
- enabled state;
- update interval и manual refresh;
- prepend/append относительно manual outbounds;
- разрешение private destinations;
- порядок нескольких subscriptions.

## Безопасный процесс

1. Считать subscription недоверенным входом.
2. Оставить private destinations запрещёнными, если они не нужны явно.
3. Выполнить parse/test до сохранения.
4. Проверить protocol, destination, TLS/REALITY и уникальность tags.
5. Сослаться на импортированные tags в routing/balancers.
6. После refresh проверить Xray config и фактический egress.

Удаление subscription убирает её outbounds при следующем reload. Не создавать rules, которые останутся с несуществующим tag.

## Риски

- remote owner меняет destination или credentials;
- collision tag prefixes;
- prepend меняет default outbound;
- private/metadata endpoint попадает в импорт;
- auto-refresh ломает ранее рабочий route;
- subscription содержит transport, не поддержанный bundled Xray.

## Источники

- [3X-UI v3.3.0 release](https://github.com/MHSanaei/3x-ui/releases/tag/v3.3.0)
- [Outbound subscription service](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/web/service/outbound_subscription.go)
- [Outbound subscription UI](https://github.com/MHSanaei/3x-ui/blob/v3.3.0/frontend/src/pages/xray/outbounds/OutboundsTab.tsx)
