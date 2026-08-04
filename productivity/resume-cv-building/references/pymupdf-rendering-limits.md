# PyMuPDF (fitz) HTML rendering limits — tested findings

Use when rendering a resume to PDF with `page.insert_htmlbox(html, css=...)`.
Discovered and verified by rendering + extracting text during a real build
(serif resume, date-right layout). PyMuPDF's HTML engine is a limited subset
of CSS — these gaps are easy to hit and silent (the call returns "ok").

## What works
- Block elements: h1/h2, p, ul/li, b/i, spans.
- `border-bottom` on h2 → underlined header (gives the "underlined all-caps header" look).
- Tight margins via the insert rect, e.g. `fitz.Rect(50, 45, w-50, h-45)` (~0.7").
- `<table>` for a 2-column split (used to right-align a date next to a title).

## What does NOT work (tested, do not rely on it)
- **CSS `float: right` is IGNORED.** A date span with `float:right` renders on the
  LEFT, immediately before the title text. The date silently ends up in the wrong place.
- **Flexbox (`display:flex; justify-content:space-between`) OVERFLOWS.** `insert_htmlbox`
  returns `overflow=True` and the layout breaks. Not supported by this engine.
- **Only a 2-column `<table>` produces a true right-aligned date column.** But tables
  are an ATS parsing hazard (parsers drop/reorder cells) — see ats-best-practices.md §1.
  A table is fine for a human PDF but risky for a strict corporate ATS.

## ATS-safe date placement (the resolution we shipped)
Put the date inline at the END of the title line as plain text:
  `Company — Role  2025 – Present`
This reads linearly for parsers and still visually sits at the line end for humans.
Verified by extracting plain text and asserting every entry line ends with its date.

## Verification pattern that caught the float bug
1. Render PDF, then `doc[0].get_pixmap()` → PNG and vision-check layout.
2. `doc[0].get_text()` → assert dates land where expected (right vs left).
The float bug was only visible via text extraction + vision, NOT via the "ok" return value.
Always extract-and-check, never trust the return code alone.
