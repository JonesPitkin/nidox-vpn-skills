# Release v1.1.0

Status: approved for local release preparation; not published.

## Recommendation

Use `v1.1.0`, not `v2.0.0`.

The update expands and corrects documentation while preserving skill names,
directory layout, routing responsibilities, and user-facing workflows. The
upstream 3X-UI API route migration is breaking for integrations, but it is
documented by this repository rather than introduced by it.

## Verified Baseline

- 3X-UI `v3.3.0`, release commit
  `f8e89cc848b908d8507f30e0e35a0a74d6fe983c`
- 3X-UI Wiki commit
  `264a7b202aacc0036a1fbb95a285d3e2981a3578`
- bundled Xray-core artifact `v26.6.1`; upstream stable `v26.3.27`
- sing-box `v1.13.13`
- Hysteria `v2.9.2`
- Cloudflare Developers documentation checked June 12, 2026

## Changed Scope

- 60 tracked files modified
- 7 new files prepared
- all five specialist Skills audited:
  `3x-ui-install`, `3x-ui-inbounds`, `3x-ui-routing`,
  `3x-ui-security`, and `3x-ui-cloudflare`
- router metadata, README, changelog, version matrix, source links, and the
  existing `3x-ui-vps` frontmatter also normalized

## New References

- `3x-ui-inbounds/references/mtproto.md`
- `3x-ui-install/references/api.md`
- `3x-ui-routing/references/outbound-subscriptions.md`
- `3x-ui-routing/references/warp.md`
- `3x-ui-cloudflare/references/xhttp.md`
- `scripts/audit_repository.py`

## New Upstream Features Documented

- managed MTProto FakeTLS through the `mtg` sidecar
- typed OpenAPI and Bearer API tokens
- subscription-based outbounds with refresh and stable tags
- manual and automatic WARP IP rotation
- custom subscription page templates
- multi-hop/node state and per-group traffic changes
- current XHTTP modes and advanced fields
- current REALITY target, ML-DSA, hybrid key exchange, and fallback risks

## Replaced or Corrected Guidance

- 3X-UI baseline `v3.2.8` replaced with `v3.3.0`
- `/panel/setting` and `/panel/xray` replaced with `/panel/api/setting` and
  `/panel/api/xray`
- SplitHTTP naming normalized to XHTTP
- legacy sing-box WireGuard outbound replaced with WireGuard endpoint guidance
- legacy sing-box GeoIP/Geosite and sniff fields replaced with rule-set and
  route-action guidance
- Cloudflare standard proxy separated from Spectrum and Tunnel capabilities
- old Cloudflare Tunnel documentation paths replaced with current connector
  paths
- Hysteria application features separated from Xray's Hysteria implementation
- source-code links pinned to the documented 3X-UI `v3.3.0` tag
- draft TODO markers replaced with explicit source limitations

## Audit Results

- repository audit: passed, 91 Markdown files and 70 references
- `quick_validate.py`: all 7 Skills passed
- local Markdown links: passed
- 3X-UI source links: 87 checked against tag `v3.3.0`, none missing
- external URLs: 148 checked; no broken documentation links
- duplicate headings: none
- empty references: none
- stale `TODO`/`FIXME`/`TBD` markers: none
- Python compilation: passed
- shell syntax checks: passed
- `git diff --check`: passed

The `https://1.1.1.1/dns-query` endpoint returns HTTP 400 when checked without
a DNS payload; this is expected and is not a broken link. Unrelated
`backend-api`/`chatgpt.com` 403 responses were excluded.

## Release Checklist

- [x] compare official sources and current repository content
- [x] update Skills and references
- [x] run structural, link, syntax, and skill validation
- [x] review this change report
- [x] confirm version `v1.1.0`
- [ ] create commit
- [ ] create tag
- [ ] publish release

The final three actions require explicit approval.
