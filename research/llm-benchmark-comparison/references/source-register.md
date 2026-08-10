# Benchmark source register (LLM model comparison)

Access methods verified 2026-08. Every number in a deliverable needs: URL + measurement date + who measured it (independent / vendor / self-reported aggregator).

| Source | URL pattern | Access method | What you get | Caveats |
|---|---|---|---|---|
| Artificial Analysis | artificialanalysis.ai/models/<slug>; /models/comparisons/<a>-vs-<b> | curl + flight-payload parse (see artificial-analysis-extraction.md) | Intelligence Index, per-eval scores (GPQA, HLE, SciCode, Terminal-Bench, CritPt, GDPval, LCR, Omniscience), agentic index, speed, pricing, reasoning-token budget | Ranks need browser; index version changes (v4.x); effort config per model may differ |
| NIST CAISI | nist.gov/news-events/news/2026/05/caisi-evaluation-... | web_extract (server-rendered) | Gov-run eval: benchmark table per model, IRT Elo, vendor-vs-CAISI gap analysis, held-out benchmarks (ARC-AGI-2 semi-private, PortBench) | Only a handful of models evaluated; "not evaluated" is itself a finding |
| LMArena (arena.ai) | arena.ai/leaderboard/text | web_extract | Elo ± CI, rank, vote count, price, context, leaderboard publish date | Vote counts vary hugely (noise proxy); serves default effort, not max; HF dataset (lmarena-ai/leaderboard-dataset) uses different aggregation — don't mix ranks |
| OpenRouter registry | openrouter.ai/api/v1/models | curl (JSON API) | Per-model pricing, context, reasoning efforts + default, canonical slugs, created timestamps, architecture | Registry only — no benchmark scores |
| OpenRouter model page | openrouter.ai/deepseek/<slug>; /tencent/<slug> | web_extract (firecrawl renders JS) or browser; curl gives nothing | "Models Arena" = Design Arena category Elos (3D/Code/UI/Website...) + Agents Arena; provider throughput/latency; apps usage | Arena section varies by model (some lack Agents Arena rows); free-tier variant pages may omit arena section |
| llm-stats | llm-stats.com/benchmarks/<bench>; /models/<slug> | web_extract | Leaderboards with rank + score + price; model cards | ALL results are self-reported (page states "X self-reported results") — aggregator, never "independent" |
| OpenLM Arena+ | openlm.ai/chatbot-arena/ | web_extract | LLM-as-judge Elo, coding Elo, AAII, MMLU-Pro per model | Undated on page; rows may point at preview weights |
| CodingFleet-style blogs | codingfleet.com/blog/... | web_extract | Head-to-head tables across many benchmarks | Often mix vendor-reported scores for one side with independent for the other — read the methodology footer |
| MathArena | matharena.ai/models/<slug> | web_extract | Independent math-bench re-runs (e.g. V4 Pro Apex 28.1% vs self-reported 38.3%) | Coverage is math-only |
| Reddit r/LocalLLaMA | reddit.com/r/LocalLLaMA/comments/<id>/... | web_search snippets only (direct scrape captcha-blocked) | OP text, upvotes/comments count, thread titles | Comment-level detail unverifiable → mark [UNVERIFIED] |
| AINews (latent.space) | latent.space/p/ainews-... | web_extract | Weekly recap of model releases with AA scores + community reaction | Secondary source; verify against primary |
| HuggingFace model cards | huggingface.co/<org>/<model> | web_extract | Vendor benchmark tables (self-reported) | Vendor source — flag as such |

## Quick access decisions

- Need model specs/pricing/reasoning modes fast? → OpenRouter `/api/v1/models`.
- Need independent intelligence scores? → Artificial Analysis (flight payload) + CAISI + arena.ai.
- Need to know who shares a leaderboard? → llm-stats.
- Need community sentiment? → Reddit via search snippets, AINews.
- Rate-limited on firecrawl? → error carries a reset timestamp; wait ~30–60s, switch to curl/browser, or shrink batch to ≤2–3 URLs.
