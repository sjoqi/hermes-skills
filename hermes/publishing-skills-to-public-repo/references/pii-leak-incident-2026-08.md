# Worked example — real PII in skill demo blocks reached a public repo (2026-08)

Session-specific detail for `publishing-skills-to-public-repo`. Kept as a reference
because the *shape* of this incident recurs; the specifics do not.

## What happened

Skills were pushed from `~/.hermes/skills` to a public repo (`sjoqi/hermes-skills`,
8 → 20 skills). A pre-push secret scan was run — but it only covered **tokens, keys,
and the user's Telegram ID**. It did **not** cover names, emails, phones, employers,
or schools. It reported clean. The push proceeded.

The user then found their own identity in the published code, by reading the repo on
GitHub — not from any tooling.

## Where the PII actually was

All three hits were in **demo / example blocks**, never in real logic:

| File | Contents |
|---|---|
| `resume-cv-building/scripts/generate_ooxml_docx.py` | Real full name, gmail, LinkedIn handle, city, employer, university, biography — in the `__main__` demo. **This one was public.** |
| `pdf-resume-builder/references/build_resume.py` | Same, **plus a real phone number** |
| `pdf-generation/references/insert_htmlbox_recipe.py` | Same, **plus a second, different phone number** |

Two of the three were local-only, so exposure was limited to one file. Discovering them
required grepping *sibling* skills after the first hit — the demo block had been
copy-pasted between related document-generation skills.

A **fourth** hit surfaced later still, in the module **docstring** `USAGE:` example
(`"Indonesian (Native)"`) — a nationality, not a name, so the name/email/phone patterns
missed it entirely. Lesson: after the first find, re-read the whole file, don't just
re-grep it.

## Blast radius assessment (do this before proposing remediation)

```bash
gh repo view OWNER/REPO --json forkCount,stargazerCount,isFork,visibility
git log --format='%h %ad %s' --date=short -- <path>   # when did it become public
git rev-list --count HEAD                              # how much history to rewrite
```

Result here: **0 forks, 0 stars, 4 commits**, exposed since a commit ~4 days earlier.
That combination makes a history rewrite genuinely clean — no downstream copies exist.

## Remediation actually performed

1. Redacted to obviously-fictional placeholders: `Jane Q. Example`,
   `jane.example@example.com`, `+1 555-0100`, `Anytown, USA`,
   `Example Logistics Co.`, `State University`.
2. **Verified by generating the artifact** — ran the generator, unzipped the resulting
   `.docx`, grepped `word/document.xml`, confirmed `CLEAN`. Source-level grep alone was
   not treated as sufficient.
3. Swept **all** skills for the same strings, catching the two local-only files.
4. Added a `⚠️ DEMO DATA MUST STAY FICTIONAL` comment at the demo block, plus a
   first-position pitfall in `resume-cv-building`, so the mistake is hard to repeat.
5. **Held the push** pending audits, so one rewrite could cover everything.

## Incidental finding worth its own note

The published `generate_ooxml_docx.py` had a pre-existing **`IndentationError`** — an
`elif` body at the wrong indent level. It could never have run. Verified against the
pristine remote copy to confirm it was pre-existing and *not* caused by the redaction
edit, then fixed.

Two lessons: published code had clearly never been executed; and when your edit is
followed by a syntax error, check the original before assuming you caused it.

## Audit dispatch shape (two parallel subagents)

The split that matters is **working tree vs. complete history**, because data committed
and later deleted is invisible in the tree yet permanently public.

- **Agent 1 — working tree.** Emails, phones (incl. `+62`), real names (with locale-aware
  naming patterns), social handles, numeric chat IDs, addresses/employers/schools, keys
  and tokens, `/Users/<name>` paths, connection strings, biographical detail in demo data.
  Require file path + line number + severity, and require obvious placeholders be reported
  as `FALSE-POSITIVE` rather than omitted, so the reviewer can check the judgement.
- **Agent 2 — full history.** Every commit's author name/email (`%an %ae` — a personal
  address in commit metadata is itself a leak unless it's a GitHub `noreply`), every file
  that ever existed (`--diff-filter=A`), the complete `git log -p` patch text, any binary
  blobs, and **most importantly** anything present in history but absent from HEAD, listed
  separately because only those require a rewrite.

Both must be told the repo is already fully cloned at a known path (`--depth 1` would
defeat the history audit) and that the known leak is being handled separately, so they
spend effort on finding *new* problems.
