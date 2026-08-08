# Legal / Privacy / GTM Risk for WiFi-Sensing Products (knowledge bank)

Condensed from primary sources fetched directly (statutes, regulator pages, FDA
databases). Use when the user asks whether a WiFi/RF sensing product is lawful,
sellable, or brand-safe — especially in hotels, rentals, or residential units.
**Research notes, not legal advice** — always say so and recommend counsel.

## The one-line thesis
**"No camera" is a PR talking point, not a legal exemption.** Privacy law
regulates *data about people*, not *lenses*. Lead with this; the user is usually
hoping the opposite is true.

## The pivot variable: presence/motion vs. breathing
Almost all risk scales with whether the product touches **vital signs**. Breathing
is simultaneously the differentiator, the GDPR Art. 9 trigger, the FDA/MDR
trigger, the failure-to-detect liability, and the PR catastrophe vector. Always
split the analysis on this axis and offer a de-risked presence-only tier.

## GDPR
- **Art. 4(1) personal data** — "identifiable… directly or indirectly, by reference
  to an identifier such as… location data… or one or more factors specific to the
  physical, physiological… identity." Room-level presence tied to a booking/lease
  record is personal data. The "we only store booleans" defence fails because the
  room→reservation mapping *is* the product.
- **Art. 4(14) biometric data** — only special-category when processed "for the
  purpose of uniquely identifying a natural person" (EDPB Guidelines 3/2019 ¶74–75;
  ICO concurs). So CSI is not automatically biometric…
- **…but** the literature undercuts any "our CSI can't identify anyone" claim:
  WifiU (ACM UbiComp 2016, ~700 cites, gait recognition from commodity CSI),
  GaitID (Tsinghua), and UCSB's "Multiple People Identification **Through Walls**
  Using Off-The-Shelf WiFi." Assume a regulator or journalist finds these.
- **Art. 4(15) health data** — "reveal information about his or her health status."
  Respiration reveals apnoea/distress/illness. Marketing emergency detection
  *concedes* this. → Art. 9 prohibition, practical gateway = explicit consent.
- DPIA is effectively mandatory (systematic monitoring of private space).
- Legitimate interests (Art. 6(1)(f)) **cannot** rescue Art. 9 data.

## US state law
- **Illinois BIPA (740 ILCS 14/10)** — definition is a **closed list**: "a retina or
  iris scan, fingerprint, voiceprint, or scan of hand or face geometry." CSI
  gait/breathing signatures are *not* on it, and "biometric information" is merely
  derivative. **This is the one genuine safe harbour** — an artifact of 2008
  drafting, not of good architecture. Don't assume it's permanent (amended by
  P.A. 103-769, eff. 8-2-24).
- **California CPRA §1798.140(c)** — the opposite: biometric information expressly
  includes "**gait patterns or rhythms, and sleep, health, or exercise data that
  contain identifying information**." Reads as if drafted for this product class.
  §1798.140(v)(1)(H) also covers "thermal, olfactory, or **similar** information"
  (catch-all reaching RF), and (K) covers inferences/profiles.
- **CA Penal Code 647(j)(1)** — criminal, and technology-neutral: viewing "by means
  of any instrumentality, including… **electronic device**… the interior of a
  bedroom… or any other area in which the occupant has a reasonable expectation of
  privacy, with the intent to invade the privacy" of those inside. **No camera
  required.** 647(j)(3)(B)(i): being a "**landlord, tenant**, cotenant, employer…"
  is expressly **not a defence**. Saving element is *intent* — disclosed safety
  products likely lack it; covert deployments do not.
- **NYC Tenant Data Privacy Act (Local Law 63 of 2021)** — smart-access systems:
  express written consent, enumerated minimum data set, **destroy authentication
  data ≤90 days**, no sale/disclosure, purpose-limited to granting access, cannot
  be used "to harass or evict a tenant," **private right of action.** A sensor
  isn't an access system so it may not bind directly — but it sets the legislative
  posture and the 90-day retention benchmark worth adopting voluntarily.

## Airbnb indoor-device policy (verified, eff. 30 April 2024)
Help Article 3061 + Newsroom: bans "security cameras or recording devices that
monitor indoor spaces… **even if these devices are turned off**." The *only*
permitted indoor sensor class is **noise decibel monitors** (sound level + duration,
**no audio recording**), and even those must be disclosed and are **banned from
bedrooms, bathrooms, or sleeping areas**.
→ A CSI sensor arguably isn't a "camera or recording device," **but do not build
GTM on that reading.** If a sound-level meter is barred from bedrooms, a
breathing sensor in a bedroom is against the grain of the rule, and platform risk
is enforced by delisting, not litigated. **Treat short-term rental as closed.**

## Medical-device classification
- **EU MDR 2017/745 Art. 2(1)** — device includes **software** intended for
  "diagnosis, prevention, **monitoring**, prediction, prognosis…" or "investigation…
  of the anatomy or of a **physiological**… process or state." Breathing is a
  physiological process → emergency-detection claims = CE marking + notified body.
- **FDA** — contactless vitals is an *already-cleared* category, so "nobody
  regulates this" is false: **Sleepiz One+ 510(k) K223163** (radar respiration/heart
  rate) and **Circadia C100 K200445** ("contactless spot checking and continuous
  measurement of respiratory rate… as part of a vital [signs monitor]").
- **Escape hatch:** FDA General Wellness policy (revised Jan 2026) — enforcement
  discretion for general-wellness + low-risk products; per Troutman, "noninvasive
  physiologic trackers may now qualify" if they don't refer to a specific disease
  or condition and don't substitute for a cleared device. **Intended use is judged
  "objectively from labeling, marketing, and other statements."**
- **Practical rule:** "occupancy and general activity insight" = plausibly outside
  device regulation. "Detects if a guest stops breathing" = regulated device.
  There is no configuration that keeps the emergency claim *and* stays unregulated.

## Failure-to-detect liability (independent of FDA)
Negligence / failure to warn; **negligent misrepresentation & express warranty
from the marketing copy itself**; and **assumed duty** — voluntarily undertaking a
rescue function creates a duty to perform it non-negligently, having induced
reliance so the operator stopped doing what they otherwise would. Disclaimers are
weak against wrongful-death claims and weaker when they contradict the sales
pitch. The B2B customer gets sued and indemnity-chases the vendor.

## Real backlash precedents (residential, documented)
- **Atlantic Plaza Towers, Brownsville Brooklyn** — landlord proposed StoneLock
  facial recognition at a rent-stabilised complex; **130+ tenants organised**;
  landlord **withdrew** after legal opposition and press.
- **Hell's Kitchen Latch litigation** — landlord blocked the key cylinder; tenants
  **sued** on privacy + accessibility (a 93-year-old became effectively homebound);
  **settled** with physical keys on request.
- **Airbnb itself** reversed globally on indoor cameras citing community privacy —
  a market signal, not just a rule.
**Pattern: defeated by organised tenants and journalists, not by courts.** The
legal question was never reached. Both fights were over *access control*, which
is strictly less invasive than in-bedroom body sensing.

## Segment ranking (reusable verdict table)
| Segment | Verdict |
|---|---|
| Short-term rental (Airbnb/Vrbo) | **Closed** — platform policy |
| Residential tenants, long-term lease | **Highest risk** — quiet enjoyment, retrofit-consent impossibility, two tenant revolts |
| Hotels w/ vital-sign claims | High — non-booking occupants can't consent; Art. 9; PC 647(j) bedrooms |
| **Hotels/commercial, occupancy+motion only, non-sleeping spaces, disclosed, zero vital-sign claims** | **LEAST friction** — clears BIPA's closed list, dodges Art. 9, fits FDA wellness, avoids the 647(j) bedroom trigger, has a non-scandalous analogue in energy-management occupancy sensing |
| Healthcare-adjacent w/ resident/family as signing customer | Medium — consent is real, but breathing claims → FDA/MDR cost |

## Consent mechanics — the structural (not UX-fixable) failures
- **Non-booking occupants** — second guest, child, visitor never signed. The booker
  can't consent for them. Mirrors EDPB ¶76 on "uncontrolled environments."
- Consent buried in booking T&Cs is neither specific nor unambiguous.
- **Mid-term lease retrofit is impossible** — can't amend a sitting tenant's lease;
  refusal can't lawfully trigger adverse action; rent-stabilised is worse.
- Consent-as-condition-of-tenancy isn't "freely given" and is politically radioactive.
- Workable hotel path: **off by default**, per-stay opt-in at check-in for a named
  feature, physical in-room notice, edge processing, genuine no-monitoring room option.

## Cheapest de-risking moves (recommend these)
Strip vital-sign/emergency language from marketing *before* it lands in a customer
contract; ship presence/motion first and treat breathing as a separate later
regulated line (separate entity if possible); default-off + per-occupant opt-in +
physical disclosure + edge processing + ~90-day retention; never deploy in
bedrooms/sleeping areas in the unregulated tier; run a real DPIA.

## Research-method notes for this class of question
- **Fetch primary text, don't rely on search snippets.** `web_extract` on
  leginfo.ca.gov, ilga.gov, gdpr-info.eu, eur-lex, nyc.gov/hpd, airbnb.com/help,
  and accessdata.fda.gov gave exact quotable statutory language; law-firm blogs
  were only useful for *interpretation* (e.g. Troutman on FDA intended use).
- **When Firecrawl `web_search` rate-limits** (429, "Consumed (req/min)"), switch to
  `web_extract` against known primary-source URLs and `search_files` over the
  cached markdown Hermes writes to `~/.hermes/cache/web/`. This is usually *better*
  sourcing than continuing to search. Batch independent extracts in one turn.
- **Big documents:** EUR-Lex MDR is ~700k chars and gets head+tail truncated. Use
  `search_files` with a distinctive phrase (e.g. "investigation, replacement or
  modification of the anatomy") plus `context:` against the cached file to pull the
  exact article.
- **Don't guess arXiv IDs** — a guessed ID returned an unrelated quantum-physics
  paper. Search for the paper by title/technique and cite what actually resolves.
- **Deliverable shape that worked:** a written markdown report at a filepath, with
  every claim carrying an inline fetched source URL, a segment risk table, an
  explicit verdict, and a short "blunt statements" section — then a compact chat
  summary of the findings rather than re-pasting the report.
