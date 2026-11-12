# Contributing

Unbullshit is a collection of portable instruction-only Agent Skills. Contributions should make the skills clearer, more evidence-led, more helpful to humans, or less likely to encourage unnecessary work.

## Before changing a skill

- Start from a concrete failure or use case. Describe the existing behavior and the desired behavior.
- Keep each skill independently installable and self-contained.
- Prefer editing an existing instruction to introducing a new framework, agent, configuration option, or mandatory checklist.
- Keep metadata descriptions specific about *when* to activate the skill.
- Make founder interviews adaptive: no compulsory question count, manufactured options, or endless re-approval.
- Respect human decisions, explicit scope, genuine security boundaries, and truthful evidence.
- Do not make "fewer files" or "less code" a substitute for useful outcomes.

## Local checks

Run:

```sh
python3 scripts/validate.py
```

This validates structural constraints only. Test instruction changes against cases in [tests/scenarios.md](tests/scenarios.md), with an actual skills-compatible agent where possible. A strong change has examples where the skill simplifies the solution **and** where it correctly keeps justified complexity.

## Pull requests

Describe the behavior you changed, a before/after example, risks of overcorrection, and the scenarios checked. Keep PRs focused. Do not add external service dependencies for a documentation-only skill collection.

## Scope

This repository provides reusable decision guidance. It is not a permission engine, audit database, hosted product, or autonomous execution framework. Changes that would turn it into one require explicit discussion and demonstrated need.
