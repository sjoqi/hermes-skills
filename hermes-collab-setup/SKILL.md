---
name: hermes-collab-setup
description: "Prepare the Hermes collaboration environment for a recurring human+AI software-building partnership: build a durable 'Home Base' (PLAYBOOK/RESOURCES/GLOSSARY) and the reusable Build-Chain skills (project-kickoff, tdd, ubiquitous-language, resource-capture, code-review) modelled on Matt Pocock's agent-skills chain. Use when a user wants to 'set up how we work together', 'prepare the environment', or 'structure our collaboration' before a big project."
platforms: [macos, linux, windows]
---

# Hermes Collaboration Setup

A repeatable way to wire up a durable human+AI software partnership so each new
project reuses the same conventions instead of re-teaching Hermes from scratch.

## When to use
- User says "set up how we work", "prepare the environment", "structure our
  collaboration", or wants reusable workflows before a big build.
- Inspiration: Matt Pocock, "Software Fundamentals Matter More Than Ever" +
  his open-source `skills` repo (github.com/mattpocock/skills) — a chain of
  plain-file skills: grill → to-spec → to-tickets → implement → code-review.

## The Build Chain (core idea)
```
grill → to-spec → to-tickets → implement (tdd) → code-review
```
Each step's output feeds the next. Roles: human = strategic architect; Hermes
= tactical executor. Shared understanding BEFORE code.

## Steps
1. **Home Base folder** at `~/hermes-home/` (or user-chosen path):
   - `PLAYBOOK.md` — roles, Build Chain, cross-cutting rules (checkpoint rule,
     deep modules, vertical slices, two-axis review, ubiquitous language + ADRs).
   - `RESOURCES.md` — distilled reusable principles from shared resources.
   - `GLOSSARY.md` — shared collaboration vocabulary.
   Pin it as a Hermes **Project** so it anchors in the sidebar.
2. **Build the 5 reusable skills** under `~/.hermes/skills/software-development/`:
   - `project-kickoff` (grill→to-spec→to-tickets + enforce git checkpoint).
   - `tdd` (red-green, one behaviour at a time; tracer bullet first).
   - `ubiquitous-language` (CONTEXT.md glossary + ADRs).
   - `resource-capture` (consume via youtube-vision/web → distil → RESOURCES.md).
   - `code-review` (two axes — Standards + Spec — never merged; parallel sub-agents).
   Each needs frontmatter `name` + `description` (description drives auto-invoke).
3. **Tee up the youtube-vision skill** if video understanding is wanted (sends
   YouTube URLs to Gemini; needs GEMINI_API_KEY in a chmod-600 `.env`).
4. **Save durable context to memory**: roles, standing rules (checkpoint rule!),
   Home Base path, profile note (one default profile — no separate agents/
   profiles needed; subagents spawned internally by Hermes).
5. **Verify**: `skill_view` each new skill returns `readiness_status: available`.

## Principles (enforced after the first build)
- **Fetch the real source before adapting.** When adapting an external
  system/skill (e.g. Matt Pocock's `skills`), pull the ACTUAL source files and
  adapt them faithfully — do NOT reconstruct from docs or a summary. The user
  explicitly caught a from-scratch reconstruction and asked to fetch-and-adapt
  instead. Source fidelity > reconstruction.
- **Dry-run the chain before declaring done.** Skills that `skill_view` as
  "available" can still have defects. Exercise the full chain (grill → spec →
  tickets → one TDD ticket → code-review) on a throwaway repo. This caught a real
  bug: `git tag checkpoint-working` errors on a duplicate tag (it already exists
  from repo init) — the fix is `git tag -f checkpoint-working`.
- **Mitigate with offsite backup.** Push Home Base + custom skills to GitHub as
  two repos (no secrets — `.env` gitignored). Add a weekly cron running a sync
  script so the backup stays live. Backup script: `~/.hermes/scripts/backup-hermes.sh`.

## Pitfalls
- Don't overbuild "CI/CD" infrastructure — Hermes isn't that; files + skills
  are the real environment.
- Never store secrets in the Home Base or memory; key in chmod-600 `.env`.
- The checkpoint rule is sacred: `git commit` + `git tag -f checkpoint-working`
  (force-move — the tag already exists from init, so plain `git tag` errors on
  duplicate) before ANY change to a working build.
- Keep the playbook editable — review/extend it per project, don't freeze it.

## Verification
After building, load one or two skills with `skill_view` to confirm they're
available and the descriptions are right.
