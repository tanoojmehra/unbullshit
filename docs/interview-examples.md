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
