# Coding Tools — Solo-Dev Consensus (2026)

Condensed from Reddit threads + aggregator roundups (dated 2026). Re-verify before acting.

## The players
- **Claude Code** (Anthropic): terminal agent, Claude-only. Best for complex refactoring / multi-file / architecture. /goal autonomy, Agent View fleet, /undo checkpointing. Plans: Pro $20 (throttles via ~45 msg/5h cap), Max 5x $100, Max 20x $200. Heavy users MUST take Max — raw API for equivalent tokens = $600-1500/mo.
- **Cursor**: VS Code fork, AI-native IDE. Best daily editor experience, visible diffs, Composer mode. Pro $20 (500 premium req/mo, hits caps on heavy use), Pro+ $60, Ultra $200. "Auto mode" routes to best model without burning the pool.
- **OpenCode** (SST/Anomaly, MIT, Go): open-source terminal code agent, 75+ providers, BYOK. Free software. Curated hosted models via **Go** ($5 first mo, then $10/mo flat) or **Zen** (PAYG). NOT bundled in Hermes — install separately (`brew install opencode`); Hermes shells into it. Best open-weight coders: GLM-5.2 (long-horizon), DeepSeek V4 Pro, Qwen3-Coder, Kimi K2.6.
- **GitHub Copilot**: budget pick $10/mo (Pro). Completions free; agent mode + premium models draw from AI Credits pool (switched to token billing June 1 2026). Weaker autonomous agent than Claude Code.
- **ChatGPT Plus + OpenCode Go**: Reddit-blessed budget combo — GPT models as reliable workhorse, flat $20, no token-meter anxiety.

## Reddit consensus (solo dev)
- Route by task, don't chase one "best" tool.
- Claude Code = hard repo work; Cursor = daily editing; Copilot = budget/GitHub-ecosystem.
- Cheap path that recurs: ChatGPT Plus + OpenCode Go (GPT reliable, flat cost).
- Most experienced solo devs run a hybrid, not a single tool.

## Hermes (this agent) vs dedicated code agents
- Hermes = generalist agent OS: coding is one capability among research, browser, cron, messaging, memory, delegation. Strong orchestrator, weak at the dedicated code-loop ergonomics (no native Plan mode, /undo on edits, worktree isolation, session resilience on disconnect).
- OpenCode/Claude Code = purpose-built code engine: Plan/Build modes, /undo /redo, worktree isolation, background subagents, server survives SSH drops.
- Best setup (budget no concern): OpenCode or Claude Code as code engine + Hermes as brain/orchestrator.
- For budget solo dev: hybrid routing — Hermes on Hy3 free (plan/research/ticket/orchestrate) + DeepSeek V4 Pro via OpenCode Go ($10 flat) for bulk code + Sonnet (Nous) reserve for hard 10%. Fits under $50/mo.
