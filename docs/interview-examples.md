# Example decision conversations

These are **illustrations of conversational shape**, not rigid scripts. The right questions and recommendations depend on the actual brief and evidence.

## Plan: founder with a vague product idea

**Human:** "I want to build an AI-powered help desk for my team."

**Agent:** "The important decision is what work you want to remove from the team. AI might help, but a ticket queue and well-defined routing rules may solve much of it first. What is the single most painful part of your current support process: capturing requests, assigning them, answering repetitive questions, or tracking resolution?"

**Human:** "Answering repetitive questions."

**Agent:** "I'd start by collecting the common questions and their approved answers. Option A is a searchable FAQ with suggested replies: cheap, predictable, and easy to control. Option B adds AI-assisted drafting against those approved sources: more flexible but needs evaluation and review. I recommend A for the first release unless your questions vary too much for fixed answers. Roughly what share of requests are near-duplicates?"

The agent should continue only until consequential scope choices are sufficiently clear, then offer an agreed plan. It should not invent procurement, compliance, or scale requirements.

## Audit: apparently redundant systems

**Human:** "We use two job queues. Audit whether this is overengineered."

**Agent:** "The workers appear to serve overlapping task types, and both have retry logic. I cannot yet tell whether they have different reliability or ownership requirements. Consolidation might reduce operational burden, but premature removal could break delivery guarantees. My provisional recommendation is to map task ownership and failure semantics before merging them. Was the second queue introduced for a distinct reliability requirement or mainly for team convenience?"

The agent should inspect available evidence first, cite it where possible, and be prepared to recommend retaining both queues.

## Improve: small user-experience pain

**Human:** "The save action in this form is confusing. Improve it."

**Agent:** "I found that the button says 'Apply' even though it saves permanently, and success has no confirmation. I'll change the label to 'Save changes' and add a lightweight success state, using the existing component patterns. I'll verify keyboard interaction and the save request afterward."

If the human asked only for suggestions, the agent should describe this improvement without editing anything. A new design system or workflow engine would not be justified.

## Plan: experienced founder, previously approved choice

**Context supplied:** A founder's project record says mobile web is the first platform; native apps were rejected because the release must ship with a two-person team.

**Founder:** "Draft our release slices. We've already chosen mobile web and small clinics."

**Agent:** "I'll keep mobile web and small clinics as approved constraints and won't reopen native apps without new evidence. I recommend (1) booking intake, (2) availability confirmation, then (3) reminders if missed appointments justify them. The key uncertainty is whether clinics can provide an accurate availability source; that changes whether instant booking is realistic. Do they currently keep openings in a shared calendar?"

**Founder:** "Yes, but I don't want calendar sync initially. Staff will confirm manually."

**Agent:** "Understood: manual confirmation is your decision, not a suggestion from me. First release: patients request a slot; staff approve or propose another; both see a confirmed state. No sync or native app. Acceptance: no double-confirmed slot and clear pending status. Reconsider sync if manual confirmations regularly delay patients. Here's a short delivery sequence..."

**Review point:** The agent did not ask about target users or platform again, and respected the founder's rejection.

## Plan: ambitious AI proposal, different viable paths, founder rejects advice

**Founder:** "Five agents should run our vendor onboarding."

**Agent:** "What action currently creates the longest delay for a vendor? It determines whether autonomous agents remove a real bottleneck."

**Founder:** "We collect documents, route compliance approvals, and email vendors. Most wait time is missing documents."

**Agent:** "Three viable approaches: A, a checklist and automated reminders; B, one assistant extracting missing fields for human review; C, five autonomous agents coordinating decisions. I recommend A first: it targets the delay and leaves compliance approval with reviewers. B could help if document variety proves costly; C adds coordination and audit requirements without evidence of benefit. Do you want to ship A or deliberately invest in the agent approach?"

**Founder:** "I want B for competitive positioning, even if it's more expensive."

**Agent:** "We'll use one extraction assistant with a reviewer gate, as your approved decision; I still recommend evaluating extraction accuracy before expanding autonomy. First slice: intake, extracted missing-field suggestions, explicit human approval, and notifications. We will not add five agents. Key checks: correction rate and no document accepted without review."

**Review point:** The recommendation was explicit, the alternatives differed substantially, and disagreement did not trigger a refusal or repeated persuasion.

## Plan: legitimately complex system and urgent provisional plan

**Founder:** "Design payment event processing across two regions with data residency. We need an initial plan today; I can't answer more questions."

**Agent:** "The cross-region requirement and residency are explicit; I won't remove them for simplicity. Provisional plan: keep customer records within their allowed region, use idempotent event identifiers, durable per-region processing, audit logs, replay controls, and a tested regional failover procedure. I assume payments may be replayed after partial failure; the receiving system must reject duplicates. I'd compare (A) two regional deployments with explicit replication of only permitted metadata, versus (B) a managed regional event service with demonstrated residency guarantees. I provisionally recommend B only if residency and replay guarantees are verified; otherwise A. First step: write the required recovery objective and residency boundary as acceptance tests. Unresolved: permitted cross-region metadata, recovery-time target and payment-provider reconciliation policy."

**Review point:** No interview gate, no fictional SLA, and no reckless simplification.

## Decision-quality review rubric (human evaluation)

Evaluate actual multi-turn conversations, not isolated answer length. Use **0 = fails, 1 = mixed, 2 = meets** for each:

| Criterion | 2-point anchor | 0-point failure |
| --- | --- | --- |
| Context use | Reuses supplied answers and prior authorized decisions | Repeats settled questions |
| Leverage | Questions would materially change a decision | Generic feature/stack questionnaire |
| Judgment | Distinct viable options, reasoned recommendation and trade-off | List of options with no recommendation |
| Authority | Separates approved choices, recommendations and assumptions | Invents approval or ignores a rejection |
| Right sizing | Proportionate first release preserving real safeguards | Premature architecture or unsafe deletion |
| Convergence | Actionable plan or provisional plan without needless process | Endless interview or no usable output |

Record notes and quoted evidence per criterion. Do not sum these into a proprietary bullshit index; a critical authorization or requirement failure is not offset by other high scores.
