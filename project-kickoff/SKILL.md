---
name: project-kickoff
description: "Start a new software project the right way: grill to resolve the design, write a spec, then break it into vertical-slice tickets — and enforce a git checkpoint before any code. Use when G says 'new project', 'kickoff', 'start the project', or shares a project idea."
platforms: [macos, linux, windows]
---

# Project Kickoff

Run this at the start of every new software project with G, **before any code**.
It walks the first three steps of the Build Chain — **grill → to-spec →
to-tickets** — and enforces G's checkpoint rule before implementation.

Adapted from Matt Pocock's `grill-with-docs` + `to-spec` + `to-tickets` skills
(github.com/mattpocock/skills), reframed for Hermes: **G = strategic architect**
(goals, boundaries, review); **Hermes = tactical executor** (implementation).

## When to use
- G says "new project", "kickoff", "start the project", or shares a project idea.
- Do NOT use for tiny changes — use `tdd` or `code-review` directly.

## Pre-flight (once)
1. Confirm the repo folder path with G (or ask for it).
2. If no git repo there yet: `git init`, initial commit, and create `.gitignore`
   covering large clones / secrets / build artifacts.
3. Pin a Hermes **Project** anchored to that folder so skills + sidebar follow.

## Step 1 — Grill (resolve the design)
Run a **grilling** session (relentless interview) adapted to G:
- Interview **one question at a time**. For each: state the question and a
  **recommended answer** (your best guess), then WAIT for G's response.
- If the answer is already discoverable from the codebase, **inspect the code**
  instead of asking G to explain what exists.
- **Push back** rather than agree — surface contradictions and weak assumptions.
- Keep going until every branch of the decision tree is resolved: goals,
  boundaries, non-negotiables, explicit scope, tech/stack constraints, and a
  definition of "done".
- As terms get coined or decisions made, run the `ubiquitous-language` skill
  (CONTEXT.md glossary + ADRs) **inline as you go** — this is the
  `grill-with-docs` behaviour: create the glossary/ADRs during the interview,
  not after.
Stop only when G would be repeating themselves — the design is unambiguous.

## Step 2 — To-spec (write the shared understanding)
Synthesise — **do NOT re-interview**. Explore the repo first (use the project's
glossary vocabulary; respect any ADRs). Then:
1. Sketch the **seams** to test at. Prefer existing seams; use the highest seam
   possible; ideal is one. Confirm the seams with G before writing.
2. Write the spec to `docs/spec.md` (or `SPEC.md`) using the spec template
   (`references/spec-template.md`). It must be in the project's own vocabulary.
   Do NOT include specific file paths or code snippets (they go stale); exception:
   a prototype-produced snippet that encodes a decision better than prose
   (state machine, reducer, schema, type shape) may be inlined, noted as from a
   prototype.

## Step 3 — To-tickets (vertical slices)
Break the spec into **tracer-bullet tickets**, each declaring its blocking edges.
1. Work from the spec/conversation. (If G passes a spec path, read it fully.)
2. Explore the codebase; ticket titles/descriptions use the glossary vocabulary.
3. Look for **prefactoring** first ("make the change easy, then make the easy
   change").
4. Each ticket cuts a COMPLETE path through every layer (schema, API, UI, tests)
   — vertical, NOT a horizontal layer. Demoable alone; sized to fit one context.
5. **Wide refactors are the exception.** A single mechanical change with huge
   blast radius → sequence as **expand–contract**: add the new form beside the
   old (expand) → migrate call sites in batches by blast radius, each its own
   ticket blocked by the expand, CI green throughout → delete the old form
   (contract), blocked by every migrate batch.
6. **Quiz G** on the breakdown (granularity, blocking edges, merge/split) and
   iterate until approved.
7. Publish: write one file per ticket under `.scratch/<feature-slug>/issues/
   <NN>-<slug>.md` (blockers first) using `references/tickets-template.md`,
   with `ready-for-agent` status. Work the **frontier** (tickets whose blockers
   are all done). Avoid specific file paths/snippets (same prototype exception).

## Step 4 — Checkpoint (before code)
Enforce G's standing rule: before ANY implementation,
`git add -A && git commit -m "checkpoint: spec+tickets ready"` and
`git tag -f checkpoint-working` (force-move the tag — see PITFALL below).

**PITFALL — duplicate tag.** The first `checkpoint-working` tag is normally set
at repo init (or by a prior checkpoint). A plain `git tag checkpoint-working`
errors with `fatal: tag 'checkpoint-working' already exists` and aborts the
checkpoint mid-project. Always use `git tag -f` to move the tag to the latest
safe point. Nothing changes a working build without a way back.

Then hand off to `tdd` / implement per ticket.
