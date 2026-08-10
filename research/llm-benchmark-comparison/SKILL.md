---
name: llm-benchmark-comparison
description: Compare AI models on independent benchmarks; verify claims.
version: 1.0.0
author: hermes-curator
license: CC-BY-4.0
metadata:
  hermes:
    tags: [benchmarks, llm, research, vendor-claims, artificial-analysis, leaderboards]
    related_skills: [grounded-citations, market-research-scrape-synthesis, product-teardown-research]
---

# LLM Benchmark Comparison Research

## When to Use

Use when the user asks to compare two AI models ("X vs Y"), verify a model's benchmark claims against independent measurement, or collect third-party model scores with sources + dates. Do NOT use for running your own benchmark harness (that is mlops/evaluation territory) or for market-demand research (that is market-research-scrape-synthesis).

Goal: produce a synthesis of **independent, third-party** measurements comparing two (or more) AI models, with a URL + measurement date for every number, so vendor claims can be tested rather than repeated.

## Workflow

1. **Anchor model facts first** (params, active params, release dates, context, license, reasoning modes) from vendor pages AND the OpenRouter registry:
   `curl -s https://openrouter.ai/api/v1/models` → JSON with per-model `pricing`, `context_length`, `architecture`, `reasoning.supported_efforts`, `reasoning.default_effort`, `canonical_slug`, and `created` (unix ts). This endpoint is server-rendered JSON and always beats scraping model pages. Note `created` timestamps ↔ release dates; check for separate `-preview` vs final slugs (crucial — preview ≠ final model).
2. **Independent labs first** (their numbers are the deliverable):
   - **Artificial Analysis** (artificialanalysis.ai) — JS-only site; data is embedded in the HTML as Next.js RSC flight payload. Extract with curl + Python (see `references/artificial-analysis-extraction.md`). Has direct comparison pages: `/models/comparisons/<slug-a>-vs-<slug-b>`.
   - **NIST CAISI** (nist.gov/news-events/news/...) — server-rendered, plain `web_extract` works. Only evaluates a subset of models; searching for a model that was NOT evaluated is itself a finding ("no independent government re-measurement exists").
   - **LMArena / arena.ai** (`https://arena.ai/leaderboard/text`) — server-rendered enough for `web_extract`; gives Elo ± CI, rank, vote count, pricing, context. Also on HuggingFace as `lmarena-ai/leaderboard-dataset` (different aggregation scope than the arena.ai table — don't mix).
   - **OpenRouter model pages** — client-rendered: plain curl returns no arena data. Use `web_extract` (firecrawl renders JS) or the browser. The "Models Arena" tab on model pages = **Design Arena** (designarena.ai) + Agents Arena, NOT a text Elo.
3. **Aggregators second, always flagged self-reported**: llm-stats.com (states "X self-reported results" on every leaderboard), benchlm.ai, pricepertoken.com, Onyx — good for finding which models share a leaderboard, never for "independent" scores.
4. **Community/press**: Reddit threads are captcha-blocked to scrapers (see Pitfalls for the fallback); AINews (latent.space), CodingFleet-style comparison blogs, and OpenLM Arena+ (openlm.ai/chatbot-arena, LLM-as-judge Elo) are useful secondary signals — check their own methodology notes (many blogs explicitly say "Hy3 scores from vendor-reported benchmarks").
5. **Write up**: markdown comparison table with a **source+date column per row**, vendor-published numbers in separate flagged rows/sections, anything unverifiable as `[UNVERIFIED]`, conflicting sources presented side-by-side with both URLs. Deliver the synthesis to a file in the workspace, not just chat.

## Methodology caveats checklist (the heart of the deliverable — always document)

1. **Vendor vs independent separation.** llm-stats/SWE-bench leaderboards are self-reported; CodingFleet-style head-to-heads often mix vendor Hy3 numbers with independent V4 Pro numbers. Independent re-runs routinely land BELOW vendor claims (e.g. CAISI SWE-bench 74% vs self-reported 80.6%; MathArena Apex 28.1% vs 38.3%). Every independent re-run of a vendor number is a data point about claim inflation.
2. **Reasoning-effort settings swing scores more than the model gap.** Check: does the source page title say "(Reasoning, Max Effort)"? What are the API's `default_effort` vs `supported_efforts`? What reasoning-token budget did the evaluator configure (AA exposes `reasoningTokens` per model)? Comparing model A at max effort vs model B at default/no-think is not a fair comparison.
3. **Serving conditions**: free-tier endpoint vs paid API vs local weights (quantization) changes speed and quality; vote counts are a quality proxy for arena data (13× fewer votes = much noisier Elo).
4. **Measurement date vs model update dates**: preview → final releases (e.g. Hy3-preview 2026-04 vs Hy3 2026-07) invalidate early data; a model that shipped in April will look worse in July leaderboards than a July release regardless of true capability.

## Pitfalls

- **AA ranks ("#6 / 101") are rendered client-side** — not in the flight payload. Get ranks via the browser, or from the page's rendered snapshot after `browser_navigate`.
- **Firecrawl rate limits** (~12–20 req/min): on `Rate Limit Exceeded` the error contains a reset timestamp — wait it out (~30–60s) or switch to curl; batch ≤2–3 URLs per `web_extract` call when probing new sites.
- **Reddit scraping fallback**: direct `.json`, `old.reddit.com`, pullpush (often 502), and redlib mirrors all fail (captcha / 403). Working pattern: `web_search` with the thread URL/title → search snippets contain the full OP text and engagement numbers; extract those and mark comment-level detail `[UNVERIFIED]`.
- **Next.js sites that aren't AA**: the flight-payload trick (`self.__next_f.push`) generalizes to any Next.js app (check the HTML for it before assuming you need a browser). OpenRouter pages embed almost nothing — go to their API instead.
- **AA params can differ from vendor claims** (299B vs 295B) and AA pricing can differ from OpenRouter pricing — cite the specific source of each number.

## Support files

- `references/artificial-analysis-extraction.md` — Python recipe for pulling model JSON out of AA pages + AA field map + URL patterns.
- `references/source-register.md` — benchmark-source map: URL, access method, data available, caveats.
