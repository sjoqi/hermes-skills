---
name: live-scribe
version: 1
author: hermes
license: MIT
description: "Live note-taker: capture an ongoing chat/brainstorm/build session into kb/ notes as it happens, by the main agent appending distilled lines (Mode A). Use when G says 'take notes', 'note this session', 'scribe on', or 'document this as we go'."
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [notes, live, session-capture, kb]
    related_skills: [knowledge-base, resource-capture]
---

# Live Scribe — the ACTIVE layer on top of `knowledge-base`

Makes the conversation itself become documentation in `~/hermes-home/kb/`,
without bloating the live session.

`knowledge-base` owns the STATIC rules (when kb/ applies, file naming, the
template, INDEX conventions, the decision matrix). **Do not restate them —
read that skill and obey it.** This skill only answers: *how do we keep the
note current WHILE the session is running?*

## When to use
- G says: "take notes", "note this session", "scribe on", "document this as we
  go".
- Any brainstorm, design argument, or build session whose reasoning is worth
  re-reading later.
- Stop / flush: "capture now", "flush", "scribe off", or session end.

## Mode A — LIVE SCRIBE (the only mode; default)
The MAIN agent maintains the note itself as the session unfolds — captured per
point, in the same turn it's thinking, **zero spawn**.

1. On trigger, pick/create the target note per `knowledge-base` (GROW an
   existing note if it's the same thread; one file per idea).
2. Every few substantive turns — after a decision, a rejected option, a
   verbatim pain quote, a new constraint — append 1–4 distilled lines to the
   right section of the note (argument / push-back / open threads).
3. Keep the visible chat reply SHORT. Note-keeping is a **side topic**: at
   most a trailing one-liner like `· scribed → kb/<file>.md`, never a recap of
   what you wrote.
4. **Why this is enough (verified, 2026-08-09):** for normal sessions it wins
   on *fidelity* (captured at-the-moment with full context) and *zero overhead*
   (no subagent spawn, no return-message tax). It does NOT shrink the live
   transcript — the file-write tool call still appears in chat — but the detail
   lives on disk so it's recoverable later and stays out of your face. A
   background recap subagent was prototyped and judged **overengineering** for
   our workflow: the same end-of-session artifact is achieved by one live recap
   pass, with no extra agent run (matters under the ~$50/mo budget ceiling).

Use LIVE SCRIBE whenever the session is the work — this is what I do with G by
default. For a clean end-of-session artifact, do ONE recap pass at the end
(me reading the session, appending), not a spawned subagent.

## Stop / capture-now
- "capture now" / "flush" → run one final pass immediately.
- "scribe off" / session end → final flush, set the note `status:` to
  `growing` or `settled`, confirm in one line with the path.

## Pitfalls
- **Distil, don't transcribe.** A raw transcript in `kb/` is worthless; write
  article-style prose with the argument, not the chatter.
- **Don't route session notes into `memory`** — memory is durable facts only.
- **One file per idea; grow, don't fork.** Check `kb/` before creating.
- **INDEX rows are punchlines**, not summaries.
- **Keep client/user verbatim pain intact** — that phrasing is the goldmine.
- **Push back in the note** where an idea was weak; a yes-man note is useless.

## References
- `references/session-export-trick.md` — the verified discovery that a
  subagent (or a future feature) can self-read a session via
  `hermes sessions export <ID>`; kept as reusable knowledge, not as a spawned
  mode.
- Sibling: `knowledge-base` skill — all static kb/ filing rules.
