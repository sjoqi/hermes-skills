# Gemini model availability for NEW free-tier keys

Hard-won fact (2026-08, verified by live test): a freshly created Gemini API
key on the free tier does NOT get access to the Gemini 2.5 family.

Observed errors when calling the Interactions API with a new free-tier key:
- `gemini-2.5-flash` -> **404** "This model ... is no longer available to new
  users. Please update your code to use a newer model."
- `gemini-2.5-pro`   -> **429** quota 0 (limit: 0 for
  `generate_content_free_tier_requests` and `..._input_token_count`).

The working default for a new key is **gemini-3.6-flash** (GA as of 2026-08).
It natively accepts a YouTube URL as a `video` part via `client.interactions.create`
and returns real frame+audio understanding (timestamps, visual-only detail a
transcript can't capture).

## Rules of thumb when building any Gemini video/visual skill

- Do NOT hardcode `gemini-2.5-*` as the default — it 404s / quota-0s for new keys.
- Pin the current GA model (gemini-3.6-flash at time of writing) but verify the
  latest GA name at
  https://ai.google.dev/gemini-api/docs/video-understanding before shipping,
  because Google rotates model names.
- Free-tier limits observed: ~15 req/min, 8 hrs of YouTube video/day, public
  videos only (no private/unlisted/age-restricted).

## Verified live call shape (python, google-genai)

```python
from google import genai
client = genai.Client(api_key=GEMINI_API_KEY)
interaction = client.interactions.create(
    model="gemini-3.6-flash",
    input=[
        {"type": "video", "uri": "https://www.youtube.com/watch?v=<ID>"},
        {"type": "text", "text": "<prompt, ask for MM:SS timestamps>"},
    ],
)
print(interaction.output_text)
```

The Interactions API (`client.interactions.create`) is GA and accepts a YouTube
URL directly as a video part — no download, no File API upload needed.
