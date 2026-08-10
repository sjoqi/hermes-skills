---
name: pre-build-design-audit
description: "Audit a design pre-code: parallel passes, approved merge."
version: 1.0.0
author: curator
license: CC-BY-4.0
metadata:
  hermes:
    tags: [design-review, delegation, risk-audit, spec, workflow]
    related_skills: [grill-with-docs, project-kickoff, working-with-g, hermes-delegation]
---

# Pre-Build Design Audit

## When to use

- A design/spec set is **complete but zero code exists**, and G wants the risks found before the build chain starts.
- G says "review the infrastructure", "find the gaps", "deep review before we build", "validate the design against the market".
- You hold multiple spec docs (e.g. `kb/` build files) and need a structured, evidence-backed audit without bloating chat context.

**Do NOT use** for code review of committed changes (that's `code-review`), or for sharpening a plan via Socratic interview (`grill-with-docs`).

## The four-phase workflow

Phase 1 **Risk audit** → Phase 2 **Blue-team fixes** → Phase 3 **Gap closure** → Phase 4 **Merge (user-approved)**.

Each phase is a **parallel `delegate_task` fan-out**: leaf subagents, one per domain lens, each with file paths + settled design decisions in `context`, told explicitly to *"be critical — find every gap, don't protect the design."* Their consolidated results re-enter as one message; never poll.

### Phase 1 — Risk audit (find what's wrong)

Fan out 5 agents, one lens each. Proven lenses for a data-pipeline spec set:

1. **Security & threat model** — attack vectors past HMAC/dedup, prompt-injection sufficiency, tunnel risks, internal-API auth, "what would a real audit flag?"
2. **Reliability & durability (SRE)** — idempotency edge cases, store corruption, replay loops, race conditions, reconciliation gaps.
3. **Architecture & code/agent boundary** — state-machine shape, code-vs-agent split, store choice failure modes, distributed-systems review.
4. **Market fit & client reality** — does the scope over/under-serve the actual buyer? what do the recurring posts demand? competitive landscape? cost viability?
5. **Operational gaps & production readiness** — monitoring, alerting, deploy, backup/DR, multi-tenancy, compliance, testing.

Each returns **structured findings: severity (critical/high/medium/low) + one recommendation per finding**. Optionally have them write full reports to files and return only summaries (keeps parent context lean).

**Synthesize into a coverage map** — the key artifact:

| # | Finding | Severity | Flagged by | Covered by |
|---|---|---|---|---|
| 1 | ... | CRITICAL | Security, Ops (independent) | `fix-spec.md` ✓ |

Cross-validation rule: findings flagged by **≥2 independent agents** are highest-confidence — mark them. Findings that are logically provable from the specs (e.g. "T11 edit bypasses GATE 1") are high-confidence even with one flagger. Present the map to G with a recommended priority order before Phase 2.

### Phase 2 — Blue-team fixes (how to fix it)

Fan out 5 agents again, one per critical/high cluster, each mission: *"research and produce a concrete, implementable spec."* Give each agent the exact gaps from Phase 1 to solve and the files they may write. Proven missions: human-approval auth, GDPR split-store, internal-API security, gateway hardening, reliability hardening. Each writes a full spec file to disk and returns a summary.

### Phase 3 — Gap closure (the items that slipped)

Compare Phase 1 findings against Phase 2 outputs. Anything uncovered (e.g. T11 edit re-validation, X-Request-ID dedup window, backup/DR, multi-vertical routing) becomes a third fan-out. **Use more than one agent — G explicitly prefers multiple agents here.**

### Phase 4 — Merge (only after G approves)

**G's hard rule (learned 2026-08-10): do NOT edit the source files mid-research.** When research is complete, present the complete edit plan first — *what changes go into which file* — then brainstorm with G, then get explicit approval, THEN edit in one pass.

Merge strategy G chose (option C, hybrid):
- **Merge critical architectural changes into the originals** (approval auth, split-store, state-machine fixes, idempotency window).
- **Keep operational specs standalone** as companions (backup/deploy, gateway hardening, reliability hardening) linked from the originals.
- Delete out-of-context tooling noise from spec files when G asks (PNG/mermaid/excalidraw generation instructions, render commands, share links — G: "unnecessary line thats really irrelevant... delete it, since its out of context"). Keep design diagrams; drop the *generation* tooling.

Execution: fan out per-file merge agents (each edits ONLY its one file, read current disk state first — earlier agents may already have patched it), while you edit the meta files (README, handoff, big-picture) yourself. Then **verify every file on disk**: required additions present, PNG notes deleted, no stale references.

## Pitfalls

- **Stale content**: subagents in earlier phases may already have patched files. ALWAYS re-read current disk state before merging — `search_files` for the old references (e.g. "1h dedup") to see what was already changed.
- **File-scope isolation**: each merge agent gets ONE file to edit, never "touch what you like". Overlapping writers corrupt each other.
- **Coverage map, not raw dump**: G values sharpness — the synthesized map is the deliverable, not 5 agent reports pasted back.
- **Don't start Phase 2 before G sees Phase 1**: the map + priority order is a decision point, not a formality.
- **Subagent self-reports aren't proof**: verify merged files yourself (read back the sections the agent claimed to change).

## Example prompts

See `references/example-mission-prompts.md` — the actual Phase 1/2/3 mission prompts from the lead-qualification audit, copyable with substitutions.
