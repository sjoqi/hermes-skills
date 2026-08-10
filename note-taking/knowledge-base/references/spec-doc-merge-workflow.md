# Spec-Doc Merge & Maintenance Workflow (kb/)

For tasks shaped like "merge node-spec hardening into `kb/target.md`" or
"update target.md with fix #N from companion.md" — the recurring delegated
subagent work on the lead-qualification / workflow spec stack. Target = ONE
file; companions = sources of the fixes. Validated on the 2026-08
agent-nodes.md merge (PromptTemplate anti-injection, draft sanitization,
score_rationale reset, PNG-fallback deletion).

## Workflow

1. **Read the CURRENT target first — in full.** A prior agent/session may have
   already patched it (in the validating session, a prior agent had added preset
   routing, a GATE-1 handoff row, and a mermaid update). Quoted line numbers in
   the task are stale after such patches — the gap-fixes doc cited lines 79/81/143,
   all off by one. Anchor every patch on **unique content strings**, never lines.
2. **Recon companions in parallel.** `search_files` on the kb/ dir for
   `*.md` to see the ecosystem, then targeted content searches with context
   (e.g. `pattern="PromptTemplate|score_rationale", context=6`), then read the
   full fix section so the merge is faithful to the source's wording, schemas,
   and failure modes. Batch the independent reads in one turn.
3. **Condense + point, don't duplicate.** The target gets the mechanism in
   compact prose — key class/function names, invariants, failure behavior
   (e.g. `error="prompt_injection_defense_triggered"` → DeadLetter) — plus a
   pointer: "Per `companion.md` fix #N" / "Fix 2". Full code blocks stay in the
   companion. Add a "Related" entry in the target's §Related pointing at each
   companion.
4. **Preserve the target's house style.** Spec docs use letter-suffix
   subsections (`4.1a`, not renumbered 4.2→4.3), pipe tables, `---` separators,
   `§` cross-refs, backticked field names. Match the genre — spec doc prose is
   terse and imperative; brainstorm notes are article-style. Don't renumber
   existing subsections to make room; append letter-suffix subsections.
5. **Edit ONLY the named file.** Even if a companion also needs the same change
   (e.g. its own copy of the Score row), it has its own patch task — leave it.
   Only the target's file path appears in any write.
6. **Serialize same-file patches.** One patch call per turn (or one V4A multi-
   hunk patch). Parallel same-file patches can race on file state.
7. **Verify by re-reading.** After all edits, re-read the changed regions and
   the file tail: confirm deletions are actually gone (the stale "PNG fallback"
   blockquote), additions landed in the right section, and no surrounding text
   drifted. Report the diff summary (line counts before/after) in the final
   summary.
8. **Touch every place the fix ripples.** A new output-schema field (e.g.
   `score_override` bool) means: schema block → handoff-table row → test
   assertions (T-score-4/T-score-6) → any mermaid note. A new test may need
   appending (T-draft-6) without renumbering existing ones.

## Pitfalls

- **Stale line numbers:** task/companion docs cite line numbers that shift as
  prior agents patch the target. Always content-match; include a couple of
  surrounding lines in `old_string` when the match could be ambiguous.
- **Deleting a blockquote:** include the preceding ``` fence and the following
  `---` in `old_string` so the match is unique and structure stays clean.
- **Deleting can leave stale prose references elsewhere:** removing the PNG-
  fallback blockquote left the §6 intro still claiming "the PNG below is the
  in-chat picture". After deleting any artifact mention, grep the file for the
  deleted subject ("PNG", "fallback", the artifact's name) and fix leftover
  references before finishing.
- **Table integrity after patch:** the patch tool once rewrote a pipe-table
  separator row to 4 cells under a 3-column header (`|---|---|---|---|` vs
  `| A | B | C |`). After any patch touching a table, re-read the region and
  verify the separator row's cell count matches the header row.
- **Companion spec beats the task brief on detail conflicts.** The delegated
  brief may paraphrase a companion imprecisely — a real case: the brief said
  the deletion API returns `410 Gone` when already erased, while the companion
  deliberately specifies idempotent `200 OK` for DELETE with `410 Gone`
  reserved for the post-erasure *replay* path. Rule: the named companion is
  the source of truth ("read companions first"); follow it, and FLAG the
  conflict explicitly in the final summary so the parent can overrule.
- **Inserting a bullet into an existing list:** place it after the logically
  related item (e.g. after "Failure:" in shared conventions), not at list end.
- **Over-merging:** resist pasting the companion's whole class/function into the
  target spec — specs stay pointer-first; the code lives in the hardening doc.
- **Subagent summary:** end with outcomes-led bullets (files touched, line
  delta, per-requirement checkmarks), not a process replay — the parent agent
  reads it into a crowded context.

## Multi-companion merges (two+ sources amend the same schema)

Validated on the 2026-08-10 entrylog-deadletter merge (GDPR split-store +
reliability-hardening + replay-api-security all touching `entry_log`):

- **Don't interleave column numbers — append.** The GDPR spec renumbered
  `entry_log` to 12 columns; reliability-hardening added `reconciled` and
  replay-security added `total_replays`, both as "column 9" of the *old*
  schema. Resolution: keep the primary spec's numbering intact and append the
  operational columns after it (13, 14), with the merge decision visible in
  the column's Purpose text.
- **Re-state the immutability rule after adding mutable columns.** The
  append-only paragraph must enumerate exactly which columns are now mutable
  (`notes`, `deletion_status`, `total_replays`, `reconciled`) so the
  "write-once" claim stays accurate; otherwise the doc contradicts itself.
- **Add an "Amended <date>" header line** naming all companions (one pointer
  line), keep the original Date line untouched, and update §Open-threads +
  §Related with a resolved/deferred entry per merged fix.
- **Ripple through the diagram too:** schema changes that move data (raw
  payload → separate `pii_store` tab) mean the mermaid flow gains a node and
  the edges re-target — update node labels and edge descriptions, not just
  the tables.
