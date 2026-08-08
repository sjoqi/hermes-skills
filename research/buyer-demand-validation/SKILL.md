---
name: buyer-demand-validation
description: "Validate and size buyer demand for a product concept across named B2B/B2C segments using public sources — vendor pricing pages, government reports, statutes, investor filings, trade associations. Covers the evidence hierarchy, per-segment WTP anchoring, checking whether regulation actually forces the purchase, adoption-velocity proxies, denominator discipline for TAM, and source-quality grading. Use when the user asks 'is there real demand / will anyone pay / how big is this' for a product idea, as opposed to coding a corpus of raw demand artifacts (that is demand-signal-mining)."
platforms: [macos, linux, windows]
---

# Buyer-Demand Validation (top-down, public sources)

Answers **"will these buyers actually pay, how much, and who signs"** for a product concept, from public evidence. Output is a structured findings doc where every claim carries a fetched URL and every gap is flagged rather than filled.

## When to use vs. sibling skills
- **This skill:** top-down. Named segments already hypothesized. Evidence = vendor pricing pages, statutes, gov reports, 10-K/investor relations, trade-association data.
- **`demand-signal-mining`:** bottom-up. Coding a longitudinal corpus of raw demand artifacts (job posts, RFPs, complaint threads) with P/S dual scoring.
- **`market-research-scrape-synthesis`:** the file-layout + subagent pipeline for large scrapes. Borrow its "keep bulk on disk, pass file paths" discipline for long runs.

Use them together when the user has both a concept and a corpus. This skill's output is a *decision doc*; that one's output is a *corpus*.

## The evidence hierarchy — spend your budget top-down

Rank every source before citing it. Most of the value comes from tiers 1–2.

| Tier | Source | Why |
|---|---|---|
| **1. Vendor public pricing page** | Exact per-unit price, billing period, what's gated to which tier | **The single best WTP evidence that exists.** A published price is a company betting revenue on that number. |
| **1. Government / regulator report** | Incidence counts, aggregate cost, compliance failure rates | Methodologically disclosed, citable, recent, no incentive to inflate |
| **1. Statute / legislation text** | What is *actually* mandated | Vendor blogs paraphrase statutes wrongly and self-servingly |
| **2. Public-company IR / 10-K** | ARPU, units deployed, ARR, direction of travel | Audited. But read the units carefully (see pitfalls). |
| **2. Trade association** | Denominators (property counts, member counts), adoption stats | Good for TAM denominators; note it advocates for members |
| **3. Vendor blog / competitor comparison** | Directional pricing, regulatory summaries | Useful but self-interested and often stale — always flag |
| **4. Law-firm marketing, coaching blogs, syndicated report mills** | Anecdote only | Cite only with an explicit low-confidence flag |
| **5. Reddit / Facebook / forum** | Counter-signals and objections | Genuinely useful for *disconfirming* evidence; never for sizing |

**Pricing pages are the highest-leverage single fetch in this entire method.** Before anything else, find the two or three incumbents in each segment and pull their pricing. If pricing is demo-gated, that is itself a finding (enterprise motion, opaque, slow) — record it as such rather than guessing a number.

## Core moves

### 1. Never blend segments
Produce a per-segment table: budget exists Y/N, validated WTP, price unit, procurement friction, verdict. Averaging a $10/unit/mo self-serve segment with a $406/unit/yr enterprise-bundle segment produces a number that describes no real buyer. State explicitly in the doc that economics are deliberately not blended.

### 2. Check what regulation LITERALLY mandates — device class, actor, and trigger
This is the highest-value check in the method and the one most likely to overturn the user's thesis.

"Regulation is forcing purchases in this market" is usually true *and usually irrelevant*, because the statute mandates a **different product** than the one being considered. Decompose every mandate into:
- **Device/service class** — wearable? fixed? software? certified to a standard?
- **Actor** — who must be equipped (employees? residents? rooms?). This sets the *purchasing denominator*, which is often not the one the user assumed.
- **Trigger** — human-activated, or passive/automatic?
- **Threshold** — property size, headcount, jurisdiction.
- **Penalty** — the actual dollar cost of non-compliance.

Worked example: US hotel panic-button laws (IL/WA/NJ/Chicago/Seattle/CA cities) genuinely force spend, with fines from $25/day to $10k/infraction. But every statute specifies a **wearable, worker-activated device reporting real-time location**, priced **per lone-worker employee**. A passive room sensor satisfies none of them and would be priced per room. The regulation is real; the tailwind is not. → Verdict: *treat regulation as proof the segment will spend on safety, not as a tailwind you can ride.*

Also hunt the **inverse**: guidance that a passive product *could* satisfy. UK HSE guidance recommends "automatic warning devices which trigger if specific signals are not received periodically from the lone worker" — a dead-man check, which passive sensing fits. Guidance is weaker than a mandate, and certification (e.g. BS 8484 + Alarm Receiving Centre connection) may be required to sell it as compliance. Flag as a legal-review item, not a finding.

### 3. Use the pledge-vs-implementation gap as an adoption-velocity proxy
When a trade association publishes both "N companies pledged" and "M properties implemented," the ratio and elapsed time are a hard, citable measure of how fast that segment adopts. Example: ~20,000 hotel properties pledged in Sept 2018, ~5,000 implemented — **~25% over ~7 years, on a legally mandated, association-backed category.** That single ratio is more decision-useful than any sales-cycle estimate, and it is *sourced*, where the sales-cycle number would be a guess.

### 4. Establish the denominator before producing any TAM
If you cannot source the unit count (listings, beds, rooms, units), **do not produce a TAM dollar figure.** Write the price anchor, name the missing denominator, and put it in the open-questions list. A TAM built on a guessed denominator is worse than no TAM because it gets quoted downstream. Say so explicitly in the doc.

### 5. Distrust syndicated market-size reports; cross-check the publisher
Report-mill sites (marketintelo, similar) will happily size two overlapping definitions of the same market at different values for the *same year* — e.g. "Wi-Fi Sensing $1.2B (2025)" and "IEEE 802.11bf Sensing $2.3B (2025)" from one publisher. When you catch this, say so in the doc and mark the numbers unusable for a deck. They establish only that analysts believe the category grows.

Prefer a bottom-up build: verified denominator × verified price point. Named analyst houses (ABI, Gartner) are better, but **only cite figures you actually read** — if you retrieved a PDF's title but not its body, say that and cite no numbers from it.

### 6. Hunt the free incumbent that suppresses WTP
Before pricing a prevention product, ask what the buyer already gets for nothing. Airbnb's AirCover gives hosts **$3M damage protection + $1M liability, free, automatically**. That structurally caps willingness to pay for damage prevention regardless of how real the damage is. The equivalent question in any segment: *is a platform, insurer, or regulator already absorbing this risk at zero marginal cost to my buyer?*

### 7. Reconcile pain-cost contradictions before pricing
Expect gross-loss figures (surveys) and net-recovery figures (operators) to disagree by an order of magnitude — e.g. "$1,560 average damage per party incident" (survey blog) vs "most approved claims land $200–400" (operator with 800+ listings, 300+ filed claims). Both can be true; they measure different things. Present both, name the discrepancy, and take the **operator/net figure** for ROI math. Combine with the base rate (<0.1% of stays) before asserting an ROI pitch works.

### 8. Look for the wedge the incumbents don't sell
The most valuable output is often not in the user's question. Read the *failure modes* in your sources: the #1 documented reason damage claims get denied is "inability to prove the guest caused the damage" → a timestamped occupancy log is a **claims-evidence** product, not a prevention product, and no incumbent leads with it. Likewise a government finding that "nursing homes failed to report 43% of falls with major injury" is a documented, publicly-visible compliance gap → an automatic objective log addresses a *star-rating* problem, which is sharper than "peace of mind."

Rule: **compliance-gap and evidence-generation wedges beat prevention wedges**, because the buyer's loss is legible, attributable, and already being measured by someone else.

### 9. Map procurement, and refuse to guess the parts you can't source
For each segment capture: who signs, self-serve vs. committee, integration/certification requirements and their *cost*, and gatekeepers. Integration cost is frequently the real barrier and is usually documented — e.g. Oracle OPERA: OPN membership $500/yr for Cloud/OHIP, **plus a $3,000/yr "License & Hardware" track for OPERA 5/Suite8**, and *"Oracle may also require a hotel customer ready to justify the integration"* — a chicken-and-egg trap for a solo founder.

If sales-cycle length or the signing role isn't sourced, write "⚠ not validated in this pass" rather than a plausible number. Substitute a sourced proxy (move 3) where one exists.

### 10. Close with a source-quality ledger and an open-questions list
End every doc with: primary/high-confidence sources, secondary/medium, low-confidence/flagged, and **fetch failures** (blocked URLs, paywalls) with what could not therefore be verified. Then an explicitly numbered open-questions list. This is what makes the doc trustworthy and re-runnable.

## Document structure that works

1. **Bottom line up front** — per-segment verdict table, then the single most important finding (especially if it overturns the user's hypothesis).
2. One section per question asked, in the user's order and numbering.
3. Inline `⚠` flags on every weak, dated, or self-interested source — at the point of use, not collected at the end.
4. **Synthesis split three ways:** what the evidence *supports*, what it *contradicts*, strategic implications.
5. Open questions requiring a follow-up pass.
6. Source-quality ledger.

Write it to a file. Give the user a tight chat summary (headline findings, contradictions, blockers) — not the whole doc pasted back.

## Pitfalls

- **Assuming "regulation exists" means "regulation forces MY product."** The single most common and most expensive error. Decompose device class / actor / trigger (Move 2).
- **Misreading ARPU units.** SmartRent's $406 is **per unit per YEAR, bundled across hardware + all services**. Dividing to "$34/mo" and comparing against a $10/mo point-solution is wrong. Always confirm period and scope, and check *direction*: that ARPU was **down 10% YoY with ARR shrinking** — a category under pricing pressure, which is a material finding on its own.
- **Producing a TAM from a guessed denominator.** Leave it blank and say why (Move 4).
- **Citing syndicated report-mill numbers as fact.** Cross-check publisher; note contradictions (Move 5).
- **Citing a PDF you retrieved but did not read.** Say "URL and title retrieved, body not extracted, no figures cited from it."
- **Claiming insurance-premium savings without a carrier source.** This is the standard unevidenced claim in every sensing/safety category. If no insurer document is found, write "NOT VALIDATED — do not put in a pitch deck without written carrier confirmation."
- **Silently dropping segments you couldn't research.** If student housing and hospitals were in the question and you found nothing, say "entirely unresearched in this pass" — do not let their absence read as a negative finding.
- **Trusting a vendor blog's "currently no statewide law."** Regulatory summaries on vendor sites go stale. Flag jurisdiction claims for re-verification and prefer statute text or a law-firm client alert with a date.
- **Ignoring the incumbent's own marketing as evidence.** When a competitor leads with exactly the arguments the user plans to use ("nobody wants to be watched," "who wants wearables?"), that is *validation of the framing* and simultaneously *proof the position is taken*. Report both halves.
- **Skipping the technical-feasibility risk in a demand doc.** If the highest-WTP segment is defended by purpose-built hardware (e.g. 4D imaging radar) and the user's concept uses a commodity signal, price that into the recommendation. Demand validation that ignores whether the product can meet the segment's accuracy bar is incomplete.
- **Letting a compelling anecdote become a market.** A vivid story (body found in a hotel room months later) with no frequency dataset behind it is demo material, not a line item. Say "no dataset found quantifying this; any TAM built on it is a guess."
- **Reporting the biggest segment as the beachhead.** Rank by *procurement friction* for a solo founder, not by market size. Self-serve + published pricing + single signer beats large-but-gatekept every time.
- **Omitting the realistic ceiling.** If the validated price point and plausible unit count imply a $100–300k ARR micro-SaaS rather than a venture outcome, state it plainly. Users make worse decisions when the ceiling is left implicit.

## Rate limits and fetch discipline

Search backends rate-limit under parallel fanout. Batch independent searches 2–4 at a time rather than 5+, and on a rate-limit error sleep ~60–70s and retry — the queries are fine, the pacing isn't. Never let a rate-limit failure become "I couldn't find data on X"; retry, then flag only if it genuinely returns nothing.

When a pricing page is blocked or errors, fall back to a competitor comparison page but **flag that the vendor's own pricing was not independently verified**.

## Reference

`references/privacy-sensing-buyer-demand-2026.md` — worked example: full segment findings for no-camera in-room occupancy/vitals sensing (hotels, STR, multifamily, senior living), including the verified panic-button statute table, WTP anchors, and the procurement blockers. Useful as a model of the output shape and as live data on adjacent proptech/safety segments.
