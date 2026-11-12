#!/usr/bin/env python3
"""Optional, dependency-free project-local Unbullshit record keeper."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

CLASSES = ("unjustified-complexity", "unnecessary-friction", "defect",
           "justified-complexity", "uncertain")
STATUSES = ("open", "needs-review", "accepted", "in-progress", "resolved", "wont-fix")
SOURCES = ("unbullshit", "unbullshit-plan", "unbullshit-audit", "unbullshit-improve")
PRIORITIES = ("high", "medium", "low", "none")
ID_RE = re.compile(r"UB-(\d{4,})$")
PATH_RE = re.compile(r"UB-(\d{4,})\.md$")
KEY_RE = re.compile(r"([a-z][a-z-]*): (.*)$")

INTRO = """# Unbullshit project records

This is a project-local record of consequential decisions and supported findings.

- REGISTER.md: generated index of findings; edit finding files, not the table.
- findings/: one Markdown file per finding, with stable UB IDs.
- decisions/: consequential founder or architecture choices, if requested.
- reviews/: summaries of audits, including useful zero-findings reviews.

A finding may be unnecessary complexity, invented friction, a defect, justified complexity, or uncertain.
Do not call defects, justified safeguards, or unverified suspicions bullshit.
Record evidence, alternatives, risks and verification. Never turn this register into a permission gate.
Do not record secrets or sensitive customer data.

See the public Unbullshit documentation at docs/recordkeeping.md.
"""
INDEX = """# Unbullshit register

Index of recorded findings. Not every finding is bullshit.
The source of truth is the individual findings/UB-XXXX.md file.

| ID | Finding | Classification | Status | Priority | Updated |
| --- | --- | --- | --- | --- | --- |
"""


def today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def project_root(base: Path) -> Path:
    base = base.expanduser().resolve()
    if not base.is_dir():
        raise ValueError(f"Not a directory: {base}")
    try:
        result = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=base,
                                capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return base
    return Path(result.stdout.strip()).resolve() if result.returncode == 0 else base


def tracked_files(root: Path) -> set[str]:
    try:
        result = subprocess.run(["git", "ls-files", "--cached", "-z"], cwd=root,
                                capture_output=True, check=False)
    except FileNotFoundError:
        return set()
    return {os.fsdecode(x) for x in result.stdout.split(b"\x00") if x} if result.returncode == 0 else set()


def select_path(root: Path, *, brain_enabled: bool = False) -> Path:
    tracked = tracked_files(root)
    brain = any(name.startswith("brain/") for name in tracked)
    docs = any(name.startswith("docs/") for name in tracked)
    markers = ("kenmark-studio", "kenmark-skills")
    detected = any(any(part.lower() in markers for part in name.split("/")) for name in tracked)
    if brain and (brain_enabled or detected):
        return root / "brain" / "unbullshit"
    if docs:
        return root / "docs" / "unbullshit"
    return root / "unbullshit"


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def initialize(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    for name, text in (("README.md", INTRO), ("REGISTER.md", INDEX)):
        path = folder / name
        if not path.exists():
            with path.open("x", encoding="utf-8") as stream:
                stream.write(text)


def read_record(path: Path) -> tuple[dict[str, str], str, str]:
    body = path.read_text(encoding="utf-8")
    lines = body.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"{path}: missing frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError(f"{path}: unclosed frontmatter") from exc
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        match = KEY_RE.fullmatch(line)
        if not match or match[1] in fields:
            raise ValueError(f"{path}: invalid or duplicate metadata")
        fields[match[1]] = match[2]
    heading = next((line[2:] for line in lines[end + 1:] if line.startswith("# ")), "")
    if fields.get("id") != path.stem or not heading:
        raise ValueError(f"{path}: ID mismatch or missing title")
    if fields.get("classification") not in CLASSES or fields.get("status") not in STATUSES:
        raise ValueError(f"{path}: invalid classification/status")
    if fields.get("priority") not in PRIORITIES or fields.get("source") not in SOURCES:
        raise ValueError(f"{path}: invalid priority/source")
    return fields, heading, body


def records(folder: Path) -> list[tuple[Path, dict[str, str], str]]:
    found: list[tuple[Path, dict[str, str], str]] = []
    directory = folder / "findings"
    if not directory.is_dir():
        return found
    for path in directory.glob("UB-*.md"):
        if not PATH_RE.fullmatch(path.name):
            raise ValueError(f"Invalid finding filename: {path.name}")
        fields, heading, _ = read_record(path)
        found.append((path, fields, heading))
    found.sort(key=lambda item: int(item[1]["id"][3:]))
    return found


def rebuild(folder: Path) -> None:
    initialize(folder)
    lines = [INDEX]
    for path, fields, heading in records(folder):
        title = heading.replace("|", r"\|").strip()
        lines.append(
            f"| [{fields['id']}](findings/{path.name}) | {title} | "
            f"{fields['classification']} | {fields['status']} | "
            f"{fields['priority']} | {fields['updated']} |\n"
        )
    atomic_write(folder / "REGISTER.md", "".join(lines))


def line(value: str, label: str) -> str:
    value = value.strip()
    if not value or "\n" in value or "\r" in value:
        raise ValueError(f"{label} must be a non-empty single line")
    return value


def add(folder: Path, args: argparse.Namespace) -> Path:
    title = line(args.title, "title")
    summary = line(args.summary, "summary")
    evidence = line(args.evidence, "evidence")
    recommendation = line(args.recommendation, "recommendation")
    initialize(folder)
    directory = folder / "findings"
    directory.mkdir(exist_ok=True)
    existing = records(folder)
    if any(t.casefold() == title.casefold() and f["status"] != "resolved" for _, f, t in existing):
        raise ValueError("An unresolved finding with this title already exists")
    next_id = max((int(f["id"][3:]) for _, f, _ in existing), default=0) + 1
    date = today()
    while True:
        identifier = f"UB-{next_id:04d}"
        path = directory / f"{identifier}.md"
        body = (
            f"---\nid: {identifier}\nclassification: {args.classification}\n"
            f"status: open\npriority: {args.priority}\nsource: {args.source}\n"
            f"created: {date}\nupdated: {date}\n---\n\n# {title}\n\n"
            f"## Observation\n\n{summary}\n\n"
            f"## Evidence and limits\n\n{evidence}\n\n"
            f"## Recommendation\n\n{recommendation}\n\n"
            "## Trade-offs, safeguards and verification\n\n"
            "Not yet documented. Confirm what must remain before making changes.\n\n"
            f"## Decision and history\n\n- {date}: Recorded as open; no implementation implied.\n"
        )
        try:
            with path.open("x", encoding="utf-8") as stream:
                stream.write(body)
            break
        except FileExistsError:
            next_id += 1
    rebuild(folder)
    return path


def set_status(folder: Path, identifier: str, status: str, note: str) -> Path:
    if not ID_RE.fullmatch(identifier):
        raise ValueError("Expected a finding ID such as UB-0001")
    note = line(note, "note")
    path = folder / "findings" / f"{identifier}.md"
    fields, _, body = read_record(path)
    date = today()
    body = body.replace(f"status: {fields['status']}\n", f"status: {status}\n", 1)
    body = body.replace(f"updated: {fields['updated']}\n", f"updated: {date}\n", 1)
    body += f"\n- {date}: {fields['status']} -> {status}. {note}\n"
    atomic_write(path, body)
    rebuild(folder)
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path("."))
    parser.add_argument("--brain-enabled", action="store_true",
                        help="Explicitly confirmed integration; requires tracked brain/")
    sub = parser.add_subparsers(dest="action", required=True)
    for item in ("locate", "init", "rebuild", "list"):
        sub.add_parser(item)
    create = sub.add_parser("add")
    create.add_argument("--title", required=True)
    create.add_argument("--classification", choices=CLASSES, required=True)
    create.add_argument("--priority", choices=PRIORITIES, default="medium")
    create.add_argument("--source", choices=SOURCES, default="unbullshit-audit")
    create.add_argument("--summary", required=True)
    create.add_argument("--evidence", required=True)
    create.add_argument("--recommendation", required=True)
    change = sub.add_parser("status")
    change.add_argument("id")
    change.add_argument("--set", dest="new_status", choices=STATUSES, required=True)
    change.add_argument("--note", required=True)
    args = parser.parse_args(argv)
    try:
        root = project_root(args.project)
        folder = select_path(root, brain_enabled=args.brain_enabled)
        if args.action == "locate":
            print(folder.relative_to(root))
        elif args.action == "init":
            initialize(folder)
            print(folder)
        elif args.action == "rebuild":
            rebuild(folder)
            print(folder / "REGISTER.md")
        elif args.action == "list":
            for _, fields, heading in records(folder):
                print(f"{fields['id']}  {fields['status']}  {fields['classification']}  {heading}")
        elif args.action == "add":
            print(add(folder, args))
        elif args.action == "status":
            print(set_status(folder, args.id, args.new_status, args.note))
        return 0
    except (OSError, ValueError) as exc:
        parser.exit(2, f"unbullshit: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
