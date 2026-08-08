# Coding Scheme Template

Adapt per source. **Stable vocabulary is the whole point** — add new tags at the bottom with a date; never silently redefine an existing one, or the longitudinal tally becomes meaningless.

## 1. Item ID
`UW-001`, `UW-002`, … sequential, never reused. Prefix per source (`UW`=Upwork, `FV`=Fiverr, `RD`=Reddit…).

## 2. Industry (`ind:`)
`ecommerce` `agency-marketing` `realestate` `healthcare` `legal` `finance-accounting` `recruiting-hr` `logistics` `education` `saas` `construction-trades` `hospitality` `insurance` `nonprofit` `creator-media` `other`

## 3. Pain category (`pain:`) — what is actually broken
Tune to domain. For business-automation work:

- `data-entry` — moving data between systems by hand
- `lead-gen` — scraping/enriching/sourcing prospects
- `crm-sync` — systems that don't talk to each other
- `reporting` — manual dashboards, recurring reports
- `doc-processing` — PDFs, invoices, contracts → structured data
- `inbox-triage` — email/DM/ticket handling
- `content-gen` — bulk content production
- `scheduling` — calendars, dispatch, bookings
- `customer-support` — chatbot / deflection / FAQ
- `internal-agent` — "AI employee" doing a role end-to-end
- `migration` — one-time move between platforms
- `scraping` — data acquisition from web
- `voice-phone` — AI callers, receptionists
- `compliance-audit` — checks, logging, regulatory
- `customer-support` — tier-1 deflection, FAQ, RAG-grounded answers
- `competitive-intel` — automated collection/analysis of competitor public content/performance
- `design-ops` — creative-asset generation (image/video) wired into workflows; quality/taste gate
- `logistics-ops` — freight/trucking/dispatch operations
- `payment` — checkout, subscriptions, dunning, processor-fit
- `other`

## 4. Tools named (`tool:`)
Record what the buyer names, even when irrelevant — *which* tools buyers name, and whether they treat them as interchangeable, is itself signal.

## 5. Job shape (`shape:`)
- `oneoff-build` — build it and leave
- `fix-repair` — existing automation broken
- `ongoing-retainer` — continuing relationship
- `staff-aug` — a body, hourly, long-term
- `advisory` — audit/consult/strategy

## 6. Budget band (`bud:`) — normalize to USD
`b0` unstated · `b1` <$500 · `b2` $500–2k · `b3` $2k–5k · `b4` $5k–15k · `b5` >$15k
Hourly: `h1` <$25 · `h2` $25–50 · `h3` $50–90 · `h4` >$90

## 7. Client quality (`cq:`)
`new` (no history) · `light` (<$5k lifetime spend) · `solid` ($5k–50k) · `heavy` (>$50k)

## 8. Competition (`comp:`)
`c1` <5 proposals · `c2` 5–15 · `c3` 15–30 · `c4` 30+

Competition is the field users most often forget to capture. Ask for it early — without it you cannot find the high-budget/low-competition quadrant that the specialist track depends on.

## 9. Track fit scores — 1–5, always with a one-line reason
- **P-score** — productizable? High = same problem, same shape, many clients, low customization.
- **S-score** — specializable? High = deep domain pain, real money at stake, buyer would pay a premium for a proven expert.

Scoring both high, or both low, is fine and common. Most marketplace posts are noise; say so.

## 10. Verbatim pain quote
Mandatory when available. The buyer's own words, unedited.

## Table header must carry the capture filter
```
**Capture filter in effect:** user logs only posts > $100.
All frequency counts are conditional on that.
```
