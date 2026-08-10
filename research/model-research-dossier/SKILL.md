---
name: model-research-dossier
description: "AI-model research dossier: specs, benchmarks, pricing."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, Models, Benchmarks, Pricing, Web]
    related_skills: [grounded-citations, product-teardown-research]
---

# Model Research Dossier

## When to Use

Use when researching an AI model (typically a new LLM release) and writing a cited
dossier for a comparison report, API/buying decision, or due diligence — "dossier on
<model>", "how does X compare to Y". Proven on the Tencent Hy3 dossier (2026-08:
preview/full split, HF card + GitHub + press release + OpenRouter + Reddit archive).

Class: research a model and write a cited markdown dossier that a parent agent can
fold into a comparison report. For closed API-only models, drop the weights section
and lean on OpenRouter/provider docs.

## Source hierarchy (primary first — fetch pages, never paraphrase snippets)

1. **HF model card** — specs table + all claims: `https://huggingface.co/<org>/<model>`.
   Also read the *sidebar* evaluation-results block (often lists 6-8 headline numbers
   that independently corroborate the chart) and the Inference Providers line.
2. **HF API metadata** — dates: `curl https://huggingface.co/api/models/<org>/<model>`
   → `createdAt`, `lastModified`, downloads, likes. `createdAt` is the *repo* date;
   the launch date comes from the press release or OpenRouter's "Released" field.
3. **GitHub repo** — README + dated "News" entries + commit dates; often carries
   instruct-benchmark tables (as images) the card links to.
4. **Official press release / corporate blog** — launch date, positioning quotes
   (e.g. "rivals flagship models with 2-5x parameters").
5. **OpenRouter page + API** — pricing, context, providers, latency/throughput,
   uptime, released date: `https://openrouter.ai/<org>/<model>` and
   `curl https://openrouter.ai/api/v1/models` (pricing is per-token decimals; ×1e6 = per 1M).
6. **Weight mirrors** (ModelScope, GitCode, CNB) — from the card's Model Links table.
7. **Community** — r/LocalLLaMA release threads via the archive API (below), X,
   Medium wrap-ups (corroborate 2-3 headline numbers; gather caveats).

## Workflow

1. **Batch the fetches**: card + GitHub + OpenRouter + press release in one
   `web_extract` call (≤5 URLs). Firecrawl rate-limits ~15 req/min — on
   "Rate Limit Exceeded" wait ~40s, or curl plain-text endpoints (HF API, OpenRouter
   API, GitHub raw) which bypass the scraper.
2. **Verify every spec from a fetched page.** Unverifiable → mark `[UNVERIFIED]`.
3. **Preview vs full split**: a preview and a full release are DIFFERENT releases —
   separate dates, sometimes different licenses. Document both; the full card usually
   states the delta ("feedback from N products, scaled-up post-training").
4. **Benchmark numbers in chart images → OCR them** with
   `scripts/ocr_vision_swift.swift` (macOS Swift + Vision framework, no installs; also
   the general fallback when vision_analyze is unavailable). Reconstruct tables by
   grouping OCR lines on y/x coordinates (details in the script header). **Cross-check
   at least one row against an independent number** (HF sidebar, secondary article)
   before trusting the rest of the extraction.
5. **Pricing: verify against the API list, not just the page.** `:free` promo variants
   get delisted after their window — absent from `/api/v1/models` = NOT currently
   servable, even if the page still renders "Free". Record the promo window
   ("free ~2 weeks from <date>"), the paid list price, and the discounted display price.
6. **Community reception**: pull top comments from the release threads verbatim
   (with scores); report criticism AND praise; prefer concrete complaints (multi-turn
   drift, tool-call failures, speed) over vibes.
7. **Write the dossier**: URL beside EVERY number; a vendor-benchmark caveat line
   ("* = vendor's own runs; reasoning effort set to max per chart notes"); a
   head-to-head table vs the comparison target if one was named; a sources list.

## Dossier format conventions (from the Hy3 run, feeds a comparison report)

- Lead with a **specs table**: total/active params, MoE config (experts, top-k),
  context, MTP, license, precision — every cell sourced.
- Separate sections per release (preview vs full) when both exist.
- Official-benchmark tables: label the extraction source (`[from official chart, OCR]`),
  carry the vendor-run caveat, mark corroborated cells (✓ + where).
- Pricing table: model id | in/1M | out/1M | cache read | context — plus provider list
  and any free path (product free tiers, HF Spaces, promos).
- Community caveats section with thread URLs.
- Flag discrepancies rather than hiding them: HF sidebar "Model size" (safetensors
  bytes, e.g. 299B) vs official "Total Parameters" (295B); OpenRouter "262K" == card's
  "256K" (262,144 tokens) — same window, don't present as conflict.

## Pitfalls

- **Reddit is not scrapable directly**: firecrawl says "site not supported", curl and
  the browser get 403/CAPTCHA. Use the arctic-shift archive API (see
  `references/source-endpoints.md`); pullpush may 502. Keep the reddit.com URLs in the
  dossier for human readers even though you read via the archive.
- **Don't trust search snippets for numbers** — extract the page. A snippet supports
  only what it literally says.
- **Vendor-run benchmark cells**: comparison-model scores on a vendor's chart are
  often the vendor's own runs (footnoted "*"). Say so; don't present them as
  third-party verified.
- **PIL can be broken in the active venv** (`cannot import name '_imaging'`) — use
  `sips` for image upscaling, not PIL.
- **No vision backend configured** (vision_analyze rejects images with
  "unknown variant `image_url`") — do not loop on it; go straight to the Swift OCR script.

## Support files

- `scripts/ocr_vision_swift.swift` — macOS Vision-framework OCR (chart/table image → text
  with y/x positions); usable for any image-OCR need.
- `references/source-endpoints.md` — exact endpoints & queries: HF card/API, OpenRouter
  models API, Reddit archive, GitHub raw, ModelScope/GitCode.
