---
name: product-teardown-research
description: "Reverse-engineer a commercial product from its public surface well enough to rebuild it — architecture, schema, economics, and competitive gap. Use when the user gives a product URL and wants to understand 'how they're operating' / 'the underlying structure' / 'so I can build my own'. Fans out three parallel subagents on fixed axes (teardown / landscape / DIY blueprint), each writing to its own numbered markdown file."
---

# product-teardown-research

Turn a single product URL into a buildable understanding of that product: how it
actually works, who else does it, why the output is bad, and what it would cost to
do it yourself.

## Load this skill when

- The user drops a product/SaaS URL and asks to understand "the structure", "how
  they're operating", "the underlying system".
- The stated or implied goal is **to build a competing/better version**.
- The user says the incumbent's output is "slop"/"generic" and wants to know why.

Do **not** use this for a simple "what does this company do" — that's one `web_extract`.

## Method

### 0. Read the target page yourself first

One `web_extract` on the given URL **before** dispatching. You need enough context to
write good subagent briefs, and the marketing page usually reveals the business model
plainly (who they integrate with = who the buyer is). Batch this with `skill_view` of
any user-discipline skill in the same turn.

### 1. Fan out three subagents on fixed axes

Always these three, in one `delegate_task` batch. They are independent by construction,
so they run fully parallel.

| # | Axis | Output file |
|---|---|---|
| 1 | **Teardown** of the target: schema/data model, API lifecycle, inferred backend, pricing mechanics, weaknesses | `01-<product>-teardown.md` |
| 2 | **Landscape**: competitors, pricing-model comparison table, *why the output is slop*, ecosystem layer | `02-competitors.md` |
| 3 | **DIY blueprint**: open-source stack options, licensing traps, reference architecture, verified cost math | `03-diy-stack.md` |

Write to `~/hermes-home/research/<topic>/`. Numbered prefixes so the reading order is
self-evident.

### 2. Brief each agent hard

Subagents know nothing about the conversation. Each brief must name:
- the exact pages/docs to read,
- the exact deliverable sections (enumerate them — "(1)… (2)… (3)…"),
- **"be technical and specific — the reader wants to rebuild it"**,
- the absolute output path,
- language, if the user isn't writing in English.

### 3. Verify before reporting

`wc -c` the output files. Subagent summaries are self-reports — a stalled `write_file`
can be reported as success. Confirm bytes on disk.

### 4. Report the synthesis, not the file list

Lead with the mechanism (what the product *actually is* in one sentence), then the
evidence table, then the economics, then the gap. Carry the agents' caveats through to
the user — unverified vendors, adversarial sources, undisclosed figures.

## Pitfalls (all observed in a real run)

- **Docs sites often serve raw markdown at `<url>.md`.** Try it before scraping HTML —
  much higher fidelity, and it bypasses the scraper. This was the single biggest
  quality win in a JSON2Video teardown.
- **Firecrawl rate-limits at roughly 15 requests.** All three agents hit it in one run.
  Fall back to `curl` for the `.md` endpoints, or pace with `sleep`.
- **Large `write_file` payloads can stall mid tool-call** and silently not execute.
  Split into chunks and concatenate; then verify with `wc -c`.
- **Never guess GitHub URLs.** Guessed repo paths 404'd repeatedly. Search, confirm,
  then cite.
- **Verify pricing on official pages only.** Competitor comparison pages are adversarial
  sources — directionally useful, not quotable. Flag them as such in the doc.
- **Don't freeze research findings into a skill.** They go stale. The skill is the
  method; the findings are artifacts on disk.

## Inference discipline

Architecture claims must be grounded in something observable, and each claim marked
**documented** vs **inferred**. Productive evidence classes:

- **Response headers** — `x-amzn-errortype` / `x-amz-apigw-id` ⇒ AWS API Gateway.
- **Shared CDN distribution IDs** across subdomains ⇒ one CloudFront origin.
- **Config vocabulary matching a known tool's flag names** — e.g. transition types named
  exactly after ffmpeg `xfade`, or a colour-correction block whose four keys are exactly
  the ffmpeg `eq` filter's ⇒ ffmpeg underneath.
- **Documented error strings** — "Error starting subprocess" ⇒ a forked render process.
- **Silent-drop behaviour on unknown keys** ⇒ CSSOM assignment ⇒ headless browser.
- **Strict closed list vs permissive passthrough** on two similar settings blocks ⇒ two
  different rendering paths (e.g. libass for subtitles, Chromium for text).

## The quality question

When the user calls the incumbent's output "slop", answer it structurally rather than
aesthetically. Ask what the *pipeline* forces. Recurring causes in template-driven
media: keyword-retrieved assets illustrating nouns instead of arguments; flat TTS
prosody; pacing computed from data boundaries rather than directed; a handful of
ubiquitous presets creating instant format recognition; template reuse depreciating the
format for every user of it.

Conclusion to test in any such market: **the differentiator is usually upstream of the
renderer.** The compositor is a commodity; sourcing, voice, and editorial judgement are
not. That's where the buildable advantage is.
