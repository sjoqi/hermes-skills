---
name: tdd
description: "Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions 'red-green-refactor', or wants integration tests. One behaviour at a time (red-green), tracer-bullet first. Prevents outrunning the headlights with unverified edits."
platforms: [macos, linux, windows]
---

# Test-Driven Development

TDD is the red → green loop. This is the reference that makes that loop produce
tests worth keeping: what a good test is, where tests go, the anti-patterns, and
the rules of the loop. Every section applies on every cycle — consult them
before and during the loop, not after.

Adapted from Matt Pocock's `tdd` skill (github.com/mattpocock/skills).

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and
interface vocabulary match the project's domain language, and respect ADRs in
the area you're touching.

## What a good test is
Tests verify behavior through public interfaces, not implementation details.
Code can change entirely; tests shouldn't. A good test reads like a
specification — "user can checkout with valid cart" — and survives refactors
because it doesn't care about internal structure.

## Seams — where tests go
A **seam** is the public boundary you test at: the interface where you observe
behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams
under test and confirm them with G. No test is written at an unconfirmed seam.
You can't test everything — agreeing the seams up front lands testing effort on
critical paths and complex logic instead of every edge case.
Ask: "What's the public interface, and which seams should we test?"

## Anti-patterns
- **Implementation-coupled** — mocks internal collaborators, tests private
  methods, or verifies through a side channel. The tell: the test breaks on
  refactor but behavior hasn't changed.
- **Tautological** — the assertion recomputes the expected value the way the
  code does (`expect(add(a,b)).toBe(a+b)`), so it passes by construction and can
  never disagree. Expected values must come from an independent source of truth
  — a known-good literal, a worked example, the spec.
- **Horizontal slicing** — writing all tests first, then all implementation.
  Bulk tests verify *imagined* behavior and go numb to real changes. Work in
  **vertical slices** instead — one test → one implementation → repeat, each
  test a **tracer bullet** responding to what the last cycle taught you.

## Rules of the loop
- **Red before green.** Write the failing test first, then only enough code to
  pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per
  cycle. The very first cycle is a **tracer bullet**: one test proving a single
  end-to-end path works before building outward.
- **Refactoring is not part of the loop.** It belongs to the review stage
  (see `code-review`), not the red → green cycle. Refactor only when green.

## Before the loop (per project)
Confirm a test runner is installed for this repo's language. If none: set one up
first — e.g. `npm i -D vitest` (JS/TS), `pip install pytest` (Python), or use the
language's built-in (Go `testing`, Rust `cargo test`). Don't run the loop against
a missing runner; wire it before the first RED.
