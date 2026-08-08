---
name: resume-cv-building
description: Build or rebuild a professional, ATS-friendly resume/CV — especially for career-switchers, freelancers, students, or anyone with non-traditional/unpaid experience. Covers honest framing, section structure, intake questions, and verifying a job opportunity's legitimacy before applying. Pair with the pdf-generation skill for the final PDF deliverable.
---

# Resume / CV Building

## When to use
User asks to create, update, rebuild, or polish a resume/CV — and especially when they are switching careers, freelancing, between jobs, a student, or have gaps / unpaid / in-progress projects.

## Step 0: get the job description FIRST (for a specific application)
If the resume targets a **specific posting**, **require the job description before building or tailoring** — do not write toward a guessed role. A resume is **tailored per application**: the same candidate needs different emphasis and keywords for each posting.
- **Ask the user to paste the JD (or link it).** Do not skip this for a "real job application."
- Then map the resume's **Summary, Skills, and Experience bullets** to that JD's exact keywords and required qualifications — honestly (only claims the candidate can back; see honest-framing rule).
- If the user wants a **general / reserve resume** instead of a tailored one, confirm that explicitly and skip tailoring.

## Step 0b: verify the opportunity BEFORE writing toward it
If the resume targets a specific posting or platform, **research it first** — a 5-minute check prevents bad advice:
- Is the company/platform real? Web search `<name> + scam / legit / reviews`.
- Impersonation check: real recruiters contact via the official platform and never ask for upfront payment or bank details in chat. Only use official `forms.gle` / company-domain links.
- Pay: compare against reported ranges for that role; flag rock-bottom rates openly.
- "Guaranteed work" / "maximum contract value" wording usually means **no guaranteed volume** — say so.
- Payment-reliability reports (Reddit, Inc., etc.): often real but late/disputed.
- **Tax-form mismatch for non-US residents:** a US **1099** requires a **W-8BEN** instead; confirm a payout method that works in their country (PayPal/Hyperwallet, not US-only).

## Step 0.5: NEW APPLICATION → always request the job description first
A resume must be **tailored per application**. Before building or revising a resume for a *specific* posting (not a generic "have one ready" request), the agent MUST ask the user for the **job description / job posting text** (and the application channel if known — Workday, LinkedIn, direct email, Upwork, etc.).
- Do NOT skip this for a "real" application. Generic one-size resumes materially underperform: sources cite tailored resumes getting ~40% more callbacks / ~2× application-to-interview rate vs generic.
- From the JD, extract: must-have keywords (tools, frameworks, verbs), required section emphasis, and any hard requirements (degree, location, certs).
- Weave those keywords **naturally into** the Summary, Skills, and Experience bullets (contextual + quantified — NOT a separate keyword-stuffing block, which 2026 ML-based ATS now penalizes).
- If the user only wants a general/master resume with no target, say so explicitly and skip this step — but flag that it should be tailored before each real submission.
- After tailoring, run the plain-text test (see reference) to confirm the JD keywords survive extraction.

## Step 1: honest framing rules (NON-NEGOTIABLE)
Never fabricate employment. Map reality to sections:
- **Real paid work** (including gig-economy: delivery, rideshare, freelance with clients) → `Experience`.
- **Unpaid / self-directed / in-progress / no-client** builds → `Projects & Self-Directed Work`, described truthfully (what was *actually* built, dates, solo/exploratory nature).
- **Invites / offers not yet worked** → keep OFF Experience. Surface the relevant strengths (skills, languages, public speaking) in Summary/Skills instead.
- Weak-but-true phrasing (e.g. "no clients landed yet") → reframe professionally ("building portfolio, seeking initial clients") while staying truthful.
- Don't pad an empty Experience section with fake jobs — a strong Projects section reads better for career-switchers.

## Step 2: intake questions (ask before writing)
1. Who is this for? (general / specific application / freelance profile) — changes emphasis most.
2. For each project: what was *actually* built? (real deliverables, not aspirations)
3. Dates / timeframe for each role & project.
4. Any metrics? (ratings, volume, attendees, % improvement)
5. Location + links (LinkedIn / GitHub / portfolio).
6. Keep pending offers off the resume? (usually yes)

## Step 3: section order (ATS-friendly)
Contact → Summary → Skills → Experience → Projects → Leadership/Community → Education & Training.
- **ONE PAGE is a HARD constraint for the delivered resume** unless the user explicitly asks for 2 pages. The user stated "it must be one page" — do not ship a 2-page doc by default. If content won't fit, tighten (see Step 3d), don't spill to page 2.
- Mark an incomplete degree as "incomplete" with dates — never as completed.

## Step 3b: what to CUT (recruiter-backed "never include")
Before finalizing, run every draft line through the "never include" checklist in `references/what-to-never-include.md`. The short version:
- **No Objective / career-goal line** — a tight fit-framing *Summary* stays, an "objective" goes.
- **No buzzword self-description wall** ("highly motivated, detail-oriented team player…") — cut.
- **No photo** on North-America-targeted resumes (region-specific; Europe often expects one — flag when relevant).
- **No bare soft-skill lists** (teamwork/leadership/communication as standalone claims) — prove via experience instead.
- **No bullets that just restate the job description** — show what improved *because you were there*.
- **No context-free skill charts/graphs.**
- **5-second test:** if a line can't be backed up in a few seconds, delete it. Never fabricate metrics to fill gaps — find a truthful proxy or leave the number off (see honest-framing rule).

## Step 3c: ATS parsing rules (so the resume actually gets read)
A human-readable PDF is not the same as an ATS-readable one. **Default to the STRICTEST ATS-safe interpretation.** Governing rule the user stated directly: *"if it's not ATS-friendlier, don't do it — make it the most ATS-friendly."* So a visual nicety only earns its place if it does NOT reduce parse-safety; when a visual nicety (e.g. a right-aligned date column via a 2-col table, or CSS float) conflicts with parse-safety, DROP the nicety — do NOT keep it "because it looks better," and tell the user the trade-off rather than silently picking the prettier-but-riskier option (see `references/pymupdf-rendering-limits.md`). Apply before finalizing:
- **Single-column, linear layout** — ATS reads top-to-bottom, left-to-right like a screen reader.
- **No tables / text boxes / graphics for layout** — parsers drop or reorder cells (common silent failure). ⚠️ The "date on the right" split-row effect (as in many example resumes) is usually a 2-column **table** — great for a human PDF, risky for strict corporate ATS. If maximum ATS safety is required, put the date on its own line under the title (or inline) instead of a table. **Offer the user this trade-off** rather than silently picking one.
- **Standard section headings** so parsers categorize correctly: `Summary` / `Professional Summary`, `Experience` / `Professional Experience`, `Education`, `Skills`, `Certifications`, `Languages`. Avoid creative renames.
- **Keywords in context, not stuffed** — 2026 ML-based ATS score contextualized, quantified keyword use above raw count. White-text keyword stuffing is now flagged as spam.
- **File type:** default to **.docx** (universally parsable). Use **PDF only if the posting requests it or it's emailed directly**, and it must be **text-based / selectable**, never image-based/scanned. Always follow the posting's stated format.
- **Plain-text test (verification):** paste the rendered resume text into a plain-text editor (Notepad / TextEdit). If it's jumbled or out of order, the ATS reads it the same way — fix before sending.
- **One-page hard constraint:** the submitted resume MUST fit exactly one page. Verify the PDF by actual render (page count) and the .docx by geometry math (estimate content height from real font sizes/margins/line-spacing; keep ~50–70pt headroom so it never spills on other viewers). Tighten via ATS-safe levers first — margins ~0.375–0.5", body 10–10.5pt, line spacing 1.0, reduced inter-element spacing — **never** tables/text boxes/graphics to save space. Only cut real content if geometry tweaks still overflow. A 2-page *detail* version is a separate optional deliverable; the primary resume stays 1 page. (See ats-best-practices §8.)
- **Summary as keyword slot:** for career-changers / non-traditional backgrounds, keep a 2–3 sentence Summary leading with the pivot + concrete stack (e.g. `n8n, OpenAI API, GoHighLevel, CRM automation`). It frames relevance the Experience section can't and loads early keywords. Never a buzzword wall.

## Step 3d: enforce ONE PAGE (when content is tight)
If the draft risks spilling to page 2, tighten in this order (all ATS-safe, proven this session):
- **Margins:** 0.375"–0.5" sides (≈540–720 twips) — tighter than the default 1".
- **Body font:** 10pt (not 10.5–11); headings 13pt.
- **Line spacing:** 1.0 (Word `w:line="240"`) not 1.15.
- **Spacing:** shrink before/after paragraph spacing (e.g. 60/20 twips) and trim the Summary to ~2–3 sentences.
- **Verify fit without a renderer:** compute content height from the actual font sizes + margins + line spacing (US Letter = 612×792pt; usable height = 792 − 2×margin). Sum per-paragraph line counts (wrap by `usable_width / (fontsize×0.5)` chars). If estimate ≤ usable height, it fits. (No Word/LibreOffice needed.) For PDF, confirm by actual render (`page.insert_htmlbox` overflow + `doc.page_count`).
- Never "fix" overflow by switching to a 2-column table or graphics — that breaks ATS.

## Step 4: deliver
- **Default output: .docx** (universally ATS-parsable — see Step 3c / ats-best-practices §5). Generate via the **pdf-generation** skill's docx path, or — when python-docx / LibreOffice / OfficeCLI are unavailable — the zero-dependency generator `scripts/generate_ooxml_docx.py` (stdlib `zipfile` + WordprocessingML, no third-party libs; validated as a clean, table-free, ATS-safe DOCX). When pip/LibreOffice/OfficeCLI are unavailable or risky (e.g. OfficeCLI's macOS-arm64 JIT breakage), the stdlib OOXML route is the safe fallback — see `references/ooxml-docx-without-libs.md`.
- **PDF only if** the posting requests it or it's emailed directly — and it must be **text-based / selectable** (render via the **pdf-generation** skill), never image-based. Always follow the posting's stated format.
- **Verify parsing before sending:** extract the rendered text (or run the plain-text test, ats-best-practices §7) and confirm section headings, dates, and JD keywords survive linearly with no jumbled order. Also confirm the file isn't blank (pdf-generation verification step) — the empty-page failure mode is silent.

## Pitfalls
- A weak Experience section is normal for switchers — compensate with a robust Projects section, not fabrication.
- Verify the generated PDF isn't blank (see pdf-generation verification step) — the empty-page failure mode is silent.
- **Research claims before asserting them.** When the user asks "is X still good practice?" / "research it first," do NOT answer from memory — web-search multiple sources and synthesize before giving a recommendation (done live for the "summary still useful?" question; research showed summary is recommended for career-changers / as an ATS keyword slot, optional otherwise, never a buzzword wall).
- **Checkpoint before editing a working build** (user's standing rule): when improving an existing resume/generator, make a restorable backup (git commit + `git tag -f checkpoint-working`, or a `*.before-<change>.bak` file if not a repo) BEFORE changing code. Done live: `build_resume.py.before-*.bak` before each generator change.
- **Finish the skill edit you announce.** When the user asks to "make a note for the skill" / "add to the file," actually write the reference file and patch SKILL.md *before* replying. Do not stop at a summary that says "now let me add it" — execute, then summarize what changed. (Caught live: a turn summarized the plan and stopped; user had to prompt "why did you stop?")
- **Prefer `references/` subfiles for session-specific research.** Condensed recruiter/industry guidance, sourced excerpts, and per-thread notes belong in `references/<topic>.md`, not inline in SKILL.md. SKILL.md stays the durable procedure; reference files carry the volatile detail and get a one-line pointer at the bottom. (User explicitly asked for "a kind of guideline files in the resume skill.")

## Related skills
- `pdf-generation` — how to render the final clean PDF.
- `ocr-and-documents` — extracting text from an existing resume PDF to rebuild it.

## Reference files
- `references/what-to-never-include.md` — recruiter-sourced "never include" checklist (objectives, buzzwords, photo, soft-skill lists, JD-restating bullets) with the ATS/fabrication nuance. Load this during Step 3b.
- `references/ats-best-practices.md` — 2026 ATS parsing/formatting/tailoring research (single-column, no tables, standard headings, keyword-in-context, file type, plain-text test). Load this during Step 0 / Step 3c.
- `references/pymupdf-rendering-limits.md` — tested PyMuPDF HTML limits (float ignored, flexbox overflows, only `<table>` right-aligns but breaks ATS) + the ATS-safe inline-date fix and the verify-by-extraction pattern. Load during Step 3 / 3c.
- `scripts/generate_ooxml_docx.py` — zero-dependency .docx generator (stdlib only). Use when python-docx / LibreOffice / OfficeCLI is unavailable or you want a clean, ATS-safe DOCX with no third-party libs. Loaded during Step 4.
- `references/one-page-fit-and-research.md` — how to *prove* one-page fit without a Word renderer (geometry math), the researched "is a Summary still useful?" answer, and the right-aligned-date reversal. Load during Step 3d / Step 0.5.
- `references/ooxml-docx-without-libs.md` — how to generate a clean .docx with stdlib `zipfile` + WordprocessingML only (when pip/LibreOffice/OfficeCLI are unavailable or risky), plus why OfficeCLI is an *edit* tool not a generator and its macOS-arm64 caveat. Load during Step 4.
