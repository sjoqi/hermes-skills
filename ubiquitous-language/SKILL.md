---
name: ubiquitous-language
description: "Build and sharpen the project's shared vocabulary (ubiquitous language) and record hard-to-reverse decisions as ADRs. Use when pinning terminology, resolving an overloaded word, or recording an architectural decision. Keeps Hermes and G speaking the same language."
platforms: [macos, linux, windows]
---

# Ubiquitous Language (domain-modeling)

Actively build and sharpen the project's domain model as you design. This is the
*active* discipline — challenging terms, inventing edge-case scenarios, and
writing the glossary and decisions down the moment they crystallise. (Merely
*reading* `CONTEXT.md` for vocabulary is not this skill — that's a one-line
habit any skill can do. This skill is for when you're changing the model.)

Adapted from Matt Pocock's `domain-modeling` skill (github.com/mattpocock/skills).

## File structure
Most repos have a single context:
```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-<topic>.md
│       └── 0002-<topic>.md
└── src/
```
If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts; the
map points to where each `CONTEXT.md`/`docs/adr/` lives. Create files lazily —
only when you have something to write.

## During the session
- **Challenge against the glossary:** when G uses a term that conflicts with
  `CONTEXT.md`, call it out — "Your glossary defines 'cancellation' as X, but you
  seem to mean Y — which is it?"
- **Sharpen fuzzy language:** propose a precise canonical term — "You're saying
  'account' — do you mean the Customer or the User? Those are different."
- **Discuss concrete scenarios:** stress-test domain relationships with specific
  edge-case scenarios to force precision about boundaries.
- **Cross-reference with code:** when G states how something works, check the
  code agrees. Surface contradictions — "Your code cancels entire Orders, but
  you just said partial cancellation is possible — which is right?"
- **Update CONTEXT.md inline:** when a term is resolved, update it right there,
  don't batch. `CONTEXT.md` is a glossary and nothing else — no implementation
  details, no spec, no scratch pad.
- **Offer ADRs sparingly:** only when all three hold:
  1. **Hard to reverse** — changing your mind later is meaningfully costly
  2. **Surprising without context** — a future reader will wonder "why this way?"
  3. **The result of a real trade-off** — genuine alternatives, you picked one
  Miss any one → skip the ADR. Use `references/adr-template.md`.

## When to use
- During `project-kickoff` grilling (coin terms live).
- An overloaded word snags the conversation.
- A trade-off decision is made.
- G or Hermes reaches for a term not yet in the glossary.
