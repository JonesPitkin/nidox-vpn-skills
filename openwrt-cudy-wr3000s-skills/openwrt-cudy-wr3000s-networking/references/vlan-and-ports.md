# Порты и VLAN Cudy WR3000S v1

## Назначение WAN

Физический порт Internet работает на скорости до 1 Гбит/с и в OpenWrt обозначается `wan`. По умолчанию он входит в логический интерфейс WAN и получает адрес по DHCP, если пользователь не выбрал PPPoE или статическую настройку.

Switch port в актуальном DTS:

```text
port@0 -> wan
```

## Назначение LAN

Четыре физических LAN-порта представлены отдельными DSA-интерфейсами:

```text
port@1 -> lan1
port@2 -> lan2
port@3 -> lan3
port@4 -> lan4
```

По умолчанию они входят в мост `br-lan`. Внутренний CPU-порт:

```text
port@6 -> cpu, 2500Base-X
```

Внутренняя скорость CPU-link не превращает внешние разъёмы в 2,5GbE.

## Карта портов

| Надпись на корпусе | Интерфейс OpenWrt | Switch port | Типичная роль |
|---|---|---:|---|
| Internet/WAN | `wan` | 0 | uplink |
| LAN 1 | `lan1` | 1 | `br-lan` |
| LAN 2 | `lan2` | 2 | `br-lan` |
| LAN 3 | `lan3` | 3 | `br-lan` |
| LAN 4 | `lan4` | 4 | `br-lan` |
| внутренний | CPU | 6 | связь SoC со switch |

Это отображение подтверждается DTS и bootlog. Не использовать примерную старую таблицу wiki с `eth0.0`, `eth0.1` и обратной нумерацией: она оставлена как незаполненный шаблон и не описывает актуальный DSA-профиль WR3000S.

## Особенности VLAN

Актуальные версии OpenWrt используют DSA:

- VLAN создаются на bridge device, обычно `br-lan`;
- для каждого VLAN задаётся tagged/untagged/off по портам;
- L3-интерфейс привязывается к `br-lan.<VID>`;
- PVID назначается untagged-порту, если он должен принимать нетегированный трафик.

Пример концепции:

| VLAN | lan1 | lan2 | lan3 | lan4 | Назначение |
|---:|---|---|---|---|---|
| 1 | untagged/PVID | untagged/PVID | off | off | основная LAN |
| 20 | off | off | untagged/PVID | tagged | IoT и trunk |
| 30 | off | off | off | tagged | гостевая сеть через trunk |

Это пример политики, а не готовая конфигурация.

## Безопасный порядок настройки

1. Сохранить резервную копию `/etc/config/network`.
2. Оставить один LAN-порт в исходной management VLAN.
3. Создать bridge VLAN filtering.
4. Добавить новый VLAN и интерфейс.
5. Настроить DHCP и firewall zone.
6. Проверить доступ через новый порт.
7. Только после проверки менять оставшиеся порты.

При удалённой настройке использовать `uci commit` только после проверки временных изменений или иметь UART/второй путь управления.

## Диагностика

```sh
ubus call system board
ip -d link show
bridge link
bridge vlan show
ubus call network.device status '{"name":"br-lan"}'
cat /etc/config/network
```

Для проверки физического линка:

```sh
ethtool wan
ethtool lan1
```

`ethtool` не входит в каждый базовый образ; при отсутствии установить пакет `ethtool` или использовать `ubus` и `ip`.

## VLAN для Podkop и домашней сети

Практичная схема:

- management VLAN для роутера и администрирования;
- trusted LAN для персональных устройств;
- IoT VLAN с ограниченным доступом;
- guest VLAN без доступа к локальным сервисам;
- отдельная политика Podkop по IP-подсетям или статическим адресам.

Podkop-маршрутизация не заменяет firewall isolation. Сначала определить L2/L3-сегментацию, затем назначать прокси-политику.

## Источники

- [OpenWrt Wiki: Specific Configuration](https://openwrt.org/toh/cudy/wr3000s_v1#specific_configuration)
- [Актуальный DTS WR3000S v1](https://github.com/openwrt/openwrt/blob/master/target/linux/mediatek/dts/mt7981b-cudy-wr3000s-v1.dtsi)
- [DTS WR3000S v1 в OpenWrt 24.10](https://github.com/openwrt/openwrt/blob/openwrt-24.10/target/linux/mediatek/dts/mt7981b-cudy-wr3000s-v1.dts)
- [OpenWrt DSA mini tutorial](https://openwrt.org/docs/guide-user/network/dsa/dsa-mini-tutorial)
