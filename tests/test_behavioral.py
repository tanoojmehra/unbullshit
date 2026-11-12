"""Contract tests for offline behavioral evaluator."""
from __future__ import annotations
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("evaluate_behavior", ROOT / "scripts/evaluate_behavior.py")
assert spec and spec.loader
ev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ev)
CASES = ROOT / "tests/behavioral/cases.json"
BASE = ROOT / "tests/behavioral/fixtures/baseline.json"
ENABLED = ROOT / "tests/behavioral/fixtures/skill.json"


class BehavioralTests(unittest.TestCase):
    def test_cases_cover_every_skill_and_expected_categories(self):
        cases = ev.load_cases(CASES)
        self.assertEqual({c["skill"] for c in cases}, set(ev.SKILLS))
        self.assertGreaterEqual(len(cases), 15)
        for case in cases:
            self.assertTrue(case["critical_requirements"])
            self.assertTrue(case["rubric"])

    def test_fixtures_match_cases(self):
        cases = ev.load_cases(CASES)
        self.assertEqual(ev.load_fixture(BASE, cases)["kind"], "illustrative")
        self.assertEqual(ev.load_fixture(ENABLED, cases)["kind"], "illustrative")

    def test_output_is_deterministic_for_saved_fixtures(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = ["--baseline", str(BASE), "--enabled", str(ENABLED), "--output-dir", tmp]
            self.assertEqual(ev.main(args), 0)
            first = (Path(tmp) / "report.json").read_bytes()
            self.assertEqual(ev.main(args), 0)
            self.assertEqual(first, (Path(tmp) / "report.json").read_bytes())
            report = json.loads(first)
            self.assertIn("illustrative", report["provenance"])
            self.assertEqual(len(report["cases"]), len(ev.load_cases(CASES)))
            self.assertEqual(report["subjective_scores"], "not assessed; human rubric required")

    def test_bad_fixture_fails_closed(self):
        cases = ev.load_cases(CASES)
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "fixture.json"
            bad.write_text(json.dumps({"kind": "live-model-run", "responses": {}}))
            with self.assertRaisesRegex(ValueError, "exactly match"):
                ev.load_fixture(bad, cases)

    def test_failed_adapter_not_reported_as_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "adapter.py"
            script.write_text("import sys\nsys.exit(7)\n")
            status = ev.main(["--adapter", "python3 " + str(script), "--output-dir", tmp])
            self.assertEqual(status, 2)
            self.assertFalse((Path(tmp) / "report.json").exists())

    def test_adapter_sees_input_only_not_answer_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "adapter.py"
            script.write_text("import json,sys\np=json.load(sys.stdin)\n"
                              "assert 'checks' not in p['case']\n"
                              "assert 'expected_positive' not in p['case']\n"
                              "assert not p['skill_instructions'] if p['variant']=='baseline' else p['skill_instructions']\n"
                              "print(json.dumps({'response':'visible output'}))\n")
            case = ev.load_cases(CASES)[0]
            config = {"timeout_seconds": 5, "model": "local", "temperature": 0, "top_p": 1, "seed": 1}
            self.assertEqual(ev.run_adapter("python3 " + str(script), case, "baseline", config, 0), "visible output")
            self.assertEqual(ev.run_adapter("python3 " + str(script), case, "skill", config, 0), "visible output")

    def test_literal_checks_are_not_semantic_scores(self):
        case = ev.load_cases(CASES)[0]
        self.assertTrue(ev.score(case, "existing")[-1]["passed"])
        self.assertFalse(ev.score(case, "reporting platform")[1]["passed"])


if __name__ == "__main__":
    unittest.main()
