#!/usr/bin/env python3
"""Run lightweight structural checks for the 3x-ui-skills repository."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
UNFINISHED = re.compile(r"\b(?:TODO|FIXME|TBD)\s*:", re.IGNORECASE)


def markdown_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts)


def local_link_issues(path: Path, text: str) -> list[str]:
    issues = []
    for raw_target in MARKDOWN_LINK.findall(text):
        target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = unquote(target.split("#", 1)[0])
        if target and not (path.parent / target).resolve().exists():
            issues.append(f"{path.relative_to(ROOT)}: missing local link {raw_target}")
    return issues


def duplicate_heading_issues(path: Path, text: str) -> list[str]:
    normalized = [
        re.sub(r"\s+", " ", heading.strip().casefold())
        for _, heading in HEADING.findall(text)
    ]
    return [
        f"{path.relative_to(ROOT)}: duplicate heading {heading!r}"
        for heading, count in Counter(normalized).items()
        if count > 1
    ]


def main() -> int:
    issues: list[str] = []
    files = markdown_files()

    for path in files:
        text = path.read_text(encoding="utf-8")
        issues.extend(local_link_issues(path, text))
        issues.extend(duplicate_heading_issues(path, text))
        if "references" in path.parts and not text.strip():
            issues.append(f"{path.relative_to(ROOT)}: empty reference")
        if UNFINISHED.search(text):
            issues.append(f"{path.relative_to(ROOT)}: unfinished marker")

    if issues:
        print("\n".join(issues))
        print(f"\nRepository audit failed: {len(issues)} issue(s).")
        return 1

    reference_count = sum(1 for path in files if "references" in path.parts)
    print(
        f"Repository audit passed: {len(files)} Markdown files, "
        f"{reference_count} references."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
