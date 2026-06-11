# Migration Guide

## From `nidox-vpn-skills/openwrt-cudy-wr3000s`

The previous meta-repository held a single broad device skill. This standalone repository becomes the source of truth and preserves the same content in a split specialist structure.

## Migration Path

1. maintain authoritative content in this standalone repository
2. sync snapshots into `nidox-vpn-skills/openwrt-cudy-wr3000s-skills/`
3. keep the older compatibility entrypoint in `skills/openwrt-cudy-wr3000s/` until downstream references are updated
