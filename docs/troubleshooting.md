# Troubleshooting installation and activation

**Installed**, **discovered**, **invoked**, and **always-on** are distinct states.

## `npx skills` cannot find the repository

```sh
npx skills add tanoojmehra/unbullshit --list
```

Check Node.js, network access, a corporate proxy and GitHub connectivity. As a fallback, clone and install locally:

```sh
git clone https://github.com/tanoojmehra/unbullshit.git
npx skills add ./unbullshit --list
```

## Installed, but the agent cannot find the skills

Use an explicit `--agent claude-code`, `--agent codex`, or `--agent cursor` parameter and check project versus `--global` scope. Inspect generated `.agents/skills/` and agent-specific links/copies, restart the agent, then invoke `unbullshit-plan` explicitly. Retry with `--copy` if symlinks don't work.

## The base skill doesn't apply to every prompt

Installing a skill only makes it available. Opt in to [`AGENTS.md` guidance](../examples/AGENTS.md), Claude's `CLAUDE.md`, or Cursor's [always-apply rule](../.cursor/rules/unbullshit.mdc). Do not overwrite existing project instructions.

## Claude Code plugin missing

In Claude Code, send `/plugin marketplace add tanoojmehra/unbullshit`, then **in a separate message** `/plugin install unbullshit@unbullshit-skills`. Restart and inspect installed plugins. Skill commands may be namespaced, e.g. `/unbullshit:unbullshit-plan`. If available, `claude plugin validate .` checks the local manifest.

## Codex plugin not in the directory

That is expected until a separate public plugin submission is completed. Use the Skills CLI for direct installation. The root portable manifest and compatibility overlay support packaging, not automatic universal publication.

## Cursor's rule doesn't apply

Copy [the MDC file](../.cursor/rules/unbullshit.mdc) to **the target project's** `.cursor/rules/` and check its Always Apply state in Cursor's rules UI. It applies to Agent, not Tab completion. Skills installation alone doesn't install this rule.

## An installed skill cannot find scripts/unbullshit_log.py

This is normal. Individual SKILL.md installs do not include the repository's optional helper. For an explicitly authorized record, follow the project-local Markdown record format in [recordkeeping](recordkeeping.md) using available host file tools, preserving history and avoiding concurrent write collisions. Do not create a register for ordinary work; never change a register during a read-only audit.

## A benchmark report says checks passed

Literal contains/absent/question-count checks are only diagnostic proxies, not proof an agent followed the user's constraints. Confirm that the response fixtures are labeled illustrative or saved-run and review the complete responses and human rubric in [benchmarking](benchmarking.md). Do not claim live host compatibility from offline fixture checks.

## CI fails

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

GitHub CI's Skills CLI smoke step also needs access to the npm registry. A network failure does not establish a malformed skill. Consult the actual run logs. A passing CLI test does not prove model behavioral improvements.

To report a reproducible issue, include the skill name, host/version, exact symptom or prompt, expected outcome, and redacted logs. See [contributing](../CONTRIBUTING.md).
