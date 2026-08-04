#!/usr/bin/env python3
"""Zero-dependency .docx generator (Python stdlib only).

A .docx file is a ZIP archive of WordprocessingML XML. This module emits a
clean, single-column, TABLE-FREE Word document (headings, paragraphs, bullet
lists, and entry title+date lines) that is maximally ATS-parseable and requires
NO third-party packages (no python-docx, no LibreOffice, no OfficeCLI binary).

WHY THIS EXISTS: it is the fallback when python-docx can't be installed and
OfficeCLI (a .NET binary) is unreliable on macOS-arm64. Hand-rolled OOXML via
zipfile sidesteps all of that and stays fully under our control.

USAGE:
    from generate_ooxml_docx import build_docx
    sections = [
        {"kind": "heading", "text": "SUMMARY"},
        {"kind": "paragraph", "text": "Career-switching technologist..."},
        {"kind": "bullets", "items": [("Languages: ", "Indonesian (Native)"), ...]},
        {"kind": "entries", "entries": [
            ("Example Logistics Co. — Driver", "2025 – Present", ["Bullet one", "Bullet two"]),
        ]},
    ]
    build_docx("resume.docx", "Full Name", "contact line", sections)

The emitted document was validated: zip testzip == None, all XML parts
well-formed, correct PK magic, and plain-text extraction is linear.
"""
import zipfile
import os


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def _run(text, bold=False, italic=False, size=None):
    rpr = ""
    if bold:
        rpr += "<w:b/>"
    if italic:
        rpr += "<w:i/>"
    if size:
        rpr += f'<w:sz w:val="{size*2}"/><w:szCs w:val="{size*2}"/>'
    rpr = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    return f'<w:r>{rpr}<w:t xml:space="preserve">{_esc(text)}</w:t></w:r>'


def _para(runs, spacing_after=80, spacing_before=0):
    ppr = f'<w:spacing w:before="{spacing_before}" w:after="{spacing_after}"/>'
    return f"<w:p><w:pPr>{ppr}</w:pPr>{runs}</w:p>"


def _heading(text, size=14, after=120, before=200):
    run = _run(text, bold=True, size=size)
    ppr = (f'<w:spacing w:before="{before}" w:after="{after}"/>'
           '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="2" w:color="1A1A1A"/></w:pBdr>')
    return f"<w:p><w:pPr>{ppr}</w:pPr>{run}</w:p>"


def _bullet(runs_inner):
    ppr = ('<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
           '<w:spacing w:after="40"/>')
    return f"<w:p><w:pPr>{ppr}</w:pPr>{runs_inner}</w:p>"


def _entry(title_text, date_text, size=10.5):
    runs = _run(title_text, bold=True, size=size) + _run("  " + date_text, italic=True, size=9.5)
    return _para(runs, spacing_after=20, spacing_before=80)


def _body(text, size=10.5, after=80):
    return _para(_run(text, size=size), spacing_after=after)


def _list_item(text, size=10.5, bold_prefix=None):
    runs = _run(bold_prefix, bold=True, size=size) if bold_prefix else ""
    runs += _run(text, size=size)
    return _bullet(runs)


# ---- OOXML boilerplate (validated) -----------------------------------------

def _document_xml(parts):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body>'
        + "".join(parts) +
        '<w:sectPr><w:pgMar w:top="720" w:right="720" w:bottom="720" w:left="720" '
        'w:header="360" w:footer="360" w:gutter="0"/></w:sectPr>'
        '</w:body></w:document>'
    )


def _styles_xml():
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:docDefaults><w:rPrDefault><w:rPr>'
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
        '<w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr></w:rPrDefault></w:docDefaults>'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
        '<w:name w:val="Normal"/></w:style>'
        '</w:styles>'
    )


def _numbering_xml():
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0">'
        '<w:numFmt w:val="bullet"/><w:lvlText w:val="•"/>'
        '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="360" w:hanging="360"/></w:pPr>'
        '</w:lvl></w:abstractNum>'
        '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>'
        '</w:numbering>'
    )


def _content_types():
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
        '</Types>'
    )


def _root_rels():
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        '</Relationships>'
    )


def _doc_rels():
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
        '</Relationships>'
    )


def _core_props(name):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:title>Resume</dc:title>'
        f'<dc:creator>{_esc(name)}</dc:creator></cp:coreProperties>'
    )


def _app_props():
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
        '<Application>resume-cv-building skill docx generator</Application></Properties>'
    )


def build_docx(path, name, contact, sections):
    """Build a .docx from structured `sections`. See module docstring for the
    section schema. Returns the output path."""
    parts = [
        _para(_run(name, bold=True, size=20), spacing_after=20),
        _para(_run(contact, size=10), spacing_after=120),
    ]
    for s in sections:
        kind = s["kind"]
        if kind == "heading":
            parts.append(_heading(s["text"]))
        elif kind == "paragraph":
            parts.append(_body(s["text"]))
        elif kind == "bullets":
        for pre, txt in s["items"]:
            parts.append(_list_item(txt, bold_prefix=pre or None))
        elif kind == "entries":
            for title, date, bullets in s["entries"]:
                parts.append(_entry(title, date))
                for b in bullets:
                    parts.append(_list_item(b))
        else:
            raise ValueError(f"unknown section kind: {kind!r}")

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", _content_types())
        z.writestr("_rels/.rels", _root_rels())
        z.writestr("word/document.xml", _document_xml(parts))
        z.writestr("word/_rels/document.xml.rels", _doc_rels())
        z.writestr("word/styles.xml", _styles_xml())
        z.writestr("word/numbering.xml", _numbering_xml())
        z.writestr("docProps/core.xml", _core_props(name))
        z.writestr("docProps/app.xml", _app_props())
    return path


if __name__ == "__main__":
    # Demo: reproduces the resume used to validate this generator.
    demo_sections = [
        {"kind": "heading", "text": "SUMMARY"},
        {"kind": "paragraph", "text": "Career-switching technologist pivoting from leadership and event management into AI-agent and workflow automation."},
        {"kind": "heading", "text": "SKILLS"},
        {"kind": "bullets", "items": [
            ("Languages: ", "English (Native), Spanish (B2)"),
            ("Automation & CRM: ", "GoHighLevel, n8n Workflows, AI Agent Design, OpenAI API"),
        ]},
        {"kind": "heading", "text": "PROFESSIONAL EXPERIENCE"},
        {"kind": "entries", "entries": [
            ("Example Logistics Co. — Motorcycle Delivery Driver (Freelance)", "2025 – Present", [
                "Maintain a 5-star service rating across 500+ completed jobs.",
                "Reliably meet tight delivery windows in a high-traffic urban environment.",
            ]),
        ]},
        {"kind": "heading", "text": "EDUCATION & TRAINING"},
        {"kind": "entries", "entries": [
            ("State University — Landscape Architecture (incomplete)", "2023 – 2024", [
                "Self-directed study: CS50x, CS50AI (HarvardX).",
            ]),
        ]},
    ]
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_resume.docx")
    build_docx(out, "Jane Q. Example",
               "Anytown, USA | jane.example@example.com | linkedin.com/in/janeexample",
               demo_sections)
    print("WROTE", out, os.path.getsize(out), "bytes")
