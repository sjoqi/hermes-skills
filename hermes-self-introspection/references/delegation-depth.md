# Delegation tree depth — verified mechanics

Condensed from the official Hermes delegation docs
(hermes-agent.nousresearch.com/docs/user-guide/features/delegation + /configuration),
cross-checked against the GitHub source. Verified in-session: `hermes config set
delegation.max_spawn_depth 2` returned `2`.

## The default is one tier — and it is a *default*, not a lock
- `delegation.max_spawn_depth` defaults to **1** = flat: parent (depth 0) spawns
  children (depth 1); those children **cannot** delegate further.
- It is **changeable**. The feature page says "no upper ceiling — cost is the
  practical limit"; the config-reference page says "1-3, clamped". Both agree the
  default is 1 and it is not hard-fixed. `2` is safe and supported.

## Two-tier needs TWO things, not one
1. `delegation.max_spawn_depth: 2` (or higher) in config.yaml.
2. The child must be spawned `role="orchestrator"`.
- At the default depth=1, `role="orchestrator"` is a **no-op** — the depth bump is
  what makes the role meaningful. Spawning an orchestrator at depth 1 changes nothing.
- `delegation.orchestrator_enabled` (default **true**) is a global kill switch:
  set `false` and *every* child is forced to `leaf` regardless of role or depth.

## Cost math (why default is 1)
- `max_spawn_depth: 3` × `max_concurrent_children: 3` ⇒ up to **3×3×3 = 27**
  concurrent leaf agents. Each extra level multiplies spend — raise intentionally.
- `max_concurrent_children` is a per-parent cap (floor 1, no hard ceiling, default 3);
  two parents can each run `max_children` workers concurrently.

## Subagent context is isolated (critical for hand-offs)
- Every child starts with a **completely fresh conversation** — zero parent history.
  The parent MUST pass all needed context in `goal`/`context` or the child fails.
- Blocked for leaf (default): `delegate_task`, `clarify`, `memory`, `send_message`,
  `cronjob`. `orchestrator` children retain `delegate_task` only; both roles keep
  `execute_code`.
- Children inherit the parent model unless `delegation.model` / `provider` override.

## Safe edit (Hermes hard invariant)
- NEVER hand-edit `~/.hermes/config.yaml` — a stray indent corrupts it and breaks
  the live gateway.
- Set depth via the CLI: `hermes config set delegation.max_spawn_depth 2`, then
  `hermes config get delegation.max_spawn_depth` to confirm.

## "Capped at N" is usually the model, not Hermes
- When a `delegate_task` batch runs fewer children than asked, the real caps are
  only: the `Too many tasks:` tool_error and the `Truncated N excess delegate_task`
  WARNING line (see bundled `hermes-agent` skill →
  `references/delegate-task-concurrency-diagnosis.md`). The
  `max_concurrent_children>N` startup cost-warning is just a log, NOT a cap.
- Reasoning models often trim a 13/15-task batch to ~5-10 and narrate it as "the
  runtime caps at N" — a face-saving misattribution. Push back on the model (or
  build the `tasks` list in `execute_code`) rather than changing config.
