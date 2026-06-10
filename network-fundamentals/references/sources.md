# Источники

Этот файл фиксирует канонические источники, на которые опирается `network-fundamentals`.

## 1. Cloudflare Learning Center

- OSI Model: <https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/>
- TCP/IP: <https://www.cloudflare.com/learning/ddos/glossary/tcp-ip/>
- UDP: <https://www.cloudflare.com/learning/ddos/glossary/user-datagram-protocol-udp/>
- DNS: <https://www.cloudflare.com/learning/dns/what-is-dns/>
- DNS records: <https://www.cloudflare.com/learning/dns/dns-records/>
- Internet Protocol / IP: <https://www.cloudflare.com/learning/network-layer/internet-protocol/>
- How does the Internet work?: <https://www.cloudflare.com/learning/network-layer/how-does-the-internet-work/>

## 2. Cisco Networking Academy

- CCNA: Introduction to Networks: <https://www.netacad.com/courses/ccna-introduction-networks>
- Networking Basics: <https://www.netacad.com/courses/networking-basics/1000>
- Networking Essentials: <https://www.netacad.com/courses/networking-essentials>
- CCNA: Switching, Routing, and Wireless Essentials: <https://www.netacad.com/courses/ccna-switching-routing-wireless-essentials?courseLang=en-US>
- Lab - Configure IPv4 and IPv6 Static and Default Routes: <https://www.netacad.com/content/srwe/1.0/courses/content/m15/en-US/assets/15.6.2-lab---configure-ipv4-and-ipv6-static-and-default-routes.pdf>
- Lab - Configuring IPv4 Static and Default Routes: <https://contenthub.netacad.com/legacy/RSE/5.02/hu/course/files/6.2.2.5%20Lab%20-%20Configuring%20IPv4%20Static%20and%20Default%20Routes.pdf>

## 3. OpenWrt Networking Docs

- Network start: <https://openwrt.org/docs/guide-user/network/start>
- Internet connection: <https://openwrt.org/docs/guide-user/network/wan/internet.connection>
- WAN interface protocols: <https://openwrt.org/docs/guide-user/network/wan/wan_interface_protocols>
- ISP configurations: <https://openwrt.org/docs/guide-user/network/wan/isp-configurations>

Примечание: на момент сборки страницы OpenWrt защищены Anubis challenge и могут быть недоступны для простого безбраузерного чтения. Ссылки оставлены как официальный практический источник по UCI, интерфейсам и реальной эксплуатации маршрутизаторов.

## 4. MDN Networking

- How does the Internet work?: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Web_mechanics/How_does_the_Internet_work>
- Web mechanics: <https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Web_mechanics>
- Internet glossary: <https://developer.mozilla.org/en-US/docs/Glossary/Internet>

## 5. RFC Editor

### Базовые протоколы

- RFC 768 - User Datagram Protocol: <https://www.rfc-editor.org/info/rfc768/>
- RFC 791 - Internet Protocol: <https://www.rfc-editor.org/info/rfc791/>
- RFC 792 - Internet Control Message Protocol: <https://www.rfc-editor.org/info/rfc792/>
- RFC 1122 - Requirements for Internet Hosts - Communication Layers: <https://www.rfc-editor.org/info/rfc1122/>
- RFC 1123 - Requirements for Internet Hosts - Application and Support: <https://www.rfc-editor.org/info/rfc1123/>
- RFC 9293 - Transmission Control Protocol (актуальная сводная спецификация TCP): <https://www.rfc-editor.org/info/rfc9293/>
- RFC 8200 - Internet Protocol, Version 6 (IPv6) Specification: <https://www.rfc-editor.org/info/rfc8200/>

### DNS

- RFC 1034 - Domain Names - Concepts and Facilities: <https://www.rfc-editor.org/info/rfc1034/>
- RFC 1035 - Domain Names - Implementation and Specification: <https://www.rfc-editor.org/info/rfc1035/>
- RFC 2181 - Clarifications to the DNS Specification: <https://www.rfc-editor.org/info/rfc2181/>
- RFC 2308 - Negative Caching of DNS Queries (DNS NCACHE): <https://www.rfc-editor.org/info/rfc2308/>
- RFC 7766 - DNS Transport over TCP - Implementation Requirements: <https://www.rfc-editor.org/info/rfc7766/>

### MTU и MSS

- RFC 1191 - Path MTU Discovery for IPv4: <https://www.rfc-editor.org/info/rfc1191/>
- RFC 4821 - Packetization Layer Path MTU Discovery: <https://www.rfc-editor.org/info/rfc4821/>
- RFC 8201 - Path MTU Discovery for IPv6: <https://www.rfc-editor.org/info/rfc8201/>
- RFC 879 - The TCP Maximum Segment Size and Related Topics: <https://www.rfc-editor.org/info/rfc879/>
- RFC 6691 - TCP Options and Maximum Segment Size (исторически важен, но отмечен как obsolete в пользу актуальной сводной модели TCP): <https://www.rfc-editor.org/info/rfc6691/>

### NAT и адресное пространство

- RFC 1918 - Address Allocation for Private Internets: <https://www.rfc-editor.org/info/rfc1918/>
- RFC 2663 - IP Network Address Translator (NAT) Terminology and Considerations: <https://www.rfc-editor.org/info/rfc2663/>
- RFC 3022 - Traditional IP Network Address Translator (Traditional NAT): <https://www.rfc-editor.org/info/rfc3022/>
- RFC 4787 - Network Address Translation (NAT) Behavioral Requirements for Unicast UDP: <https://www.rfc-editor.org/info/rfc4787/>
- RFC 5382 - NAT Behavioral Requirements for TCP: <https://www.rfc-editor.org/info/rfc5382/>
- RFC 6598 - Shared Address Space Request: <https://www.rfc-editor.org/info/rfc6598/>
- RFC 6888 - Common Requirements for Carrier-Grade NATs (CGNs): <https://www.rfc-editor.org/info/rfc6888/>

### IPv6 и диагностика

- RFC 4291 - IP Version 6 Addressing Architecture: <https://www.rfc-editor.org/info/rfc4291/>
- RFC 4443 - ICMPv6: <https://www.rfc-editor.org/info/rfc4443/>
- RFC 4861 - Neighbor Discovery for IP version 6 (IPv6): <https://www.rfc-editor.org/info/rfc4861/>
- RFC 4862 - IPv6 Stateless Address Autoconfiguration: <https://www.rfc-editor.org/info/rfc4862/>
- RFC 8504 - IPv6 Node Requirements: <https://www.rfc-editor.org/info/rfc8504/>

### Порты

- RFC 6335 - IANA Procedures for the Management of the Service Name and Transport Protocol Port Number Registry: <https://www.rfc-editor.org/info/rfc6335/>
- RFC 6056 - Recommendations for Transport Port Randomization: <https://www.rfc-editor.org/info/rfc6056/>

### Маршрутизация

- RFC 1812 - Requirements for IP Version 4 Routers: <https://www.rfc-editor.org/info/rfc1812/>
- RFC 2328 - OSPF Version 2: <https://www.rfc-editor.org/info/rfc2328/>
- RFC 4271 - A Border Gateway Protocol 4 (BGP-4): <https://www.rfc-editor.org/info/rfc4271/>

## Практическое правило для Codex

- Исторические справки брать из RFC и MDN.
- Простые объяснения и прикладные аналогии брать из Cloudflare и Cisco.
- Практику интерфейсов маршрутизатора и сетевой конфигурации брать из OpenWrt docs.
- Нормативные определения и ограничения протоколов сверять по RFC.
