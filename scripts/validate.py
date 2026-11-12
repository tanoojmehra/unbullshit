#!/usr/bin/env python3
"""Dependency-free structural validation of the four public Agent Skills."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
EXPECTED = {
    "unbullshit",
    "unbullshit-plan",
    "unbullshit-audit",
    "unbullshit-improve",
}
NAME_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    file = path / "SKILL.md"
    if not file.is_file():
        return [f"{path.name}: missing SKILL.md"]

    text = file.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return [f"{path.name}: missing YAML frontmatter"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return [f"{path.name}: unclosed YAML frontmatter"]

    # Deliberately validate the minimal single-line metadata used in this repo.
    # This is not intended as a general-purpose YAML parser.
    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"{path.name}: malformed metadata line: {line!r}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in metadata:
            errors.append(f"{path.name}: duplicate metadata key {key}")
        metadata[key] = value.strip()

    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if name != path.name:
        errors.append(f"{path.name}: metadata name must equal directory name")
    if not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        errors.append(f"{path.name}: invalid skill name")
    if not description or len(description) > 1024:
        errors.append(f"{path.name}: description required, max 1024 characters")
    if len(lines) > 500:
        errors.append(f"{path.name}: SKILL.md exceeds 500 lines")
    if not any(line.strip() for line in lines[end + 1 :]):
        errors.append(f"{path.name}: missing instructions")
    if not text.endswith("\n"):
        errors.append(f"{path.name}: missing final newline")
    return errors


def main() -> int:
    if not SKILLS.is_dir():
        print("Missing skills directory", file=sys.stderr)
        return 1
    actual = {path.name for path in SKILLS.iterdir() if path.is_dir()}
    errors = [
        *(f"Missing skill: {name}" for name in sorted(EXPECTED - actual)),
        *(f"Unexpected skill directory: {name}" for name in sorted(actual - EXPECTED)),
    ]
    for name in sorted(actual & EXPECTED):
        errors.extend(validate_skill(SKILLS / name))
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"OK: {len(EXPECTED)} portable skills validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
