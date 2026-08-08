---
name: hermes-model-routing
description: Choose and configure the right Hermes model for a given budget and use case — inspect current config, compare free models on the Nous provider, understand provider routing and free-tier degradation, pin subagent/delegation models, and plan a paid plan (Sonnet/Opus) for production solo-dev work. Load when the user asks "which model", "what models are free", "switch my model", "best model for coding", or is planning a subscription/budget for a build.
---

# Hermes Model Routing & Selection

## When to load
- User asks about available models, free models, or wants to switch/compare.
- User is planning a paid subscription or has a budget cap for a build.
- Questions about subagent model inheritance, delegation pinning, or provider routing.

## Inspect current state
```
hermes config get model          # shows {default, provider}
hermes config show               # full config incl. API keys, model, context compression
```
Pitfall: there is NO top-level `provider` key — provider lives inside the model object as `model.provider`. `hermes config get provider` errors with "Config key not set".

## Key mechanics (avoid common confusion)
- **Provider field + default model**: active model is `model.default`, served via `model.provider`. On G's setup: `tencent/hy3:free` via `nous`.
- **`nous` provider = OpenRouter-backed**: Nous Portal serves 250 models via OpenRouter. "Free" plan = free models only.
- **`:free` tiers are degraded by design**: hard rate limits (20 req/min, 50–1000/day) and deprioritized queueing. A free model is NOT the same quality as its paid sibling. Do NOT judge a model by headline param count when served free.
- **MoE marketing trap**: e.g. Nemotron 3 Ultra "550B" has only 55B ACTIVE params/token. Headline param count ≠ per-token compute. A smaller active model served well can beat a huge one served degraded.
- **Same identity, different brain**: Hermes persona/memory/tools are the wrapper; the underlying model changes how "smart" it feels. That's why one free model felt smarter than a "bigger" one.

## Free models on Nous (snapshot 2026-08-05 — VERIFY, free list drifts)
See references/nous-free-models-2026-08-05.md for the full snapshot + how it was obtained.
1. Tencent Hy3 (free) — tencent/hy3:free  [G's default]
2. Ling-3.0-flash (free) — inclusionai/ling-3.0-flash:free
3. StepFun Step 3.7 Flash — stepfun/step-3.7-flash:free
4. Poolside Laguna S 2.1 — poolside/laguna-s-2.1:free  [coding-specialized, larger tier]
5. Poolside Laguna XS 2.1 — poolside/laguna-xs-2.1:free [smallest, coding-leaning]
Pitfall: DeepSeek V4 Flash was removed from Nous free (404s reported). Don't assume a previously-free model is still free — re-check the live catalog.

### Ranking by use case
- General assistant / mixed work / tool+terminal agent loops: **Hy3 (free)** wins — proven, clean tool use.
- Coding agent specifically: **Poolside Laguna S 2.1 (free)** — coding-specialized, larger tier. Laguna XS weaker; Ling/Step unproven for agent loops.
- For a real verdict, run a live A/B (same prompt through Hy3, Ling, Step) rather than reasoning from tier labels.

## Subagent / delegation model
- Subagents inherit the parent model by default (so they'd run Hy3 unless changed).
- Pin globally via `delegation.model` / `delegation.provider` in config.yaml — but it is GLOBAL (all subagents), NOT per-call.
- For G: keep Hy3 as both default AND delegation model (mixed workload). Switch to a coding model per-task only as a manual call, not a default.

## Paid-plan strategy (solo dev, microSaaS / iOS, $50 cap)
- NO $30 Claude plan usable for agent work. Anthropic Pro ($20) is consumer chat with harsh limits. Real path: **Nous Plus $20/mo → $22 credits (+10% bonus)**, or pay-as-you-go top-ups.
- **Use Sonnet as the workhorse** ($1.60/$8 per 1M on Nous). A microSaaS MVP via an agent runs ~$15–70 total → $50/mo covers steady part-time solo dev to MVP and beyond.
- **Avoid Opus as default** ($12/$60 per 1M) — same build is $100–200, blows a $50 cap in a week. Reserve Opus for 1–2 hardest architecture calls only.
- **Hybrid**: keep Hy3 (free) for chat/exploration/boilerplate/refactors; spend Claude credits only on real production code.
- **Process beats model**: plan→tickets→TDD discipline prevents expensive loop-and-retry burns. Context compression (on by default) cuts waste.
- iOS: the $99/yr Apple Dev fee + Xcode/cert/App Store steps are separate from AI cost; the agent can't do all of it.
- Get Nous Plus rather than scattering top-ups — the 10% bonus is free money.

## Style note (G's preference)
When G asks for a quick ranking/decision ("just answer in short", "which is best"), LEAD with the short answer, then offer deeper analysis as a follow-up — don't dump full reasoning first. When G says "don't do anything yet" / "leave it" / "don't change anything", ANALYZE ONLY; do NOT run config set / model switches. Confirm before any config mutation.

## Verification
Always re-pull the live catalog before asserting the free list:
```
web_search "Nous Portal free models"
# and check hermes config show for current default/provider
```
