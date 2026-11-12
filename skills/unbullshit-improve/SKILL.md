---
name: unbullshit-improve
description: Make practical, focused improvements to an existing feature, workflow, product, or codebase without an elaborate planning exercise. Use when a user wants something clearer, simpler, more useful, or less painful; inspect the relevant area, propose a right-sized approach, execute within authorization, and verify.
license: MIT
---

# Unbullshit Improve

**Make it better without making it bigger.** Address a real pain point with the smallest justified change. Do not turn a targeted improvement into an architectural initiative.

Use for an existing feature, interaction, workflow, process, or modest enhancement with a reasonably clear objective. If the goal itself, product direction, or major architecture is undecided, recommend `unbullshit-plan`. If the user wants an independent project-wide diagnosis, recommend `unbullshit-audit`. Never force a switch when the current request can be handled.

## The focused loop

1. **Understand the pain.** What is inconvenient, confusing, slow, costly, fragile, or missing? What user-visible outcome would count as better?
2. **Inspect the relevant area.** Look at existing behavior, patterns, constraints, previous approved decisions, existing utilities and dependencies. Avoid sweeping scans unless the change genuinely spans the project.
3. **Find the simplest sufficient improvement.** Prefer reuse, consolidation, clarification, or a small targeted change over a new framework, service, workflow, or feature family.
4. **Surface a material choice if one exists.** Explain trade-offs in plain language, recommend an approach, and ask **one focused question** when the answer affects behavior, data, architecture, or significant cost. Otherwise proceed.
5. **Act within the request.** If the user authorized implementation and tools allow it, make the bounded change. If the user asked for ideas or a review only, present recommendations without modifying anything.
6. **Verify and stop.** Check relevant outcomes and regressions, including critical existing requirements; report what changed, tests actually run and their results. If a write failed, a tool was unavailable, or tests failed, report partial progress and the blocker, not completion. Stop rather than initiating unrelated cleanup.

## Reality check

Ask before increasing complexity:

- Does this directly improve the named pain point?
- Would an existing component or normal process work?
- Is the new abstraction or dependency needed *now*?
- Does the change preserve expected behavior, accessibility, security, data integrity, and operational safety?
- Is the migration effort proportional to the benefit?

Do not treat lower lines-of-code or fewer features as proof of success. A slightly larger solution may be better when it removes user friction or increases correctness.

## Interview style

Be conversational, practical, and brief. Explain an important alternative only when there is a meaningful decision. For reversible implementation details consistent with the user's instructions, choose sensibly rather than asking permission.

When the user disagrees with the recommendation, respect the decision within authorized scope. Do not silently weaken requirements to make the work easier.

## Output

For advice-only work: summarize the pain, recommend the targeted change, and give the key trade-off or next step.

For implementation: give a short outcome, changed areas, relevant checks actually performed (including failures), and remaining limitations. Do not generate a lengthy plan, risk register, tickets, changelog, or large refactor unless the task warrants or explicitly requests them.

## Boundaries

Do not turn a suggestion into permission to edit; do not change unrelated features, dependencies, architecture, or product strategy. Keep real protections and explicit constraints. If a change turns out to require major product decisions, explain that boundary and propose the smallest decision needed before continuing.

## Updating project findings (only when authorized)

Routine small improvements need no register, ticket, or extra ceremony. If an authorized improvement addresses an existing recorded Unbullshit finding, locate that project's active `findings/UB-NNNN.md` record and **when authorized to update project records**, append the actual change, verification, remaining risks, and dated status transition; rebuild `REGISTER.md`. Do not call an improvement resolved until verification supports it.

Choose one project-local location using **tracked** paths: `brain/unbullshit/` only when the project is confirmed to use `kenmark-studio` or `kenmark-skills` **and** has tracked `brain/` files; otherwise `docs/unbullshit/` if tracked `docs/` files exist; otherwise root `unbullshit/`. Preserve an already-active register rather than creating a competing one. Never store the target project's records in the installed skill's source directory.

For a new significant finding, use the same stable-ID register with a supported classification and actual evidence; do not manufacture an audit for a minor fix. For consequential choices the human wants saved, use `decisions/YYYY-MM-DD-topic.md`. Keep status history, existing links, and real safeguards intact. Logging does not authorize changes outside the requested improvement.


**Installed-skill portability:** The helper CLI is optional and may not be present. Use ordinary host file tools in the **target project** only when writing records is authorized. Inspect the existing register and canonical files first; never create a competing folder. Follow the frontmatter and dated history in the recordkeeping specification: stable UB-NNNN IDs, append status/history instead of replacing it, and rebuild REGISTER.md from findings. For concurrent writers require exclusive creation plus a cooperative lock/transaction around reading, writing and reindexing; if unavailable, stop rather than risk collision. A malformed finding or conflicting active registers must be resolved, not overwritten. Never write during read-only work or automatically on activation.

## Done means

The named problem is improved or there is a clear, grounded recommendation for improving it, with no unnecessary ceremony or unrequested expansion.
