# Migration Guide

## From `nidox-vpn-skills/skills/3x-ui`

The legacy `skills/3x-ui/` directory in `nidox-vpn-skills` is a thin pointer. The standalone source of truth is this repository.

## Recommended Migration

1. use this standalone repository for authoring and publication
2. sync a full snapshot into `nidox-vpn-skills/3x-ui-skills/`
3. keep the legacy `skills/3x-ui/README.md` as a compatibility marker until downstream automation is updated

## Skill Routing

- start with [`3x-ui`](3x-ui/SKILL.md) when the operator request is broad
- go directly to domain skills when the task is already scoped
- use `3x-ui-vps` only when remote infrastructure mutation is explicitly requested
