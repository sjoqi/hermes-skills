---
name: code-review
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when G wants to review a branch, a PR, work-in-progress changes, or asks to 'review since X'."
platforms: [macos, linux, windows]
---

# Code Review (two axes, never merged)

Two-axis review of the diff between `HEAD` and a fixed point G supplies:
- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / PRD / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's
context, then this skill aggregates their findings.

Adapted from Matt Pocock's `code-review` skill (github.com/mattpocock/skills),
using Hermes `delegate_task` for the parallel axes.

## Process

### 1. Pin the fixed point
Whatever G said is the fixed point — a commit SHA, branch name, tag, `main`,
`HEAD~5`, etc. If they didn't specify, ask.
Capture the diff command: `git diff <fixed-point>...HEAD` (three-dot, against the
merge-base). Also `git log <fixed-point>..HEAD --oneline`.
Before going further, confirm the fixed point resolves (`git rev-parse
<fixed-point>`) and the diff is non-empty. A bad ref or empty diff must fail
here — not inside the sub-agents.

### 2. Identify the spec source
Look for the originating spec, in order:
1. Issue references in commit messages (`#123`, `Closes #45`) — fetch if possible.
2. A path G passed as an argument.
3. A PRD/spec file under `docs/`, `specs/`, or `.scratch/` matching the branch.
4. If nothing found, ask G where the spec is. If none, the **Spec** axis skips
   and reports "no spec available" (never invents requirements).

### 3. Identify the standards sources
Anything documenting how code should be written: `CODING_STANDARDS.md`,
`CONTRIBUTING.md`. On top of that, the Standards axis always carries the
**smell baseline** below (Fowler, _Refactoring_ ch.3) — applies even when a repo
documents nothing. Two rules bind it:
- **The repo overrides** — a documented repo standard always wins.
- **Always a judgement call** — each smell is a labelled heuristic, never a hard
  violation; skip anything tooling already enforces.

Smell baseline (each: what it is → how to fix):
- **Mysterious Name** — name doesn't reveal what it does/holds → rename it.
- **Duplicated Code** — same logic shape in >1 hunk/file → extract and call.
- **Feature Envy** — a method reaches into another object's data more than its
  own → move the method onto the data it envies.
- **Data Clumps** — same few fields/params travel together → bundle into one type.
- **Primitive Obsession** — a primitive/string standing in for a domain concept →
  give it its own small type.
- **Repeated Switches** — same switch/if-cascade on the same type recurs →
  polymorphism, or one shared map.
- **Shotgun Surgery** — one logical change forces scattered edits → gather into
  one module.
- **Divergent Change** — one file edited for several unrelated reasons → split.
- **Speculative Generality** — abstraction/params/hooks for needs the spec lacks
  → delete; inline until a real need shows.
- **Message Chains** — long `a.b().c().d()` navigation → hide behind one method.
- **Middle Man** — a class/function that mostly delegates → cut it, call direct.
- **Refused Bequest** — a subclass that ignores/overrides most of what it
  inherits → drop inheritance, use composition.

### 4. Spawn both sub-agents in parallel
Use `delegate_task` with **two leaf agents** (no memory of this chat). Pass each
the diff command + commit list and relevant context.
- **Standards agent**: report per file/hunk — (a) every violation of a documented
  standard (cite file + rule); (b) any baseline smell (name it, quote the hunk).
  Distinguish hard violations from judgement calls; skip tooling-enforced. <400 words.
- **Spec agent**: report (a) spec requirements missing/partial; (b) behavior not
  asked for (scope creep); (c) requirements implemented but looking wrong. Quote
  the spec line per finding. <400 words.
If the spec is missing, skip the Spec agent and note it in the report.

### 5. Aggregate
Present the two reports under `## Standards` and `## Spec` headings, verbatim or
lightly cleaned. Do **not** merge or rerank — the axes are deliberately separate.
End with one line: total findings per axis, and the worst issue within each axis.
Don't pick a single winner across axes.

## Why two axes
A change can pass one axis and fail the other (standards-clean but wrong thing;
spec-exact but breaks conventions). Separate reporting stops one masking the other.

## Notes
- This skill is the tail of the Build Chain; `project-kickoff` produces the spec
  it checks against.
