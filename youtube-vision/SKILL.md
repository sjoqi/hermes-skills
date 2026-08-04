---
name: youtube-vision
description: "Watch and fully understand a YouTube video — visual frames AND audio — by sending the URL to Google Gemini's video-understanding API. Use when the user shares a YouTube link and wants real comprehension of what is shown (not just auto-generated captions)."
platforms: [macos, linux, windows]
---

# YouTube Vision

## Why this exists

The sibling `youtube-content` skill only reads the *transcript* (spoken words /
captions). For many videos — demos, product reveals, charts, visual essays —
half the meaning is on screen, not spoken. This skill fixes that by handing the
YouTube URL to **Google Gemini**, the only mainstream model that accepts a
YouTube URL as native video input. Gemini watches the actual frames + audio and
returns grounded understanding, which Hermes then relays and can reason over.

## Setup (one time)

Dependencies are installed by `uv` automatically on first run. You only need a
free Gemini API key:

1. Get one (free): https://aistudio.google.com/apikey
2. Save it in the skill folder (already done once; to redo):
   ```
   echo "GEMINI_API_KEY=your-key" > ~/.hermes/skills/media/youtube-vision/.env
   chmod 600 ~/.hermes/skills/media/youtube-vision/.env
   ```
   The key is loaded from that `.env` (chmod 600) or from the `GEMINI_API_KEY`
   env var. It is never written to memory, logs, or git (see `.gitignore`).

## Usage (Hermes runs this)

`SKILL_DIR` is `~/.hermes/skills/media/youtube-vision`. The script lives in
`SKILL_DIR/scripts/watch.py`.

```bash
# Full visual+audio understanding (default prompt: summary w/ timestamps)
uv run python3 SKILL_DIR/scripts/watch.py "https://youtube.com/watch?v=VIDEO_ID"

# Ask a specific question about what is SHOWN
uv run python3 SKILL_DIR/scripts/watch.py "URL" \
  --prompt "What does the presenter draw on the whiteboard around 04:30, and what does it mean?"

# Best-quality model (gemini-2.5-pro is quota-zero on new free-tier keys;
# gemini-3.6-flash is the working default for new keys)
uv run python3 SKILL_DIR/scripts/watch.py "URL" --model gemini-3.6-flash

# Save the answer to a file
uv run python3 SKILL_DIR/scripts/watch.py "URL" --out ~/Desktop/video-notes.md
```

Accepts: full watch URLs, youtu.be links, shorts, embeds, live links, or a raw
11-character video ID.

## When to use

- User pastes a YouTube link and wants to *know what's in it*.
- The video is visual (demo, talk with slides, product reveal, tutorial).
- User asks about something shown on screen, not just said.

## Workflow

1. **Verify the URL** with the user if ambiguous; otherwise normalize it.
2. **Run** `uv run python3 SKILL_DIR/scripts/watch.py "<url>" [--prompt ...]`.
   First run installs `google-genai` into the uv-managed env.
3. **Relay** Gemini's answer to the user in plain language. Add your own
   synthesis/context on top — the skill fetches; you explain.
4. **Verify**: if the output is empty or errors, see Error Handling.

## Output formats / prompts

Tailor `--prompt` to what the user wants:
- *Summary* (default): "Summarize this video covering both what is said and
  what is shown, with MM:SS timestamps."
- *Tutorial extraction*: "List every on-screen code snippet or command with the
  timestamp it appears at."
- *Visual Q&A*: "Answer: what chart/diagram appears at <timestamp> and what does
  it show?"
- *Chapter list*: "Produce a timestamped chapter list of the video's sections."

## Error handling

- **Empty / error output**: confirm the video is public (no private, unlisted,
  or age-restricted). Gemini can only read public URLs.
- **Key missing**: print the setup step above; don't retry blindly.
- **Rate limit** (free tier ~15 req/min): wait a minute, retry.
- **Long videos are slow**: Gemini processes the whole video before replying;
  be patient, or use `--model gemini-3.6-flash` for speed.
- **Model unavailable (404/429)**: new free-tier keys do NOT get the Gemini 2.5
  family — `gemini-2.5-flash` returns 404 ("no longer available to new users")
  and `gemini-2.5-pro` returns quota-0. Use **gemini-3.6-flash** (the working
  default). If a model is later retired, check the current GA model at
  https://ai.google.dev/gemini-api/docs/video-understanding — details in
  `references/gemini-models.md`.

## Honesty note

Gemini samples video at ~1 frame/second by default, so very fast on-screen
action may lose detail. It also can't see private/unlisted videos. State these
limits when relevant rather than overclaiming.

## Reference files

- `references/gemini-models.md` — live-verified Gemini model availability for
  new free-tier keys (why `gemini-2.5-*` fails, what to pin instead, and the
  working `interactions.create` call shape). Read before changing the default
  model.
