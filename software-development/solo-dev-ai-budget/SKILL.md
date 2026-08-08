---
name: solo-dev-ai-budget
description: Choose cost-effective AI coding tools, subscriptions, and model routing for a budget-capped solo developer using agent/terminal workflows (Hermes). Covers credits-vs-subscription trade-offs, message-cap vs token-meter, and the hybrid free-chat + paid-code pattern. Use when the user asks which AI plan/tool to buy, how to budget an AI-assisted build, or how to route models for cost.
---

# Solo Dev AI Budget & Tooling

## When to use
- User is a solo/small-team dev planning or running an AI-assisted build and asks: which plan, which tool, how much will it cost, credits or subscription?
- User wants to maximize AI output within a hard monthly budget (e.g. $50 cap).
- User runs an agent/terminal workflow (Hermes) rather than an IDE-first tool.

## Core decision framework
1. **Billing model beats brand.** Compare HOW you pay, not which logo:
   - Token/credit-based (Nous, OpenRouter, Anthropic API): scales with efficiency; prompt caching (0.1x input) slashes agent-loop cost.
   - Message-capped subscription (Claude Pro ~45 msgs / 5h rolling): each agent tool call/file read counts as a message. THROTTLES agentic coding hard. Bad for builds.
   - Flat Max subscription (Claude Max 5x $100 / 20x $200): cheaper than raw API for heavy users, but usually over a $50 cap.
2. **Hybrid routing is the budget move.** Free model (Hy3 / DeepSeek V4 Flash) for chat/explore/boilerplate; premium (Sonnet) only for the hard ~10% (architecture, gnarly debug). Bulk code generation → a cheap open-weight coder. Don't route everything through the paid model.
3. **Bulk code → cheap open-weight coder.** DeepSeek V4 Pro is ~7x cheaper than Sonnet ($0.435/$0.87 vs $3/$15 per 1M). GLM-5.2 = strongest open-weight for long coding agents. Route via OpenCode Go ($5 first mo, then $10/mo flat, curated models, generous limits) OR OpenRouter BYO (pay-as-you-go, no sub). Flat beats token-metered anxiety for budget solo devs.
4. **Single pool, single bill.** Prefer one credit account (Nous Portal) over scattering keys. The 10% subscription bonus (Nous Plus $20→$22) beats a 1:1 top-up.
5. **Discipline = cost control.** Plan→spec→tickets→TDD prevents expensive retry storms. Bound max_turns. Don't subagent everything (each re-sends full context).
6. **Hermes (generalist agent) vs OpenCode (dedicated code agent).** For the build loop itself, a purpose-built code-agent (OpenCode/Claude Code) has tighter ergonomics (Plan mode, /undo, worktree isolation, session resilience). Keep Hermes as the brain/orchestrator (research, planning, ticketing, memory, messaging); put the code engine in OpenCode. OpenCode-free models (DeepSeek V4 Flash, GLM-5.2) mean near-$0 code generation. OpenCode is NOT bundled in Hermes — install separately (`brew install opencode`); Hermes can shell into it but no native bridge.

## Claude Pro myth (correct this if user believes it)
Claude Pro ($20/mo) is NOT just "consumer chat useless for agents." It DOES power Claude Code, but via a ~45-message / 5-hour rolling cap shared across chat + Code. For agentic building that cap is the bottleneck, not a missing feature. Max 5x ($100) clears it but breaks a $50 budget. So for budget builds: token/credit model (Nous/OpenRouter) > Claude Pro.

## Cost levers (biggest first)
1. Prompt caching — cached input = 0.1x. In agent loops the repo context repeats every turn; caching ~halves cost.
2. Hybrid routing — free model eats the cheap 70% of tokens.
3. Bound max_turns (stops runaway loops).
4. Reserve subagents for genuinely parallel independent work only.
- Don't recommend IDE-first tools (Cursor) as default for a terminal/agent workflow user; different paradigm, not better for their setup.
- VERIFY provider + model ID from source BEFORE editing config.yaml. Native Hermes providers: `nous`, `openrouter`, `opencode-go` (needs `OPENCODE_GO_API_KEY` in .env), `anthropic`. Under `opencode-go` the model ID is the bare name (e.g. `deepseek-v4-pro`), NOT `openrouter/deepseek-v4-pro`. Guessing a provider with no key breaks the user's working session — leave config untouched and hand the user the block + .env line to apply after they subscribe.
- Reddit direct scrape often hits "Prove your humanity" CAPTCHA; use web_search for thread leads or old.reddit.com.

## Reference
- `references/pricing-2026.md` — condensed 2026 rate tables (Sonnet, DeepSeek V4 Pro across providers, OpenCode Go plan, Nous free models).
- `references/tools-comparison.md` — Claude Code vs Cursor vs OpenCode vs Copilot solo-dev consensus + Hermes-as-orchestrator pattern.

## Pitfalls
- Don't "all-in" paid credits — you pay premium rate for work a free model does fine and lose buffer against debug-loop spikes.
- Never claim "$0 cost" when a subscription floor exists. Hybrid-on-Hy3 means $0 extra tokens, but the $20 Nous / $10 OpenCode Go floor is real. State the floor explicitly — user will catch the omission.
- Don't assume a $20 "Claude plan" includes Sonnet for agents — Claude Pro is message-capped; true agent capacity needs Max or API credits.
- OpenRouter intro $2/$10 Sonnet rate expired Aug 31 2026; afterward ~$3/$15 like Nous — then Nous's 10% bonus wins.
- Don't recommend IDE-first tools (Cursor) as default for a terminal/agent workflow user; different paradigm, not better for their setup.
