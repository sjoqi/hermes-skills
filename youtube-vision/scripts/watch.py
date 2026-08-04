#!/usr/bin/env python3
"""YouTube Vision — send a YouTube URL to Google Gemini so it can WATCH the
video (frames + audio), then print back what Gemini understood.

Gemini is the only mainstream model with native YouTube-URL video input, so
this gives Hermes genuine *visual* understanding of a video, not just its
auto-generated transcript.

Requires: google-genai (installed on first run via `uv run`)
Auth:     GEMINI_API_KEY env var, or a .env file next to this script.
"""

import os
import re
import sys
import argparse

# ---------------------------------------------------------------------------
# Load GEMINI_API_KEY from .env in the skill dir (no python-dotenv needed)
# ---------------------------------------------------------------------------
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))


def load_env_key():
    env_path = os.path.join(SKILL_DIR, "..", ".env")
    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() == "GEMINI_API_KEY":
                        return v.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return None


# ---------------------------------------------------------------------------
# URL validation — accept any standard YouTube form / raw 11-char ID
# ---------------------------------------------------------------------------
YT_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{11}$")


def normalize_youtube_url(raw: str) -> str | None:
    raw = raw.strip()
    if YT_ID_RE.match(raw):
        return f"https://www.youtube.com/watch?v={raw}"
    if "youtu.be/" in raw:
        vid = raw.split("youtu.be/")[1].split("?")[0].split("/")[0]
        if YT_ID_RE.match(vid):
            return f"https://www.youtube.com/watch?v={vid}"
    if "youtube.com/" in raw:
        return raw  # watch?, shorts/, embed/, live/ all pass through
    return None


def main():
    p = argparse.ArgumentParser(description="Watch a YouTube video with Gemini vision.")
    p.add_argument("url", help="YouTube URL, youtu.be link, or 11-char video ID")
    p.add_argument(
        "--prompt",
        default="Fully understand this video. Summarize what it is about, "
        "covering both what is said AND what is shown visually. "
        "Include key moments with MM:SS timestamps.",
    )
    p.add_argument(
        "--model",
        default="gemini-3.6-flash",
        help="Gemini model (default: gemini-3.6-flash, the working free-tier model for new keys).",
    )
    p.add_argument(
        "--out",
        default=None,
        help="Optional path to save the answer as a .md file.",
    )
    args = p.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY") or load_env_key()
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found. Put it in .env next to this script "
              "or export it as an environment variable.", file=sys.stderr)
        sys.exit(2)

    video_url = normalize_youtube_url(args.url)
    if not video_url:
        print(f"ERROR: could not parse a YouTube URL from: {args.url!r}", file=sys.stderr)
        sys.exit(3)

    # Lazy import so `uv run` can install the dep on first invocation.
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("ERROR: google-genai not installed. Run: uv pip install google-genai",
              file=sys.stderr)
        sys.exit(4)

    client = genai.Client(api_key=api_key)

    # Interactions API: Gemini accepts a YouTube URL as a video part directly.
    interaction = client.interactions.create(
        model=args.model,
        input=[
            {"type": "video", "uri": video_url},
            {"type": "text", "text": args.prompt},
        ],
    )

    answer = getattr(interaction, "output_text", None)
    if answer is None:
        # Fallback for alternate response shapes
        answer = str(interaction)

    print(answer)

    if args.out:
        with open(args.out, "w") as f:
            f.write(f"# YouTube Vision summary\n\nSource: {video_url}\nModel: {args.model}\n\n")
            f.write(answer)
        print(f"\n[ saved to {args.out} ]", file=sys.stderr)


if __name__ == "__main__":
    main()
