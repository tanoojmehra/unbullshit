# Project-local Unbullshit recordkeeping

A lightweight way to **retain evidence and decisions between agent sessions**. The register belongs to the *target project*, never the installed skill package. This is optional documentation, not a new approval gate, project-management framework or dependency.

## Location: exact precedence

Inspect the target project's **tracked** paths (for example with `git ls-files`). Apply the first matching rule:

| Context | Destination |
| --- | --- |
| The project is known to use **kenmark-studio** or **kenmark-skills**, and has tracked files in `brain/` | `brain/unbullshit/` |
| Otherwise the project has tracked files in `docs/` | `docs/unbullshit/` |
| Otherwise | `unbullshit/` at repository root |

A plain `brain/` directory isn't evidence that those integrations are in use. Confirm via the user's statement, installed environment or a verified project marker. An empty, untracked `docs/` directory does not count as tracked docs. For non-Git folders, use root `unbullshit/` unless the user chooses another path.

An existing active register (index, canonical findings, decisions, or reviews) wins even if another location would now be preferred. If multiple locations contain active records, stop and reconcile explicitly. Never silently migrate, merge or overwrite them.

**Do not create a second register** if the project already uses one of these locations. Continue the existing register and preserve history; discuss migration before moving it.

The optional local helper `scripts/unbullshit_log.py` applies this precedence. Its `--brain-enabled` option signals positively confirmed project context, not an assumption about all repositories with a `brain/` directory.

## Directory layout

Create files when they are useful, not as a mandatory preflight action.

```text
<selected-parent>/unbullshit/
├── README.md             # Purpose and usage for the project
├── REGISTER.md           # Regenerable index of findings
├── findings/
│   ├── UB-0001.md        # Stable record ID
│   └── UB-0002.md
├── decisions/
│   └── YYYY-MM-DD-topic.md
└── reviews/
    └── YYYY-MM-DD-scope.md
```

`findings/`, `decisions/` and `reviews/` can be absent until used. A review with **zero** bullshit findings is legitimate.

## Canonical finding record

`REGISTER.md` is an index, **not** the source of truth. Each finding has a stable identifier in `findings/UB-NNNN.md` and fields designed for human editing:

```markdown
---
id: UB-0001
classification: unjustified-complexity
status: open
priority: medium
source: unbullshit-audit
created: 2026-11-13
updated: 2026-11-13
---

# Duplicated workflow layer

## Observation

What exists and why it causes friction or waste.

## Evidence and limits

The inspected files, relevant lines, observed behavior, requirements and uncertainties.

## Recommendation

One preferred approach and alternatives if they matter.

## Trade-offs, safeguards and verification

What must not break, and how to prove the change is safe.

## Decision and history

- 2026-11-13: Recorded as open; awaiting review.
```

**Classifications:**

- `unjustified-complexity` — demonstrably excessive infrastructure, scope, or abstractions.
- `unnecessary-friction` — invented policy or governance blocking already-authorized work.
- `defect` — broken intended behavior; fix it, don't mislabel it as discretionary policy.
- `justified-complexity` — a real need or safeguard that should be retained.
- `uncertain` — a candidate whose intent, necessity or evidence is unresolved.

**Statuses:** `open`, `needs-review`, `accepted`, `in-progress`, `resolved`, `wont-fix`.

**Priorities:** `high`, `medium`, `low`, `none`, relative to real impact and project needs. There are no invented bullshit scores or mandatory quotas.

**Sources:** `unbullshit`, `unbullshit-plan`, `unbullshit-audit`, `unbullshit-improve`.

One issue, one canonical ID. Keep resolved records and append dated status changes with verification. Never delete or renumber for appearance. Link to existing issues/PRs rather than duplicating them.

## Decisions and audit summaries

- **`decisions/YYYY-MM-DD-short-topic.md`**: Record consequential founder-approved choices, alternatives considered, reasoning, explicit constraints and review triggers. Never represent an unchosen recommendation as an approved decision.
- **`reviews/YYYY-MM-DD-scope.md`**: Record the audit's reviewed scope, evidence coverage, findings links, what was justified and retained, uncertainty, and useful next steps. When zero problems are found, record that honestly without manufacturing register entries.

These are Markdown, not a required YAML database. Avoid sensitive data, credentials, raw customer records, and unnecessarily long transcripts.

### Example approved decision (only after opt-in)

Save as decisions/2026-11-13-manual-confirmation.md, using the actual decision date:

```markdown
# Manual confirmation for launch

- Date: 2026-11-13
- Status: approved
- Approval basis: founder explicitly chose this during planning
- Decision: staff manually confirm requested appointment slots
- Rationale: no initial calendar integration; staff already maintain availability
- Alternatives: automatic sync (rejected for launch); no booking (rejected)
- Constraints and trade-offs: mobile web only; show pending state; slower confirmations
- Assumptions and open questions: staff can respond during working hours
- Review trigger: frequent delays or conflicting confirmations
- Related finding: none
- Supersedes: none
```

This is a **format illustration**, not an actual recorded founder approval. When an approval basis is unknown, label it unknown; do not invent a person or a sign-off. Preserve rejected and superseded alternatives so future sessions do not reopen them reflexively.

## Mapping to each skill

| Skill | How to use the project record |
| --- | --- |
| **Base `unbullshit`** | Never create folders or log routine work automatically. When explicitly asked to retain a consequential finding, create/update one entry. Otherwise complete the task without ceremony. |
| **`unbullshit-plan`** | Interview the founder, explain options and track decisions conversationally. When the human asks to save/maintain decisions, write approved, material choices to `decisions/` and link to related UB findings. Do not log every question. |
| **`unbullshit-audit`** | Read-only unless the human authorizes writing project findings. Then create/update evidence-backed `findings/`, update `REGISTER.md` and save a scoped `reviews/` summary if useful. Keep actual defects and justified complexity distinctly classified. |
| **`unbullshit-improve`** | For an authorized fix tied to an existing UB ID, update its status, links and verification. Other small improvements need no record unless requested. |

**The request to maintain a register is project-documentation authorization only**, not permission to modify code, deploy, or impose future approvals.

## Optional command-line helper

When working in a checkout of the Unbullshit source repository, you can run its dependency-free helper against a target project. It is *not* automatically installed alongside individual `SKILL.md` directories.

```sh
python3 scripts/unbullshit_log.py --project /path/to/project locate
python3 scripts/unbullshit_log.py --project /path/to/project --brain-enabled init
python3 scripts/unbullshit_log.py --project /path/to/project --brain-enabled add \
  --title "Duplicate approval" \
  --classification unnecessary-friction \
  --source unbullshit-audit \
  --summary "An extra manual approval blocks an already-authorized release" \
  --evidence "Verified in deployment workflow and interview" \
  --recommendation "Remove the duplicate after confirming no separate safety requirement"
python3 scripts/unbullshit_log.py --project /path/to/project --brain-enabled status UB-0001 \
  --set resolved --note "Duplicate removed and deployment checks passed"
python3 scripts/unbullshit_log.py --project /path/to/project --brain-enabled rebuild
```

The helper creates unique `UB-XXXX.md` files using exclusive creation, regenerates the index, and records status updates. In projects without this helper, an agent can use its usual file tools to produce the same Markdown records.

For parallel work, use a single cooperative writer per selected register, or an exclusive directory lock around **read → ID assignment → canonical write → index rebuild**. The optional helper takes that lock; on a crash a stale .unbullshit-write.lock directory must be inspected and manually cleared. A busy lock fails closed. Files are exclusively created, and existing records updated atomically while holding the lock. No tool can prevent an unrelated editor that ignores the lock from racing; reconcile external edits before retrying. If a process crashes after a canonical creation but before an index update, the canonical file wins: run rebuild after investigating the stale lock.

**Installed-skill fallback, without the helper:** On a specifically authorized write, identify the target-project root and active register; inspect the canonical finding files, fail on malformed metadata or conflicting registers, allocate the next unused stable UB-NNNN ID, create the new file *exclusively*, append dated history to existing findings (never replace history), and regenerate REGISTER.md sorted by numeric ID from the canonical files. Serialize concurrent writers with the host's available locking/transaction support; if atomic creation or safe locking is not available, do not risk a write collision—present the intended record for manual application. Read-only requests never create even an empty folder.

**Decision continuity:** When consequential planning is requested, consult available approved decision files before reopening a choice. Record only on explicit opt-in: decision, rationale, alternatives and rejected options, approval basis or owner if known, constraints, assumptions, date, related UB IDs and conditions for revisiting. If newer evidence contradicts the decision, say so and ask for a new human choice rather than silently superseding it.

**Malformed records:** Treat missing IDs, invalid classification/status/priority/source, missing dates, or conflicting numeric IDs as errors. Never rebuild an index from partial data or replace a corrupt finding while guessing its intent.

## Boundaries

- Logging is **not** a prerequisite to Plan, Audit, Improve or a normal task.
- A register is **not** a policy authority or a way to grant/withdraw permissions.
- Don't manufacture findings to justify the skill, or turn bugs into a bullshit tally.
- Respect explicit read-only requests and the available filesystem permissions.
- No hidden telemetry or communication with an external service.
