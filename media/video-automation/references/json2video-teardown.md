# JSON2Video — condensed competitor teardown

Verified 2026-08-07 against `https://json2video.com/docs/v2/` (raw `.md`), the
pricing page, `cdn.json2video.com`, and DNS/HTTP probes. Re-verify before
quoting prices. Full write-up produced at
`~/hermes-home/research/video-automation/01-json2video-teardown.md`.

This is the benchmark to beat. Read it before designing a competing JSON→video DSL.

## What it is
Declarative video compositor as a service. POST one JSON "movie" → 16-char
`project` ID → async render → MP4 on CloudFront. Three public endpoints only:
`/movies` (POST/GET/DELETE), `/templates`, `/media`. Auth `x-api-key`, base
`https://api.json2video.com/v2/`.

## Schema shape (worth copying)
```
Movie: resolution|width|height|fps(25)|quality(low|medium|high)|cache|template
       variables{} · client-data{} (hyphen!) · preload[] · exports[] · elements[] · scenes[]
Scene: background-color · duration(-1 fit) · transition{type:"xfade",style,duration}
       import · condition · variables · preload
       iterate / iterate-from(incl) / iterate-to(EXCL) / iterate-step
Element: type discriminator, 9 types:
       image video text html component audio voice audiogram subtitles
```
- **Duration protocol** (elegant, steal this): `>0` explicit · `-1` intrinsic
  asset length · `-2` match container.
- **Common props**: id, condition, variables, comment, duration, start,
  extra-time, z-index(−99..99), cache, fade-in/out.
- **Visual adds**: position(+x,y), width/height(-1=aspect), resize
  (cover|fill|fit|contain), rotate{angle,speed}, crop, zoom(−10..10),
  pan/pan-distance/pan-crop, chroma-key{color,tolerance}, correction
  {brightness,contrast,gamma,saturation}, flip-h/v, mask(greyscale PNG or video).
- **Audio adds**: muted, volume(0..10).
- **keyframes[]**: animate x/y/width/height/zoom. `time` = seconds, negative
  (before end), or `"50%"`. 33 easings (easings.net set) + per-property
  `easing-x/-y/-width/-height/-zoom`.
- **`iterate`** = data-driven scene templating: duplicates a scene per item of a
  movie-level array **of objects**; fields flatten to `{{name}}` (never
  `{{item.name}}`); auto-vars `iteration`, `first_iteration`, `last_iteration`.

## Architecture (evidence-graded)
**[OBS] via dig/curl -I, 2026-08-07** — all AWS:
- `api.json2video.com` → **AWS API Gateway** (proof: `x-amzn-errortype:
  MissingAuthenticationTokenException`, `x-amz-apigw-id`, stock CORS header list).
- `assets.` and `cdn.` → **the same CloudFront distribution** `d3isqg0r0e4lkp`
  over S3 (`server: AmazonS3`). Outputs at `clients/<acct>/renders/<date>-<n>.mp4`.

**[INF, strong] ffmpeg + headless Chromium, two substrates one schema:**
| Fingerprint | Implies |
|---|---|
| documented error `500 Error starting subprocess` | render is a forked child process |
| `transition.type:"xfade"` + styles fade/wipeleft/slideup/circleopen/dissolve/pixelize | verbatim ffmpeg **xfade** filter enum |
| `correction{brightness,contrast,gamma,saturation}` | ffmpeg **eq** filter, exactly |
| chroma-key, mask (PNG *or video*), speed 0.5–4 pitch-preserved | colorkey, alphamerge, atempo+setpts |
| `.ass` exposed on status; subtitle settings = outline/shadow/box/all-caps | burned in via **libass**; settings map to ASS v4+ style fields |
| html element: `tailwindcss` flag, `wait` 0–5s before capture, JS, `src`=live URL | **headless Chromium** (Puppeteer/Playwright) |
| `text.settings` = arbitrary CSS, unknown keys **silently dropped** | CSSOM assignment semantics → browser rendering |
| components = "animated HTML templates rendered on their own canvas", catalogue at `cdn.json2video.com/data/components/schemas/index.json` | components+text share the browser path; library is CDN data, not code |
| voice `model` enum names vendors; `connection`=BYO key | TTS is **vendor passthrough** (Azure + ElevenLabs) |
| subtitles `model: whisper` vs `default`, `keywords` boosting, 44 codes incl. hi-Latn/es-419/nl-BE/de-CH | two ASR backends; "default" is Deepgram-shaped |
| docs: "scenes render in PARALLEL, split work into scenes" | scene-level worker fan-out |
| `pending` = "queued, no worker has picked it up" | explicit queue + worker pool |

Pipeline: resolve (vars/template/import/condition/iterate) → preload+ffprobe →
TTS → rasterize text/html/component in Chromium → per-scene ffmpeg compose
(parallel) → xfade concat → transcribe+burn ASS **last** → encode → S3 →
exports sequentially → bill.

## Pricing / limits
- **1 credit = 1 second of OUTPUT**, resolution-independent. Failed renders free.
  Cached assets not re-billed. TTS + ASR currently **0 credits**.
- ⚠️ **Doc contradiction**: `/pricing/` FAQ claims 4K = 4×; the newer
  code-generated `credit-consumption` reference says resolution doesn't change
  the rate. Trust the reference; verify empirically.
- Free 600 credits (watermarked) · Hobby $16.95/mo 3k (max 1min video) ·
  Professional $49.95/mo 12k (10min) · Startup $99.95/mo 30k (30min) ·
  prepaid $49.95/7.2k, $99.95/15.6k. Subscription credits expire monthly,
  prepaid never; subscription drains first. Paddle is MoR.
- **Effective $/min of output: $0.42 (prepaid small) → $0.20 (Startup).**
  A 30s clip = 30 credits ≈ $0.10–0.21. **This is the number to beat** — the
  DIY FFmpeg/GPU-Spot model in `reference-architecture.md` lands ~$0.008/clip.
- Canvas 50–3840px. Poll floor 5s. List range ≤93 days. `html.wait` ≤5s.
  Observed throughput: 108.2s output in 195s wall ≈ **1.8× realtime** @1080×1920.
- **Explicitly NOT offered**: AI image gen, AI video gen, avatars, face-swap.
  It's a compositor — you bring assets. (A DIY stack's asset/AI layer is
  therefore a genuine differentiator, not just parity.)

## Weaknesses = your differentiation list
1. **Webhooks unsigned, unretried, fire-and-forget, single un-named event.**
   HMAC + at-least-once w/ backoff is cheap table stakes.
2. **No server-side render timeout** — client is told to invent `timeout` at
   15min while server still reports `running`.
3. **POST not idempotent**, no `Idempotency-Key`. Retry burns credits.
4. **Silent failure everywhere**: unknown `text.settings` keys dropped; var names
   starting `?`/`$`/`@` dropped; `iterate` over an array of strings makes the
   scene *vanish* with no error; short `content-type` silently falls back to JSON.
   Ship strict validation instead.
5. **Published JSON Schema is a 1.1KB placeholder stub** — its own `description`
   says "PLACEHOLDER … Phase 6" — even though their agent-rules page tells agents
   to validate against it. Ship a real machine-readable schema day one.
6. Two incompatible `settings` regimes (CSS-permissive `text` vs closed-list
   `subtitles`) is a real usability wart born of the two-substrate design.

## Design decisions worth stealing
Declarative JSON + async job + poll/webhook, 3 endpoints, complexity in the
schema · three-level `cache` (movie/scene/element) defaulting true · scene
parallelism as a user-facing contract · two substrates one schema (ffmpeg for
pixels/timing, browser for typography/animation — the only sane way to get
Google Fonts + Tailwind + 33 easings) · vendor passthrough with BYO-key
connections · billing on output seconds only (predictable; makes render speed
pure margin) · `iterate` as data-driven templating.
