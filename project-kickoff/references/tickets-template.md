# <NN> — <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the
user's perspective — not a layer-by-layer implementation list. Each ticket is a
tracer bullet: a narrow but COMPLETE path through every layer (schema, API, UI,
tests), demoable on its own.

**Blocked by:** the numbers/titles of the tickets that gate this one, or
"None — can start immediately".

**Status:** ready-for-agent

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

---
Write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`,
numbered from `01` in dependency order (blockers first). Work the frontier:
any ticket whose blockers are all done. Avoid specific file paths/code snippets
(same prototype-snippet exception as the spec).
