"""Tests for deterministic location selection and record history."""

from __future__ import annotations

import importlib.util
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "unbullshit_log.py"
spec = importlib.util.spec_from_file_location("unbullshit_log", SOURCE)
assert spec and spec.loader
log = importlib.util.module_from_spec(spec)
spec.loader.exec_module(log)


def track(root: Path, relative: str) -> None:
    file = root / relative
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text("example\n", encoding="utf-8")
    subprocess.run(["git", "add", "--", relative], cwd=root, check=True,
                   capture_output=True)


class RecordTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True, capture_output=True)

    def test_special_project_brain_precedes_docs(self):
        track(self.root, "brain/kb/note.md")
        track(self.root, "docs/readme.md")
        self.assertEqual(log.select_path(self.root, brain_enabled=True),
                         self.root / "brain/unbullshit")

    def test_brain_without_integration_does_not_override_docs(self):
        track(self.root, "brain/kb/note.md")
        track(self.root, "docs/readme.md")
        self.assertEqual(log.select_path(self.root), self.root / "docs/unbullshit")

    def test_tracked_integration_detected(self):
        track(self.root, "kenmark-skills/README.md")
        track(self.root, "brain/kb/note.md")
        self.assertEqual(log.select_path(self.root), self.root / "brain/unbullshit")

    def test_tracked_docs_destination(self):
        track(self.root, "docs/readme.md")
        self.assertEqual(log.select_path(self.root), self.root / "docs/unbullshit")

    def test_brain_only_without_integration_goes_to_root(self):
        track(self.root, "brain/note.md")
        self.assertEqual(log.select_path(self.root), self.root / "unbullshit")

    def test_untracked_directories_not_mistaken_for_tracked(self):
        (self.root / "docs").mkdir()
        (self.root / "brain").mkdir()
        (self.root / "docs" / "untracked.md").write_text("untracked")
        self.assertEqual(log.select_path(self.root), self.root / "unbullshit")

    def test_existing_register_wins_over_new_placement_rule(self):
        track(self.root, "docs/readme.md")
        original = self.root / "unbullshit"
        log.initialize(original)
        self.assertEqual(log.select_path(self.root), original)

    def test_competing_existing_registers_require_resolution(self):
        log.initialize(self.root / "docs/unbullshit")
        log.initialize(self.root / "unbullshit")
        with self.assertRaisesRegex(ValueError, "Multiple existing"):
            log.select_path(self.root)

    def test_no_git_destination_uses_root(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            (project / "docs").mkdir()
            self.assertEqual(log.select_path(project), project / "unbullshit")

    def test_locating_does_not_create_files(self):
        location = log.select_path(self.root)
        self.assertFalse(location.exists())

    def test_findings_index_and_status_history(self):
        location = log.select_path(self.root)
        args = SimpleNamespace(title="Duplicate approval", classification="unnecessary-friction",
                               source="unbullshit-audit", priority="high",
                               summary="A redundant approval blocks a release",
                               evidence="Workflow file examined", recommendation="Consolidate")
        first = log.add(location, args)
        self.assertEqual(first.name, "UB-0001.md")
        second = log.add(location, SimpleNamespace(**{**vars(args),
                             "title": "Speculative queue", "classification": "unjustified-complexity"}))
        self.assertEqual(second.name, "UB-0002.md")
        register = (location / "REGISTER.md").read_text()
        self.assertLess(register.index("UB-0001"), register.index("UB-0002"))
        log.set_status(location, "UB-0001", "resolved", "Verified by tests")
        self.assertIn("| resolved |", (location / "REGISTER.md").read_text())
        self.assertIn("Verified by tests", first.read_text())
        self.assertTrue((location / "README.md").exists())

    def test_resolved_finding_keeps_its_identity(self):
        folder = log.select_path(self.root)
        args = SimpleNamespace(title="Redundant queue", classification="unjustified-complexity",
                               source="unbullshit-audit", priority="medium",
                               summary="Duplicated behavior", evidence="Reviewed workflows",
                               recommendation="Consolidate")
        log.add(folder, args)
        log.set_status(folder, "UB-0001", "resolved", "Verified remediation")
        with self.assertRaisesRegex(ValueError, "already exists"):
            log.add(folder, args)
        log.set_status(folder, "UB-0001", "open", "Regression reopened for review")
        self.assertEqual(len(log.records(folder)), 1)
        self.assertIn("Regression reopened", (folder / "findings/UB-0001.md").read_text())

    def test_duplicate_open_finding_rejected(self):
        folder = log.select_path(self.root)
        args = SimpleNamespace(title="Duplicate approval", classification="defect",
                               source="unbullshit-audit", priority="medium",
                               summary="Broken result", evidence="Observed failure",
                               recommendation="Fix behavior")
        log.add(folder, args)
        with self.assertRaisesRegex(ValueError, "already exists"):
            log.add(folder, args)

    def test_malformed_record_rejects_rebuild(self):
        folder = log.select_path(self.root)
        log.initialize(folder)
        path = folder / "findings" / "UB-0001.md"
        path.parent.mkdir()
        path.write_text("---\nid: UB-0001\nclassification: fake\n"
                        "status: open\npriority: high\nsource: unbullshit-audit\n"
                        "updated: 2026-11-13\n---\n# Broken record\n")
        with self.assertRaises(ValueError):
            log.rebuild(folder)


    def test_indexless_existing_records_keep_their_location(self):
        original = self.root / "unbullshit"
        (original / "findings").mkdir(parents=True)
        (original / "findings" / "UB-0001.md").write_text("incomplete record")
        track(self.root, "docs/readme.md")
        self.assertEqual(log.select_path(self.root), original)

    def test_cli_read_only_commands_do_not_create_register(self):
        for command in ("locate", "list"):
            result = subprocess.run([sys.executable, str(SOURCE), "--project", str(self.root), command],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / "unbullshit").exists())

    def test_concurrent_adds_have_unique_ids_and_consistent_index(self):
        jobs = []
        for n in range(6):
            jobs.append(subprocess.Popen([
                sys.executable, str(SOURCE), "--project", str(self.root), "add",
                "--title", "Distinct finding " + str(n), "--classification", "defect",
                "--summary", "Observed failure", "--evidence", "Reproduced locally",
                "--recommendation", "Fix with tests"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
        for process in jobs:
            out, err = process.communicate(timeout=30)
            self.assertEqual(process.returncode, 0, err + out)
        folder = self.root / "unbullshit"
        entries = log.records(folder)
        self.assertEqual(len(entries), 6)
        self.assertEqual({e[1]["id"] for e in entries},
                         {"UB-" + str(n).zfill(4) for n in range(1, 7)})
        index = (folder / "REGISTER.md").read_text()
        self.assertEqual(index.count("](findings/"), 6)

    def test_stale_lock_fails_without_overwriting(self):
        folder = self.root / "unbullshit"
        log.initialize(folder)
        (folder / ".unbullshit-write.lock").mkdir()
        before = (folder / "REGISTER.md").read_text()
        with patch.object(log.time, "monotonic", side_effect=[0, 11]):
            with self.assertRaisesRegex(ValueError, "Write lock busy"):
                log.rebuild(folder)
        self.assertEqual((folder / "REGISTER.md").read_text(), before)

    def test_malformed_date_fails_safely(self):
        folder = self.root / "unbullshit"
        args = SimpleNamespace(title="Incomplete", classification="defect", priority="low",
                               source="unbullshit-audit", summary="Broken", evidence="Observed",
                               recommendation="Fix")
        path = log.add(folder, args)
        original = path.read_text()
        path.write_text(original.replace("created: ", "creation: ", 1))
        before = (folder / "REGISTER.md").read_text()
        with self.assertRaisesRegex(ValueError, "dates"):
            log.rebuild(folder)
        self.assertEqual((folder / "REGISTER.md").read_text(), before)

    def test_duplicate_numeric_ids_rejected(self):
        folder = self.root / "unbullshit"
        args = SimpleNamespace(title="One", classification="defect", priority="low",
                               source="unbullshit-audit", summary="Broken", evidence="Observed",
                               recommendation="Fix")
        first = log.add(folder, args)
        second = first.parent / "UB-00001.md"
        second.write_text(first.read_text().replace("UB-0001", "UB-00001").replace("# One", "# Two"))
        with self.assertRaisesRegex(ValueError, "Duplicate numeric"):
            log.rebuild(folder)

    def test_unwritable_project_fails_without_creating_finding(self):
        folder = self.root / "unbullshit"
        with patch.object(log, "write_lock", side_effect=PermissionError("read-only")):
            with self.assertRaises(PermissionError):
                log.add(folder, SimpleNamespace(title="No", summary="No",
                                                  evidence="No", recommendation="No"))
        self.assertFalse((folder / "findings").exists())

    def test_installed_skills_describe_cli_free_recording(self):
        for name in ("unbullshit", "unbullshit-plan", "unbullshit-audit", "unbullshit-improve"):
            text = (SOURCE.parents[1] / "skills" / name / "SKILL.md").read_text()
            self.assertIn("helper CLI is optional", text)
            self.assertIn("target project", text)


if __name__ == "__main__":
    unittest.main()
