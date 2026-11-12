---
name: unbullshit-audit
description: Investigate an existing project, codebase, feature, technical architecture, roadmap, AI workflow, or operating process for unjustified complexity, scope drift, friction, and questionable decisions. Use evidence-first inspection, targeted human interviews, fair classification, and prioritized recommendations. Read-only by default.
license: MIT
---

# Unbullshit Audit

**Investigate before criticizing.** Audit the *decisions and project direction*, not just code style or file count. A good audit can conclude that a sophisticated architecture is appropriate—or that no meaningful bullshit was found.

Use when the person wants an independent reality check of an existing project, plan, implementation, process, or portfolio of features. A codebase is useful evidence when available, not a prerequisite.

## Scope before depth

- Identify what is under review: product scope, architecture, feature set, AI systems, operations, code, delivery process, or a combination.
- Start with the user's actual concern and the most relevant artifacts. Expand only where findings or uncertainty justify it.
- Inspect what exists: requirements, user journeys, prior decisions, dependency manifests, key entry points, ownership boundaries, operational evidence, tests, and representative workflows, as available.
- If access or evidence is missing, say what you could and could not inspect. Never invent file paths, line numbers, runtime observations, metrics, or stakeholder intent.

Prefer high-signal investigation over an exhaustive inventory performed for its own sake.

## The audit lenses

Evaluate against real goals, users, scale, risks, constraints, and observed behavior:

- **Problem and scope:** Features without a demonstrated user problem; roadmap inflation; speculative scaling or flexibility; unnecessary bespoke work when a simpler alternative exists.
- **Architecture and operations:** Duplicate responsibilities, accidental complexity, overlapping services, queues, layers, configuration, integrations, or deployment paths; maintenance and operational cost.
- **AI and agent design:** AI where deterministic workflows suffice; multi-agent coordination without independent workstreams; unnecessary retrieval layers, prompts, tool wrappers, orchestration, or autonomy policy.
- **Authority and workflow friction:** Product-invented restrictions, repeated approvals, mandatory process, artificial limits, and friction that blocks already-authorized work.
- **Preserved essentials:** Genuine security, privacy, accessibility, data integrity, reliability, compliance, operational recovery, and performance requirements. These must not be called "bloat" merely for existing.

Distinguish technical debt from unnecessary product scope, and bugs from intentional policy. Never recommend deleting a genuine boundary simply because its current implementation is annoying.

## Evidence and classification

For each credible candidate, ask:

1. **What exactly is happening?** State an observable symptom, requirement, or code location.
2. **Why is it there?** Locate the decision or owner intent when possible.
3. **What cost does it cause?** Time, complexity, money, errors, risk, cognitive burden, or delayed delivery.
4. **Is it justified?** Compare to actual requirements and simpler alternatives.
5. **What would change safely?** Include migration and verification if removal affects live behavior.

Classify findings honestly as:

- **Unjustified complexity / scope:** Removing or reducing it preserves necessary outcomes.
- **Unnecessary friction / invented rule:** A discretionary restriction obstructs work already authorized.
- **Defect:** Intended behavior is broken; fix it rather than pretending a policy must be removed.
- **Justified complexity / retained safeguard:** Keep and explain why.
- **Uncertain:** Not enough evidence to recommend a consequential change.

A finding is not true merely because the system looks elaborate. Count only distinct, supported findings; do not manufacture a quota or assign arbitrary precision scores.

## Human interview — after investigation

Use the human to resolve **material intent or trade-offs**, not to substitute for inspection.

- Present the evidence and your current hypothesis before asking.
- Explain the alternatives, recommend a path when possible, and ask **one focused question** if the answer would materially change the recommendation.
- Do not infer that undocumented intent is invalid intent. Explicitly mark an ambiguity and invite correction.
- Do not keep interviewing when evidence is adequate or when the user simply wants a limited preliminary audit.
- Carry the human's decisions forward without re-asking them.

## Report

Lead with the overall judgment and the most important evidence, including what is already well justified. Then provide a prioritized set of **only** supported findings. For each meaningful finding, include:

- **Observation and evidence:** Link/path/line, document, quote, or runtime result when available; otherwise the precise evidence gap.
- **Why it matters:** Actual effect on users, maintainers, budget, time, or risk.
- **Recommendation:** Retain, remove, simplify, combine, defer, replace, or investigate; explain why and what functionality must remain.
- **Trade-off and confidence:** What may be lost, what you still need to confirm, and the safest verification.
- **Priority:** Relative to the user's goals and impact, not a universal severity taxonomy.

If asked, add a small sequence of proposed improvements; **do not** automatically create tickets, rewrite architecture, change policy, or edit files. Audits are read-only unless the user explicitly authorizes implementation.

## Done means

The human knows what is unjustified, what is legitimately necessary, what is broken rather than overengineered, and which change—if any—is most worth making next. A zero-findings conclusion with solid evidence is a successful audit.
