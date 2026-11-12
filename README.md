# unbullshit

**Build what matters. Cut what doesn't.**

Unbullshit is a free, open-source family of four portable [Agent Skills](https://agentskills.io/) for better decisions about projects, products, workflows, and software. It helps people and AI agents avoid invented requirements, speculative architecture, pointless ceremony, and work that does not advance the real goal.

**Unbullshit is not a mandate to make everything smaller.** The right solution can be sophisticated. What matters is whether its complexity is justified by real needs and constraints.

## The four skills

| Skill | Use it when | What it does |
| --- | --- | --- |
| [`unbullshit`](skills/unbullshit/SKILL.md) | Everyday requests, as lightweight background guidance | Stays true to user intent, avoids scope drift and speculative work, then finishes. |
| [`unbullshit-plan`](skills/unbullshit-plan/SKILL.md) | A new project, major feature, significant redesign, or consequential decision | Brainstorms with the human, interviews on the decisions that matter, recommends alternatives, and produces a right-sized plan. |
| [`unbullshit-audit`](skills/unbullshit-audit/SKILL.md) | Reviewing an existing project, plan, codebase, architecture, or direction | Investigates evidence, distinguishes genuine problems from justified complexity, and provides a prioritized, actionable assessment. |
| [`unbullshit-improve`](skills/unbullshit-improve/SKILL.md) | A focused improvement to something that already exists | Understands the pain point, recommends the smallest sufficient change, implements when authorized, and verifies. |

They are **independent entry points**, not a required sequence. The three specialist skills include the core principles themselves; you do not need to load the base skill twice.

## The defining behavior: interview, recommend, let humans decide

For a decision with meaningful consequences, an Unbullshit skill should:

1. Understand the human's desired outcome and constraints.
2. Investigate what is already known before asking for information.
3. Explain the real trade-offs in plain language.
4. Recommend a direction, with reasons and conditions that would change it.
5. Ask **one high-value question at a time** when an answer is needed.
6. Respect the human's decision and carry it forward without repeatedly reopening it.

A founder should never have to understand the difference between a message queue and an event bus to explain their business problem. Translate technical choices into capability, cost, delivery time, risk, and ongoing maintenance.

This is **not** an interview for every trivial change. `unbullshit` and `unbullshit-improve` proceed on ordinary, authorized tasks. `unbullshit-plan` uses a more deliberate conversation. `unbullshit-audit` investigates first and asks only where material intent or constraints remain unclear.

## Try it

```text
Use unbullshit: Add CSV export to the customer table. Reuse what is there and avoid expanding the feature.

Use unbullshit-plan: Help me brainstorm an internal CRM for 100 people. Interview me about decisions that affect the scope, recommend a practical direction, then plan it.

Use unbullshit-audit: Review this architecture and repository. Where have we overcomplicated the product, AI workflows, and deployment? Cite evidence, including cases where complexity is justified.

Use unbullshit-improve: Simplify the current notification settings without changing their behavior. Inspect, make the focused change, and verify.
```

Skill invocation syntax depends on the host. The plain-language examples work as prompts for agents that discover these installed skills.

## Install

Install with the [Skills CLI](https://github.com/vercel-labs/skills), or manually copy any of the four self-contained skills under [`skills/`](skills/).

**Discover the skills:**

```sh
npx skills add tanoojmehra/unbullshit --list
```

**Install all four for your current project:**

```sh
npx skills add tanoojmehra/unbullshit --skill '*' -y
```

**Install only the lightweight base skill for everyday use across projects:**

```sh
npx skills add tanoojmehra/unbullshit --skill unbullshit --global -y
```

The CLI supports explicit agent targets (for example, `--agent codex` or `--agent claude-code`). Omitting `--global` keeps installation project-scoped. An installed skill is discoverable/invocable, **not guaranteed to run on every turn**.

Want a persistent, always-on version of the base principles? Opt in by copying or merging [`examples/AGENTS.md`](examples/AGENTS.md) into a project's `AGENTS.md`, or into `CLAUDE.md` for Claude Code. This is **separate from installing the skill**; it doesn't modify execution permissions.

**Native plugin options:** The repository also contains a root `plugin.json` for compatible Agent Plugins/Codex hosts and a Claude Code marketplace. See [installation and validation instructions](docs/install.md), including commands, scope selection, and test status.

For manual installation into a project with the common `.agents/skills` convention:

```sh
git clone https://github.com/tanoojmehra/unbullshit.git
mkdir -p /path/to/your-project/.agents/skills
cp -R unbullshit/skills/* /path/to/your-project/.agents/skills/
```

Agent-specific skill directories and plugin support vary; follow your host's documentation. Skill installation does not grant filesystem, network, or execution permissions.

## How the skills differ

- **Plan asks:** What should we build, and which consequential choices must the human make?
- **Audit asks:** What is actually wrong, unjustified, missing, or risky? What evidence supports that?
- **Improve asks:** What is the smallest useful improvement to this defined problem?
- **Base asks:** Am I doing exactly the justified work the human requested?

These questions work for business workflows and physical-world projects as well as for software. When there is no repository, reason from the brief and available documents; don't invent code evidence.

## Principles

- **Intent over invention:** Do the job asked for; do not manufacture product requirements.
- **Proportionality over austerity:** Prefer the least complex solution that actually satisfies the need.
- **Evidence over confidence:** Label assumptions, uncertainty, estimates, and unverified claims.
- **Existing capability over reinvention:** Reuse proven systems before adding new ones.
- **Human agency over hidden governance:** Explain consequential choices; don't silently override a decision.
- **Quality over shortcuts:** Keep appropriate security, privacy, accessibility, correctness, observability, recoverability, and reliability.
- **Progress over ceremony:** No mandatory forms, scores, extra agents, elaborate plans, or process for its own sake.
- **Honest finish:** Verify what can be verified and say what was not checked.

No skill should invent an approval gate or silently take away access granted by the agent host. Equally, no skill should bypass real permissions or treat an unverified success as complete.

## Quality and contribution

This repository uses the open `SKILL.md` format: required `name` and `description` frontmatter, with focused Markdown instructions. There are no runtime dependencies.

Run the lightweight structural validator:

```sh
python3 scripts/validate.py
```

See [behavioral test scenarios](tests/scenarios.md) for manual evaluations that probe interview quality, right-sizing, grounded audits, and scope discipline. Static validation does **not** establish model-behavior reliability; test skills with real agent runs as well.

Contributions are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE).
