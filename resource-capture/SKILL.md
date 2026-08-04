---
name: resource-capture
description: "Capture a shared resource (YouTube video, article, link) into the Home Base library: consume it, distil the reusable principle, append to ~/hermes-home/RESOURCES.md, and update the playbook/glossary/skills if it changes how we work. Use when G shares something to 'save', 'watch later', or 'add to resources'."
platforms: [macos, linux, windows]
---

# Resource Capture

Turn a shared resource into a durable, reusable insight in the Home Base.

## When to use
- G pastes a link/video/article to keep, or says "capture this", "save it",
  "watch later".
- Default: **ad-hoc, on the spot**. If G sends many at once or says "later",
  batch them (optionally on a schedule) and tell G when done.

## Workflow
1. **Consume:**
   - YouTube/video → use the `youtube-vision` skill:
     `uv run python3 ~/.hermes/skills/media/youtube-vision/scripts/watch.py "<url>" --prompt "Distil the reusable engineering/collaboration principles, with timestamps."`
   - Article/link → `web_extract` (or `web_search` to locate).
2. **Distil** the *reusable principle* — not a raw transcript. What would we
   apply to future projects?
3. **Append** to `~/hermes-home/RESOURCES.md` under `## Resource Library`:
   ```
   ## <Type>: <Title>
   - URL: <url>
   - Captured: <date> (via youtube-vision / web)
   - Core thesis: <1-2 sentences>
   - Reusable principles: <bullets>
   - How we apply it: <link to playbook/skill/glossary>
   ```
4. **If it changes HOW we work** (new rule, new step, corrected assumption),
   update `~/hermes-home/PLAYBOOK.md` and/or `GLOSSARY.md`, and note if a skill
   needs a follow-up build/edit. Don't silently rewrite conclusions — state the
   change explicitly.

## Notes
- Never store API keys or secrets; the Home Base is plain notes.
- Keep entries principle-level so the library stays searchable and small.
