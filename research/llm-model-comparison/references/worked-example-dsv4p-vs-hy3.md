# Worked example: DeepSeek V4 Pro vs Tencent Hy3 (snapshot 2026-08-10)

Dated snapshot illustrating the comparison pattern. Model landscape moves fast — re-verify
everything before reuse. Session artifacts live in `~/hermes-home/research/model-compare/`
(three dossiers + independent synthesis + raw live-test JSON) if a future session wants
the full detail.

## Specs (verified from primary sources)

| | DeepSeek V4 Pro | Tencent Hy3 |
|---|---|---|
| Release | 2026-04-24; still "Preview" as of 2026-08-10 | preview 2026-04-23; full 2026-07-06 |
| Params | 1.6T total / 49B active | 295B total / 21B active (+3.8B MTP) |
| Context | 1M (384K max out) | 256K (262,144) |
| License | MIT, open weights (FP4+FP8 quantized) | Apache 2.0 full / community license preview |
| Reasoning | thinking/non-thinking; high (default) / xhigh (max) | no_think (default) / low / high |
| API price /1M | $0.435 in / $0.87 out (official; ~75% cut from May) | $0.132 in / $0.528 out (OpenRouter `tencent/hy3`) |

## Independent numbers (all fetched 2026-08-10)

- **AA Intelligence Index**: 45 (#6/101) vs 42 (#12/101) — V4 Pro +3.
- **LMArena text Elo**: 1457±4 (#50, 51k votes) vs 1453±10 (#57, 3.9k votes) — near-tie; Hy3's CI overlaps.
- **AA GPQA Diamond**: 88.8 vs 89.7 (Hy3 slightly ahead). **AA Terminal-Bench 2.1**: 64.0 vs 64.4 (≈tie).
- **AA Agentic Index**: 37.8 vs 31.4 (V4 Pro +6.4). HLE: 37.5 vs 33.5 (V4 Pro).
- **NIST CAISI** (V4 Pro only, May 2026): ~8 months behind frontier; IRT Elo 800 vs GPT-5.5 1260;
  SWE-bench Verified 74% (vs self-reported 80.6); held-out PortBench 44%, ARC-AGI-2 semi-private 46%.
- **CodingFleet aggregator** (Jul 2026): Hy3 wins 12/18 — but explicitly built on vendor-reported
  Hy3 numbers; treat as claims, not measurement.

## Lessons this example embodies

- A 2.3× active-param gap (49B vs 21B) buys only ~1–3 independent index points → the community
  "intelligence density" critique of V4 Pro. Cost-efficiency favors Hy3 ($0.13/$0.53 vs $0.435/$0.87).
- Highest-trust single source: NIST CAISI (`nist.gov/news-events` CAISI evaluations) — pre-committed
  benchmark suite, held-out sets, developer-recommended settings, reproduces vendor GPQA result.
- Vendor self-reports were inflated on the DeepSeek side (CAISI gap); Hy3's full-release numbers were
  partially corroborated by the HF-card sidebar but had no independent government re-run — asymmetry
  matters for the verdict.
- **Live-test verdict FLIPPED between identical runs (2026-08-10):** run 1 Hy3 18/18 vs DS 17/18
  (DS hit the 4096-token cap with empty content on the trailing-zeros question, twice); same-day
  re-run DS 18/18 vs Hy3 17/18 (Hy3 hit the same cap, DS answered `5` cleanly). Corrected verdict:
  statistical tie on capability; the budget-exhaustion failure is stochastic, not a model trait.
  Lesson: never conclude on a 1-question margin from a single run — the ~$0.03 re-run is mandatory.

## Reusable API test setup (what worked)

- Model-id discovery before testing: `curl -s https://api.deepseek.com/models` and
  `curl -s https://openrouter.ai/api/v1/models` — never assume the slug.
- Keys: `set -a; source ~/.hermes/.env; set +a`; grep key NAMES only for discovery.
- 12 self-written questions, temp 0, max_tokens 4096, raw JSON saved per question;
  scoring: run returned code locally, strict numeric checks for math.
- Cost reported from usage fields at published per-1M prices (kept under ~$0.30 total).
