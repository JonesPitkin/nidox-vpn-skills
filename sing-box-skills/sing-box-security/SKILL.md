---
name: sing-box-security
description: "Production skill по security в sing-box: TLS, certificates, REALITY, ECH migration context, fingerprint caveats, inbound/outbound TLS roles и безопасное проектирование клиентских и серверных transport paths."
---

# sing-box Security

Security в `sing-box` нельзя сводить к флажку `tls.enabled: true`. На production-уровне это слой, который включает:

- корректную server/client роль TLS;
- управление сертификатами;
- проверку имени сервера;
- pinning и related trust controls;
- REALITY role separation;
- понимание deprecated и migrated ECH fields;
- осторожное обращение с fingerprint-like механизмами;
- версионную дисциплину.

Неправильный security design почти всегда маскируется под generic network issue: соединение “вроде доходит”, порт открыт, но handshake не работает. Этот skill нужен, чтобы разбирать такие ситуации системно и строить безопасные шаблоны без folklore.

## Official Source Map

- TLS shared fields: `https://sing-box.sagernet.org/configuration/shared/tls/`
- Certificate: `https://sing-box.sagernet.org/configuration/certificate/`
- Certificate providers in official future docs: `https://sing-box.sagernet.org/configuration/shared/certificate-provider/`
- Migration: `https://sing-box.sagernet.org/migration/`
- Deprecated: `https://sing-box.sagernet.org/deprecated/`
- Changelog: `https://sing-box.sagernet.org/changelog/`

## Stable Security Baseline

Production baseline этой базы знаний остаётся `1.13.13`.

Практические выводы:

- official docs already contain future `1.14` material;
- stable configs must not blindly require alpha-only security fields;
- deprecated docs already warn about legacy ECH fields and older paths;
- WireGuard and DNS migrations indirectly affect security behavior because resolver and transport paths change.

## TLS Roles

Самая частая ошибка на production — мыслить TLS как симметричный блок. В действительности inbound-TLS и outbound-TLS имеют разные задачи и разные допустимые поля.

### Inbound TLS

Server side должен:

- предъявить корректный сертификат;
- иметь соответствующий private key;
- optionally enforce client-side constraints depending on design;
- понимать, какой transport под TLS находится.

### Outbound TLS

Client side должен:

- верифицировать сертификат;
- задать правильный `server_name`;
- optionally pin certificate or public key;
- быть согласован с transport, SNI and target certificate identity.

## Real TLS Configurations

### Minimal Inbound TLS

```json
{
  "tls": {
    "enabled": true,
    "certificate_path": "/etc/sing-box/cert.pem",
    "key_path": "/etc/sing-box/key.pem"
  }
}
```

Use case:

- server-side VLESS/Trojan or HTTP proxy with TLS.

### Minimal Outbound TLS

```json
{
  "tls": {
    "enabled": true,
    "server_name": "example.com"
  }
}
```

### TLS with ALPN and Version Control

```json
{
  "tls": {
    "enabled": true,
    "server_name": "example.com",
    "alpn": [
      "h2",
      "http/1.1"
    ],
    "min_version": "1.2",
    "max_version": "1.3"
  }
}
```

### TLS with Public Key Pinning

```json
{
  "tls": {
    "enabled": true,
    "server_name": "example.com",
    "certificate_public_key_sha256": [
      "BASE64_OR_HEX_DIGEST"
    ]
  }
}
```

Production note:

- pinning strengthens trust but raises operational coupling;
- key rotation becomes a deployment event, not an invisible maintenance action.

## REALITY

REALITY требует особенно аккуратного role separation.

### Server Side REALITY Example

```json
{
  "tls": {
    "enabled": true,
    "reality": {
      "enabled": true,
      "handshake": {
        "server": "google.com",
        "server_port": 443
      },
      "private_key": "UuMBgl7MXTPx9inmQp2UC7Jcnwc6XYbwDNebonM-FCc",
      "short_id": [
        "0123456789abcdef"
      ],
      "max_time_difference": "1m"
    }
  }
}
```

### Client Side REALITY Example

```json
{
  "tls": {
    "enabled": true,
    "server_name": "example.com",
    "reality": {
      "enabled": true,
      "public_key": "jNXHt1yRo0vDuchQlIP6Z0ZvjT3KtzVI-T4E7RoLJS0",
      "short_id": "0123456789abcdef"
    }
  }
}
```

Production rules:

- server stores `private_key`;
- client uses `public_key`;
- `short_id` must align;
- REALITY does not excuse sloppy overall TLS/route/DNS design.

## ECH and Migration Awareness

Stable official deprecated notes say that legacy ECH fields are deprecated and ECH support migrated to stdlib path starting from `1.12.0`.

Practical meaning:

- avoid old ECH snippets from community posts;
- if debugging old config, compare against `migration` and `deprecated`;
- do not assume every exotic ECH field in future docs belongs in stable production.

## Certificates

Production certificate strategy in `sing-box` should answer:

- where certificates live;
- who rotates them;
- what path points to them;
- what breaks if they change;
- whether file permissions and deployment sequencing are controlled.

### File-Based TLS Deployment

```json
{
  "tls": {
    "enabled": true,
    "certificate_path": "/etc/sing-box/fullchain.pem",
    "key_path": "/etc/sing-box/privkey.pem"
  }
}
```

This remains the most operationally legible baseline.

## Fingerprints and uTLS Caveats

Официальный changelog отдельно предупреждает о фундаментальных ограничениях uTLS. Production takeaway:

- не продавать `utls.fingerprint` как универсальный ответ на censorship;
- использовать fingerprint-like features только с пониманием limits, compatibility and future maintenance cost.

If a design requires `utls`, skill should document why and what fallback exists.

## OpenWrt Examples

### OpenWrt Client Outbound TLS

```json
{
  "tls": {
    "enabled": true,
    "server_name": "edge.example.com"
  }
}
```

Operational note:

- routers need especially predictable cert and name validation because blind retries are expensive in diagnosis.

## Linux Server Examples

### Linux Server Inbound TLS

```json
{
  "tls": {
    "enabled": true,
    "certificate_path": "/etc/sing-box/cert.pem",
    "key_path": "/etc/sing-box/key.pem",
    "min_version": "1.2",
    "max_version": "1.3"
  }
}
```

### Linux Server REALITY Client

Attach the client-side REALITY block to the corresponding outbound and validate it separately from transport path.

## VPS Examples

### VPS Public Inbound TLS

```json
{
  "tls": {
    "enabled": true,
    "certificate_path": "/etc/sing-box/fullchain.pem",
    "key_path": "/etc/sing-box/privkey.pem",
    "alpn": [
      "h2",
      "http/1.1"
    ]
  }
}
```

### VPS REALITY Server

Use the server-side REALITY structure shown earlier and keep the private key off all client artifacts.

## Podkop-Compatible Examples

Only sing-box-native client-side security examples are valid.

### Podkop-Compatible VLESS TLS

```json
{
  "tls": {
    "enabled": true,
    "server_name": "example.com"
  }
}
```

### Podkop-Compatible REALITY Client

```json
{
  "tls": {
    "enabled": true,
    "server_name": "example.com",
    "reality": {
      "enabled": true,
      "public_key": "jNXHt1yRo0vDuchQlIP6Z0ZvjT3KtzVI-T4E7RoLJS0",
      "short_id": "0123456789abcdef"
    }
  }
}
```

## 3x-ui-Compatible Examples

Only sing-box-side client examples:

### 3x-ui-Compatible Trojan TLS

```json
{
  "tls": {
    "enabled": true,
    "server_name": "panel.example.com"
  }
}
```

### 3x-ui-Compatible VLESS REALITY Client

Use the same client-side REALITY structure as above, matching the panel-provisioned public key and short ID.

## Routing/Security Interaction

Security is not isolated from route:

- if a domain-based proxy host resolves via wrong path, TLS fails downstream;
- if `direct`/`proxy` policy sends resolver traffic incorrectly, handshake diagnostics become misleading;
- if TUN loops exist, TLS symptoms appear but root cause is routing.

Production implication:

- do not isolate TLS debugging from DNS and route review.

## Comparison Table

| Mechanism | Strength | Main Risk | Best Fit |
|---|---|---|---|
| Plain TLS | standard trust model | cert/SNI mismatch | most deployments |
| TLS with pinning | stronger trust control | painful key rotation | tightly controlled infra |
| REALITY | specialized server/client pairing | role confusion and exact-field mismatch | specific supported designs |
| Legacy ECH snippets | none in new design | migration breakage | avoid in new configs |

## Common Mistakes

### 1. Mixing inbound and outbound TLS roles

Result:

- wrong fields in wrong place;
- hard-to-read configs.

### 2. Using `server_name` that does not match certificate identity

Result:

- verify failures or mysterious connection resets.

### 3. Client stores server-side REALITY material

Result:

- security mistake and broken connectivity.

### 4. Blindly copying old ECH/uTLS snippets

Result:

- version mismatch and unsupported semantics.

### 5. Treating `insecure: true` as normal production practice

Result:

- hidden trust collapse.

## Troubleshooting

### Symptom: TCP connect works, TLS fails

Check:

- `server_name`;
- cert path or peer cert;
- client vs server field placement;
- route and resolver path for domain-based upstream.

### Symptom: REALITY does not connect

Check:

- client has `public_key`, not private;
- server has private key and matching short ID;
- target transport and routing are sane.

### Symptom: cert looks valid but service still fails

Check:

- file permissions;
- actual cert/key pair alignment;
- ALPN or version constraints;
- whether another layer is failing first.

### Symptom: old config broke after upgrade

Check:

- legacy ECH fields;
- deprecated TLS-related settings;
- migration notes around version jump.

## Best Practices

- Keep the minimal working TLS config before adding advanced features.
- Separate security debugging from transport mythology.
- Store private materials only where the role requires them.
- Prefer explicit `server_name`.
- Use pinning intentionally and document the rotation process.
- Re-check `migration` and `deprecated` before carrying security snippets across versions.

## Version Compatibility

### 1.10

- simpler baseline, fewer modern migration caveats.

### 1.11

- broader endpoint and route evolution begins to affect transport security patterns indirectly.

### 1.12

- ECH migration becomes explicit;
- certificate-related thinking broadens.

### 1.13 stable

- baseline for this repository;
- security design should assume stable TLS + migration-aware REALITY/ECH understanding.

### 1.14 alpha

- official future docs contain more knobs, but do not force them into `1.13` production.

## Completion Criteria

Skill применён корректно, если:

- TLS/REALITY roles are separated clearly;
- cert and name validation path explained;
- version traps for ECH and future-only fields called out;
- environment examples included.

## Security Rollout Playbooks

### Playbook: New TLS Deployment

1. Start with minimal TLS only.
2. Validate cert/key or peer verification.
3. Validate `server_name`.
4. Add ALPN/version tuning only if required.
5. Add pinning or advanced features last.

### Playbook: REALITY Introduction

1. Prove the non-REALITY transport or basic path first when possible.
2. Add server-side REALITY keys and short IDs.
3. Add client-side public key and short ID.
4. Validate no DNS/route issue is misread as REALITY failure.

### Playbook: Version-Aware Security Review

1. Check target stable version.
2. Open `deprecated` and `migration`.
3. Remove old ECH snippets and unsupported assumptions.
4. Confirm no future-only docs were copied into current stable config.

## Validation Checklist

- TLS role clearly identified.
- `server_name` justified.
- Cert and key paths valid.
- REALITY keys on correct sides.
- No blind `insecure: true`.
- Migration-sensitive features reviewed against stable docs.

## Senior Review Questions

- What exact identity is the client verifying?
- What breaks if the cert rotates tonight?
- Is this security knob solving a real problem or adding folklore complexity?
- Can we explain this TLS block without referencing unofficial guides?

## Field Notes

### `server_name`

This field is one of the highest-signal review points in outbound TLS. If it looks copy-pasted or unexplained, the whole security posture deserves re-checking.

### Cert Material Paths

Absolute paths, rotation semantics and filesystem permissions are part of the security design. A clean JSON with a wrong path is not a networking issue, it is still a security deployment issue.

### REALITY Keys

Because the field names look simple, teams often under-document them. Senior practice is to state explicitly which key lives where, who generates it and which artifacts are safe to distribute.

## Scenario Catalog

### Scenario: Public VPS Service

Keep the first TLS deployment boring: normal certificate files, explicit name, minimal ALPN. Fancy features come later.

### Scenario: Managed Client Fleet

Where many clients share one outbound profile, `server_name`, pinning policy and rotation process become documentation requirements, not just config details.

### Scenario: Migration from Old Snippets

If the config contains obscure ECH or fingerprint fields from old posts, assume debt first and sophistication second. Compare everything against stable docs before trusting it.

## Change Management Notes

Security changes should move from trust-simple to trust-complex:

1. minimal TLS;
2. correct identity verification;
3. protocol-specific extras;
4. advanced controls such as pinning or specialized handshakes.

If rollback from a security change is not documented, the change is not production-ready. This is especially true for certificate rotations and REALITY parameter changes.
