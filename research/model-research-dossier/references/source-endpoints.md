# Model-research source endpoints

All verified working 2026-08 during the Tencent Hy3 dossier run.

## Hugging Face
- Model card: `https://huggingface.co/<org>/<model>` — specs table, claims, Model
  Links, license, Inference Providers, sidebar eval results.
- Metadata (repo createdAt/lastModified, downloads, likes):
  `curl -s https://huggingface.co/api/models/<org>/<model>`
- Card assets (benchmark charts, logos):
  `https://huggingface.co/<org>/<model>/resolve/main/assets/<file>.png`
- Sidebar evaluation-results block independently corroborates several headline
  numbers (e.g. Hy3: SWE-bench Verified 78, GPQA Diamond 90.4, HLE 53.2).

## OpenRouter
- Full models list (pricing per-token decimals ×1e6 = per 1M tokens, context_length):
  `curl -s https://openrouter.ai/api/v1/models`
- Model page: `https://openrouter.ai/<org>/<model>` — list price, discounted display
  price, providers table, latency/throughput/uptime, tool-call error rates, "Released"
  date, top client apps.
- **Servability check**: only ids present in `/api/v1/models` are servable. `:free`
  promo variants disappear after their window (e.g. `tencent/hy3:free` existed
  2026-07-07 + ~2 weeks, then 404 on the API even though the page still rendered
  "Free"). Document the promo window + both prices.

## Reddit — NOT directly scrapable
firecrawl: "Website Not Supported". curl/browser: 403 / "Prove your humanity" CAPTCHA.
Working path — arctic-shift archive API (returns JSON, no auth):
- Comments by thread: `curl -s "https://arctic-shift.photon-reddit.com/api/comments/search?link_id=<base36-id>&limit=50"`
- The base36 id is the segment in the thread URL: `reddit.com/r/<sub>/comments/<id>/<slug>/`
- Older archive (may 502): `https://api.pullpush.io/reddit/search/submission/?ids=<id>`
- Keep the canonical reddit.com URLs in the final dossier for human readers; you only
  use the archive for reading.

## GitHub
- Raw assets: `https://github.com/<org>/<repo>/raw/main/assets/<file>`
- Commit dates (release-day evidence): `https://github.com/<org>/<repo>/commits/main/`
- News entries in READMEs often carry dated release announcements.

## Weight mirrors (from the card's Model Links table)
- ModelScope: `https://modelscope.cn/models/<org>/<model>`
- GitCode: `https://ai.gitcode.com/<org>/<model>`
- CNB: `https://cnb.cool/ai-models/<org>/<model>`

## Image OCR for benchmark charts
`scripts/ocr_vision_swift.swift` in this skill — macOS Swift + Vision framework,
no installs. Upscale 2x with `sips` first; reconstruct tables from y/x coordinates;
cross-check one row against an independent source before trusting the rest.
