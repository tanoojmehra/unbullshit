# Compatibility matrix

Unbullshit ships four self-contained skills. The entries below distinguish **designed support** from **verified runtime behavior**.

| Host | Install route | CLI install check | Skill discovery / invocation | Always-on option | Limitation |
| --- | --- | --- | --- | --- | --- |
| Claude Code | Skills CLI or native marketplace | Configured in GitHub CI; check live result | Expected via skill selector or `/unbullshit:unbullshit-plan`; live host not yet verified | Opt-in `CLAUDE.md` | No automatic hooks or persistent skill mode |
| Codex | Skills CLI or portable plugin package | Configured in GitHub CI; check live result | Expected through skill discovery; live host not yet verified | Opt-in `AGENTS.md` | GitHub manifest is not a public directory listing |
| Cursor | Skills CLI plus optional rule | Configured in GitHub CI; check live result | Skills via Agent; live UI not yet verified | Opt-in `.cursor/rules/unbullshit.mdc` | Always-apply rule is manual; no Tab-completion effects |
| Other skills-compatible agents | Skills CLI or manual copy | Not directly tested | Host-specific, unverified | Host-specific | Do not assume automatic support |

[View GitHub Actions checks](https://github.com/tanoojmehra/unbullshit/actions/workflows/validate.yml).

## Verification workflow for each host

For Claude Code, Codex and Cursor, verify in sequence: (1) manifest and SKILL.md validation, (2) isolated skill installation and exact file paths, (3) native host lists the four installed skills, (4) a real session invokes each skill, and (5) controlled baseline-versus-enabled conversations are reviewed for requirement preservation, evidence integrity and scope. Record host version, installation method, date, command/output and any failures. **Passing (1) or (2) does not establish (3)-(5).**

The four canonical definitions live in skills/*/SKILL.md. The optional Cursor rule and host manifests are distribution aids, not separate skill logic. Installed SKILL.md files do **not** ship scripts/unbullshit_log.py; recordkeeping works through ordinary project file tools when explicitly authorized. Keep new integrations unverified until actual host discovery and activation have been tested.

## What each verification level means

- **Static validation:** Files and manifests have the expected format.
- **CLI installation:** The Skills CLI actually writes all four skills to an isolated project.
- **Native host discovery:** An installed Claude Code, Codex, or Cursor application lists the skills.
- **Activation:** A real session successfully invokes a skill.
- **Behavior:** Controlled model runs show better decisions and fewer inappropriate additions without losing requirements.

CI tests the first two categories. The other three require actual host and model testing and must not be claimed solely from package structure.

For behavioral evidence, see [offline fixtures and live adapter contract](benchmarking.md); authored fixture differences are not host compatibility measurements.

See [installation commands](install.md), [troubleshooting](troubleshooting.md) and [behavioral scenarios](../tests/scenarios.md). Add more hosts when there is a user request and reproducible verification.
