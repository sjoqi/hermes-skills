---
name: market-research-scrape-synthesis
description: Collect market-research / job-post / competitor-demand data by scraping into a folder of markdown files (append-only raw dump + coding scheme + scored table + patterns + summary), then spawn parallel subagents to analyze and fold findings back into a SUMMARY. Use when G wants to turn a raw scrape (Upwork posts, marketplace demand, job boards, etc.) into an evidence-weighted decision without bloating the chat context.
---

# Market-Research Scrape → Synthesis Pipeline

Turns a messy scrape into a decision-ready synthesis while keeping the chat lean
(the bulk lives in files; only findings enter the conversation). Proven on the
Upwork-automation dataset (UW-001→045) but generic to any demand-scraping task.

**Scope check:** this is the pipeline for a *scrape* — many low-value items whose aggregate is
the point. If the user instead names segments up front and asks whether those buyers will pay
(pricing, market size, regulation, procurement), that is `buyer-demand-validation` — a
single-pass, public-source, per-segment evidence doc, not a corpus build.

## Why this shape
- The context compressor only shrinks the CHAT window, never files on disk. So
  keep raw volume in `.md` files; pass file paths to subagents, not pasted text.
- A pure one-message-at-a-time edit loop is the worst option: every turn re-pays
  system-prompt + memory overhead for no safety gain. Batch into files instead.
- Subagents have NO memory of the conversation. Every fact they need (file paths,
  the question, constraints) MUST be in the dispatch `context`.

## Folder layout (create once)
Under e.g. `~/hermes-home/<project>/02-market-research/<topic>/`:
- `RAW-JOBS.md` — append-only messy dump. Start each batch with
  `## Batch YYYY-MM-DD` + the **search terms used** (so selection bias is correctable later).
- `CODING-SCHEME.md` — stable tag vocabulary (industry, pain, tool, shape, budget band,
  client quality, competition, P/S track-fit scores 1–5, verbatim-quote rule). Add new
  tags at the bottom with a date; never silently redefine.
- `JOBS-TABLE.md` — one row per item, normalized from the raw dump (scores + tags).
- `PATTERNS.md` — recurring patterns with frequencies.
- `SUMMARY.md` — the distillation: dataset shape, candidate tracks, patterns table,
  contradictions resolved, directional conclusions, gaps, next steps.
- `README.md` — what the folder is + how to use it.
- `LOGGING-TEMPLATE.md` — blank next-item skeleton + resume priorities (see §5).

## Step-by-step
1. **Scrape → RAW-JOBS.md.** Paste anything, messy is fine. One block per item,
   sequential ID (`UW-001`…) never reused. Mandatory: verbatim pain quote when present.
   Note search terms per batch.
2. **Normalize → JOBS-TABLE.md + PATTERNS.md.** Apply CODING-SCHEME tags; score
   P (productizable) and S (specializable) 1–5 with a one-line reason each.
3. **Distill → SUMMARY.md.** Dataset shape, the two candidate tracks with
   evidence-for/against, pattern table w/ frequencies, contradictions found & resolved,
   directional conclusions, explicit GAPS, next steps. Keep confidence levels honest
   (thin samples = directional, not conclusive).
4. **When a cluster saturates OR chat hits ~80%:** STOP inline dumping. Spawn parallel
   leaf subagents (below). Never paste the whole raw file into chat.
5. **Dispatch analysis subagents** (parallel, background). Each reads the SAME source
   files and writes its OWN `AGENT-X-*.md`. Pattern:
   - Agent A: deep-dive the thinnest/riskiest sub-segment (e.g. regulated verticals) —
     extract by ID, assess the core hypothesis, state n and what would confirm/refute.
   - Agent B: pull the under-represented cluster (e.g. non-lead ops) — same treatment.
   - Agent C: draft the one-page decision memo (verdict + 2–3 ranked bets + confidence +
     next-evidence steps), weighting the whole dataset.
   Dispatch template (fill paths + question per agent):
   ```
   delegate_task(tasks=[
     {"goal":"<specific question>", "role":"leaf",
      "context":"Read these ABSOLUTE PATHS: <list>.
       YOUR TASK: <extract/assess/conclude, cite IDs>.
       Write output to <folder>/AGENT-A-<topic>.md (markdown, ~300-500 words).
       Do NOT modify other files. Return a 3-sentence summary of your conclusion."},
     ... B, C ...
   ])
   ```
   They run in background; result re-enters chat as one consolidated message. Dispatch
   with NO `goal` at top level — use `tasks` only.
6. **Fold into SUMMARY.md §7.** Read the three `AGENT-*.md` (verify, don't trust the
   chat summary alone), then patch SUMMARY.md with: the converged verdict, the refined
   hypothesis (with confidence %), the ranked bets, and the next-evidence list. This
   survives compression and the next session.
7. **Resume template.** Write `LOGGING-TEMPLATE.md` biased toward the EVIDENCE GAPS
   (thin n, saturated cluster) so future samples strengthen weak spots, with a blank
   next-ID skeleton pre-wired to the coding scheme.

## Pitfalls
- Don't build a SaaS for "service buyers." The decisive signal is the budget/hire
  inversion: in the Upwork data ALL hired jobs were ≤$600 (clear scope); ALL $1k+ posts
  stalemated at 50+/0 interviews. Buyers pay for a bounded task, not software.
- "Regulated = moat" is a trap. Regulation alone does NOT suppress competition — the
  suppressant is TITLE LEGIBILITY (domain reads as needing non-fakeable knowledge).
  Checkbox compliance (name-dropped GDPR/HIPAA) buys nothing. Verify with bid counts.
- Thin n (2–6) = directional only. State confidence %; recommend one cheap validation
  sprint, not a committed direction.
- Subagent `context` must be self-contained: absolute file paths + the exact question +
  "write only AGENT-X.md, don't touch others." Missing paths = agent fails or guesses.
- This is research logging, NOT code — no git checkpoint needed for data appends.
- Keep the chat lean: pass file paths, not pasted raw. The compressor won't eat disk files.

## Verification
- All `AGENT-*.md` files exist and were written by the subagents (check on disk, not
  just the chat summary).
- SUMMARY.md §7 reflects the converged verdict and cites specific post IDs.
- LOGGING-TEMPLATE.md next-ID matches the last logged item (no gaps/reuse).
