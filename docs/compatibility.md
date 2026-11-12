# Compatibility matrix

Unbullshit ships four self-contained skills. The entries below distinguish **designed support** from **verified runtime behavior**.

| Host | Install route | CLI install check | Skill discovery / invocation | Always-on option | Limitation |
| --- | --- | --- | --- | --- | --- |
| Claude Code | Skills CLI or native marketplace | Configured in GitHub CI; check live result | Expected via skill selector or `/unbullshit:unbullshit-plan`; live host not yet verified | Opt-in `CLAUDE.md` | No automatic hooks or persistent skill mode |
| Codex | Skills CLI or portable plugin package | Configured in GitHub CI; check live result | Expected through skill discovery; live host not yet verified | Opt-in `AGENTS.md` | GitHub manifest is not a public directory listing |
| Cursor | Skills CLI plus optional rule | Configured in GitHub CI; check live result | Skills via Agent; live UI not yet verified | Opt-in `.cursor/rules/unbullshit.mdc` | Always-apply rule is manual; no Tab-completion effects |
| Other skills-compatible agents | Skills CLI or manual copy | Not directly tested | Host-specific, unverified | Host-specific | Do not assume automatic support |

[View GitHub Actions checks](https://github.com/tanoojmehra/unbullshit/actions/workflows/validate.yml).

## What each verification level means

- **Static validation:** Files and manifests have the expected format.
- **CLI installation:** The Skills CLI actually writes all four skills to an isolated project.
- **Native host discovery:** An installed Claude Code, Codex, or Cursor application lists the skills.
- **Activation:** A real session successfully invokes a skill.
- **Behavior:** Controlled model runs show better decisions and fewer inappropriate additions without losing requirements.

CI tests the first two categories. The other three require actual host and model testing and must not be claimed solely from package structure.

See [installation commands](install.md), [troubleshooting](troubleshooting.md) and [behavioral scenarios](../tests/scenarios.md). Add more hosts when there is a user request and reproducible verification.
