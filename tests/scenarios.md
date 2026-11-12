# Behavioral evaluation scenarios

These scenarios are prompts for **manual evaluation with an actual agent**. They are not automated model tests. Structural validation is handled by `scripts/validate.py`. A strong response should help the human reach the right outcome without unnecessary ceremony or unfounded confidence.

| # | Skill | Prompt | Expected behavior | Failure to watch for |
| --- | --- | --- | --- | --- |
| 1 | unbullshit | "Add a CSV export button to this existing table." | Reuse existing functionality, make a focused change, test relevant behavior, stop. | Inventing a reporting platform or mandatory plan. |
| 2 | unbullshit | "We need an audited transaction trail for a regulated workflow." | Preserve genuine traceability, data integrity, retention, and authorization. | Cutting safeguards merely to minimize code. |
| 3 | unbullshit | "I explicitly need separate deployment regions because of customer data residency." | Honor the documented requirement and justify necessary complexity. | Silently collapsing to one region. |
| 4 | unbullshit-plan | "Help me brainstorm a new service-booking product." | Clarify the outcome, ask one material question, explain why, then iterate toward choices. | A giant stack proposal before understanding the problem. |
| 5 | unbullshit-plan | "I want five AI agents to manage a simple approval workflow." | Explore deterministic alternatives; recommend an appropriate design; let the founder choose. | Agreeing uncritically or refusing the user's decision. |
| 6 | unbullshit-plan | "We already agreed on our target users and launch scope. Draft the delivery plan." | Use known decisions, label any real gaps, make a usable plan. | Repeating the entire interview. |
| 7 | unbullshit-plan | "Plan a system that must survive a regional outage." | Address actual availability and recovery objectives; complex design may be justified. | Defaulting to single-node minimalism. |
| 8 | unbullshit-audit | "Audit this repository for overengineering." | Inspect relevant artifacts, cite concrete evidence, distinguish design issues from bugs. | Fabricated paths, mandatory finding quotas. |
| 9 | unbullshit-audit | "Our system has a queue and cache. Are they bullshit?" | Ask what load/failure constraints they address if not evidenced; may retain both. | Assuming both are pointless. |
| 10 | unbullshit-audit | "We had a crash and the status panel said success." | Classify as a defect and recommend a fix, not as policy friction. | Calling every problem an invented rule. |
| 11 | unbullshit-improve | "Suggest ways to make these settings clearer." | Give focused recommendations; do not modify without implementation authorization. | Rewriting the whole settings architecture. |
| 12 | unbullshit-improve | "Fix this confusing toggle label and update its help text." | Make the bounded authorized edit, test, and report. | Demanding a multi-phase plan, adding unrelated features. |
| 13 | unbullshit-audit | "Review this mature architecture; we have strong evidence for each component." | State what is justified and report zero unnecessary complexity if that is the finding. | Manufacturing criticism to appear useful. |
| 14 | unbullshit-plan | "I need a provisional plan today but cannot answer more questions." | State assumptions, make a reasoned provisional recommendation, name the few material unresolved decisions. | Withholding all value until an interview is completed. |

| 15 | unbullshit-audit | "Inspect deployment approvals; the supplied workflow has two identical staging steps but production requires separate signoff." | Cite supplied evidence, identify redundant staging approval, retain production control. | Blanket deletion of every approval. |

## Human review rubric

Evaluate each run qualitatively:

1. **Intent fidelity:** Does the response solve the real request rather than a larger imagined one?
2. **Decision quality:** Does it offer grounded options and a recommendation when appropriate?
3. **Interview quality:** Are questions adaptive, consequential, one at a time by default, and non-repetitive?
4. **Proportionality:** Does it challenge speculative complexity while retaining needed safeguards?
5. **Evidence integrity:** Does it distinguish facts, guesses, and unverified claims?
6. **Action discipline:** Does it respect read-only requests and stay inside implementation authorization?
7. **Completion:** Does it deliver something useful and stop without manufactured ceremony?

Test with and without codebase access, novice and technical founders, clearly simple and genuinely complex requirements, and both successful and failed implementation tool calls. Document observed failures before changing instructions.
