# Reproducible behavioral benchmarking

These checks expose *some* differences between saved responses. They do not establish that an agent behaves better in production. Structural CI, illustrative fixtures, human judgment, and live-model experiments are different evidence levels.

## Validate, compare, extend

No model or paid API is required:

```sh
python3 scripts/evaluate_behavior.py --validate \
  --baseline tests/behavioral/fixtures/baseline.json \
  --enabled tests/behavioral/fixtures/skill.json

python3 scripts/evaluate_behavior.py \
  --baseline tests/behavioral/fixtures/baseline.json \
  --enabled tests/behavioral/fixtures/skill.json \
  --output-dir /tmp/unbullshit-behavior
```

Output: report.json includes every saved response, check, verdict, settings and provenance. report.md lists passed/total *literal checks* and failed check IDs for every scenario; there is no opaque overall score. The committed fixtures are **authored illustrations**, not observed baseline/skill model runs, so differences between them are **not evidence of model improvement**.

Cases reside in tests/behavioral/cases.json. Add a unique ID, initial request, context, explicit positive/failure behaviors, critical requirements, human rubric, deterministic checks, and any followups or simulated tool results. Add responses for that ID to both fixture files. Checks are simple contains / absent / regex / max_questions proxies; they cannot reliably establish correctness, accuracy, evidence, task completion, or authorization compliance. Review the full transcript against the rubric to assess those properties. Do not infer significance from a few examples.

## Optional real-agent adapter

A contributor can pass --adapter 'python3 path/to/adapter.py' in place of fixture files. The command receives one JSON object on stdin with case, variant (baseline or skill), skill_instructions (empty for baseline, the target skill's actual SKILL.md text for enabled), settings and repetition. It must print JSON with a response string. The case input sent to adapters deliberately excludes expected behaviors, grading checks and human rubrics. The adapter is responsible for genuinely injecting the instructions into otherwise identical agent contexts and handling followups/tool results; do not claim it did so without examining it.

Example: ```sh
python3 scripts/evaluate_behavior.py --adapter "python3 my_adapter.py" \
  --model model-id --temperature 0.2 --top-p 1 \
  --seed 42 --repetitions 3 --timeout-seconds 120 \
  --output-dir /tmp/unbullshit-live
```

The runner passes sampling settings to the adapter, but cannot guarantee the model supports them. Record adapter name/version, provider, actual model ID, system-prompt order, tool permissions, seeds when honored, date, and raw output. Save real runs separately and label provenance accurately; do not turn live results into illustrative fixtures.

## Human rubric

For each run, give 0 (not met), 1 (partial), or 2 (met) and cite response evidence for: user intent fidelity; recommendation usefulness; interview relevance and non-repetition; critical-requirement preservation; proportional architecture; evidence truthfulness and false positives; authorization boundaries; honest verification after failures; task completion and process overhead. Flag catastrophic omissions independently of any subtotal. The evaluator intentionally leaves these scores blank for humans.

Before making adoption claims, use representative real agents and blinded human reviewers, compare baseline versus skill using identical inputs and permissions, and disclose raw cases, errors and sample size. A passing keyword check is not a causal claim.

## CI

The regression suite validates scenarios, fixture completeness, runner determinism and failure handling offline. No CI job runs paid models. Host discovery, skill activation and improved real-agent decisions remain unverified until observed directly.
