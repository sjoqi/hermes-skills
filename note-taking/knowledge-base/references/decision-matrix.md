# Where does this note go? — Decision Matrix & Rationale

G wanted a second brain, but his memory and existing files already serve specific roles.
Routing the right content to the right place keeps each layer clean.

## The four homes
| Content | Destination | Why |
|---|---|---|
| Durable OPERATING fact (budget ceiling, model routing, delegation limits, standing rules) | `memory` | Injected every session; must be tiny + high-signal. Char ceiling ~2,700. |
| One reusable principle / lesson (one-liner) | `RESOURCES.md` | Distilled insight library, grep-able, no prose. |
| Long-form, growable idea / research / brainstorm | `~/hermes-home/kb/` | Article-style, cross-session, human-readable, grows over time. |
| Raw personal capture | G's Obsidian | Leave it; don't duplicate into our system. |

## Why NOT holographic memory for these notes
- Holographic memory is an entity/relationship store for **queryable facts**, not a prose
  notebook. Stuffing article-style notes in bloated it and hit the 2,700-char ceiling in
  one session.
- Notes are meant to be *read as prose* and *grep-ed by topic*, which files do well.
- Memory should stay reserved for operating facts so it stays high-signal.
- Compromise we adopted: store ONE compact memory entry pointing at `kb/` ("notes live in
  kb/, check it for agent/workflow topics") so future sessions know to look — without
  copying the content into memory.

## Why a separate `kb/` folder and not just RESOURCES.md
- `RESOURCES.md` is designed for one-liners / distilled principles. Long-form prose would
  bury the one-liners and make the file unwieldy.
- `kb/` lets each idea be its own growable file with structure (TL;DR, push-back, open
  threads) and an INDEX.md map. Scales as ideas accumulate.

## Conventions enforced in kb/
- One file per idea; grow it across sessions rather than forking.
- `kb/INDEX.md` row = a PUNCHLINE, not a summary (keeps the map a map).
- Status: open / growing / settled.
- Cross-link related notes.
