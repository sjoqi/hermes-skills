# Extracting model data from Artificial Analysis (artificialanalysis.ai)

AA is a Next.js app: page HTML contains the model data server-side as an RSC **flight payload** (`self.__next_f.push` chunks), so you do NOT need a browser. The same trick generalizes to any Next.js site — check the HTML for `self.__next_f.push` before reaching for the browser.

## Recipe (curl + python3)

```bash
curl -sL --max-time 40 "https://artificialanalysis.ai/models/<slug>" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36" \
  -o aa_page.html
```

```python
import re
html = open('aa_page.html', encoding='utf-8', errors='ignore').read()
chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)</script>', html, re.S)
text = ''.join(chunks).encode().decode('unicode_escape', errors='ignore')
i = text.find('"slug":"<slug>"')          # locate the model's JSON entry
seg = text[i:i+2600]                       # the entry is one contiguous JSON blob
# pull fields with regex:
def g(field):
    m = re.search(f'"{field}":([^,}}]+)', seg)
    return m.group(1) if m else None
print(g('intelligenceIndex'), g('releaseDate'), g('parameters'), g('inferenceParametersActiveBillions'))
```

Notes:
- The entry JSON is one contiguous blob starting at `"slug":"<slug>"`; fields are flat (not nested), comma/`}`-delimited, so the simple regex works.
- Unescape step: `.encode().decode('unicode_escape')` handles `\"` and `\n` escapes in the flight chunks.
- If `"slug":"<slug>"` is not found, try the canonical AA slug (e.g. `hy3`, `deepseek-v4-pro`) — AA slugs differ from OpenRouter slugs (`tencent/hy3` → AA `hy3`).
- **Ranks ("#6 / 101") and speed/price ranks are NOT in the flight payload** — they are computed client-side. Get them via `browser_navigate` on the model page (the accessibility snapshot includes them), not curl.

## AA JSON field map (per model entry)

| Field | Meaning |
|---|---|
| `intelligenceIndex` | Artificial Analysis Intelligence Index (composite of 9 evals in v4.1.1: GDPval-AA v2, τ³-Banking, Terminal-Bench v2.1, SciCode, HLE, GPQA Diamond, CritPt, AA-Omniscience, AA-LCR) |
| `intelligenceIndexIsEstimated` | true = estimate, not a real run |
| `agenticIndex` | agentic capability composite |
| `gdpval` / `gdpvalNormalized` | GDPval-AA v2 Elo / normalized |
| `tauBanking`, `terminalbenchV21`, `scicode`, `lcr`, `hle`, `gpqa`, `critpt` | per-eval scores (0–1 fractions) |
| `omniscience` + `omniscienceBreakdown.{accuracy,hallucinationRate}` | knowledge reliability; negative = more wrong than right |
| `reasoningTokens` | reasoning-token budget the evaluator configured for this model — EFFORT MISMATCH WARNING: a model run with 2,000 vs 4,375 reasoning tokens is not an apples-to-apples comparison |
| `releaseDate`, `parameters`, `inferenceParametersActiveBillions`, `contextWindowTokens` | specs (AA params can differ from vendor claims, e.g. 299B vs 295B) |
| `price1mInputTokens`, `price1mOutputTokens`, `cacheHitPrice` | AA-listed API pricing (can differ from OpenRouter's) |
| `isOpenWeights`, `licenseName`, `openSourceCategorization` | licensing |

## URL patterns

- Model page: `https://artificialanalysis.ai/models/<slug>`
- Direct comparison: `https://artificialanalysis.ai/models/comparisons/<slug-a>-vs-<slug-b>` (both orderings redirect to the same page; contains BOTH models' full JSON + FAQ text like "Which is more intelligent...")
- Leaderboard: `https://artificialanalysis.ai/leaderboards/...` routes 404 for some paths; the per-model-page comparison chart is usually enough — or use the browser on the model page.
- Evaluations glossary: `https://artificialanalysis.ai/evaluations/<slug>` (methodology for each eval).

## Verification pattern

After extraction, sanity-check against the rendered page text (firecrawl `web_extract` output includes the FAQ prose: "Hy3 scores 42 on the Artificial Analysis Intelligence Index"). If the two disagree, the site updated between fetches — record the fetch date.
