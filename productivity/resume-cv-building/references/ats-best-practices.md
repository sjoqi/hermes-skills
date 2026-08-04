# ATS Best Practices (2026 synthesis)

Source: 2026 web research across resumeoptimizerpro, autotailor.app, cvanywhere,
flavoredresume, SCU Career Center, r/resumes ATS-parsing thread, Workday/LinkedIn
parser guides, and tailored-resume outcome studies. Use when making a resume
*actually parseable*, not just human-readable. Condensed — not a mirror of upstream.

## 1. Parsing-safe layout
- **Single-column, linear** (top-to-bottom, left-to-right). ATS reads like a screen reader.
- **Avoid tables, text boxes, graphics, and headers/footers for layout.** Parsers drop or
  reorder cells; header/footer content is often skipped entirely. This is the #1 silent
  failure. (Note the date-right "split row" many examples show is usually a 2-col table —
  fine for human PDFs, risky for strict corporate ATS. See skill Step 3c.)
- Standard body 10–12pt, common readable font.

## 2. Standard section headings (so parsers categorize)
Workday / LinkedIn key off exact names. Use:
`Summary` / `Professional Summary` · `Experience` / `Professional Experience` ·
`Education` · `Skills` · `Certifications` · `Languages`
Creative renames (e.g. "Where I've Made An Impact") get miscategorized or ignored.

## 3. Keywords — in context, not stuffed
- 2026 ML-based ATS score *contextualized, quantified* keyword use ABOVE raw keyword count.
  A resume with 10 rich, quantified bullets beats 30 generic keyword hits.
- Match the JD's exact phrasing where truthful.
- White-text / invisible keyword stuffing is now actively flagged as spam.

## 4. Tailoring per application (this is the norm, not optional)
- Tailored resumes show materially higher application→interview rates
  (sources cite ~40% more callbacks / ~2x interview rate vs generic).
- Therefore: build toward a SPECIFIC job description. A general/reserve resume is a
  different deliverable — confirm which the user wants.

## 5. File type
- **.docx is the safest default** (universally parsable).
- **PDF only if the posting requests it or it's emailed directly.** Must be
  **text-based / selectable**, never image-based or scanned.
- Always follow the posting's stated format instruction.

## 6. Summary as keyword slot + narrative
For career-changers / non-traditional backgrounds, keep a 2–3 sentence Summary leading
with the pivot + concrete stack (e.g. `n8n, OpenAI API, GoHighLevel, CRM automation`).
It frames relevance the Experience section can't and loads early keywords. Never a
buzzword wall. (Pairs with the "never include" file: keep Summary, kill Objective.)

## 7. Verification — plain-text test
Paste the rendered resume text into a plain-text editor (Notepad / TextEdit). If it's
jumbled or out of order, the ATS reads it the same way. Fix before sending.

## 8. Length — must be ONE page (hard constraint)
- A resume for application forms / most job hunts must fit **exactly one page**. This is
  a hard requirement, not a preference. The PDF is verified by actual render (page count).
  The .docx is verified by geometry math (no Word/LibreOffice renderer needed):
  estimate content height from real font sizes + margins + line spacing and confirm it is
  <= usable page height (US Letter 792pt − 2×margin). Keep headroom (~50–70pt) so it never
  spills to a 2nd page on different viewers.
- **Tighten-to-fit levers (all ATS-safe — apply before cutting content):**
  - Margins ~0.375–0.5 in (540–720 twips), not 1 in.
  - Body 10–10.5 pt; line spacing 1.0 (Word `w:line="240"` / CSS `line-height:1.0`), not 1.15.
  - Reduce inter-element spacing (before/after) and bullet spacing.
  - Tight single-column layout (the ATS-safe layout from §1 already avoids waste).
- **Never** use tables, text boxes, or graphics to "save space" — they break parsing (§1).
- Only cut real content if geometry tweaks still overflow. Prefer a 2-page *detail* version
  as a separate deliverable for real job hunts, but the primary submitted resume stays 1 page.

