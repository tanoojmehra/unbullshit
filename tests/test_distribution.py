"""Minimal standard-library regression tests for the distribution."""
from __future__ import annotations

import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("unbullshit", "unbullshit-plan", "unbullshit-audit", "unbullshit-improve")


class DistributionTests(unittest.TestCase):
    def test_metadata_and_skills(self):
        for name in SKILLS:
            with self.subTest(skill=name):
                body = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue(body.startswith(f"---\nname: {name}\ndescription:"))
                self.assertIn("\n---\n", body)

    def test_three_manifests_share_version(self):
        for filename in ("plugin.json", ".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
            with self.subTest(file=filename):
                value = json.loads((ROOT / filename).read_text(encoding="utf-8"))
                self.assertEqual(value["name"], "unbullshit")
                self.assertEqual(value["version"], "1.0.0")

    def test_codex_skills_path(self):
        data = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(data["skills"], "./skills/")

    def test_brand_graphics_parse_as_svg(self):
        for filename in ("assets/logo.svg", "assets/wordmark.svg"):
            with self.subTest(file=filename):
                root = ET.parse(ROOT / filename).getroot()
                self.assertTrue(root.tag.endswith("svg"))

    def test_cursor_rule_is_optional(self):
        body = (ROOT / ".cursor/rules/unbullshit.mdc").read_text()
        guide = (ROOT / "docs/install.md").read_text()
        self.assertIn("alwaysApply: true", body)
        self.assertIn("copying", guide.lower())
        self.assertIn("target project", guide.lower())

    def test_readme_local_links_resolve(self):
        readme = (ROOT / "README.md").read_text()
        for target in re.findall(r"\]\(([^)]+)\)", readme):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            path = target.split("#", 1)[0]
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).exists(), f"Broken README link: {path}")


if __name__ == "__main__":
    unittest.main()
