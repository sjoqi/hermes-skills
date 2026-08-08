---
name: video-automation
description: Build or advise on DIY programmatic video rendering services — compare open-source render stacks (Remotion / FFmpeg / Revideo / Motion Canvas / editly / Chromium / Blender-Manx), model cloud render cost, check licensing traps (Remotion BSL), design the asset/AI (TTS, stock, image/gen-video) layer, and reverse-engineer/tear down incumbent managed video APIs (JSON2Video et al.) — their JSON movie schema, render architecture, and unit economics. Use when the user wants to build, price, or choose a stack for an automated video-generation pipeline, write a stack blueprint, teardown/reverse-engineer a competitor video API, or beat a managed API by owning the compositing layer.
---

# Video Automation — DIY Programmatic Rendering

Class of work: standing up (or advising on) an in-house service that turns a
JSON spec / script / template into finished video, at lower unit cost than a
managed API. The differentiator vs. managed slop is **owning the compositing
core + the DSL + the asset pipeline**, not calling someone else's renderer.

## When to load this skill
- "Build a video rendering service / pipeline / engine."
- "Compare Remotion vs FFmpeg vs [X] for programmatic video."
- "What does it cost to render N videos ourselves?" / cloud cost modeling.
- "Is Remotion free for commercial use?" (licensing trap — see below).
- "Replace JSON2Video / a managed video API with our own."
- Any blueprint, architecture, or stack-decision doc for automated video.

## Stack comparison framework (the core deliverable)
For each candidate, evaluate on: **(1)** how compositing works, **(2)** render
speed (×realtime for 1080p30), **(3)** $/minute of video (compute), **(4)**
license for commercial/automated use, **(5)** build complexity. Concrete data
in `references/stacks-pricing-2026.md` (verified 2026-08-08 — re-verify before
budget sign-off, prices drift).

Quick verdict:
- **FFmpeg `filter_complex` + your own JSON→graph DSL** = free, fastest
  (GPU/NVENC ~10× RT), total control, zero per-render license. The DSL *is* the
  moat. Recommended core.
- **Remotion (React→video) + Lambda** = browser-grade effects, but **Business
  Source License** — NOT free for business (see trap). Use as premium tier.
- **Revideo (MIT)** = open-source server-side Node rendering; the no-BSL answer
  to Remotion's automation tier, but smaller ecosystem (you shard yourself).
- **Motion Canvas (MIT)** = browser-only, no render farm; authoring tool, not batch.
- **editly (MIT)** = FFmpeg wrapper; great low-complexity MVP, then graduate to
  custom DSL.
- **Chromium frame-capture** = max fidelity (full web platform), max cost.
- **Blender / Manim (GPL/MIT)** = niche asset generators (3D / math explainers),
  feed frames into the FFmpeg core — not the main pipeline.

## The Remotion licensing trap (verify before recommending)
Remotion is **source-available under a custom BSL**, not open source for
business:
- Free only for individuals / companies **≤ 3 people** (Free License, unlimited
  commercial use).
- **Companies of 4+ people** running a **batch/automated product** need
  **"Remotion for Automators": $0.01 per render + $100/month minimum**
  (automation devs do NOT need a seat). Do not tell a client "Remotion is free."
- BSL has a non-compete: can't fork Remotion to sell a competing video-creation
  product. Building *your own* automation service that uses it as a dependency is
  fine. Re-read the FAQ: https://www.remotion.dev/docs/license/faq
- Escape hatch: **Revideo (MIT)** for server-side React-style composition.

## Reference architecture (serverless-ish, stateless workers)
```
client → API Gateway (validate JSON spec, return jobId)
       → Job Queue (SQS Standard, or Redis/BullMQ; big payloads → S3 via Extended Client)
       → Stateless Render Workers (ECS Fargate / EC2 Spot ASG, GPU g4dn for NVENC)
       → S3 output (Standard $0.023/GB us-east-1)
       → Webhook callback (retry w/ backoff) + DynamoDB job status
```
- **Scale**: one job per worker vCPU slice; g4dn.xlarge (T4) ~2 NVENC-parallel
  renders; warm pool to beat cold start; scale on `ApproximateNumberOfMessagesVisible`.
- **Cost math** (1000 × 30s 1080p30, GPU Spot): compute ≈ $8 total → **~$0.008/
  clip** vs $0.50–$2.00 on managed APIs. On-demand ≈ $27; +Remotion fee ≈ $37.
  Full example in `references/reference-architecture.md`.

## Asset / AI layer
- **TTS**: default **Kokoro** (Apache-2.0, 82M, self-hosted = free beyond EC2);
  **OpenAI tts-1** $15/1M chars and **Azure Neural** $15/1M as cheap premium;
  **ElevenLabs** ~$0.15–0.20/1M only for hero/branded voices. TTS is ~free vs.
  compute.
- **Stock**: Pexels/Pixabay/Unsplash (CC0, REST APIs); Storyblocks/Shutterstock
  for production. Cache in S3/GCS so workers don't refetch.
- **Image gen**: FLUX on Replicate (schnell $0.003 / dev $0.03 / pro $0.055 per
  image) or self-host on g5/g4dn.
- **Generative VIDEO (Sora 2 etc.) is the cost bomb**: $0.10/sec → $3.00 for one
  30s clip, $3,000 for 1000. Keep it **opt-in**, behind a plan tier.

## Tearing down a competitor API (JSON2Video and friends)
When the task is "reverse-engineer <managed video API>'s architecture/schema",
run this sequence. Worked end-to-end on JSON2Video; findings in
`references/json2video-teardown.md`.

1. **Get the raw docs, not the HTML.** Many modern docs sites serve the source
   markdown at the same URL + `.md`
   (e.g. `…/reference/json-syntax/movie` → `…/movie.md`). Raw markdown keeps
   full property tables, defaults, and enum values that HTML scraping loses,
   and it's plain text so **`curl` beats the browser and the scraper**. Try
   `.md` first on any docs URL.
2. **When the scraper rate-limits, switch to `curl`, don't wait.** These are
   static files. A `for p in <paths>; do curl -sL ".../$p.md" -o …; done` loop
   fetches 10 pages in one call with no quota. (Hit exactly this at ~15
   Firecrawl requests mid-session.)
3. **Probe the live infrastructure — it's free, fast, and non-inferential.**
   `dig +short api.<host>` / `assets.` / `cdn.` / apex, plus `curl -sI` on the
   API base. Response headers name the vendor outright: `x-amzn-errortype` +
   `x-amz-apigw-id` ⇒ AWS API Gateway; `server: AmazonS3` + `via: … cloudfront`
   ⇒ S3/CloudFront; a shared CNAME across `assets.`/`cdn.` ⇒ one distribution.
4. **Read the error tables and the "rules for AI agents" page.** Vendors publish
   candid operational truth there that the marketing pages omit — queue
   semantics, parallelism, poll floors, deprecations. JSON2Video's
   `500 Error starting subprocess` single-handedly proved a forked renderer.
5. **Fingerprint the engine from schema vocabulary.** Enum values leak the
   implementation: `xfade` + its style names = ffmpeg's xfade filter;
   `{brightness,contrast,gamma,saturation}` = ffmpeg `eq`; ASS output +
   outline/shadow/box settings = libass; `tailwindcss`/`wait`-before-capture/JS
   = headless Chromium; "unknown CSS keys silently ignored" = CSSOM assignment.
6. **Grade every claim inline: `[DOC]` / `[OBS]` / `[INF]`** (documented /
   directly observed / inferred-with-evidence-named). This is the single biggest
   quality lever on a teardown — it keeps inference honest and makes the doc
   reusable by someone who wasn't there. Never let an inference read as a fact.
7. **Hunt for doc self-contradictions and stale artifacts** — they're findings.
   JSON2Video's pricing FAQ says 4K costs 4×; its newer code-generated credit
   reference says resolution is irrelevant. Their published JSON Schema is a
   placeholder stub that still says "TODO". Prefer the code-generated page and
   flag the conflict rather than silently picking one.
8. **Close with a "weaknesses = your differentiation list"** and a
   rebuild shopping list mapping each of their layers to a substitute. That's
   what makes a teardown actionable rather than trivia.

### Writing very large deliverables
A 500+ line / 40KB markdown file **will blow the tool-call payload limit and
stall the stream**. Don't retry the same big write. Write it as
`_p1.md`…`_p4.md` in the target directory, then `cat _p1.md _p2.md _p3.md _p4.md
> final.md && rm _p*.md`. Keep each chunk under ~8K tokens. (Note the cleanup
`rm` of 4 files may trip the mass-deletion security scanner — it auto-approves,
but expect the flag.)

## Research / verification pitfalls (Firecrawl web tools)
- `web_search` takes **`query`**, NOT `url` (passing `url` → "Query cannot be
  empty"). Use `web_extract` for known URLs.
- Firecrawl **rate-limits hard** (~15 req/min). On "Rate Limit Exceeded", switch
  to `curl` for static/plain-text pages (fastest fix), or `sleep 30–45` then
  retry. Don't loop-fail. Note the tool fires all URLs in a batch call against
  the same quota, so two parallel 5-URL calls can exhaust it in one turn.
- `web_extract` caches the full page to `~/.hermes/cache/web/<file>.md` — when the
  returned text is truncated ("TRUNCATED … read_file path=…"), use `read_file` /
  `search_files` on that cache path to get the omitted middle instead of re-fetching.
- Some GitHub org casings 404 (e.g. `codewithfan/revideo`, `Revideo/revideo`);
  correct repos: `revideo/revideo`, `motion-canvas/motion-canvas`, `mifi/editly`.
- Always **cite the official pricing/license page inline** and stamp "verified
  <date>" — prices change.

## Deliverable shape
A blueprint markdown with: stack comparison table, reference architecture diagram
(ASCII), cost math example, asset/AI layer with pricing, phased implementation
plan, risks/caveats, and an inline cited-sources section. See the produced
`03-diy-stack.md` pattern under the user's research folder.

## Reference files
- `references/stacks-pricing-2026.md` — condensed verified stack + pricing + licensing data bank (with sources).
- `references/reference-architecture.md` — architecture detail + 1000×30s cost model.
- `references/json2video-teardown.md` — the incumbent's full schema, AWS/ffmpeg/Chromium architecture (evidence-graded), unit economics ($0.20–0.42/min of output — the number to beat), and its weaknesses as a differentiation list. Read before designing a competing JSON→video DSL.
