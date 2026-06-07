# Architecture and Operations Guide

## Contents

1. Provenance
2. Diagnostic model
3. Architecture matrix
4. Direct Xray endpoint
5. Cascade through an intermediate VPS
6. Selective WARP egress
7. OpenWrt split tunneling
8. CDN path
9. Security checklist
10. Validation and troubleshooting

## Provenance

This reference is distilled from:

- Repository: `https://github.com/xcvtt/miniature-octo-palm-tree`
- Source commit: `85c57d1cb4fc184081594aeddde44845df123b4c`
- Source update date: 2026-06-07
- Source title: `Обход блокировок в 2026 - обзор доступных методов`

The source is a field guide, not an authoritative specification. Verify changing claims and commands against upstream documentation before use.

## Diagnostic Model

Classify the failure before changing architecture:

| Symptom | Likely layer | Useful comparison |
| --- | --- | --- |
| Domain fails but known IP works | DNS | ISP DNS versus encrypted DNS |
| TCP connects but TLS fails | SNI/TLS filtering or wrong certificate | `openssl s_client`, alternate SNI |
| Small responses work, sustained transfers stall | Traffic shaping | same endpoint from another ISP/VPS |
| TCP works, UDP fails | UDP/QUIC filtering | TCP-only client mode |
| Direct foreign VPS fails, local VPS works | destination/IP policy or shaping | cascade path |
| Proxy works, specific service rejects it | egress reputation/geolocation | selective WARP |
| One client works, router path fails | TPROXY/routing loop/DNS | SOCKS test before transparent mode |

Do not infer a nationwide mechanism from one ISP or one test. Record the network, location, time, protocol, destination, and client version.

## Architecture Matrix

| Topology | Use when | Advantages | Costs and limits |
| --- | --- | --- | --- |
| Client -> foreign VPS | Direct route works | Minimal moving parts | Easiest target for IP policy/shaping |
| Client -> intermediate VPS -> foreign VPS | Direct foreign path is degraded | Alternate first hop; can add failover | Extra latency and VPS |
| Cascade -> selective WARP | Some services reject VPS egress | Better destination compatibility | Another dependency; route only needed domains |
| Router -> cascade | Many devices need policy routing | No per-device client | Router CPU/RAM and routing complexity |
| Client/intermediate -> CDN -> origin | CDN edge remains reachable | Alternate ingress and domain-based TLS | Domain, certificates, CDN limits; no Reality through CDN |

Start with direct access as a control even when the expected final topology is more complex.

## Direct Xray Endpoint

Typical baseline:

- Debian or another supported server OS.
- Xray-core installed from the official upstream release/install method.
- VLESS inbound using XHTTP plus Reality when currently supported by both server and client.
- Port `443` when available and appropriate.
- Random UUID, X25519 key pair, non-obvious path, and valid short ID.
- A plausible Reality target verified with the current Xray tooling.
- `freedom` and `blackhole` outbounds.

Required checks:

```bash
xray -test -c /usr/local/etc/xray/config.json
systemctl status xray
ss -lntup
journalctl -u xray --since "10 minutes ago"
```

For client links, populate UUID, address, port, transport, path, public key, SNI, fingerprint, and short ID from the validated server config. Treat links and subscription URLs as secrets.

### 3X-UI

Use the official repository and current installation documentation. Before exposing the panel:

- Require HTTPS.
- Generate unique credentials, port, and base path.
- Change or disable the default subscription path/service.
- Enable 2FA if supported.
- Restrict panel access by firewall or private administration network.
- Back up panel data and Xray config.

Do not assume old installation scripts, certificate issuance, or UI field names still apply.

## Cascade Through an Intermediate VPS

### Fixed relay with iptables

Use DNAT and MASQUERADE when one public local port maps to one fixed foreign endpoint. Preserve SSH first.

Essential sequence:

1. Record console/out-of-band recovery access.
2. Enable IPv4 forwarding persistently.
3. Allow loopback, established traffic, SSH, and the relay port.
4. Add TCP DNAT; add UDP only when the selected transport needs it.
5. Add destination-specific MASQUERADE and FORWARD rules.
6. Change default policies only after testing in a second SSH session.
7. Persist and verify after reboot.

Avoid indiscriminately flushing a production firewall. If replacing existing rules is necessary, export them first with `iptables-save`.

### HAProxy relay

Use TCP mode. Add:

- Explicit connect/client/server timeouts.
- Backend health checks.
- `leastconn`, `roundrobin`, `source`, or another algorithm chosen for the actual workload.
- A statistics listener bound to localhost or an administration network only.

Validate before restart:

```bash
haproxy -c -f /etc/haproxy/haproxy.cfg
systemctl reload haproxy
```

### Xray intermediate

Use when the intermediate server must terminate the client connection and route selected domains directly while forwarding the remainder to the foreign Xray endpoint.

Requirements:

- Separate inbound credentials and endpoint credentials.
- Distinct outbound tags such as `direct`, `proxy`, and `block`.
- Specific domain rules before the fallback proxy rule.
- Sniffing when routing by observed domain.
- Correct geosite syntax; keep each entry separate.

This adds encryption/decryption, CPU load, latency, and another place where fingerprint behavior may differ.

## Selective WARP Egress

Use WARP on the foreign VPS when selected services reject or misclassify the VPS IP.

Workflow:

1. Install from Cloudflare's current official repository for the server OS.
2. Register and configure local proxy mode on a loopback port.
3. Confirm WARP status and test the local SOCKS endpoint.
4. Add an Xray SOCKS outbound pointing to `127.0.0.1:<port>`.
5. Route only required domains to the WARP outbound.
6. Confirm other traffic continues through `freedom`.

Check the current WARP CLI syntax rather than relying on historical `warp-cli` commands.

## OpenWrt Split Tunneling

Prefer a maintained package such as Podkop when its supported OpenWrt releases and behavior fit the request.

For manual Xray TPROXY:

1. Confirm OpenWrt version, CPU architecture, free storage, RAM, firewall4/nftables, and interface names.
2. Install a matching current Xray binary and geo data.
3. Create a `procd` service with restart behavior and asset location.
4. Add a temporary SOCKS inbound for endpoint testing.
5. Add a `dokodemo-door` TPROXY inbound for TCP and UDP.
6. Create a policy-routing table and an `fwmark` rule.
7. Create an nftables interval set and mark/TPROXY only selected destinations.
8. Connect dnsmasq domain rules to that nftables set.
9. Forward DNS through a verified encrypted resolver if required.
10. Remove the temporary test SOCKS listener or bind it to localhost.

Always exclude:

- The VPS endpoint itself.
- Router and LAN subnets.
- Loopback, multicast, broadcast, and management paths.
- Any destination required to establish the tunnel.

Test the SOCKS path before enabling transparent routing:

```bash
curl https://ifconfig.me
curl --socks5-hostname 127.0.0.1:1080 https://ifconfig.me
```

Then verify:

```bash
xray -test -c /etc/xray/config.json
ip rule show
ip route show table tproxy
nft list ruleset
logread -e xray
```

## CDN Path

A conventional CDN needs the real domain identity to route the connection. Do not combine it with a Reality handshake intended for a direct origin path.

Typical Full (Strict) design:

```text
client or intermediate VPS
  -> CDN edge on TLS 443
  -> nginx origin with valid certificate
  -> loopback TCP or Unix socket
  -> Xray VLESS over WS or XHTTP without a second local TLS layer
```

Requirements:

- Domain delegated/configured at the CDN.
- Proxied DNS record when CDN routing is enabled.
- Valid origin certificate and strict TLS mode.
- WebSocket, gRPC, or XHTTP support enabled as required.
- nginx routes only a secret path to Xray; normal paths serve a legitimate site or return an ordinary response.
- Xray backend binds to `127.0.0.1` or a protected Unix socket.
- Client uses `security=tls`, the real domain as SNI/host, and the matching path.

Validate:

```bash
xray -test -c /usr/local/etc/xray/config.json
nginx -t
curl -I https://example.com/
openssl s_client -connect example.com:443 -servername example.com
```

Test direct origin and CDN-proxied states separately when DNS controls allow it.

## Security Checklist

- Use key-based SSH, disable password/root login when recovery access is known to work, and keep a second session open during firewall changes.
- Patch the OS and pin no stale package source.
- Limit listening addresses and firewall exposure.
- Use random independent credentials for every hop and client.
- Rotate leaked UUIDs, keys, links, passwords, and certificates.
- Keep subscription links out of logs, screenshots, tickets, and shell history.
- Review remote install scripts before execution; prefer pinned releases and checksums.
- Back up configs with mode `0600`.
- Avoid public statistics, admin, SOCKS, and DNS listeners.
- Document provider terms and local legal constraints.

## Validation and Troubleshooting

### Layered acceptance test

1. The service starts with no config errors.
2. The expected socket listens on the expected address.
3. The client completes the transport and TLS/Reality handshake.
4. Proxied egress IP matches the intended hop.
5. Selected domains follow the intended outbound.
6. Non-selected domains remain direct where split tunneling is configured.
7. DNS uses the intended resolver and returns usable A/AAAA records.
8. TCP and UDP work according to design.
9. Configuration survives reboot.
10. Rollback restores access.

### Common failures

| Failure | Inspect |
| --- | --- |
| Immediate connection refusal | listener, firewall, wrong IP/port |
| TLS error | SNI, certificate chain, clock, CDN TLS mode |
| Reality handshake failure | target/SNI compatibility, keys, short ID, client fingerprint |
| Works via SOCKS but not TPROXY | nftables hook, mark, route table, loop exclusion |
| Domain rule ignored | sniffing, DNS strategy, rule order, geosite data |
| CDN gives HTTP error | host/path, upgrade/grpc headers, origin listener |
| SSH lost after firewall change | INPUT policy/order and actual SSH port |
| High CPU/latency | double termination, router capacity, transport choice |
| Some apps bypass policy | IPv6, QUIC/UDP, hard-coded DNS, certificate pinning |

When a fingerprint change appears to help, report it as an observation tied to a client version and date, not as a durable universal fix.
