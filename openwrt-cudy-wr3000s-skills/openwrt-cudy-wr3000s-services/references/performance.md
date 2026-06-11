# Производительность Cudy WR3000S v1

## Содержание

- [Что считать реальной производительностью](#что-считать-реальной-производительностью)
- [Профили нагрузки MT7981](#профили-нагрузки-mt7981)
- [Рекомендации по количеству VPN-клиентов](#рекомендации-по-количеству-vpn-клиентов)
- [Использование sing-box](#использование-sing-box)
- [Использование Podkop](#использование-podkop)
- [Нагрузка от FakeIP](#нагрузка-от-fakeip)
- [Ограничения 256 МБ RAM](#ограничения-256-мб-ram)
- [Мониторинг памяти](#мониторинг-памяти)
- [Аппаратное ускорение NAT](#аппаратное-ускорение-nat)
- [Методика измерения](#методика-измерения)
- [Источники](#источники)

## Что считать реальной производительностью

Cudy WR3000S v1 использует MediaTek MT7981BA: два Cortex-A53 по 1,3 ГГц, 256 МБ RAM, коммутатор MT7531 и гигабитные внешние Ethernet-порты. Внутренний линк CPU–switch работает на 2,5 Гбит/с, но каждый внешний порт ограничен 1 Гбит/с.

Для этого роутера нет официального универсального результата VPN, sing-box или Podkop в Мбит/с. Скорость меняется в зависимости от:

- протокола и реализации шифрования;
- удалённого сервера и задержки до него;
- TCP или UDP;
- размера пакетов и MTU;
- числа одновременных потоков;
- Wi-Fi или Ethernet;
- nftables, TProxy, DNS и rule-set;
- SQM и flow offloading;
- версии OpenWrt, sing-box и Podkop.

Поэтому не переносить результаты WR3000, WR3000H, других MT7981-устройств или OEM firmware как гарантированный benchmark WR3000S.

## Профили нагрузки MT7981

### Обычный NAT и маршрутизация

Для прямого LAN→WAN трафика OpenWrt может использовать Software или Hardware Flow Offloading. Аппаратный fast path MediaTek снижает участие CPU в обработке подходящих established TCP/UDP flows. В таком режиме ограничителем может стать гигабитный внешний порт, а не Cortex-A53.

Это не означает, что любой трафик автоматически ускоряется. Flow offload применяется к подходящим пересылаемым соединениям и не заменяет измерение на конкретной конфигурации.

### VPN, sing-box и TProxy

Трафик, который перенаправляется в локальный userspace-процесс sing-box, проходит шифрование, дешифрование и обработку правил на CPU. Hardware NAT/PPE не превращает такой путь в гигабитный fast path.

OpenWrt для Filogic включает ARMv8 Crypto Extensions и пакет `kmod-crypto-hw-safexcel`, но нельзя считать, что любой userspace-протокол sing-box автоматически использует Safexcel. Фактическая скорость всё равно должна измеряться.

### Wi-Fi

Wi-Fi 6 и WED могут разгружать часть обмена Wi-Fi↔Ethernet, но радиоэфир, клиенты, ширина канала, DFS и помехи обычно создают больший разброс, чем проводной тест. Производительность VPN сначала измерять по Ethernet, затем отдельно по Wi-Fi.

## Рекомендации по количеству VPN-клиентов

Указывать фиксированный максимум клиентов для MT7981 некорректно: бездействующий peer почти не создаёт нагрузки, а один активный клиент с большим зашифрованным потоком может загрузить процессор полностью.

Использовать следующий эксплуатационный подход:

| Нагрузка | Рекомендация |
|---|---|
| Один высокоскоростной VPN/proxy-поток | Базовый сценарий для первичного теста |
| Несколько клиентов с вебом, мессенджерами и редким видео | Добавлять по одному и контролировать CPU, RAM, задержку и потери |
| Несколько одновременных загрузок или потоков 4K через туннель | Считать тяжёлой нагрузкой; проверять оба ядра и скорость сервера |
| Много настроенных, но неактивных peers | Обычно менее важно, чем число активных соединений и rule-set |
| VPN-сервер, Podkop, SQM и дополнительные службы одновременно | Не назначать лимит без нагрузочного теста всей комбинации |

Практический критерий достаточности:

1. Запустить один клиент и измерить baseline.
2. Добавлять активных клиентов по одному.
3. Остановиться, когда одно из условий перестаёт выполняться:
   - скорость каждого клиента соответствует задаче;
   - latency под нагрузкой остаётся приемлемой;
   - нет packet loss и повторных соединений;
   - `sing-box` или VPN-процесс не удерживает CPU на пределе;
   - `MemAvailable` не снижается с течением времени;
   - в kernel log нет OOM.

Для гарантированной высокой скорости многих клиентов использовать отдельный x86/ARM64-сервер, а WR3000S оставить маршрутизатором и точкой доступа.

## Использование sing-box

- Использовать один основной процесс sing-box, если нет подтверждённой причины запускать несколько экземпляров.
- Сначала тестировать один outbound и минимальный набор правил.
- Добавлять Selector, URLTest и дополнительные outbounds после проверки базовой конфигурации.
- Ограничивать debug-логирование: оно создаёт CPU, RAM и flash I/O.
- Не загружать одновременно несколько крупных пересекающихся rule-set.
- Измерять проводной throughput через каждый тип outbound отдельно.
- Проверять процесс:

  ```sh
  pidof sing-box
  top -b -n 1 | head -n 30
  cat /proc/$(pidof sing-box)/status
  ```

В `/proc/<pid>/status` смотреть прежде всего `VmRSS`, `VmHWM`, число threads и динамику между замерами.

## Использование Podkop

Podkop работает поверх sing-box, модифицирует его конфигурацию и использует nftables/TProxy. Проект требует OpenWrt 24.10 или новее и минимум 25 МБ свободного flash-пространства.

Для WR3000S:

- сохранять простую политику `источник → список → действие → outbound`;
- добавлять секции по одной;
- не дублировать одинаковые домены в нескольких больших списках;
- после обновления проверять конфигурацию и очищать LuCI cache согласно документации Podkop;
- использовать встроенную диагностику FakeIP и routing;
- не запускать второй независимый sing-box с пересекающимися TProxy/DNS-портами;
- проверять ресурсы после каждой крупной смены rule-set.

Подробная настройка приведена в [podkop-on-wr3000s.md](podkop-on-wr3000s.md).

## Нагрузка от FakeIP

Podkop использует sing-box DNS на `127.0.0.42` и IPv4 FakeIP range `198.18.0.0/15`. Размер диапазона не является заранее выделенным объёмом RAM. Нагрузка определяется реальным числом DNS-записей, активных отображений, соединений, cache entries и правилами маршрутизации.

FakeIP добавляет:

- обработку DNS в sing-box;
- таблицу соответствий домен↔FakeIP;
- состояния соединений и nftables/TProxy;
- при включённом persistent cache — операции с `cache.db`.

Рекомендации:

- не считать FakeIP бесплатным, но и не оценивать память по числу адресов в `/15`;
- не включать чрезмерно широкие списки без необходимости;
- хранить cache на пути, который не вызывает нежелательные частые записи в NAND;
- учитывать, что `/tmp` находится в RAM и очищается после перезагрузки;
- сравнивать `VmRSS` sing-box до и после прогрева DNS/cache;
- проверять рост памяти через несколько часов типичной нагрузки.

sing-box умеет сохранять FakeIP в cache file через `store_fakeip`. Включать persistent cache только осознанно: он улучшает сохранение соответствий между перезапусками, но создаёт запись в выбранную файловую систему.

## Ограничения 256 МБ RAM

256 МБ — это общий объём для kernel, Wi-Fi firmware/driver, network stack, LuCI, dnsmasq, sing-box, Podkop, rule-set, conntrack и page cache.

Linux использует свободную RAM как cache, поэтому поле `free` само по себе не показывает нехватку памяти. Основной системный показатель — `MemAvailable`.

Риски:

- крупные rule-set и DNS cache;
- несколько процессов sing-box;
- AdGuard Home вместе с Podkop;
- подробные логи;
- большое число соединений/conntrack;
- дополнительные серверные приложения;
- отсутствие swap и USB/extroot.

На WR3000S нет USB, поэтому не планировать swap или extroot как штатный способ компенсации нехватки RAM. При стабильной нехватке памяти сокращать службы или переносить их на домашний сервер.

## Мониторинг памяти

Базовые команды:

```sh
free -m
grep -E 'MemTotal|MemFree|MemAvailable|Buffers|Cached|Slab|SReclaimable' /proc/meminfo
top
ps w
logread | grep -Ei 'out of memory|oom|killed process'
dmesg | grep -Ei 'out of memory|oom|killed process'
```

Мониторинг конкретного процесса:

```sh
pid=$(pidof sing-box)
grep -E 'VmRSS|VmHWM|VmSize|Threads' /proc/$pid/status
```

Проверка conntrack:

```sh
sysctl net.netfilter.nf_conntrack_count
sysctl net.netfilter.nf_conntrack_max
```

Методика:

1. Записать baseline после чистой загрузки.
2. Записать показатели после запуска Podkop.
3. Повторить после прогрева DNS и обычного трафика.
4. Повторить во время максимальной ожидаемой нагрузки.
5. Исследовать устойчивый рост `VmRSS`, падение `MemAvailable`, перезапуски процесса или OOM.

Не задавать универсальный безопасный порог в мегабайтах без наблюдения за конкретным набором пакетов. Важны запас, отсутствие постоянного снижения и успешное прохождение максимальной нагрузки.

## Аппаратное ускорение NAT

### Когда включать

Для обычного прямого NAT без SQM и без необходимости анализировать каждый пакет:

1. Сначала измерить скорость без offload.
2. Включить Software Flow Offloading.
3. Повторить throughput и latency test.
4. При необходимости проверить Hardware Flow Offloading.
5. Оставить режим только при стабильной работе всех нужных функций.

LuCI:

```text
Network → Firewall → Routing/NAT Offloading
```

UCI:

```sh
uci set firewall.@defaults[0].flow_offloading='1'
uci set firewall.@defaults[0].flow_offloading_hw='1'
uci commit firewall
/etc/init.d/firewall restart
```

Проверка MediaTek PPE:

```sh
mount -t debugfs debugfs /sys/kernel/debug 2>/dev/null
cat /sys/kernel/debug/ppe0/entries
```

Наличие записей зависит от версии kernel, debugfs и подходящего трафика.

### Когда не рассчитывать на ускорение

- Трафик, направленный через TProxy в sing-box, обрабатывается локальным userspace и не получает обычного NAT-only fast path.
- Flow offload не устраняет стоимость VPN-шифрования.
- Hardware Flow Offloading несовместим с SQM/QoS, которым требуется обработка пакетов в kernel.
- Offload может обходить функции, которым нужен per-packet inspection или accounting.

Для смешанной конфигурации direct + Podkop оценивать два пути отдельно:

```text
direct traffic -> возможен flow offload
proxy/VPN traffic -> CPU, sing-box, nftables/TProxy
```

Не включать Hardware Flow Offloading только потому, что опция доступна. Проверить direct routing, Podkop, DNS, статистику, ограничения доступа и latency после включения.

## Методика измерения

1. Подключить тестовый клиент и `iperf3`-сервер по Ethernet.
2. Измерить LAN routing без VPN.
3. Измерить WAN/direct NAT.
4. Измерить один VPN или sing-box outbound.
5. Повторить с Podkop/FakeIP.
6. Повторить с нужным числом активных клиентов.
7. Для каждого теста записать:
   - throughput;
   - latency и packet loss;
   - CPU по ядрам;
   - `MemAvailable`;
   - `VmRSS` sing-box;
   - conntrack count;
   - включённые SQM/offload options.

Не смешивать Wi-Fi, смену сервера, новый протокол и изменение rule-set в одном сравнении.

## Источники

- [OpenWrt Techdata: Cudy WR3000S v1](https://openwrt.org/toh/hwdata/cudy/cudy_wr3000s_v1)
- [MediaTek MT7981B open datasheet](https://mirror2.openwrt.org/docs/MT7981B_Wi-Fi6_Platform_Datasheet_Open_V1.0.pdf)
- [OpenWrt Flow Offloading](https://openwrt.org/docs/guide-user/perf_and_log/flow_offloading)
- [OpenWrt SQM](https://openwrt.org/docs/guide-user/network/traffic-shaping/sqm)
- [OpenWrt 24.10 Filogic target defaults](https://github.com/openwrt/openwrt/blob/openwrt-24.10/target/linux/mediatek/filogic/target.mk)
- [Podkop README](https://github.com/itdoginfo/podkop)
- [Podkop constants: FakeIP и DNS](https://github.com/itdoginfo/podkop/blob/main/podkop/files/usr/lib/constants.sh)
- [sing-box FakeIP](https://sing-box.sagernet.org/configuration/dns/server/fakeip/)
- [sing-box Cache File](https://sing-box.sagernet.org/configuration/experimental/cache-file/)
