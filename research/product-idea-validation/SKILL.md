---
name: product-idea-validation
description: "Orchestrate a full go/pivot/kill validation of a product or business idea before any code is written — check first-hand evidence, dispatch three parallel research lanes (demand, competitive+IP, legal/regulatory), consolidate into a decision memo, and file it durably in the product-brainstorm Home Base. Use when the user brings an idea and asks whether it's worth pursuing, whether the market is real, or for 'market research validation'. This is the ORCHESTRATOR; the demand lane's method lives in buyer-demand-validation."
platforms: [macos, linux, windows]
---

# Product-Idea Validation (orchestrator)

Idea in → **go / pivot / kill** verdict out, evidence-backed and filed. The user is a
strategist, not hands-on: he defines the goal, you do the ground work, he decides.

## Sibling skills — do not duplicate them
- **`buyer-demand-validation`** — the *method* for the demand lane (evidence hierarchy, WTP
  anchoring, the regulation device-class/actor/trigger decomposition, TAM denominator discipline).
  **Load it before writing the Agent-A brief.** Do not re-derive it here.
- **`market-research-scrape-synthesis`** — the corpus/scrape pipeline and subagent dispatch
  discipline. Use when the input is many raw artifacts rather than a stated concept.
- **`demand-signal-mining`** — bottom-up coding of marketplace demand artifacts.

This skill owns only what those don't: **the three-lane fan-out, the first-hand-evidence
precheck, the decision-memo shape, and the filing convention.**

## Step 0 — Check first-hand evidence BEFORE dispatching (highest leverage)
If the idea rests on a specific technology, repo, or tool, check whether **we have already
touched it**: `skills_list` → `skill_view` any relevant skill → `session_search`.

Worked example: the WiFi-CSI room-sensing idea died fastest not on market data but on our own
prior deployment, which showed the upstream accuracy claims were **retracted** (pose: claimed
92.9%, real held-out ≈19%; vitals endpoint returns simulated data without hardware). Surface
this to the user in your first reply, before the agents return. **First-hand evidence outranks
any web-sourced market claim.**

Also check for **existing sibling skills before creating a new one** — the first version of this
skill was created without that check and overlapped three existing research skills. Apply Step 0
to yourself, not just the research.

## Step 1 — Dispatch three parallel lanes
Always three, always one `delegate_task` call with a `tasks` array (no top-level `goal`).

1. **DEMAND** — brief it from `buyer-demand-validation`. Who pays today, documented dollar cost
   of the pain, per-segment WTP, what regulation *literally* mandates, procurement reality.
2. **COMPETITIVE + IP** — every incumbent by name: what they do, hardware needed, public pricing,
   funding/stage, logos. Then **patent/FTO risk** and any **standard that may commoditize the
   core**. Explicitly demand *dead and pivoted-away* competitors — highest-signal findings.
   Also ask directly: *is the gap technological, or merely channel?*
3. **LEGAL / REGULATORY / RISK** — the kill-shot lane. Privacy law, sector regulation, **platform
   policy** (app stores, Airbnb, marketplaces — these close channels overnight), medical-device
   or licensing triggers, liability if the product fails at its claimed job, and **real backlash
   precedent**. Must end naming the **least-friction segment**.

### Put in every context block
> No citation, no claim. Every assertion carries a source URL you actually fetched. Prefer
> primary sources. Flag guesses, pre-2023 data, and contradictions rather than smoothing them.
> If a number isn't obtainable, leave it blank — do not estimate.

Plus: analyse segments **separately, never blended**; state the output file path; and the user's
language/tone requirements. Subagents cannot use `clarify` — pre-load every constraint.

## Step 2 — While they run
Don't idle. Deliver the Step-0 first-hand reality and a one-paragraph method note. Then stop.

## Step 3 — Consolidate
**Verify files exist on disk (`ls`) — subagent self-reports are not proof.** One agent reported a
mid-write stall; the file had in fact been written correctly.

Memo structure that worked:
1. **VERDICT in the first line** — kill / pivot / go, plainly
2. **Numbered kill (or risk) factors**, each *independently sufficient*
3. **Market reality** — price ceiling, consolidation, regulation-is-not-your-tailwind
4. **Surviving wedges** — usually from findings the user *didn't* ask about
5. **Recommended next step** — 2–3 concrete options, your pick marked
6. **"Research quality notes — things I will not pretend are solid"** — contradictions, unusable
   TAMs, unsourced claims, unverified vendors. The user values this section specifically.

## Step 4 — File in Home Base (without being asked)
```
~/hermes-home/product-brainstorm/02-market-research/<idea-slug>/
  README.md            # verdict + file guide + "do not reuse these claims" + method note
  DECISION-MEMO.md     # start here
  AGENT-A-DEMAND.md  AGENT-B-COMPETITIVE.md  AGENT-C-LEGAL.md
```
Then **update `product-brainstorm/INDEX.md`**: bump `_Last updated:_` and add the entry under
`## Validated-negative (closed, do not re-litigate without new evidence)` for kills, or
`## Active research streams` for go/pivot. **An unindexed folder is a lost folder.**

## Pitfalls
- **Don't leave outputs in `~/`.** Subagents default to the home dir. Move them, then verify.
- **Kill findings are wins.** Frame as "one idea validated-negative, cheaply, before any code."
- **Keep chat terse** (context hygiene): detail to files; chat carries verdict + reasoning spine
  + what's new only.
- **The legal lane usually decides surveillance/health/fintech ideas** — never treat it as the
  optional third wheel. Platform policy alone (e.g. Airbnb's indoor-device ban) can close a
  whole channel independent of law.
- Don't push third-party installed skills as your own work; check authorship, not file mtime.
