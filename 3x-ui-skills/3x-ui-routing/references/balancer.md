# Balancers

## Описание

Balancer выбирает один из outbounds по selector. Текущая schema 3X-UI поддерживает `random`, `roundRobin`, `leastPing`, `leastLoad`, optional `fallbackTag` и strategy settings.

## Требования

- минимум один selector;
- tags выбранных outbounds существуют;
- для latency/load strategies настроены observatory/burst observatory согласно Xray;
- fallback outbound проверен независимо.

## Настройка

1. Создать несколько рабочих outbounds с согласованным tag prefix, например `proxy-a`, `proxy-b`.
2. Проверить каждый outbound отдельным rule.
3. Создать balancer:

```json
{
  "tag": "balancer-rr",
  "selector": ["proxy-a", "proxy-b"],
  "fallbackTag": "direct",
  "strategy": {
    "type": "roundRobin"
  }
}
```

4. В routing rule задать только `balancerTag`.
5. Перезапустить и проверить распределение/переключение.

Пример `leastLoad` из repository fixture использует `expected`, `maxRTT`, `tolerance`, `baselines` и `costs`. Не копировать значения без измерений.

## Выбор стратегии

- `random`: простой случайный выбор.
- `roundRobin`: последовательное распределение.
- `leastPing`: минимальная измеренная задержка.
- `leastLoad`: учитывает доступные load/RTT параметры и требует более тщательной observatory-настройки.

## Ошибки

- Selector не совпадает ни с одним outbound tag.
- Health observation отсутствует, но ожидается `leastPing`.
- Fallback ссылается на тот же неисправный путь.
- Sticky session ожидается от round-robin без дополнительной логики.
- В rule одновременно указаны `outboundTag` и `balancerTag`.

## Диагностика

Сначала временно заменить balancer rule прямым `outboundTag` и проверить каждый путь. Затем проверить observatory logs и только после этого стратегию.

## Источники

- [3X-UI balancer schema](https://github.com/MHSanaei/3x-ui/blob/main/frontend/src/schemas/routing.ts)
- [3X-UI balancer fixtures](https://github.com/MHSanaei/3x-ui/tree/main/frontend/src/test/golden/fixtures/balancer)
- [Xray routing balancers](https://xtls.github.io/en/config/routing.html)
