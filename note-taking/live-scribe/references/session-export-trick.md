# Session export trick — a subagent can self-read a session

**Type:** reference / discovery
**Date:** 2026-08-09
**Status:** settled

## TL;DR
A background subagent cannot stream the live transcript, but it CAN read a
**persisted snapshot** of the parent session itself via:

```
hermes sessions list              # discover recent session ids
hermes sessions export <ID> --format markdown -o /tmp/sess.md
```

No parent-fed digest needed — the subagent reads ground truth, so fidelity loss
from a handoff summary is eliminated. Verified live: a test subagent auto-
discovered the parent session, read 167 messages, and wrote a `kb/` note,
reporting one line.

## Why it matters
- Reusable for future features: cross-session review, a subagent that audits a
  past session, batch recap of a long thread — without the main agent pasting
  context.
- Honest limits: `export` is **point-in-time**, not live; the one-line report
  still lands in chat (negligible); for huge sessions read the relevant window
  selectively.

## What we decided
We prototyped a "recap scribe" mode (background subagent that self-exports and
writes the note), then **judged it overengineering** for our workflow: the same
end-of-session artifact is achieved by one live recap pass by the main agent,
with no extra agent run — which matters under the ~$50/mo budget ceiling. So
`live-scribe` stays Mode A (live, in-context) only. This trick is kept as
knowledge, not as a spawned mode.

## Sources
- Parent session `20260809_184251_29ccdc` (note-taking debate + test).
- `hermes sessions --help`, `hermes sessions export --help`.
- Verification artifact: `kb/note-taking-architecture-test.md` (status: settled).
