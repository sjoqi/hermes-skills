# Nous Portal Free Models — Snapshot 2026-08-05

## How this was obtained
- `web_extract` of https://portal.nousresearch.com/ → full model list (200+ models, OpenRouter-backed).
- Filtered for `$0.00/1M` pricing (Free plan = "free models only"). Matches via regex `\$(0\.00|0\.00)/1M` and `(free)` label.
- Cross-checked `hermes config show` → default `tencent/hy3:free`, provider `nous`.

## Confirmed FREE on Nous (this date)
| Model | OpenRouter ID | Notes |
|---|---|---|
| Tencent Hy3 (free) | tencent/hy3:free | G's default. General all-rounder, clean tool/terminal use. |
| Ling-3.0-flash (free) | inclusionai/ling-3.0-flash:free | Recent Alibaba-family flash model. |
| StepFun Step 3.7 Flash | stepfun/step-3.7-flash:free | Chinese model, flash tier. |
| Poolside Laguna S 2.1 | poolside/laguna-s-2.1:free | Coding-specialized, larger tier. |
| Poolside Laguna XS 2.1 | poolside/laguna-xs-2.1:free | Coding-leaning, smallest tier. |

## NOT free (drift warnings)
- DeepSeek V4 Flash: previously free, removed from Nous (`deepseek/deepseek-v4-flash:free` → HTTP 404 per Reddit r/hermesagent). Now shows at $0.01/1M, not free.
- NVIDIA Nemotron 3 Ultra (free): `nvidia/nemotron-3-ultra-550b-a55b:free` — MoE, 550B total / 55B ACTIVE. Free tier, deprioritized. Was judged "dumber" than Hy3 in practice.

## Paid pricing reference (Nous, $/1M, in/out)
- Sonnet (workhorse): ~$1.60 / $8.00
- Opus: ~$12.00 / $60.00  ← avoid as default
- DeepSeek V4 Flash 0731: $0.01 / $0.02 (cheap non-free option)
- GLM 4.7 Flash: $0.05 / $0.32

## MicroSaaS/iOS budget math ($50 cap)
- Sonnet build to MVP: ~$15–70 total. $50/mo = sustainable part-time solo dev.
- Opus build to MVP: ~$100–200. Exceeds $50/mo quickly.
- Nous Plus $20/mo → $22 credits (+10% bonus) is the realistic entry subscription.

## Caveat
Free list drifts. Re-pull live catalog before relying on this for a model switch.
