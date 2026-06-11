# Contributing

## Principles

- use official upstream sources whenever behavior, fields, or UI flows are version-sensitive
- keep secrets, tokens, UUIDs, private keys, short IDs, and panel credentials out of the repository
- prefer additive updates to `references/` instead of bloating `SKILL.md`
- keep each skill focused on a single responsibility boundary

## Pull Request Checklist

1. verify Markdown links
2. verify `SKILL.md` plus `agents/openai.yaml`
3. verify that new operational advice is backed by official sources
4. verify that no sample contains live secrets
5. update `CHANGELOG.md` when repository behavior changes materially

## Validation

Run local validation before publishing:

```sh
git status --short
find . -name '.DS_Store' -o -name '*.tmp'
```
