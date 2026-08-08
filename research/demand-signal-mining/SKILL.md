---
name: demand-signal-mining
description: "Turn raw marketplace demand evidence (Upwork/Fiverr/Contra job posts, job boards, RFPs, forum complaints, review-site 2-3 star gripes) into a coded, longitudinal corpus that can support a real business decision — productized product vs specialized service. Covers the capture workspace layout, a stable coding scheme, dual-track scoring, selection-bias discipline, and when it is legitimate to draw a conclusion. Use when the user is doing market research by collecting real demand artifacts over multiple sessions."
platforms: [macos, linux, windows]
---

# Demand-Signal Mining

Longitudinal market research from **real demand artifacts** — job posts, RFPs, complaint threads — rather than from opinion or market-size reports. The user dumps evidence over many sessions; you maintain the corpus and the analysis.

## When to use
- User says they're "scraping/browsing job posts to see what the market wants", doing "market research", "finding pain points", "seeing what people will pay for".
- User is choosing between **building a product** and **selling a service**, and wants evidence.
- Any multi-session collection where individual items are near-worthless but the aggregate is the point.

**Not this skill — route to `buyer-demand-validation` instead** when the segments are already named and the question is top-down ("will hotels/landlords/clinics pay for X, how much, how big is it, who signs"). That work is answered from vendor pricing pages, statutes, government reports and investor filings in a single pass, not from coding a corpus of artifacts over many sessions. The two compose: this skill builds the corpus, that one validates a concept against public evidence.

## The core design decision: score every item TWICE

Most such research quietly collapses into "there is demand for X", which supports no decision. Two strategic bets need *opposite* evidence:

| Track | Bet | Evidence that supports it |
|---|---|---|
| **P — Productized** | Build once, sell many (SaaS/template/plug-and-play) | **Sameness + frequency.** Same problem, same shape, many buyers, low per-client customization. Interchangeable connectors. |
| **S — Specialized service** | Become the expert for one painful problem | **Budget + pain depth.** Rare is fine. Expensive, domain-specific, buyer pays a premium for proven competence. |

Score both 1–5, **always with a one-line reason**. Items scoring high on P are frequently *bad* S candidates and vice versa. A single blended "opportunity score" destroys the entire value of the exercise — never create one.

## Workspace layout

Create under the user's notes/research home (e.g. `~/hermes-home/product-brainstorm/02-market-research/<source>/`):

```
README.md          purpose, workflow, capture filter, bias warnings
RAW-JOBS.md        append-only raw dump, batched by date + SEARCH TERMS USED
JOBS-TABLE.md      normalized one-row-per-item table + verbatim quotes section
CODING-SCHEME.md   the stable tag vocabulary
PATTERNS.md        running tally, updated at each review
SUMMARY.md        compressed synthesis (pattern table, P/S read per cluster, contradictions resolved, gaps to fill) — written proactively for resumption after chat compression, not only at the end
```

A ready-to-adapt coding scheme lives in `references/coding-scheme-template.md`.
Worked examples of high-signal reads live in `references/signal-reading-playbook.md`.

Wire the folder into the parent `INDEX.md` immediately so it doesn't orphan.

## Workflow
1. User dumps raw items (any format, messy is fine). Never make them format anything.
2. You append **verbatim** to `RAW-JOBS.md`, then normalize into `JOBS-TABLE.md` with tags.
3. Every ~20–30 items: update `PATTERNS.md`, then brainstorm.
4. At ~50+ items: the corpus can support a real decision → write to `04-decisions/`.

## Non-negotiable capture rules

**Record the capture filter, in the artifact, not just in chat.** If the user only logs posts above $100, or only ones they find "interesting", every frequency count is conditional on that. Put it in the table header. Otherwise a future session will mistake the user's taste for market frequency.

**Expect duplicates; enrich, never re-add.** Marketplace feeds recycle posts, and a re-encounter often carries fields the first sighting lacked (activity panel, skill tags). Tell the user to dump anything that looks familiar anyway — you dedupe. Merge new fields into the existing item, add a dated "re-encountered" note, and keep the unique-item count explicit in every reply so the corpus size never silently inflates.

**Log the search terms per batch.** You only see what was searched. A week of "n8n automation" searches concludes n8n is the market — that's search history, not reality.

**Capture the buyer's pain in their exact words, unedited.** Do not summarize it away. Their phrasing is the highest-value artifact in the whole corpus — it becomes landing-page copy, cold-outreach language, and positioning. Maintain a dedicated verbatim-quotes section.

**Quote the throwaway line, not just the requirements list.** The spec says what they want built; a stray clause says what they're afraid of. "so leads aren't silently missed" is the product promise. "This is not a generic ChatGPT integration" is a buyer who has been burned. These are worth more than the bulleted scope.

## Analytical discipline

**Frequency ≠ opportunity.** A pain appearing constantly on a freelance marketplace often means it is *commoditized and cheap*, not lucrative. High proposal counts mean high demand AND brutal competition.

**For the specialist track, hunt high budget + LOW competition.** That combination signals a problem most freelancers cannot solve. High-budget + high-proposals is just a popular auction. **But low competition is ambiguous** — it equally marks a job the competent have read and declined. Always cross it with the scope/price ratio and the unanswered-invite count before treating it as opportunity (see Move 12).

**Deliberately log contrast cases.** A corpus of only high-P items cannot distinguish "this is the market" from "this is what I collect". An n=1 personal workflow, or an item that scores low on both tracks, is worth logging precisely because it sharpens the boundary of the cluster. Note explicitly *why* it fails to fit.

**Name hypotheses explicitly, early, as falsifiable statements.** Write "H1: ... If true → Track P" into the notes as soon as a shape appears. This makes later evidence a *test* rather than accumulating confirmation. Actively ask the user for items that would break the current hypothesis — the disconfirming dump is worth ten confirming ones.

**Record contradictions and surprises in their own section.** They are the most useful entries and the easiest to unconsciously discard.

**Watch for value/price inversion.** When the technically hardest ask carries the lowest price, that is not stingy buyers — it is a market with **no price anchor**. This argues for a product (buyer pays $49–99/mo willingly) over a service (buyer underprices it at $300). It is one of the strongest signals available; call it out when it repeats.

**Tag every item by whether failure is REGULATORY or merely INCONVENIENT.** In one corpus this single variable predicted price better than tool choice, technical difficulty, buyer sophistication, or competition: the same job shape (fix a half-built broken automation) went for **$100** in a lead-gen agency and **$2,500** in regulated disability care. Where a broken workflow means an audit finding, a funding clawback, or a harmed person, buyers fund the work properly. "Same skill, regulated vertical" is usually a larger and cheaper win for the user than "more skill, same vertical" — surface it whenever a second regulated item appears.

**Separate tool moats from domain moats when explaining low competition.** A single hot, uncommoditized tool named in a title collapsed proposals from 50+ to <5 for near-identical work. That is real pricing power *today*, but it decays as adoption spreads. Domain moats (regulation, language, an API-less last mile) are expensive to acquire and durable. Both look like "low competition" in the data; say which one an item is. And note the corollary: **a moat only suppresses competition when it is legible in the posting** — the most regulated item in that corpus drew 50+ bidders because its niche was invisible in the title.

**Capture where the human stays in the loop.** Sophisticated buyers across unrelated industries independently specify it — escalation with handoff, approval gates, "what stays human-reviewed", AI-suggests/human-confirms. Treat it as a first-class field beside the pain quote: it is simultaneously a design requirement and the user's positioning language. Best phrasing seen: *automate the repetitive technical work, never the judgment.* Record whether the gate is **fixed or graduating** — buyers who ask for "approval now, automatic later" are describing a trust ramp, which is a product design requirement (Move 22).

**Distrust the category name; read the money.** A corpus collected under a hot search term will *look* like that category's market. Where an item exposes internal budget allocation (per-milestone pricing), use it — it is the most honest data available. In one corpus the best-funded, most competent project put **12% on AI and 79% on integration, data modeling, and dashboards**, despite "AI automation" being the search term that found it. Correct the narrative when the money disagrees with the label (Move 23).

**State the channel's structural bias before concluding anything.** Freelance marketplaces systematically under-represent high-value work, which is bought by referral and never posted. Conclusions will be sound at the commodity end and incomplete at the premium end. Say so rather than over-claiming, and propose supplementary channels (agency pricing pages, communities where those buyers complain) for the premium end.

**Reduce saturated clusters to a primitive, then steer at the gaps.** When one category passes ~30% of the corpus, further members stop informing. Strip the connectors away and name the smallest behaviour every variant pays for — in one corpus, nine lead-handling items reduced to *non-response detection and the nudge that follows*, since capture itself was already free. Then redirect the user's collecting toward the corpus's empty cells by name (unobserved price bands, absent pain categories, the variable that best predicted price) rather than asking for more of the same (Moves 26–27).

**Copy any worked input→output example verbatim, and classify the output.** Rare and disproportionately valuable — it is an acceptance test the customer wrote for free. Then ask whether the output is a *score* (Hot/Warm/Cold → commodity, competes with free) or a *typed domain schema* (buyer/seller/landlord/tenant; property type, budget, timeline → the vertical wedge). Industries with an industry-standard schema are the strongest productization candidates because the data model is identical for every buyer in the vertical (Move 29).

**Record whether buyers want autonomy or a checkpoint — they consistently want the checkpoint.** Across one 24-item corpus, 30% of buyers specified a human review gate and *none* asked for full autonomy; the clearest stated it as "the golden rule … rather than fully autonomous fire-and-forget." Sophisticated buyers want leverage with a checkpoint. Two consequences: an offer premised on "more autonomous = more valuable" argues against the evidence, and every HITL buyer independently needs the same missing component — **a staging/review queue** — which is an underserved productizable seam (Move 30).

**Note the hire/budget inversion on freelance marketplaces (Move 32).** The posts that actually *hire* (Hires:1) in one 34-item corpus were all ≤$600; the highest-budget generics (≥$1.5k) sat at 50+ proposals with **zero interviews** and went stale — the buyer either paralysed or hired off-platform. High Upwork budget is therefore a *weakness signal* for conversion, not a strength. Pair with Move 30: what converts is a decisive, crisp scope (and often an active, screening buyer), **not** budget. Directionally strong at n=6 hires with a clean split, but state it as directional — a couple of high-budget hires would reopen it.

**Refine the hire rule with scope clarity (Move 32-b).** Price alone is not sufficient. Across one 43-item corpus, every actual hire (5 of them, all ≤$600) had **clear, bounded scope** even at $100 — whereas a low-budget post with **unbounded/impossible scope** ("autonomous AI platform… automates the entire workflow start to finish," $280) drew only 1 interview and did *not* hire. → **low budget + clear scope = fast hire; low budget + vague/impossible scope = no hire.** Scope clarity predicts conversion alongside price, so when a cheap post stalemates, check scope before concluding "the market won't pay."

**Track the "database" layer buyers actually choose (Move 33).** Across corpora, SMB automation buyers overwhelmingly pick a spreadsheet or Airtable as the system of record over a real CRM (HubSpot/Salesforce). The product surface for this market is spreadsheet-first; model the data layer accordingly, and treat "Google Sheets as CRM / single source of truth" as a deliberate, repeatable buyer choice rather than naivety.

**Retract single-point scarcity/moat inferences when contradicted (Move 34).** One post with a specific stack drew unusually low competition; a second with the *same* stack drew 50+. The first was the outlier, not the pattern — GHL+n8n is NOT a reliable scarcity signal at the low tier. Only a clean, *repeated* effect (one named tool collapsing proposals to <5 across independent posts) earns a moat claim. When a contradicting item appears, say so plainly and withdraw the earlier inference; do not let it linger as a "finding."

**Track recurring language-specialization signals as their own moat class (Move 35).** A buyer who requires a *specific language* (Arabic for MENA customs/consultancy, multilingual EN/FR/DE/ES for localized content, Arabic + multilingual for healthcare/UAE) is naming a barrier most automators cannot fake. It behaves like a domain moat: it suppresses capable competition even when the rest of the stack is generic, and (unlike a hot tool) it does not decay as adoption spreads. When the *same* language recurs across independent posts (e.g. Arabic in two unrelated verticals), promote it from "one-off quirk" to "recurring niche" in the synthesis — it is a durable specialization signal, distinct from tool scarcity.

**Flag data-capture artifacts in pasted job text (Move 36).** When a pasted "job summary" contains a stray paragraph that is clearly the marketplace's own UI/platform copy rather than the buyer's words (e.g. an editorial aside about what kind of portfolios to filter for), log it as a **capture artifact, not buyer intent**. The real buyer signal is absent; the leaked text is noise. Do not score or quote it as if the buyer wrote it. Treat any first-person helper note, meta-commentary on the posting process, or formatting that doesn't match the rest of the listing as suspect, and note it for methodology rather than analysis.

**Treat design/quality-gate moats as a distinct class from tool or regulatory moats (Move 37).** Some buyers require a *judgment* skill no generalist can fake: graphic-design fundamentals (layout/typography/composition) for creative automation, voice-preservation ("rewrite as if it's from me") for owner-operator comms, RAG-accuracy ("answers must be accurate, not generic") for support. These are taste/quality barriers — real, but *learnable* and non-licensed, so they sit below hard regulatory moats (NDIS/customs/TCPA) in durability. Classify each moat as **regulatory / language / tool-scarcity / design-quality / last-mile-integration** and say which one an item is before asserting defensibility; conflating them overstates the moat.

**Track telecom-compliance as a cross-border defensible specialization (Move 38).** Within one corpus the *same* shape (an AI voice/SMS agent for local businesses) surfaced two different national regimes: **US TCPA** (consent capture, DNC scrubbing, call-window, state AI-disclosure, two-party consent) and **Canada CASL** (anti-spam consent for outbound SMS) — plus **A2P 10DLC** carrier registration underneath both. When a second jurisdiction's regime appears, promote telecom-compliance from "one regulated post" to a *repeatable cross-border niche*: the buyer screening on "how do you keep outbound SMS compliant for Canada?" is paying for knowledge most automators lack, and it transfers across clients within that jurisdiction. This is the regulatory-moat class (Move 20/37) made operational for the voice/SMS builder — fold it into the same cluster as NDIS/customs, and note a *jurisdiction stack* (US + CA + 10DLC) is a stronger, more durable moat than any single country's rule.

**Capability-specificity suppresses competition at ANY price — retire "low budget = crowded" (Move 39).** Across one 46-item corpus, generic low-budget posts drew crowds while *specific* low-budget posts drew almost none, at the same $200: a generic n8n catch-all drew 50+ (UW-033) and a generic GHL job 50+ (UW-035), but a **specific** $200 post — multi-brand social publishing + ads with named platforms and 3-brand separation (UW-046) — drew only 5–10, and a **specific** $200 voice+TCPA-compliance agent (UW-039) drew 15–20. Earlier single-point scarcity effects (Clay <5 at UW-012; a GHL post at 15–20 at UW-034) resolve into one rule: **supply narrows on capability specificity, independent of price.** A buyer who names a concrete, non-generic problem filters to the few who have built it; a buyer who names only "n8n automation" invites the whole crowd. So a low proposal count at a low price is NOT automatically "the competent declined" (Move 12) — check whether the scope was specific. Pair with Move 32-b: the conversion rule is *low budget + clear specific scope = fast hire*; the competition rule is *specific scope = few bidders regardless of budget*. Both are the same mechanism, observed from two sides.

**Note when buyers treat components as interchangeable.** "OpenAI, Claude, or Gemini" / "HubSpot, GoHighLevel, or Airtable" / "n8n, Make, or Zapier, whichever you recommend" — three buyers, three layers, all declared fungible. Buyers are not purchasing intelligence, they are purchasing wiring that does not break. Building *on* a component the buyer has already called swappable is not a moat, and a tool-agnostic buyer is a **product** customer rather than a build customer (Move 28).

## Reporting style for the per-item response

The user is dumping in a loop. Keep each response **short and additive** — they are not reading an essay per item.

- Confirm logged + the two scores + one-line reasons.
- Surface the single most interesting line in the item, quoted.
- Note only what *changed* about the picture (new pattern, streak broken, hypothesis strained).
- Do NOT re-summarize prior items every turn.
- Do NOT declare conclusions from a handful of items — say plainly that N items is still an anecdote.
- End with a specific ask for the next dump that would most improve the corpus (a missing field, a price band never yet seen, a disconfirming category). Ask for the gap, not "keep going".

## Manage your own context during long dump loops

This is a **many-item, single-session loop**, which is exactly the shape that degrades an agent's judgment. Each item adds the raw paste, the tool calls, and your commentary. By item 6 the context is large and the analysis gets mushy and repetitive — the failure mode is producing longer, more confident, *worse* reads while feeling productive.

Discipline:
- **The files are the memory, not the conversation.** Once an item is written to `RAW-JOBS.md` / `JOBS-TABLE.md`, stop carrying it in your replies. Never re-derive the whole picture each turn.
- **Per-item replies should get shorter as the corpus grows**, not longer. Early items justify some framing; by item 5+ it should be a few lines.
- **Batch the writes.** One patch to the raw file, one to the table, per item. Do not fan out into many small edits.
- **Push the heavy analysis to subagents.** The periodic `PATTERNS.md` review and the final synthesis are large reasoning jobs over material already on disk — delegate them with file paths rather than doing them inline in a saturated context.
- If you catch yourself restating earlier items to sound thorough, that *is* the degradation. Cut it.

**Context management — the token limit is AUTOMATIC; do not block on it (corrected Aug 2026).** Hermes auto-compresses with no user action required: the agent `ContextCompressor` fires at **50%** of the model window (configurable via `compression.threshold` in config.yaml; G runs 0.5 with `target_ratio: 0.4`, landing ~20% of window), and a gateway **session-hygiene** safety net fires at **85%** using a rough estimate — that one can look like a bigger drop (~40-50%). There is no "/compress" command to press. Implications:
- You do NOT need to stop the loop or tell the user to manually compress for the token limit. They observed the auto-drop firsthand and corrected an earlier wrong model that said otherwise.
- The compressor is **lossy**: it summarizes the MIDDLE, keeping the first 3 + last `protect_last_n` (default 20) messages verbatim. Over a very long session, early specifics degrade — that is the only real cost.
- Therefore `SUMMARY.md`'s real purpose is **cross-session persistence** (it survives `/new` and compression because files on disk are never summarized), NOT staying under the limit. Still write it at natural breakpoints / before any `/new`, but never frame it as the crash-avoider.
- Keep the BULK of raw data in files on disk (RAW-JOBS.md etc.), never in the chat stream — files are immune to the context engine and to compression. This is the primary lever; auto-compression is the backstop.
- The user can freely continue a long "dumping" session; just keep pushing heavy analysis to subagents and keep per-item replies short so the recent-20 tail stays useful.

**Proactive synthesis at natural breakpoints (not as a crash-avoidance step).** Write a compressed `SUMMARY.md` (pattern table, P/S read per major cluster, contradictions resolved, specific gaps to fill) whenever the corpus crosses a review milestone or the user is about to end/resume — not because the window is full, but so the next session has a sharp on-ramp. Confirm working files are current. Resume from `SUMMARY.md` + tables; the conversation history need not be re-read.

Users notice sharpness loss before you do. One flagged it directly: *"the more build up tokens the more you're likely to have a kind of slop judgement, you can always spawn agent if that helps, i want you to stay sharp."* Treat sustained sharpness as part of the deliverable — use subagents for the heavy reasoning, keep the chat lean.

## Pitfalls
- Letting the user's implicit filter become an invisible assumption. Always surface it.
- Paraphrasing the pain quote. Destroys the most valuable field.
- Blending P and S into one score.
- Concluding at n=3 because a streak looks strong. Name it as a hypothesis instead.
- Treating a `contract-to-hire` / "trial project" flag as a great signal — with heavy competition and no interviews it is often a way to get production work cheap. Note it skeptically.
- Reformatting or "cleaning" the user's dump before saving. Save raw, normalize separately.
- Forgetting a `reliability/ops` pain category. Marketplace corpora fill up with *broken existing automation*, not just greenfield builds; without the tag that whole cluster hides inside other categories. Same for a `fix-repair` job shape.
- Omitting the activity panel (proposals / interviews / invites / hires) from the capture list. It is often more informative than the description — see Move 9 in `references/signal-reading-playbook.md`.
- Scoring an item high on S because the *post* is impressive. A demanding buyer with no stated budget is a common trap; band it `b0` and say the budget is unconfirmed rather than inferring wealth from good writing.
- Letting one articulate post dominate the read. Well-written ≠ representative.
- Reading a low proposal count as a rare-skill signal without checking scope/price. On a cheap marketplace it usually means the competent declined (Move 12).
- Missing that the buyer specified *product properties* (multi-tenancy, runtime config, "without developer assistance", handover docs). That buyer is trying to end their dependence on a contractor — strong Track-P datum, Track-S warning (Move 13).
- Ignoring mismatched skill tags. Tag/description mismatch measures **buyer competence**; where buyers can't tell a durable build from a brittle one, quality cannot be priced (Move 14).
- Only tallying the presence of the dominant theme. Its **absence** in the item that most warrants it marks a pre-burn naive buyer, a distinct segment worth tracking (Move 15).
- Missing the item posted by someone **already running the business model under evaluation** (an agency subcontracting its delivery work). That item is a direct price quote on the user's own proposed labour, and usually reveals that margin sits with client ownership rather than technical skill (Move 16). But do not generalize from **one** such item — agency delivery prices in the same corpus spanned 20x ($150 vs $3,000) and measure the agency's own health, not the market rate (Move 25).
- Reporting a single high-budget or high-competition item as the market's shape. The recurring trade is **generic + well-paid → crowded; specific + moderate → empty**; name the tradeoff rather than the outlier (Move 25).
- Logging a named vertical SaaS as a tool detail. When a buyer treats a vertical product as immovable and asks for capability *around* it, that is the repeatable "system of record + satellite layer" shape — one of the few that is both productizable and domain-moated (Move 24).
- Treating future upside as a one-off quirk. When "contract-to-hire" / "full-time conversion" / "co-worker opportunity" recurs *across* the corpus, the carrot has structurally replaced the budget on that channel (Move 17).
- Assuming niche always means low competition. A moat only suppresses bidders when it is **legible in the title**; an invisible domain moat draws the full crowd (Move 20).
- Collecting only items that fit the emerging thesis. Log contrast cases and say why they don't fit.
- Continuing to log near-duplicates as if each were a discovery once a cluster is saturated. The third copy is frequency evidence, not information — reduce the cluster to its primitive and steer the next dumps at unfilled cells (Moves 26–27).
- Using the marketplace's stated experience level or project-complexity label as a filter. Buyers routinely mark two-hour work "Expert / Complex project"; the field carries no information (Move 14).
- Treating a buyer's choice of AI model, CRM, or automation platform as meaningful when they listed alternatives. That is a commodity-layer tell, and it says the value is in the integration (Move 28).
- Skipping a scope-less, absurdly-cheap item as "no signal". Log one or two **market-floor** items deliberately, scored `P=n/a`: 50+ bidders on undisclosed requirements at $120, with a 5-star review offered as compensation, is the citation that makes "price competition here is unwinnable" a fact rather than an opinion (Move 31).
- Assuming a high budget always implies a domain moat. Architectural judgment — HITL design, agentic system design, shipping cadence — can carry the premium by itself; check the preferred-region field and the interview count before treating the number as a clearing price (Move 30).
- Letting a rich, already-written umbrella tempt you into re-deriving its content inline. The playbook exists so per-item replies stay short — cite the move number, don't restate the move.
- Inferring a scarcity/moat signal from a single low-competition data point, then generalizing. One post drew 15–20 bidders on a specific stack; a second with the *same* stack drew 50+. Retract the single-point inference when a contradicting item appears; only a clean, repeated effect (e.g. one tool collapsing proposals to <5 across independent posts) earns a moat claim (Move 34).
- Treating a high fixed budget as a quality or conversion signal. On freelance marketplaces high budget correlates with buyer paralysis / off-platform hiring — the ≥$1.5k generics in one corpus never interviewed and went stale while every actual hire was ≤$600. See Move 32.
- Skipping a dedicated `SUMMARY.md` synthesis when a long dump loop is about to be compressed. Without a compressed handoff file the next session must re-read the whole corpus to regain footing; write it proactively at the ~80% context mark, not only at the end (see the context-handoff protocol under "Manage your own context").
- Treating pasted job text as fully buyer-authored. Marketplace UI/platform copy sometimes leaks into the pasted "summary" (editorial asides about filtering, portfolio expectations). Flag such lines as capture artifacts and exclude them from scoring/quoting (Move 36).
- Asserting a moat without naming its class. "Low competition" can come from regulation, a specific language, a hot-but-decaying tool, a design/quality gate, or an integration last mile — these have very different durability. Say which one before claiming defensibility (Move 37).
- Concluding "the market won't pay" from a cheap post that stalemated, without checking scope. Vague/impossible scope stalemates even at low price; bounded scope hires fast even at $100 (Move 32-b).
- Reading a low proposal count at a low price as "the competent declined" (Move 12) without checking scope specificity. Generic $200 posts drew 50+; *specific* $200 posts drew 5–10. Low competition at low price can mean a sharp, well-defined problem that filters the crowd — not a declined job (Move 39).
- Treating telecom-compliance as a one-off regulatory quirk. When US TCPA and Canada CASL both appear for the same voice/SMS shape, it is a repeatable cross-border niche — fold it into the regulated-moat cluster with NDIS/customs, and note a jurisdiction stack (US + CA + 10DLC) is the durable form (Move 38).
