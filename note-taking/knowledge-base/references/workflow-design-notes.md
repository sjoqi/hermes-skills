# Workflow-Design Note Patterns (from the "Hermes as the workflow" thread)

Reusable shapes for article-style `kb/` notes about agentic automation / workflow design.
Load this when writing a workflow/automation design note so the structure is consistent
and the hard-won design insights carry forward.

## 1. Big picture BEFORE specs (planning-phase discipline)
When designing a workflow/automation — especially presented like a freelance dev to a
client — lead with the SHAPE, not the nodes:
- A big-picture diagram (mermaid/ASCII) of the whole job end to end, with every node
  tagged **CODE vs AGENT** inline.
- ONE concrete, deliberately SIMPLE example grounded in REAL prior research (not a toy),
  so the shape is legible.
- An explicit **"what we are NOT deciding yet"** section (node specs, infra, state store,
  webhook exposure) deferred to the build session.
Matches G's instruction: "architecture diagram / big picture before detailing the node
and workflow specification."

## 2. Two-gate review split (machine → human)
Do NOT collapse review into one queue. Split it:
- **Auto-validation gate (machine, CODE):** answers "did we do the job CORRECTLY &
  COMPLETELY?" — schema valid, score in enum, dedup clean, no silent field loss. Fires
  automatically BEFORE any human is involved; $0.
- **HITL final judgment (human):** answers "is this the ACTION we want to take?" — send
  outreach? route to rep? The human owns the business call; the machine only confirmed
  correctness.
Benefit (G's insight): a human never wastes attention approving a *broken* job — the
machine catches that first, so the human queue holds only real business decisions.

## 3. Code-vs-agent ruling (the governing rule)
For each node ask: "if the failure mode is 'data was lost or duplicated' → CODE; if it's
'judgment was mediocre' → AGENT." Everything load-bearing (connectors, dedup, verify,
retry, review-queue storage, final write) is code; only extract / score / draft / judge
are agents. This keeps cost ~$0.01/run vs ~$1 for a 100-agent DAG.

## 4. Ground the example in the demand research
Pull the simple example from the actual mined dataset (e.g. UW-021 FB Lead Ads → score →
GoHighLevel, $100, fixed Hot/Warm/Cold) rather than inventing one. Recurring shapes in
the data make the build reusable, not a one-off.
