---
name: llm-model-comparison
description: "Use when comparing two AI models head-to-head."
version: 1.0.0
author: Hermes curator
license: MIT
tags: [research, benchmarks, llm, comparison, subagents, live-test]
metadata:
  hermes:
    tags: [research, benchmarks, llm, comparison, subagents, live-test]
    related_skills: [hermes-delegation, grounded-citations, working-with-g]
---

# LLM Model Comparison (research + live test)

## When to use
- User asks to compare / benchmark / "which is better" for two AI models, and wants the answer tested and verifiable rather than vibes.
- Any head-to-head where vendor marketing exists on both sides.

## Core principles
1. **Ground truth first.** Verify both models exist before dispatching (web_search → official release pages). Capture exact: release date, total/active params, context, license, API model id(s), price per 1M. Never trust blog summaries for specs.
2. **Separate vendor-reported from independently-measured in every table.** Vendors cherry-pick benchmarks. Independent labs (NIST CAISI, Artificial Analysis, MathArena) routinely measure BELOW vendor claims. Worked example (Aug 2026): DeepSeek V4 Pro self-reported ≈Opus 4.6/GPT-5.4 parity; NIST CAISI measured it ~8 months behind the frontier (≈GPT-5 level). Treat every vendor table as a claim.
3. **Never trust a subagent self-report** — verify artifacts on disk (read_file each produced .md) and spot-check 2–3 load-bearing primary sources yourself (web_extract). "I fetched it" is not evidence.
4. **Deliver with a citation ledger** (grounded-citations skill) and PASS/FAIL footnote (G's reporting style).

## Workflow
1. Load skills: `working-with-g`, `hermes-delegation`, `grounded-citations`.
2. Quick grounding pass in the PARENT (don't delegate this): confirm both models, register the release pages into the citation ledger at retrieval time (`sources.py add <url> --title ...`).
3. Check local API access WITHOUT printing secrets:
   - List key NAMES only: `grep -oE '^[A-Za-z_][A-Za-z0-9_]*' ~/.hermes/.env | sort -u`
   - Discover model ids: `curl -s https://api.deepseek.com/models -H "Authorization: Bearer $DEEPSEEK_API_KEY"` (and OpenRouter: `https://openrouter.ai/api/v1/models`) — use whatever the API lists, don't assume the id.
   - Load keys: `set -a; source ~/.hermes/.env; set +a` — never echo key values into any output or file.
4. Fan out subagents as **separate single-goal `delegate_task` calls in one turn** (batched `tasks:` arrays can fail to parse — see hermes-delegation skill). Typical 4-way split, all leaf:
   - Agent A — dossier model X: primary sources, URL next to EVERY number, mark unverifiable items `[UNVERIFIED]`.
   - Agent B — dossier model Y: same spec.
   - Agent C — INDEPENDENT (non-vendor) benchmark synthesis: Artificial Analysis, LMArena/arena.ai, OpenRouter, NIST CAISI, SWE-bench/AIME/GPQA leaderboards, community threads; mandate a methodology-caveats section.
   - Agent D — adversarial LIVE API test (see below). Frame it as "try to disprove the vendor claims".
   - Subagents are amnesiac: pass everything (result dir, model facts, fairness rules) in `goal`/`context`. Have each write its deliverable to a shared dir and return paths + key numbers in the summary.
5. Verify: read every produced file; web_extract the most load-bearing primary pages yourself (e.g. NIST CAISI page, vendor release page) and confirm the dossier numbers match.
6. Render the deliverable: spec table, benchmark table (vendor vs independent separated), top-3 methodology caveats, verdict, Sources block rendered from the ledger (`sources.py render --cited-in`).

## Live API test design (lean, cost-aware — G is cost-sensitive)
- 10–12 questions: math (exact numeric), coding (runnable), logic, knowledge, instruction-following. Write your own; no leaked benchmark items.
- Identical system prompt, temperature 0, max_tokens capped (4096 — reasoning-model thinking chains count against it), stream off. Same params both models, same date.
- Save raw response JSON to `raw-test/<model>_q<N>.json` (verifiability). Retry once on error, else mark honest failure.
- Report exact token usage per model and estimated cost from published per-1M prices; compute a per-question score table (run returned code locally to check it).
- Document effort settings used — reasoning models swing ±5–20 pts between non-think/high/max.

## Pitfalls
- **Reasoning-effort mismatch is the #1 score distortion** (e.g. V4 Pro tested at max-effort with 4,375 thinking tokens vs Hy3 default no-think with 2,000 in the same harness).
- **Serving differences bias Elo**: free-tier endpoints get fewer votes + different quantization; LMArena serves defaults, not max effort. Check vote counts and provider.
- **Version drift**: preview vs full releases are different models (Hy3 preview 2026-04-23 ≠ Hy3 full 2026-07-06). Date-stamp every number; note which variant each measurement used.
- **Reasoning models can burn the whole output budget and return EMPTY content** (worked example: DeepSeek V4 Pro on a trailing-zeros math question derived the correct answer, then "But wait!"-spiraled into self-doubt, hit `max_tokens` with `finish_reason=length` and zero content — twice in run 1, while Hy3 answered correctly in budget). Score as a failure; it is a budget/usability failure, not necessarily a competence one. **A larger cap or lower effort often fixes it — and the failure is STOCHASTIC, not a stable model trait: a same-day identical re-run flipped it (Hy3 hit the cap with empty content while DeepSeek answered `5` cleanly).** Never present a budget-exhaustion failure on ONE run as a model's reliability property — it hits both models on the same question.
- **Subagents over-verify**: a child ran two extra verification passes to fix a $0.00001 rounding difference in its own cost figure, "concluding" three times. The parent's disk check is the real gate; instruct children to stop after one verification pass and not re-verify cosmetic precision.
- **Vendor inflation is asymmetric**: one vendor's numbers may survive independent re-runs while another's show 6–10 pt gaps (CAISI SWE-bench 74% vs self-reported 80.6%; MathArena Apex 28.1% vs 38.3%). The vendor with no independent re-run carries the same inflation risk in the OPPOSITE direction of the narrative.
- **Citation ledger script needs Python 3.10+**: on this Mac system python3 is 3.9.6 and `sources.py` crashes (`TypeError: unsupported operand type(s) for |`). Run with `/Users/<you>/hermes-home/.venv-img/bin/python3` (3.13) or `/opt/homebrew/bin/python3.13`.
- **Reddit blocks direct scraping** (captcha as of 2026): use the arctic-shift archive API for thread bodies; mark comment-level detail `[UNVERIFIED]`.
- **Vendor benchmark charts are images**: OCR them (macOS Vision framework via a small local Swift tool) instead of guessing numbers; flag cells as `[from official chart, OCR]`.
- **Cost control**: cap max_tokens and question count, compute cost from usage fields, and remember a 4-agent fan-out costs ~4× research tokens (children inherit the parent model).

## Evidence handling — raw API responses are PRIMARY evidence (G correction, 2026-08-10)
**Raw response JSONs are the independent-verification evidence of a live test — the thing that makes results checkable instead of self-reported. Never delete them as part of a "cleanup" unless the user explicitly names them.**
- When G says "clean the unrelevant unnecessary raw files", the expendable parts are scratch: harness scripts, parsed intermediates, temp verifiers. The raw response JSONs are NOT expendable — G flagged exactly this mistake ("the raw json files for independent verification is a strong evidence of the test right? its relevant. but you delete it").
- Default: keep all raw responses. If a cleanup is requested, ask before deleting anything in the evidence set, or delete only scratch and say so explicitly.
- Re-verify from the raw files BEFORE any cleanup, and record that verification in the report so the report doesn't later claim files exist that were removed.
- If raw evidence was lost, recovery is partial at best: `rm` bypasses Trash, no APFS snapshots by default, and subagent sessions are NOT in the session DB. The delegation live transcript (`~/.hermes/cache/delegation/live/<id>/task-0.log`) preserves the evidence trail (model ids, finish_reasons, token counts, verification outputs) but not the full raw bodies. Re-running the test (~$0.03, question files intact) regenerates fresh evidence — same methodology, not the original files.

## Re-run discipline — single-run verdicts flip (worked example, 2026-08-10)
**A live head-to-head with a 1-question margin is NOT a result. Re-run it before concluding.**
- Run 1: Hy3 18/18 vs DeepSeek 17/18 → "Hy3 wins on reliability". Same-day identical re-run (same harness, prompts, temp 0, max_tokens 4096): **DeepSeek 18/18 vs Hy3 17/18** — the verdict flipped, and the only differentiator (q102 budget-exhaustion) moved to the other model. Correct conclusion after both runs: statistical tie on capability (36/36 on answered questions each), with DeepSeek consistently faster/leaner and Hy3 cheaper.
- Cost of the re-run is trivial (~$0.03, question files intact) — there is no excuse for concluding on a single run when the margin is 1 question and the differentiator is a stochastic failure mode.
- When the user pushes back on evidence (e.g. "you deleted the raw files"), the re-run is not just restoration — it is a genuine methodological improvement that can overturn the conclusion. Say so honestly in the updated report (add a "Re-run" section; keep both runs' tables; withdraw the overturned claim explicitly).

## Decisive verdict (G's follow-up pattern)
After the full hedged report, G will compress the question: "ignore the cost, based on performance, who won." Answer with a **small split-by-category table** (agentic/coding · live head-to-head · reasoning · arena Elo) plus a **named winner** and at most one honest caveat line. Do NOT re-dump the hedged report — the hedging lives in the report, not in the follow-up answer. Category-split verdicts ARE the honest decisive answer when no single model wins everything; a tie verdict is acceptable only when the data genuinely supports it (e.g. "capability tied across two runs — DeepSeek faster/leaner, Hy3 cheaper, neither reliable winner on the one stochastic failure"). G values sharpness over thoroughness on the follow-up.

## References
- `references/worked-example-dsv4p-vs-hy3.md` — full worked example (dated snapshot, Aug 2026): specs, independent tables, CAISI verdict, session artifacts to copy.
