# Privacy-Preserving In-Room Sensing — Buyer Demand (researched 2026-08-08)

Worked example for `buyer-demand-validation`. Concept under test: no-camera WiFi CSI sensing
(presence / motion / breathing) sold to hotels, STR, landlords, senior living.
Full output doc was written to `/Users/you/wifi-sensing-demand-findings.md`.

All figures below carry the source that was actually fetched. Re-verify prices before reuse —
vendor pricing pages change.

---

## Verified WTP anchors (the most reusable part)

| Segment | Price | Unit | Source |
|---|---|---|---|
| STR monitoring | $5 / $10 / $15 per month | per home, billed annually, **hardware separate** | https://www.minut.com/pricing |
| STR — human call-handling add-on | +$10/mo | per rental unit | https://www.minut.com/pricing |
| STR competitor | $15/mo ($180/yr) + $99 one-time outdoor | per property (NoiseAware) | competitor comparison only — vendor page blocked |
| Medical alert subscription | $20–$55/mo | per user | https://aginginplace.org/medical-alert-systems/cost-of-medical-alert-systems/ |
| Fall-detection add-on | $5–$15/mo (~$10 typical) | per user | same |
| Contactless radar hardware | ~$240–250/device, ~3 per home | Vayyar Care | https://www.calcalistech.com/ctechnews/article/rj0cnyqiq |
| Multifamily smart-apt bundle | **$406 per unit per YEAR**, ↓10% YoY | all services bundled | https://investors.smartrent.com/news/news-details/2026/SmartRent-Reports-Fourth-Quarter-and-Full-Year-2025-Financial-Results/default.aspx |

Senior living WTP is **2–5x** STR for the same underlying capability. STR is the cheapest
segment and the easiest to sell; the two facts are related.

Minut defines a "rental unit" to include *"a multi-tenant building or hotel, where each
apartment or room is rented separately"* — i.e. one vendor applies $5–15/unit/mo across STR,
multifamily AND hotel rooms. Greystar (major multifamily operator) is on their logo wall.

## Hotel panic-button mandates — verified table

Purchasing denominator is **lone-worker employees**, not rooms. Device must be
**wearable, worker-activated, location-reporting**. Passive room sensing satisfies none of these.

| Jurisdiction | Threshold | Requirement |
|---|---|---|
| Illinois (Hotel Employee Safety Act) | >100 rooms | Wireless panic buttons, full + part time, by July 2020, free to employee |
| Washington | 60+ rooms | Personal safety device Jan 2020; <60 rooms by Jan 1 2021 |
| New Jersey | 25+ rooms | Electronic device or two-way radio (2018); **>100 rooms → Bluetooth panic button** since June 2019 |
| Massachusetts | — | Law passed |
| Chicago ("Hands Off Pants On") | — | By July 1 2018, employees working alone in guest rooms/restrooms |
| Seattle | 60+ rooms | Cleaning, room service, maintenance staff |
| California | — | **No statewide law** (per vendor blog — VERIFY, may be stale). City ordinances: Santa Monica, Oakland, Sacramento County, City of Sacramento, Long Beach, LA + Glendale (2022) |
| Nevada / Las Vegas | — | NOT mandated; pursued via union CBAs |

- **No US federal mandate.** Confirmed on https://www.ahla.com/5-star
- Penalties: **$25/day to $10,000 per infraction**
- Some laws also require guest notification + activation record-keeping
- AHLA State Law Tracker: https://www.ahla.com/new-state-local-center
- Sources: https://roarforgood.com/blog/hotel-panic-button-regulation-and-compliance/ (vendor, substantively accurate, possibly stale on CA);
  https://www.lawandtheworkplace.com/2017/10/chicago-passes-ordinance-requiring-hotels-to-provide-panic-buttons-to-certain-employees/ (Proskauer);
  https://www.mrla.org/uploads/1/2/1/3/121332115/hotel_panic_buttons_whitepaper.pdf

### UK/EU
No specific lone-worker law. HSWA 1974 + Management of H&S at Work Regs 1999, qualified
"so far as is reasonably practicable." **HSE guidance recommends "automatic warning devices
which trigger if specific signals are not received periodically from the lone worker"** —
the one hook a passive product could arguably satisfy. BS 8484 + Alarm Receiving Centre
connection likely required to sell as compliance. Regs implement EU Directive 89/391/EEC.

## Adoption-velocity proxy (the reusable technique)

AHLA 5-Star Promise, pledged **September 2018**:
- ~60 member companies / **~20,000 properties** pledged, ~1.2M employees
- **"more than 5,000 hotels have implemented employee safety devices"**
→ **~25% implementation over ~7 years on a legally mandated, association-backed category.**

This is the best available sourced answer to "how slow is hotel tech adoption," and it beats
any unsourced sales-cycle estimate.

## Denominators

- US lodging: **64,000+ properties** (incl. **33,200+ small-business properties**),
  **5.7M guest rooms**, 1.3B guest nights/yr — https://www.ahla.com/about/our-industry
  (33,200 independents = the serviceable denominator for a solo founder; no brand-mandated stack)
- OPERA PMS estate: ~**40,000 hotel properties**; PMS of choice for Marriott, Four Seasons,
  Hyatt, Radisson (2023 est., via https://www.altexsoft.com/blog/opera-pms-integration/)
- SmartRent: **890,870 units deployed** FY2025 (+10%); later disclosure 929,487; ARR ~$64.5M,
  Q1 2026 ARR $60.9M, revenue $38.7M down from $41.3M — shrinking

## Pain-cost data

### Senior living — best-quantified pain found (HHS OIG, 2025, report OEI-05-24-00181)
- **42,864 falls** with major injury + hospitalization among Medicare-enrolled nursing home
  residents in one year (Jul 2022–Jun 2023); **1,911 died while hospitalized**
- **Medicare + enrollees paid >$800 million** for resulting hospital care
- Most residents **had fall risk factors identified beforehand**
- Lower nurse staffing + lower quality ratings → higher fall rates
- https://oig.hhs.gov/reports/all/2025/serious-falls-resulting-in-hospitalization-among-medicare-enrolled-nursing-home-residents-july-2022-june-2023/
- **Companion finding — the commercial hook:** nursing homes **failed to report 43% of falls
  with major injury**, corrupting CMS Care Compare star ratings.
  https://oig.hhs.gov/reports/all/2025/nursing-homes-failed-to-report-43-percent-of-falls-with-major-injury-and-hospitalization-among-their-medicare-enrolled-residents/

### STR damage — the contradiction, and how it resolved
- "$1,560 average damage per unauthorized party" — https://rapideyeinspections.com/blog/airbnb-damage-claim-statistics/ (survey blog, methodology undisclosed)
- **vs.** operator with 800+ listings / 300+ claims filed: "most approved claims land between
  **$200 and $400**", highest-ever recovery $2,000 — https://strassistance.com/airbnb-host-damage-protection/
- Base rate "<0.1% of stays" (coaching blog, uncited, low confidence)
- **Free incumbent suppressing WTP:** AirCover = **$3M damage protection + $1M liability, free,
  automatic** — https://www.airbnb.com/help/article/937
→ Prevention ROI pitch is weak. Take the net figure.

### The wedge hiding in the denial data
Top documented causes of denied Airbnb claims: wear and tear 20%, pre-existing damage 13%,
outside scope 7% — and the top four include **"no pre-stay baseline photos"** and
**"inability to prove the guest caused the damage."**
→ A timestamped no-camera occupancy/motion log is a **claims-evidence product**.
Minut does not lead with this. Best differentiated wedge found in the whole pass.

## Procurement blockers

**Oracle OPERA integration (hotels) — the hard number:**
- OPERA Cloud / OHIP: Oracle Partner Network **$500/yr** + Hospitality expertise track (no extra fee)
- OPERA 5 / Suite8 (legacy estate): OPN **plus "License & Hardware" track $3,000/yr**
- *"Oracle may also require a hotel customer ready to justify the integration"*
  → chicken-and-egg: need a signed hotel before you can build what the hotel asked for
- https://www.altexsoft.com/blog/opera-pms-integration/

**STR:** self-serve "Buy now" per tier → store checkout. Single signer. PMS integration
(30+ platforms) gated to top tier; OTA sync at mid-tier. Integrations are table stakes for
$15/unit, not for launch.

**Senior living:** channel-partner route — K4Connect ↔ Vayyar is the documented pattern.

## Competitive framing note
Vayyar markets on **exactly** the arguments this concept would use: *"Nobody wants to be
watched"*, *"Who wants wearables?"*, hidden-fall danger — https://vayyar.com/care-docs/b2c/
→ Framing validated AND position taken. They use **4D imaging radar**; competing on
breathing/fall accuracy with commodity WiFi CSI is the biggest unpriced technical risk.

## What could NOT be validated (kept as gaps, not guessed)
- Hotel ESD per-unit pricing — all vendors demo-gated
- Hotel sales-cycle length; who signs in a hotel
- Any insurer offering a premium discount for occupancy sensing — **nothing found**
- Landlord/tenant legal position on sensing inside leased premises (possessory rights,
  quiet enjoyment) — unresolved, and a hard blocker for multifamily
- Student housing and hospitals — entirely unresearched
- US STR listing count / senior-living bed count → **no TAM figure produced**
- Whether a non-FDA-cleared presence sensor qualifies under RPM CPT 99453/99454/99457/99458
  (the ~$145–185/patient/mo figure came from a vendor site, not CMS)

## Unusable sources encountered
- marketintelo.com sized the same 2025 market at **$1.2B** ("Wi-Fi Sensing") and **$2.3B**
  ("IEEE 802.11bf Sensing") — same publisher, contradictory, methodology undisclosed. Do not cite.
- ABI Research Wi-Fi sensing whitepaper: URL + title retrieved, **body not extracted** →
  no figures cited from it.
- noiseaware.com/pricing returned a blocked-URL error.
