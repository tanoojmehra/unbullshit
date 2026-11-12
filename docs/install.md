# Install Unbullshit

All four skills are independent `SKILL.md` bundles. There are no required runtime dependencies, MCP servers, hooks, or permissions. The optional repository CLI scripts are **not** bundled with individual installed skills; recordkeeping instructions in each SKILL.md work without them.

## Skills CLI — Claude Code, Codex and Cursor

```sh
npx skills add tanoojmehra/unbullshit --list
npx skills add tanoojmehra/unbullshit --skill '*' --agent claude-code -y
npx skills add tanoojmehra/unbullshit --skill '*' --agent codex -y
npx skills add tanoojmehra/unbullshit --skill '*' --agent cursor -y
```

To install only the base skill globally:

```sh
npx skills add tanoojmehra/unbullshit --skill unbullshit --global -y
```

Requires Node.js and network access. The installer and supported agents can change; see the [Skills CLI documentation](https://github.com/vercel-labs/skills/blob/main/docs/commands.md). Use `--copy` where symlinks cannot work. Refresh the agent session to discover newly installed skills.

## Claude Code native plugin

The repo includes [Claude plugin metadata](../.claude-plugin/plugin.json) and a [marketplace entry](../.claude-plugin/marketplace.json). In a Claude Code session, send these commands **separately**:

```text
/plugin marketplace add tanoojmehra/unbullshit
/plugin install unbullshit@unbullshit-skills
```

Plugin skill invocations use namespaced names such as `/unbullshit:unbullshit-plan`. A supported Claude Code CLI can validate a local checkout with `claude plugin validate .`. Native plugin installation must be checked in a running Claude Code host; a valid JSON manifest alone is not proof.

## Codex

The canonical portable package is [`plugin.json`](../plugin.json), with a [.codex-plugin compatibility manifest](../.codex-plugin/plugin.json). Both refer to the root `skills/` directory.

For straightforward skill installation, prefer:

```sh
npx skills add tanoojmehra/unbullshit --skill '*' --agent codex -y
```

Local plugin/marketplace installations vary by host version. GitHub publication **does not automatically list a plugin in the universal directory**. See [official packaging guidance](https://developers.openai.com/plugins/build/plugins).

## Cursor

Install the skills with `--agent cursor`. For persistent everyday rules, **opt in** by copying [`unbullshit.mdc`](../.cursor/rules/unbullshit.mdc) into your target project's `.cursor/rules/`. It sets `alwaysApply: true` and applies to Cursor Agent chats—not Tab completion. The Skills CLI does not automatically install the rule.

Alternatively, merge [the standing rules](../examples/AGENTS.md) into your project's `AGENTS.md`. Avoid duplicating both mechanisms unless intended.

## Manual skills installation

```sh
git clone https://github.com/tanoojmehra/unbullshit.git
mkdir -p /path/to/your-project/.agents/skills
cp -R unbullshit/skills/* /path/to/your-project/.agents/skills/
```

Check your host's actual skill path. Installing a skill is not the same as activating it every turn. Use the optional standing guidance when that's desired; do not overwrite existing project rules or grant extra tool permissions.

## Verify actual use

After installing, confirm the four SKILL.md paths exist, restart the chosen host, check whether the host **discovers** the skills, and explicitly invoke one in a small task. If it is missing, see [troubleshooting](troubleshooting.md). A successful file-copy, manifest, or CLI install is not proof of discovery, activation, or better behavior. Compare saved baseline/skill responses offline with [the behavioral runner](benchmarking.md); live comparisons require a real adapter and human review.

## Verify

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

The [CI workflow](../.github/workflows/validate.yml) performs distribution checks and isolated Skills CLI installs for the three hosts. Check [actual Actions results](https://github.com/tanoojmehra/unbullshit/actions/workflows/validate.yml) rather than assuming they passed. Read [compatibility](compatibility.md) and [troubleshooting](troubleshooting.md) for the difference between installed, discovered, activated and always-on.
