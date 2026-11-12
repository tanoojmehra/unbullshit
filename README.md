<p align="center"><img src="assets/wordmark.svg" alt="unbullshit. — Build what matters. Cut what doesn't." width="680"></p>

<p align="center"><strong>Four open Agent Skills. Better decisions. Less unnecessary work.</strong></p>

<p align="center"><a href="docs/install.md">Install</a> · <a href="docs/compatibility.md">Compatibility</a> · <a href="examples/demo.md">90-second demo</a> · <a href="examples/before-after.md">Before &amp; after</a> · <a href="CONTRIBUTING.md">Contribute</a></p>

Unbullshit is a free, open-source collection of four portable [Agent Skills](https://agentskills.io/) for pragmatic project decisions. It challenges invented requirements, speculative architecture, unnecessary AI agents, and process theater—without sacrificing what the user actually needs.

**Not always less. The right amount, for the right reasons.**

## Install

```sh
# Discover four skills
npx skills add tanoojmehra/unbullshit --list
# Install all four in this project
npx skills add tanoojmehra/unbullshit --skill '*' -y
# Or install the lightweight base globally
npx skills add tanoojmehra/unbullshit --skill unbullshit --global -y
```

Choose a specific host with `--agent claude-code`, `--agent codex`, or `--agent cursor`. Installation makes the skill available; it **doesn't automatically activate the base skill for every turn**.

[Detailed installation](docs/install.md) · [Troubleshooting](docs/troubleshooting.md) · [Host compatibility](docs/compatibility.md)

## Four independent skills

| Skill | Use it for | Main outcome |
| --- | --- | --- |
| [`unbullshit`](skills/unbullshit/SKILL.md) | Everyday work | Stay on scope, avoid speculative work, verify and stop. |
| [`unbullshit-plan`](skills/unbullshit-plan/SKILL.md) | New projects, major features, consequential decisions | Brainstorm, interview, explain options and create a right-sized plan. |
| [`unbullshit-audit`](skills/unbullshit-audit/SKILL.md) | Existing projects, codebases, decisions and roadmaps | Evidence-led findings that distinguish unjustified complexity, defects and necessary safeguards. |
| [`unbullshit-improve`](skills/unbullshit-improve/SKILL.md) | Focused improvements | Make useful changes without an elaborate planning exercise. |

No forced Plan → Audit → Improve pipeline. Each specialist skill stands alone.

## Human-first judgment

When a consequential decision is unclear, the agent should explain alternatives, recommend a direction, and ask **one useful question at a time**. The human makes the call. When a routine task is already authorized, the agent proceeds without inventing an approval process.

```text
Use unbullshit while adding CSV export to this table. No unrelated features.

Use unbullshit-plan to brainstorm a small appointment-booking product.
Interview me on major choices and recommend a sensible first release.

Use unbullshit-audit on this architecture. Cite actual evidence,
identify unjustified complexity, and say what's justified too.

Use unbullshit-improve to simplify these notification settings.
Preserve their behavior and verify the changes.
```

See [before/after examples](examples/before-after.md) and the [90-second walkthrough](examples/demo.md).

## Persistent base guidance (optional)

To apply Unbullshit's core principles in everyday agent turns, intentionally merge the [standing guidance template](examples/AGENTS.md) into your project instructions. For Cursor, copy the [always-apply project rule](.cursor/rules/unbullshit.mdc) into **your project's** `.cursor/rules/`. For Claude Code, use `CLAUDE.md`.

No accounts, API keys, background services, hidden telemetry, new permission gates or mandatory hooks.

## Quality and release

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

CI is configured to run these checks and Skills CLI installation smoke tests for Claude Code, Codex, and Cursor. **Smoke tests do not prove that a model follows the skills correctly.** See [compatibility](docs/compatibility.md) and [behavioral scenarios](tests/scenarios.md).

[Contributing](CONTRIBUTING.md) · [Brand assets](docs/brand.md) · [MIT license](LICENSE) · [v1.0.0 release notes](docs/releases/1.0.0.md)
