---
name: hermes-memory-setup
description: >
  Configure Hermes Agent persistent memory — built-in MEMORY.md/USER.md
  (char budgets, consolidation, frozen-snapshot behaviour) and external
  memory providers (holographic, honcho, hindsight, mem0, openviking,
  retaindb, byterover, supermemory). Covers provider selection trade-offs,
  install via `hermes config set memory.provider <x>`, the config write-guard
  pitfall, and E2E-verifying a provider against the Hermes venv Python.
  Load when the user asks about memory budget/limits, "set up memory",
  "use honcho/holographic/mem0", consolidating MEMORY.md/USER.md, or any
  "which memory provider should I use" question.
---

# Hermes Memory Setup

Two memory layers, both optional-to-configure but the built-in one is always on:

1. **Built-in** — two text files, always injected into the system prompt.
2. **External provider** — ONE active at a time, additive on top of built-in.

## 1. Built-in memory (MEMORY.md / USER.md)

- Locations: `~/.hermes/memories/MEMORY.md` and `~/.hermes/memories/USER.md`.
- Hard char caps (config: `memory.memory_char_limit` / `memory.user_char_limit`):
  - MEMORY.md = 2200 chars (~800 tokens) — agent's environment/convention/lesson notes.
  - USER.md  = 1375 chars (~500 tokens) — user identity, style, standing rules.
- **Frozen snapshot**: injected once at session start, never changes mid-session.
  Writes persist to disk immediately but only appear next session. This preserves
  the prompt cache (don't try to force mid-session injection).
- **Over-limit behaviour**: when a write would exceed the cap, the `memory` tool
  returns an ERROR (no silent drop). Agent must consolidate/remove first, then retry.
  Symptom in practice: files sitting at 97–98% with no room to learn → consolidate.
- **Consolidation recipe**: split into clean roles, drop ephemeral "ACTIVE/project
  status" lines (those belong in `session_search`, which already stores every
  session in `~/.hermes/state.db` with FTS5 — free, no token cost). Keep only
  durable, always-relevant facts.
- **What to save**: preferences, env facts, corrections, conventions, resolved
  incidents, explicit requests. **Skip**: trivial/obvious, re-discoverable, raw
  data dumps, session-ephemera, anything already in SOUL.md/AGENTS.md.

## 2. External providers

`hermes memory status` shows built-in + active provider. Only ONE external
provider can be active; it runs ADDITIVELY (never replaces built-in).

Selection trade-offs (free-first, since G is cost-sensitive):

| Provider | Storage | Cost | Needs | Best for |
|---|---|---|---|---|
| **Holographic** | Local SQLite | Free, zero-dep | Nothing (numpy opt.) | Lightweight local fact store + algebraic recall. PICK THIS for zero-ops. |
| **Honcho** | Cloud / self-host | Paid / free-selfhost | API key OR Docker server | Dialectic user-modeling, cross-session "who is G" understanding. |
| **Hindsight** | Cloud / local PG | Paid / free-local | API key OR local Postgres | Knowledge graph + `reflect` cross-memory synthesis. |
| Mem0 | Cloud / self-host / OSS | Paid / free | API key or server | Server-side LLM auto-extraction. |
| OpenViking | Self-host server | Free (AGPL) | `openviking` + server | Filesystem knowledge hierarchy. |
| RetainDB | Cloud | $20/mo | API key | Teams already on RetainDB. |
| ByteRover | Local / cloud | Free / paid | `brv` CLI | Portable local-first tree. |
| Supermemory | Cloud | Paid | API key | Semantic recall + session graph. |

**Decision shortcut for G:**
- Zero-ops local fact memory → **Holographic** (install numpy, see pitfalls).
- Want the agent to genuinely understand you over time → **Honcho** (run a server;
  paid cloud or free self-hosted).
- Want relationship/knowledge-graph recall → **Hindsight** (local Postgres).

## 3. Setup commands

```bash
hermes memory setup        # interactive picker + per-provider config
hermes memory status       # confirm what's active
hermes memory off          # disable external provider (built-in stays)
# or non-interactive:
hermes config set memory.provider holographic
```

Holographic config block (reads `plugins.hermes-memory-store` from config.yaml):
```yaml
plugins:
  hermes-memory-store:
    db_path: $HERMES_HOME/memory_store.db   # default if omitted
    auto_extract: false                     # true = LLM call at session end (cost!)
    default_trust: 0.5
    min_trust_threshold: 0.3
```
DB lives at `~/.hermes/memory_store.db` — local only, no key, fully free.

## PITFALLS (hit and verified this session)

**P1 — Config write-guard.** The agent CANNOT directly edit `~/.hermes/config.yaml`
(the write tool refuses: "security-sensitive configuration"). Use the CLI instead,
which supports nested keys:
```bash
hermes config set memory.provider holographic
hermes config set plugins.hermes-memory-store.auto_extract false
```
Verify the block landed with `search_files`/grep on config.yaml (it's written after
the long `disabled:` list, not near `plugins:` top).

**P2 — Provider code runs on the Hermes VENV Python (3.11), not system python3.**
On this Mac `python3` is 3.9 and the plugins use 3.10+ syntax (`str | None`), so
importing a plugin under system python fails with `TypeError: unsupported operand`.
The real runtime is `/Users/<you>/.hermes/hermes-agent/venv/bin/python3` (3.11.x).
Always E2E-test plugins against THAT interpreter. See `references/verification.md`.

**P3 — Holographic HRR algebra needs numpy.** Without numpy, `probe`/`related`/
`reason`/`contradict` raise `RuntimeError("numpy is required...")` and the tool layer
returns a graceful error-JSON (no crash, but the headline feature is dead). FTS5
`add`/`search`/`list`/`fact_feedback` still work. Fix:
```bash
/Users/<you>/.hermes/hermes-agent/venv/bin/pip install "numpy>=1.24"
```
Then HRR vectors populate and the algebraic tools work.

**P4 — FTS5 is fine on macOS** (Apple's bundled SQLite includes it) — no action needed,
just don't assume it's missing.

## 5. Verification (do this before declaring success)

Never assume "status: available" means it works. Exercise the real plugin code
against the venv Python — full recipe in `references/verification.md`.
Expect: FTS5 search returns rows, `probe(entity)` returns that entity's facts,
`reason([e1,e2])` returns compositional results, and `hrr_vector` column is
non-null after a numpy install.

## 6. Incremental rollout (G's preferred cadence)

Report real settings → recommend tiers (0=free now, 1=local provider, 2=paid
cloud) → let G decide the next step. Don't auto-install a paid/cloud provider.
Consolidate built-in memory first (Tier 0) since it's at ~98% and rejects writes.
