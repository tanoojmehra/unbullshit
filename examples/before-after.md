# Before and after

Illustrative conversation examples, **not measured agent results**.

## Base — ordinary feature

**Request:** "Add CSV export to this contacts table."

**Before:** "Let's add a reporting platform, worker queue, export templates and another database."

**After (`unbullshit`):** "I'll inspect the existing table and reuse any CSV functionality. I'll add the export action with correct escaping, a relevant test, and stop. We can revisit background exports only if size or latency requires it."

**Why:** A proportional solution, not a promise to skip correctness.

## Plan — founder interview

**Request:** "Let's build an AI-powered complaint portal."

**Before:** "We'll use six agents, a vector database, real-time orchestration, and Kubernetes."

**After (`unbullshit-plan`):** "If customers mainly submit complaints and your staff responds, a simple portal may cover the core need. AI triage could come later if volume or complexity warrants it. What is the biggest current pain: collecting cases, routing them, or resolving them?"

**Why:** Interview the founder on the decision that changes the scope.

## Audit — distinguish different problems

**Request:** "Our release workflow has duplicate approvals and sometimes reports success after a failure."

**Before:** "Delete every approval and replace the deployment system."

**After (`unbullshit-audit`):** "The false-success report is a defect. The two approvals may represent duplicated policy, but I'll examine their purpose and evidence before recommending removal. These are different problems and need different solutions."

**Why:** Evidence first; no quota of things to remove.

## Improve — focused pain point

**Request:** "The save button is confusing."

**Before:** "We need a new settings architecture, process map and state machine."

**After (`unbullshit-improve`):** "I'll inspect the save action, clarify the label and feedback with existing UI patterns, preserve behavior and test the affected path."

**Why:** A small improvement doesn't require an enterprise project.

## Counterexample — complexity is justified

**Request:** "The service must remain available if a whole region fails."

**Bad reduction:** "Use one server because distributed systems are overengineering."

**Correct judgment:** "That availability requirement justifies redundancy. First define recovery time, acceptable data loss, residency and budget; then recommend the simplest design that meets them."

**Why:** The objective is justified complexity, not minimal complexity.
