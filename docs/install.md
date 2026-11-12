# Installing Unbullshit

The four [Agent Skills](../skills/) are independent. Install one or all four. There are no model credentials, MCP servers, background processes, hooks, or runtime services.

## Skills CLI (recommended cross-agent route)

Requirements: Node.js and a working `npx` command, plus GitHub access.

```sh
# Discover available skills before installing
npx skills add tanoojmehra/unbullshit --list

# Interactive choice of skills and agent
npx skills add tanoojmehra/unbullshit

# All four, current project
npx skills add tanoojmehra/unbullshit --skill '*' -y

# Base skill only, current project
npx skills add tanoojmehra/unbullshit --skill unbullshit -y

# Base skill only, user-global (available across projects)
npx skills add tanoojmehra/unbullshit --skill unbullshit --global -y

# Target one supported host explicitly (example: Codex)
npx skills add tanoojmehra/unbullshit --skill '*' --agent codex -y
```

Omit `--global` for project scope. Restart or refresh your agent session if the newly installed skills aren't listed. Do not assume a skill is active merely because its files exist; check it in the agent's skill selector or ask the agent to use `unbullshit-plan`.

The CLI and supported agent list can change: see the [Skills CLI documentation](https://github.com/vercel-labs/skills/blob/main/docs/commands.md).

## Optional standing instructions (always-on)

**Skills aren't automatically always-on.** If you want Unbullshit's *base* philosophy applied to everyday work, explicitly opt in to standing project instructions.

1. Read [`examples/AGENTS.md`](../examples/AGENTS.md).
2. Merge its contents into your project's existing root `AGENTS.md`, or copy it there if no such file exists.
3. For Claude Code, use the same text in the project's `CLAUDE.md`; use `~/.claude/CLAUDE.md` if you intentionally want personal instructions across projects.
4. Confirm in a new agent session that the instructions are being read.

Avoid overwriting existing project instructions. Standing guidance does not add privileges or override legitimate tool policies, safety boundaries, or explicit project requirements. It should not automatically trigger the specialist interview workflows.

## Claude Code native plugin

A native Claude Code plugin manifest lives in [`.claude-plugin/plugin.json`](../.claude-plugin/plugin.json), and [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json) describes the source repository.

With Claude Code installed, run:

```sh
claude plugin marketplace add tanoojmehra/unbullshit
claude plugin install unbullshit@unbullshit-skills
claude plugin list
claude plugin details unbullshit
```

Skill commands inside Claude Code are namespaced by plugin; the corresponding forms are `/unbullshit:unbullshit`, `/unbullshit:unbullshit-plan`, `/unbullshit:unbullshit-audit`, and `/unbullshit:unbullshit-improve`.

From a local checkout, you can validate packaging without installing:

```sh
claude plugin validate .
```

Claude Code installs plugins with its own scopes and may require session reload. Installing this plugin exposes its skills but does **not** make the base skill an unconditional hook; use standing guidance for that. See [Claude Code plugin documentation](https://code.claude.com/docs/en/plugins).

## Codex and portable Agent Plugins

The root [`plugin.json`](../plugin.json) follows the portable Agent Plugins manifest layout; the canonical skill contents remain under `skills/`.

The broadly supported direct path for Codex remains the Skills CLI:

```sh
npx skills add tanoojmehra/unbullshit --skill '*' --agent codex -y
```

Codex also recognizes locally installed project skills in `.agents/skills/` and user skills in `~/.agents/skills/`. Some Codex / ChatGPT plugin environments support loading a root `plugin.json` from a local marketplace or plugin package, but exact UI and commands depend on the installed host version. **A manifest in GitHub is not the same as a plugin-directory publication.**

Refer to the current [Agent Plugins packaging documentation](https://developers.openai.com/plugins/build/plugins) for that route.

## Manual install without the CLI

```sh
git clone https://github.com/tanoojmehra/unbullshit.git
mkdir -p /path/to/your-project/.agents/skills
cp -R unbullshit/skills/* /path/to/your-project/.agents/skills/
```

For Claude Code, the conventional project skills directory is `.claude/skills/`; for Codex, it is `.agents/skills/`. Check your host's current conventions if they differ.

## Verification status

- The project contains four standalone `SKILL.md` files with required name and description frontmatter.
- The dependency-free `python3 scripts/validate.py` checks skill structure and distribution manifests.
- GitHub Actions is configured to run the structural validator and a Skills CLI listing/install smoke test on pushes and pull requests.
- Claude Code native plugin validation and installation require an installed Claude Code CLI; the repository does **not** claim those tests passed without actually running them.
- Real model behavior (interview quality, recommendations, justified complexity) must be tested in an agent; structural validation is not behavioral proof. See [scenarios](../tests/scenarios.md).
