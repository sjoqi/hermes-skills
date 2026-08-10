---
name: hermes-self-introspection
description: "When uncertain about Hermes's own config, capability, routing, memory, tools, skills, delegation limits, desktop UI, or cron — introspect FIRST via real `hermes` subcommands before answering from assumption. Prevents overguessing and self-inflicted breakage. Mirror of the delegation diagnosis ethos."
version: 1.0.0
author: G + Hermes
license: MIT
tags: [hermes, self-introspection, introspection, configuration, debugging, capability, safe-edits]
---

# Hermes Self-Introspection

**Core rule:** If you are unsure about Hermes's own behavior, configuration, or
capability, **read the running state before you assert anything.** Hermes ships
a full self-inspection toolkit as `hermes` subcommands. The cap you think you
hit is often the *model* rationalising a self-limit, not Hermes. Verify first.

This skill mirrors the proven pattern in `references/delegate-task-concurrency-diagnosis.md`
(located in the `hermes-agent` skill): every "wall" has a recipe of **read-only**
commands plus the **common wrong-guess to avoid**.

## Hard safety invariant (do NOT tune yourself into a break)

- **Never hand-edit `~/.hermes/config.yaml`.** A stray indent corrupts it and
  breaks the live gateway. Always use `hermes config set KEY VAL` (verify with
  `hermes config get KEY`). The one exception the tooling allows is
  `hermes config edit` (opens the file in a managed editor) — prefer `set`/`get`.
- **Prompt caching is sacred.** Do not mutate past context, swap toolsets, or
  rebuild the system prompt mid-conversation. The only allowed exception is
  context compression.
- **The core is a narrow waist.** Capability lives at the edges (skills, CLI
  commands, plugins) — prefer extending those over assuming a missing core tool.
- Secrets go ONLY in the env file (`hermes config env-path`); never in config.yaml.

## Per-wall recipes

### Wall: "What is the current value of setting X?" / "Where does X live?"
```bash
hermes config get <key>          # resolved value (ground truth)
hermes config show               # full resolved config
hermes config path               # config file path
hermes config env-path           # secrets env file path
hermes config check              # missing/outdated config
```
**Wrong-guess to avoid:** Don't assert a default from memory — `get` it. Defaults
change between versions. The official `delegation` keys: `max_iterations`,
`max_concurrent_children` (floor 1, no hard ceiling, default 3), `max_spawn_depth`
(default 1 = flat; raise to 2 for two-tier, which ALSO requires the child be
`role="orchestrator"`), `orchestrator_enabled` (default true; false = all leaf),
`model`/`provider`/`base_url`/`api_key` overrides (empty = inherit parent).

### Wall: "Is the agent set up correctly / healthy?"
```bash
hermes doctor                    # static health/consistency check
hermes doctor --live             # + real bounded network probes per backend
hermes status --all --deep       # component status (redacted for sharing)
hermes dump                      # copy-pasteable setup summary for support
```
**Wrong-guess to avoid:** Don't guess at a diagnosis; `doctor` lists concrete
advisories with IDs (`hermes doctor --ack <ID>` to clear).

### Wall: "What tools / skills do I actually have right now?"
```bash
hermes tools list                # all tools + enabled/disabled state
hermes tools --summary           # enabled per platform
hermes skills                    # installed/loadable skills
```
**Wrong-guess to avoid:** Tool/toolset availability is per-platform and
configurable — `list` it, don't assume. A tool you "should" have may be disabled
on this platform.

### Wall: "Did something actually fire, or did the model self-limit?"
```bash
hermes logs -n 100 --level WARNING --component <gateway|agent|tools|cli|cron|...>
hermes logs --session <session_id> --since 1h
hermes logs gui                  # desktop app log
hermes logs list                 # available log files
```
**Wrong-guess to avoid:** The `delegate_task` "capped at N" is usually the model
trimming a batch, not Hermes. See `delegate-task-concurrency-diagnosis.md`
(hermes-agent skill) — actual caps are the `Too many tasks:` tool_error and the
`Truncated N excess delegate_task` WARNING line. The `max_concurrent_children>N`
cost-warning is just a log, NOT a cap.

### Wall: "Why am I on this model / provider? Routing?"
```bash
hermes model                     # current model + provider
hermes status                    # provider/routing posture
hermes fallback                  # configured fallback providers
```
**Wrong-guess to avoid:** Don't assume the model from the persona; `model` is
the source of truth. Free vs paid routing (`nous` provider) is config-driven.

### Wall: "How big is my context / what's in my memory?"
```bash
hermes prompt-size               # system prompt + skills + memory + tool-schema budget (offline)
hermes journey                   # Memory Graph / Star Map (learned skills + memories over time)
hermes journey list              # node ids for delete/edit
```
**Note:** `hermes memory-graph` is aliased to `journey`. `hermes memory` manages
*external* memory providers only; built-in memory (MEMORY.md/USER.md) is always
active and read directly. To inspect/trim built-in memory, read MEMORY.md/USER.md
or use `jourmes`/`journey`.

### Wall: "What's my cost / usage trend?"
```bash
hermes insights --days 30        # token usage, cost, tool patterns, activity
```

### Wall: "Cron / scheduled jobs — what's running?"
```bash
hermes cron --help               # list / create / run / update / remove
hermes cron list                 # current jobs
```
**Wrong-guess to avoid:** Don't guess job IDs — `cron list` first. Never let a
cron run recursively schedule more cron jobs.

### Wall: "Desktop UI changed / something missing in the app?"
```bash
hermes desktop                   # launch (or inspect) the native app
hermes logs gui                  # desktop/electron logs
# Load skill: skill_view(name='inspecting-hermes-desktop-dom') for live CDP DOM read
```
**Wrong-guess to avoid:** A "missing" UI element is usually a config-default
change (e.g. status bar became opt-in), not a deletion. Check config +
current-version behavior before concluding it's gone. CDP on packaged builds is
often closed; rely on config + bundle-strings + logs.

## Diagnostic mindset (the discipline)

1. **Name the wall** (config? capability? routing? memory? UI? cron?).
2. **Run the read-only recipe** for that wall. Real output beats recollection.
3. **Only then assert** — and label it "verified" vs "from training memory."
4. **To change config:** `hermes config set KEY VAL` + `hermes config get KEY`
   to confirm. Never edit the YAML by hand.
5. **When stuck across walls:** `hermes dump` + `hermes debug share --local`
   produce a shareable, redacted report — hand that to the user or a human
   maintainer rather than guessing further.

## Pitfalls / gotchas
- `hermes config edit` opens the YAML in an editor — fine, but `set`/`get` is
  safer and avoids indentation breakage.
- The `delegate` cost-warning log line prints at startup when value > 10; it is
  NOT a cap. Only `Too many tasks` and `Truncated...` indicate real capping.
- `hermes doctor --live` makes real network calls — use when static checks are
  insufficient, not by default.
- `hermes logs` filters by `--component` and `--session`; scope before dumping
  all lines.
- Memory is capacity-limited (built-in store ~2.2k chars). Keep memory entries
  as short *pointers*; put detail in skills like this one.

## Knowledge bank (references/)
- `references/delegation-depth.md` — verified `max_spawn_depth` / two-tier mechanics,
  the "depth>=2 AND role=orchestrator" gotcha, cost math, and safe `hermes config set`.
  Load it when a delegation-depth or "why can't my subagent spawn?" question arises.
