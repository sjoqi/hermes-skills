# One-page fit + "research first" — session-validated notes

## 1. One-page fit WITHOUT a Word/LibreOffice renderer
When no DOCX->PDF engine is installed (no soffice/libreoffice/pandoc-pdflatex), you can still
*prove* a DOCX fits one page by computing content height from its own geometry:

- US Letter = 612 x 792 pt.
- Margin M (twips): pt = M/20. Usable height = 792 - 2*(M/20). Usable width = 612 - 2*(M/20).
  - 540 twips ~ 0.375" -> usable 738pt tall x 558pt wide.
  - 720 twips ~ 0.5"   -> usable 720pt tall x 540pt wide.
- Per paragraph: chars-per-line ~ usable_width / (fontsize_pt * 0.50) (Times New Roman avg ~0.5em).
  Wrap: lines = ceil(len(text)/cpl). Height = lines * (fontsize * line_spacing).
- Line spacing: Word w:line="240" w:lineRule="auto" = 1.0; "276" = 1.15.
- Sum all paragraphs + heading/title blocks; if total <= usable height -> fits one page.

Validated live: tightened to 0.375" margins, 10pt body, 1.0 spacing -> est 667pt <= 738pt -> ONE PAGE.
PDF fit confirmed by actual render (insert_htmlbox overflow=False, page_count==1).

If it overflows: tighten margins -> 10pt body -> 1.0 spacing -> shrink paragraph before/after ->
trim Summary. NEVER fix overflow with a 2-col table or graphics (breaks ATS).

## 2. "Research before asserting" — verified answer to "is a Summary still good practice?"
User asked this; answered from web research, not memory. Synthesis:
- KEEP a Summary; KILL the Objective (the recruiter "never include" list targets objectives, not summaries).
- Summary is RECOMMENDED for career-changers / non-traditional backgrounds (frames transferable
  relevance the Experience section can't) and serves as an ATS keyword slot (load n8n, OpenAI
  API, GoHighLevel, CRM automation early).
- Make it 2-3 sentences, keyword-rich, role-tailored — NEVER a buzzword wall
  ("adaptable, resourceful, self-driven...").
- Optional only when the candidate has a strong traditional track record and "nothing that sets them apart."

## 3. Right-aligned dates = NOT ATS-friendlier (user reversed a prior ask)
User initially liked right-aligned dates; after learning they require a 2-col table (ATS hazard) or
a separate right-aligned paragraph (no parsing benefit), said "if it's not ATS-friendlier, don't do it."
Resolution: INLINE date on the same line as the title — most ATS-safe, no table. Governing rule:
a visual nicety only stays if it does NOT reduce parse-safety.
