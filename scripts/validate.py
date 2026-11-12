#!/usr/bin/env python3
"""Dependency-free structural and distribution checks for Unbullshit."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ("unbullshit", "unbullshit-plan", "unbullshit-audit", "unbullshit-improve")
VERSION = "1.0.0"
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def parse_json(path: str, errors: list[str]) -> dict:
    try:
        value = json.loads((ROOT / path).read_text(encoding="utf-8"))
        if isinstance(value, dict):
            return value
        errors.append(f"{path}: expected JSON object")
    except (OSError, ValueError) as exc:
        errors.append(f"{path}: {exc}")
    return {}


def check() -> list[str]:
    errors: list[str] = []
    if not (ROOT / "skills").is_dir():
        return ["Missing skills directory"]
    actual = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
    if actual != set(SKILLS):
        errors.append(f"Unexpected skill directories: {sorted(actual)}")
    for name in SKILLS:
        path = ROOT / "skills" / name / "SKILL.md"
        if not path.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue
        content = path.read_text(encoding="utf-8")
        lines = content.splitlines()
        if not lines or lines[0] != "---":
            errors.append(f"{name}: missing frontmatter")
            continue
        try:
            end = lines.index("---", 1)
        except ValueError:
            errors.append(f"{name}: unclosed frontmatter")
            continue
        metadata: dict[str, str] = {}
        for line in lines[1:end]:
            if not line.strip():
                continue
            if ":" not in line:
                errors.append(f"{name}: invalid frontmatter line")
                continue
            key, value = [piece.strip() for piece in line.split(":", 1)]
            if key in metadata:
                errors.append(f"{name}: duplicate frontmatter key {key}")
            metadata[key] = value
        if metadata.get("name") != name or not NAME.fullmatch(metadata.get("name", "")):
            errors.append(f"{name}: invalid name")
        if not 1 <= len(metadata.get("description", "")) <= 1024:
            errors.append(f"{name}: invalid description")
        if not any(line.strip() for line in lines[end + 1:]) or len(lines) > 500:
            errors.append(f"{name}: instructions empty or too large")
        if not content.endswith("\n"):
            errors.append(f"{name}: missing final newline")

    root = parse_json("plugin.json", errors)
    claude = parse_json(".claude-plugin/plugin.json", errors)
    codex = parse_json(".codex-plugin/plugin.json", errors)
    marketplace = parse_json(".claude-plugin/marketplace.json", errors)
    for path, data in (
        ("plugin.json", root),
        (".claude-plugin/plugin.json", claude),
        (".codex-plugin/plugin.json", codex),
    ):
        if data.get("name") != "unbullshit" or data.get("version") != VERSION:
            errors.append(f"{path}: incorrect identity or version")
    if root.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        errors.append("Portable plugin schema missing")
    ext = root.get("extensions", {}).get("com.openai", {})
    interface = ext.get("interface", {}) if isinstance(ext, dict) else {}
    if not interface.get("displayName") or not interface.get("defaultPrompt"):
        errors.append("Portable plugin presentation missing")
    if codex.get("skills") != "./skills/":
        errors.append("Codex skill path missing")
    entries = marketplace.get("plugins", [])
    if (
        marketplace.get("name") != "unbullshit-skills"
        or not isinstance(entries, list)
        or len(entries) != 1
        or not isinstance(entries[0], dict)
        or entries[0].get("name") != "unbullshit"
        or entries[0].get("source") != "./"
    ):
        errors.append("Claude marketplace entry mismatch")

    rule = ROOT / ".cursor" / "rules" / "unbullshit.mdc"
    if not rule.is_file():
        errors.append("Cursor project rule missing")
    else:
        body = rule.read_text(encoding="utf-8")
        if not body.startswith("---\ndescription:") or "\nalwaysApply: true\n" not in body:
            errors.append("Cursor project rule frontmatter invalid")
    if not (ROOT / "examples" / "AGENTS.md").is_file():
        errors.append("Opt-in standing guidance missing")

    for graphic in ("assets/logo.svg", "assets/wordmark.svg"):
        try:
            ET.parse(ROOT / graphic)
        except (ET.ParseError, OSError) as exc:
            errors.append(f"{graphic}: {exc}")

    required = (
        "README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md",
        "docs/install.md", "docs/compatibility.md", "docs/troubleshooting.md",
        "docs/brand.md", "docs/releases/1.0.0.md",
        "examples/demo.md", "examples/before-after.md",
    )
    for name in required:
        if not (ROOT / name).is_file():
            errors.append(f"Missing {name}")
    changelog = ROOT / "CHANGELOG.md"
    if changelog.exists() and "## 1.0.0" not in changelog.read_text(encoding="utf-8"):
        errors.append("Missing version 1.0.0 in changelog")
    return errors


def main() -> int:
    errors = check()
    if errors:
        for problem in errors:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1
    print(f"OK: {len(SKILLS)} portable skills and v{VERSION} packaging validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
