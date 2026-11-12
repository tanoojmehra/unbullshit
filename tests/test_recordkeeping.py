"""Tests for deterministic location selection and record history."""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

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


if __name__ == "__main__":
    unittest.main()
