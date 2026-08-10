---
name: publishing-skills-to-public-repo
description: "Publish agent skills (or any working-directory artifacts) from ~/.hermes to a PUBLIC GitHub repo safely — screening for PII and secrets before the push, excluding third-party and personal skills you shouldn't republish, and running incident response when sensitive data has already been committed. Load whenever the user says 'push my skills to GitHub', 'publish this repo', 'sync the skill library', or reports that private information reached a public repo."
platforms: [macos, linux]
---

# Publishing skills to a public repo

Pushing `~/.hermes/skills` to GitHub feels routine. It is not: skill directories
accumulate **real user data** from the tasks that created them — resumes, invoices,
API keys in examples, `/Users/<name>` paths, client names. A public repo is
**irreversible**: once a commit lands, deleting the file later does not remove it.

Sibling: `hermes-skill-plugin-install` covers *installing* skills from a repo. This
skill covers the opposite direction.

## Step 1 — Decide WHAT is yours to publish (authorship, not mtime)
`find -mtime -N` lists recently *touched* files, which includes **third-party skills
installed** in that window. Publishing those republishes someone else's work under the
user's name.

Before selecting, classify every candidate:
- **Authored with the user** → publishable.
- **Third-party installed** (hub `tap`/`install`, `plugins install`, a vendor bundle —
  e.g. an `omh/*` plugin pack, `defuddle`, `browser-cdp`) → **exclude**.
- **Bundled with Hermes** → exclude.
- **Personal/operational** (skills encoding the user's private working rules, standing
  corrections, personal preferences — e.g. a `working-with-<user>` skill) → **do not
  push silently to a public repo. Ask.** It may be fine, but it is the user's call.

State the exclusions and the reason in your reply — don't drop them quietly.

## Step 2 — Screen for PII and secrets BEFORE the first push
Run against the staging copy, not just the source. Use `scripts/screen_for_pii.sh`.

Cover at minimum: emails, phone numbers (**including non-US formats** like `+62`),
real names, LinkedIn/GitHub/Telegram/social handles, numeric chat IDs, cities and
employers and schools, API keys (`sk-`, `gho_`, `ghp_`, `AKIA`, `AIza`, `xoxb-`, JWTs,
`PRIVATE KEY`), `.env` contents, and absolute paths containing a username
(`/Users/<name>`, `/home/<name>` — an identity leak on its own).

**Highest-risk file classes** (grep these first — they are where PII hides):
- Resume/CV, invoice, letter, and document-generation scripts — *made of* PII.
- `__main__` demo blocks, docstring `USAGE:` examples, `references/*.py` recipes.
- Anything with "example", "demo", "sample", or "test" in the name. The word "demo"
  creates false confidence; demo data is exactly where real data gets pasted.

## Step 3 — Verify the redaction actually worked
- **Grep the generated artifact, not just the source.** For `.docx`/`.xlsx`/`.pptx`,
  unzip and grep the inner XML (`word/document.xml`). PII assembled at runtime is
  invisible to a source-level grep.
- **Re-run the screening script over the staging dir after edits.**
- **Widen the pattern after the first hit.** The initial grep catches the obvious
  fields; docstrings, comments, and output filenames often retain a nationality,
  employer or name variant the first pattern missed.
- **Check sibling skills.** Demo blocks get copy-pasted between related skills. Finding
  PII in one document-generation skill means grepping *all* of them.

## Step 4 — Verify the push by fresh clone
Never trust local state or the push output. `git clone` into a temp dir and list the
files actually on the remote. Confirm the commit hash and the expected file set.

## Step 5 — Incident response: PII is already public
Redacting in a new commit is **not remediation** — `git log -p` still serves the
original. Work in this order:

1. **Assess blast radius first.** `gh repo view --json forkCount,stargazerCount,visibility`.
   Zero forks / zero stars / few commits = a clean rewrite is viable. Forks mean the
   data is copied beyond your control and you must say so plainly.
2. **Date the exposure.** `git log --format='%h %ad' --date=short -- <path>` — the user
   needs to know how long it was public.
3. **Full clone, not shallow.** `--depth 1` hides history; audits need everything.
4. **Audit the whole repo, not just the reported file.** Split into two parallel
   subagents: one on the **working tree**, one on **complete history** (deleted files,
   every commit diff, binary blobs, **and `git log --format='%an %ae'`** — the commit
   author email is itself a leak if it isn't a GitHub `noreply` address).
5. **Fix locally and hold the push** until audits return, so there is exactly one
   history rewrite rather than several.
6. **Let the user choose the remediation** — history rewrite (`git filter-repo` +
   force-push) vs. delete-and-recreate the repo vs. accept. Rewriting public history
   is destructive and is the user's decision, not yours. Present blast radius and
   trade-offs, then ask.
7. **Tell the user credentials must be rotated, not just redacted.** Any exposed token
   is compromised permanently regardless of what you do to the repo.

## Pitfalls
- **`--depth 1` clones hide the problem.** Shallow clones make history look clean.
- **"It's just demo data" is how this happens.** Treat every example block as publishable
  to the world, because it is.
- **Fixing the reported file and stopping.** The user reports what they noticed; assume
  more exists and audit systematically.
- **Don't wait on the audit to fix what you already found** — redact locally while
  subagents run, but do not push until they report.
- **Non-US phone/address formats evade naive regexes.** Match the user's actual locale.
- **A pre-existing bug may be sitting in the same file.** The leaked script here also had
  a never-executable `IndentationError` — published code had clearly never been run. When
  you touch a published script, syntax-check and actually execute it.
- **Distinguish your own edit's breakage from pre-existing breakage** before claiming a
  fix: verify against the pristine remote copy, then say which it was.

## Reference
- `references/pii-leak-incident-2026-08.md` — worked example: real resume PII in three
  skill demo blocks, one already public. Detection, redaction, verification, blast-radius
  assessment, and the audit dispatch briefs.
- `scripts/screen_for_pii.sh` — re-runnable pre-push screen. Run before every push.
