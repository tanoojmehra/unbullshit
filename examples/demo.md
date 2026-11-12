# Six guided demonstrations (authored, not measured)

These are repeatable *prompts and expected review criteria*, not agent transcripts, customer stories or evidence that any model improved. Start with the [installation guide](../docs/install.md); the four skills are independent, and none requires the others.

To compare **illustrative saved responses**, run:

```sh
python3 scripts/evaluate_behavior.py \
  --baseline tests/behavioral/fixtures/baseline.json \
  --enabled tests/behavioral/fixtures/skill.json \
  --output-dir /tmp/unbullshit-behavior
```

The output counts **literal checks on authored fixtures**, not user value or model performance. For a real comparison, use a tested adapter and human review as described in [benchmarking](../docs/benchmarking.md).

## 1. Founder trims an oversized AI idea

**Original request:** "I want five AI agents to collect vendor documents and approve compliance."

**Context:** Missing documents cause most delays; human approval is mandatory.

**Use:** Ask unbullshit-plan to identify the actual problem, present genuine alternatives and recommend a first release. A useful response proposes a checklist/reminder flow or one assistive extractor with human review, explains why five autonomous agents are not yet justified and accepts the founder's final call.

**Preserve:** Human signoff and audit needs. **Reproduce:** plan-ai-proposal case in [cases.json](../tests/behavioral/cases.json). **Limit:** Authored demonstration, not a measured agent outcome.

## 2. Ordinary implementation avoids speculative architecture

**Original request:** "Add CSV export to an existing table."

**Context:** The project already has a CSV utility and tests.

**Use:** Ask unbullshit to inspect and reuse the utility, implement only the export and verify escaping. A reporting platform, extra queue or planning ceremony is not required.

**Preserve:** Correct CSV encoding, authorized scope. **Reproduce:** base-csv. **Limit:** No actual repository implementation is contained in this example.

## 3. Audit finds unjustified complexity, without inventing evidence

**Original request:** "Review whether a redundant approval is useful."

**Context:** In the scenario, deploy.yml has two staging approvals routed to the same group; policy.md requires only one for staging but a separate signoff for production.

**Use:** Ask unbullshit-audit to cite those actual *supplied scenario files*, classify the duplicate staging step as unnecessary friction, recommend removing only that step after verification, and retain independent production approval. If policy or intent were unknown, the finding should instead be uncertain.

**Preserve:** Required production dual control. **Reproduce:** audit-confirmed-friction, audit-false-positive and audit-fabricated-evidence. **Limit:** Evidence is synthetic test context; no real deployment was audited.

## 4. Audit retains justified complexity

**Original request:** "Remove our queue and cache to make the code simpler."

**Context:** The queue retries provider failures; the cache respects an upstream rate limit.

**Use:** Ask unbullshit-audit for a reasoned retention decision grounded in those requirements. The correct answer preserves retry guarantees and the rate-limit protection.

**Preserve:** Reliability and provider constraints. **Reproduce:** audit-justified-queue. **Limit:** The supplied facts are scenario assumptions, not verified traces.

## 5. Improve one interaction without refactoring

**Original request:** "Make the Save button clearer."

**Context:** Existing design patterns and accessible labels must remain.

**Use:** Ask unbullshit-improve to change the label to "Save changes", inspect existing components, check accessibility and the save action, then stop.

**Preserve:** Form behavior and accessible name. **Reproduce:** improve-copy and improve-tool-failure (an honest failure response). **Limit:** The fixture is authored; no UI tests were run for a real application.

## 6. Reuse a previously approved decision

**Original request:** "Draft a clinic-booking release plan."

**Context:** Approved: mobile web, small clinics, manual confirmation; native apps and calendar sync were rejected for launch.

**Use:** Ask unbullshit-plan for slices consistent with those choices, and to reopen them only if there is new evidence. It should not invent founder consent or re-ask the platform question.

**Preserve:** Prior approval and constraints. **Reproduce:** plan-continuity. **Limit:** A supplied decision is not proof that an agent can recover records from every host.

See [before and after](before-after.md) for short scripted contrast examples. Real case studies should include permission, anonymized evidence, exact model and host settings and independent verification.
