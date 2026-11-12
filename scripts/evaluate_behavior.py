#!/usr/bin/env python3
"""Offline-first, transparent behavioral checks; not a measure of model quality."""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "tests" / "behavioral" / "cases.json"
SKILLS = ("unbullshit", "unbullshit-plan", "unbullshit-audit", "unbullshit-improve")
CHECKS = ("contains", "absent", "max_questions", "regex")


def load_cases(path: Path) -> list[dict]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list) or not value:
        raise ValueError("cases must be a non-empty JSON array")
    seen: set[str] = set()
    for case in value:
        if not isinstance(case, dict):
            raise ValueError("each case must be an object")
        required = ("id", "description", "category", "request", "context",
                    "skill", "expected_positive", "failure_behaviors",
                    "critical_requirements", "rubric", "checks", "followups")
        if any(name not in case for name in required):
            raise ValueError("case missing fields: " + repr(case.get("id")))
        identifier = case["id"]
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z][a-z0-9-]+", identifier) or identifier in seen:
            raise ValueError("duplicate or invalid case ID: " + repr(identifier))
        seen.add(identifier)
        if case["skill"] not in SKILLS or not all(isinstance(case[name], str) and case[name].strip()
                                                  for name in ("request", "description", "category")):
            raise ValueError(identifier + ": invalid skill or text")
        for name in ("context", "expected_positive", "failure_behaviors", "critical_requirements", "followups"):
            if not isinstance(case[name], list):
                raise ValueError(identifier + ": " + name + " must be a list")
        if not all(isinstance(x, str) and x for key in ("expected_positive", "failure_behaviors",
                                                        "critical_requirements") for x in case[key]):
            raise ValueError(identifier + ": invalid behavioral expectations")
        if not isinstance(case["rubric"], dict) or not case["rubric"]:
            raise ValueError(identifier + ": rubric must explain human judgment")
        if not isinstance(case["checks"], list) or not case["checks"]:
            raise ValueError(identifier + ": checks are required")
        names = set()
        for check in case["checks"]:
            if not isinstance(check, dict) or any(key not in check for key in ("id", "type", "value", "dimension")):
                raise ValueError(identifier + ": incomplete check")
            if check["type"] not in CHECKS or check["id"] in names:
                raise ValueError(identifier + ": duplicate/unknown check")
            names.add(check["id"])
            if check["type"] == "max_questions":
                if not isinstance(check["value"], int) or check["value"] < 0:
                    raise ValueError(identifier + ": bad max_questions")
            elif not isinstance(check["value"], str) or not check["value"]:
                raise ValueError(identifier + ": bad check value")
            if check["type"] == "regex":
                re.compile(check["value"])
    return value


def load_fixture(path: Path, cases: list[dict]) -> dict:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(fixture, dict) or fixture.get("kind") not in (
        "illustrative", "saved-agent-run", "live-model-run"
    ):
        raise ValueError("fixture must declare illustrative, saved-agent-run or live-model-run provenance")
    responses = fixture.get("responses")
    if not isinstance(responses, dict) or set(responses) != {case["id"] for case in cases}:
        raise ValueError("fixture case IDs must exactly match the benchmark suite")
    for identifier, samples in responses.items():
        if isinstance(samples, str):
            samples = [samples]
            responses[identifier] = samples
        if not isinstance(samples, list) or not samples or not all(
                isinstance(sample, str) and sample.strip() for sample in samples):
            raise ValueError("fixture response must be nonempty text: " + identifier)
    return fixture


def score(case: dict, response: str) -> list[dict]:
    """Literal proxies only. A passed token check never proves semantic quality."""
    scored = []
    for check in case["checks"]:
        kind, value = check["type"], check["value"]
        if kind == "contains":
            passed = value.casefold() in response.casefold()
        elif kind == "absent":
            passed = value.casefold() not in response.casefold()
        elif kind == "max_questions":
            passed = response.count("?") <= value
        else:
            passed = re.search(value, response, flags=re.IGNORECASE) is not None
        scored.append({"id": check["id"], "dimension": check["dimension"],
                       "passed": passed, "type": kind, "expected": value})
    return scored


def run_adapter(command: str, case: dict, variant: str, settings: dict, repetition: int) -> str:
    skill = ""
    if variant == "skill":
        skill = (ROOT / "skills" / case["skill"] / "SKILL.md").read_text(encoding="utf-8")
    payload = {"case": case, "variant": variant, "skill_instructions": skill,
               "settings": settings, "repetition": repetition}
    proc = subprocess.run(shlex.split(command), input=json.dumps(payload), text=True,
                          capture_output=True, timeout=settings["timeout_seconds"], check=False)
    if proc.returncode:
        raise RuntimeError("adapter exited " + str(proc.returncode) + ": " + proc.stderr[-500:])
    try:
        result = json.loads(proc.stdout)
    except ValueError as exc:
        raise ValueError("adapter must print a JSON object with response") from exc
    if not isinstance(result, dict) or not isinstance(result.get("response"), str):
        raise ValueError("adapter must return a text response")
    return result["response"]


def evaluate(cases: list[dict], responses: dict[str, list[str]]) -> dict:
    result = {}
    for case in cases:
        samples = []
        for response in responses[case["id"]]:
            checks = score(case, response)
            samples.append({"response": response, "checks": checks,
                            "passed": sum(item["passed"] for item in checks),
                            "total": len(checks), "needs_human_review": True})
        result[case["id"]] = samples
    return result


def markdown(report: dict) -> str:
    lines = [
        "# Unbullshit behavioral evaluation",
        "",
        "**Provenance:** " + report["provenance"],
        "",
        "Checks are literal response proxies, not proof of intent, implementation, "
        "evidence integrity, or improved model behavior. Human review is required. "
        "No aggregate 'bullshit score' is calculated.",
        "",
        "| Scenario | Baseline checks | Skill checks | Failed checks (baseline / skill) |",
        "| --- | --- | --- | --- |",
    ]
    for identifier in sorted(report["baseline"]):
        a = report["baseline"][identifier]
        b = report["skill"][identifier]
        def stats(samples):
            return str(sum(s["passed"] for s in samples)) + "/" + str(sum(s["total"] for s in samples))
        def failed(samples):
            missing = sorted({c["id"] for s in samples for c in s["checks"] if not c["passed"]})
            return ", ".join(missing) or "none"
        lines.append("| " + identifier + " | " + stats(a) + " | " + stats(b) +
                     " | " + failed(a) + " / " + failed(b) + " |")
    lines += ["", "## Limits", "",
              "- The same case inputs and checks are used for both variants.",
              "- Rule-based checks cannot reliably detect hallucination, user intent, or genuinely useful judgment.",
              "- Review full responses and case-specific human rubrics before drawing product conclusions.",
              "- For live comparisons, verify the adapter actually injects the provided skill instructions.",
              ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--validate", action="store_true", help="validate case and optional fixture schemas only")
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--enabled", type=Path)
    parser.add_argument("--adapter", help="opt-in executable that reads a JSON payload and prints a JSON response")
    parser.add_argument("--model", default="unspecified")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top-p", type=float, default=1.0)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--timeout-seconds", type=int, default=90)
    parser.add_argument("--output-dir", type=Path, default=Path("behavioral-report"))
    args = parser.parse_args(argv)
    try:
        cases = load_cases(args.cases)
        if args.repetitions < 1 or args.timeout_seconds < 1 or not (0 <= args.temperature <= 2) or not (0 < args.top_p <= 1):
            raise ValueError("invalid sampling settings")
        if bool(args.baseline) != bool(args.enabled) or (args.adapter and args.baseline):
            raise ValueError("provide both fixture paths OR an adapter, not both")
        base_fixture = load_fixture(args.baseline, cases) if args.baseline else None
        skill_fixture = load_fixture(args.enabled, cases) if args.enabled else None
        if args.validate:
            print("OK: " + str(len(cases)) + " case schemas" +
                  (" and both fixture sets" if base_fixture else "") + " validated; no model execution")
            return 0
        if not args.adapter and not base_fixture:
            raise ValueError("provide --baseline and --enabled, or --adapter")
        settings = {"model": args.model, "temperature": args.temperature, "top_p": args.top_p,
                    "seed": args.seed, "timeout_seconds": args.timeout_seconds}
        if args.adapter:
            responses = {"baseline": {}, "skill": {}}
            for variant in responses:
                for case in cases:
                    responses[variant][case["id"]] = [
                        run_adapter(args.adapter, case, variant, settings, n)
                        for n in range(args.repetitions)
                    ]
            provenance = "external-adapter (live status unverified; inspect adapter and outputs)"
        else:
            responses = {"baseline": base_fixture["responses"], "skill": skill_fixture["responses"]}
            provenance = "saved fixtures: baseline=" + base_fixture["kind"] + ", skill=" + skill_fixture["kind"]
        report = {"provenance": provenance, "settings": settings,
                  "cases": [case["id"] for case in cases],
                  "baseline": evaluate(cases, responses["baseline"]),
                  "skill": evaluate(cases, responses["skill"]),
                  "subjective_scores": "not assessed; human rubric required"}
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (args.output_dir / "report.md").write_text(markdown(report), encoding="utf-8")
        print("Wrote " + str(args.output_dir / "report.json") + " and report.md (" + provenance + ")")
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print("behavioral evaluation: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
