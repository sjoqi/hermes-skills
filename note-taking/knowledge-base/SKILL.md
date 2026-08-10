---
name: knowledge-base
version: 1
author: hermes
license: MIT
description: Manage G's growable kb/ notes for brainstorms and resources.
metadata:
  hermes:
    tags: [notes, knowledge-base, second-brain, research, brainstorming]
    related_skills: [resource-capture, hermes-collab-setup]
---

# Knowledge Base (kb/) — Note Manager for Brainstorms & Resources

## When to Use
- G says "save this", "note this down", "save the talk", "add it to the kb", or shares a
  video / link / idea to keep across sessions.
- Starting research on agent / workflow / automation topics — CHECK `kb/` first so prior
  thinking carries forward.
- Editing / maintaining existing kb/ docs (merging fixes from companion specs, stale-note
  cleanup) — same growth-over-fork rule; see the merge & maintenance discipline below.
- Do NOT use for durable operating facts (→ `memory`) or one-line principles (→ `RESOURCES.md`).

G wanted a second brain: article-style, growable notes for ideas, videos, links, and
research — distinct from (a) durable memory facts, (b) one-line principles in
RESOURCES.md, and (c) his raw Obsidian dumps. We built `~/hermes-home/kb/` for this and
it is now the home for long-form think-pieces that survive across sessions.

## Trigger
- G shares a resource ("watch this", "save this", "read this") or a brainstorm idea and
  wants it kept for later / cross-session.
- "Note this down", "save the talk", "I'll come back to this", "add it to the kb".
- When starting research on agent / workflow / automation topics, CHECK `kb/` first (it
  was seeded with notes on those) so prior thinking carries forward into the new session.

## Style rule (G's explicit preference)
During a brainstorm / design talk / build session, **note management is a SIDE
TOPIC, not the headline.** Do the file work quietly (ideally in the background)
and keep the visible chat reply on the *idea*, with at most a one-line note of
what was filed. Do NOT narrate how you organised, renamed, or indexed notes, and
do NOT recap note contents in chat — G reads `kb/` directly later. This applies
to both spontaneous note-taking and the `live-scribe` skill.

**Broader brainstorm mode (same root preference):** when G is in learning /
brainstorm mode, PRIORITISE teaching and exploring the *idea* over producing
artifacts or decisions. Do not rush to build, write files, or "resolve" the
topic unless G explicitly asks. Recurring phrasings this session: "just focus on
teaching me", "continue this as my learning space", "dig into the risk", "save
this for the production phase later". When G says defer/save-for-later, note it
mentally (or in a skill reference) and do NOT act on it now. Conclude a
brainstorm turn with the idea + a concise next-step question, not a file summary.

## When NOT to use
- A durable OPERATING fact (budget ceiling, routing rules, delegation limits) → `memory`.
- A single reusable PRINCIPLE / one-liner → `RESOURCES.md` (distilled, not article).
- G just wants raw capture into his own Obsidian → leave it; don't duplicate.

## The system (on disk)
- `~/hermes-home/kb/INDEX.md` — the map. One row per note: **punchline** (NOT a summary),
  tags, date, status. This is the table of contents; keep rows scannable.
- `~/hermes-home/kb/_template.md` — copy per idea. Structure: TL;DR → stimulus → argument →
  connection to our work → push-back → what stays true → open threads → sources.
  (A ready-to-copy version ships in this skill's `templates/note-template.md`.)
- One file per idea. Name: `kebab-case-topic.md`. Cross-link related notes.
- `~/hermes-home/INDEX.md` top-level table points at `kb/` so the workspace map stays synced.

## How to file a note (steps)
1. Read any prior notes on the topic in `kb/` — avoid duplicates; GROW an existing note if
   it's the same thread rather than forking a new file.
2. Create `kb/<kebab-case>.md` from the template. Keep it article-style: prose, sharp, and
   PUSH BACK where an idea is weak — G values a sharp partner, not a yes-man.
3. Add a row to `kb/INDEX.md` with a one-line PUNCHLINE + tags + date.
4. If the note is a resource (video/link), also distil the reusable principle into
   `RESOURCES.md` (kb/ holds the long form; RESOURCES.md holds the one-liner).
5. If it changes how we work, also touch `PLAYBOOK.md`.

## Editing existing kb/ docs — merge & maintenance discipline

kb/ is not only brainstorm notes — it also holds the engineering spec stack
(`lead-qualification-*.md`, workflow-architecture docs) that gets patched via
delegated merge tasks ("merge fix #N from companion.md into target.md"). Same
growth-over-fork rule, plus:

- **Read the CURRENT target first.** A prior agent may have already patched it —
  quoted line numbers in the task are stale. Anchor patches on unique content
  strings, never line numbers.
- **Edit ONLY the named file.** Companions have their own patch tasks; don't
  touch them even if they also need the change.
- **Condense + point, don't duplicate.** Compact mechanism prose (key names,
  invariants, failure modes) + "Per `companion.md` fix #N" — never paste the
  companion's full code blocks into the target.
- **Preserve the file's house style** (letter-suffix subsections like `4.1a`,
  pipe tables, `§` cross-refs, backticked field names) and update the schema /
  handoff-table / test rows the fix touches, not just the prose.
- **Serialize same-file patches** (one patch call at a time) and **verify by
  re-reading** the changed regions + file tail after all edits (confirm
  deletions like stale blockquotes are actually gone).

Full step-by-step: `references/spec-doc-merge-workflow.md`.

## Decision matrix (where does this note go?)
| Content | Goes to |
|---|---|
| Durable operating fact (budget, routing, delegation limits) | `memory` |
| One reusable principle / lesson | `RESOURCES.md` |
| Long-form, growable idea / research / brainstorm | `kb/` |
| Raw personal capture | G's Obsidian (do nothing) |

Full rationale (incl. why NOT holographic memory for notes) in `references/decision-matrix.md`.

## Conventions
- Notes are RESOURCES, not memory: long-form, human-readable, grep-able.
- Grow a note across sessions; don't fork it into new files.
- Status values: `open` / `growing` / `settled`.
- Check `kb/` at the start of any agent / workflow / automation research.

## Pitfalls
- Don't route article-style notes INTO memory — memory is for durable facts only; notes
  bloat it and hit the char ceiling fast (we hit the 2,700-char limit this session).
- Don't summarize away the source's own wording, especially verbatim client pain in
  research — that phrasing is the product-language goldmine.
- Don't make `kb/INDEX.md` a summary dump; keep rows to a punchline so the map stays a map.

## References
- `templates/note-template.md` — copy for each new note.
- `references/decision-matrix.md` — full where-does-it-go rationale.
- `references/spec-doc-merge-workflow.md` — step-by-step for merging companion-spec fixes into a target kb/ doc.
- Live folder: `~/hermes-home/kb/` (seeded with graph-engineering + workflow notes).
