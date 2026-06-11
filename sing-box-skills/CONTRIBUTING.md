# Contributing

Thank you for contributing to `sing-box-skills`.

## Contribution Principles

This repository accepts only material grounded in:

- official `sing-box` documentation
- official SagerNet repositories
- official release and migration information

Do not contribute:

- third-party blog guidance as canonical truth
- forum folklore
- speculative compatibility claims
- new-config recommendations based on deprecated `GeoSite` or `GeoIP` paths

## Contribution Workflow

1. Identify the target version of `sing-box`.
2. Validate the change against official sources.
3. Update the relevant `SKILL.md` or repository guide.
4. Update `VERSION_MATRIX.md` or `MIGRATION_GUIDE.md` if version semantics are involved.
5. Keep examples in the correct JSON shape for the intended stable line.
6. Re-check internal links and repository structure before finalizing.

## Review Expectations

Contributions should preserve:

- production-safe wording
- version awareness
- migration awareness
- explicit separation between stable and alpha guidance
- clear environment targeting for Linux, OpenWrt, VPS and sing-box-compatible scenarios

