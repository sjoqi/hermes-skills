# Generating a .docx with NO third-party libraries (stdlib-only fallback)

Use this when the target machine has no `python-docx`, no LibreOffice/soffice, and
`pip install` is broken (e.g. a corrupted venv pip that errors on `dataclass(slots=...)`),
or when you must avoid pulling a 25k-star .NET binary like OfficeCLI (which has a
documented macOS arm64 JIT/entitlement breakage: "unusable on Hardened-Runtime-enforcing
macOS, observed on macOS 26 / arm64").

## The fix (not a refusal)
A `.docx` is just a ZIP of WordprocessingML XML. Build it with the stdlib only:

- `zipfile` to assemble the package.
- Required parts: `[Content_Types].xml`, `_rels/.rels`, `word/document.xml`,
  `word/_rels/document.xml.rels`, `word/styles.xml`, `word/numbering.xml`,
  `docProps/core.xml`, `docProps/app.xml`.
- `document.xml` body = a sequence of `<w:p>` paragraphs; headings are bold runs with a
  bottom border (`<w:pBdr><w:bottom …/>`); bullets use `<w:numPr>` referencing a
  numbering definition. Set `<w:sectPr><w:pgMar …/></w:sectPr>` for margins
  (720 twips = 0.5", 540 = 0.375").
- Validate after writing: `zipfile.ZipFile.testzip()` must be `None`, and each XML part
  must parse with `xml.dom.minidom.parseString`. Confirm magic bytes `PK\x03\x04`.
- **ATS-safe shape:** single-column, NO tables, dates inline with the title on one line,
  standard headings. This is the generator in `scripts/generate_ooxml_docx.py`.

## Why not OfficeCLI here
OfficeCLI is purpose-built for *AI agents to edit existing* Office files — great for
downstream tweaks (bulk keyword swaps across many tailored versions), but (a) it's a .NET
single binary with the macOS-arm64 JIT/entitlement failure noted above, and (b) it's an
*edit* tool, not a from-scratch clean generator. For fresh ATS-safe generation, the
stdlib OOXML route is lower-risk. Keep OfficeCLI as an optional *later* edit tool, tested
in a throwaway first given that caveat.

## Verification without a Word renderer
No Word/LibreOffice needed to confirm correctness: extract the plain text (regex
`<w:t[^>]*>(.*?)</w:t>`) and confirm headings, inline dates, and (if tailored) JD keywords
appear linearly. For one-page fit, see `references/one-page-fit-and-research.md` (geometry
math). This pattern is what let us ship a verified, ATS-safe DOCX on a machine with no
working pip and no Office renderer.
