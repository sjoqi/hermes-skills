---
name: session-title-rename
description: "Session done or drifted — rename it to its real topic."
version: 1.0.0
author: G + Hermes
license: MIT
tags: [hermes, sessions, rename, titles, organization]
metadata:
  hermes:
    tags: [hermes, sessions, rename, titles, organization]
    related_skills: [hermes-agent, hermes-self-introspection]
---

# Session Title Rename

Sessions are auto-titled from the **first prompt**, which usually stops matching what the session actually covered once the conversation grows. This skill renames the live session to a descriptive title so the user can find it later in `hermes sessions list`, `hermes sessions browse`, or the desktop app's session list.

## When to Use

- **Explicit user signal** — the user says the session is done or asks for a rename:
  "ok this session is done", "wrap it up", "session done", "rename this session", "ok done", "close this session", etc.
- **Agent-side judgment** — once the REAL topic is clearly established and differs from the current title. Typically: right after the first substantive exchange, at a natural break, when a multi-step task completes, or when the conversation visibly pivoted away from the opening prompt.

## How to do it

1. **Get the current session ID** (verified: available as an env var in every interactive session):
   ```bash
   echo "$HERMES_SESSION_ID"
   ```
   If empty (subagent / sandbox / cron), fall back to:
   ```bash
   hermes sessions list --limit 5
   ```
   and pick the newest session whose source is `cli` or `desktop` and whose content matches this conversation. Never guess an ID.

2. **Synthesize the title from the conversation's ACTUAL content** — not the first prompt:
   - 3–8 words, plain language, descriptive nouns.
   - Name the real topic / the deliverable produced / the question answered.
   - Examples: `Proton vs Sync pricing comparison`, `n8n webhook auth fix`, `Agency client onboarding docs`.
   - No dates, no emojis, no "Session about..." prefix.
   - If the conversation covered several sub-topics, use the dominant theme.

3. **Rename** (title takes multiple words — quote it):
   ```bash
   hermes sessions rename "$HERMES_SESSION_ID" "New Title Here"
   ```

4. **Verify** the rename landed:
   ```bash
   hermes sessions list --limit 3
   ```

## Pitfalls

- **No title churn** — rename once when the real topic is established; rename again only if the topic genuinely pivots or at session end. Don't rename every few turns.
- Skip renaming if `HERMES_SESSION_ID` is empty and no matching session can be found — don't guess a session ID.
- Don't rename gateway/cron/system sessions (sources like `telegram`, `discord`, `cron`) unless the user explicitly asks — those titles may be the user's thread names.
- Keep the title short — it exists for recall in a list, not as a summary.
- The user can also name a session manually by typing `/title My Name` in chat — mention this once when relevant (e.g. if they want a different style).
- Desktop app: the title is read from the session store; if the new title doesn't show immediately, it appears on the next session-list refresh.
