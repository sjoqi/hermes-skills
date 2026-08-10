---
name: hermes-mobile-access
description: Get Hermes into a user's pocket via a messaging platform (Telegram-first), explain where sessions/chat history are actually stored, and move a live conversation between desktop and phone. Use when the user wants to chat with Hermes from their phone, asks which messaging platform to pick (cost/performance concerns), asks where sessions live, or wants to continue a desktop session on mobile (or vice versa).
---

# Hermes Mobile Access (phone / messaging gateway)

## When to use
- User wants to talk to Hermes from a phone or outside the desktop app.
- User asks "which platform should I use — Telegram/Discord/WhatsApp/Signal?"
- User asks where chat history / sessions are stored, or whether a session lives in a project folder.
- User wants to hand a live conversation to their phone (or pull it back to desktop).
- User runs `hermes pairing approve ...` or asks about bot setup.

## Core mental model (answer from this, don't guess)
1. **The messaging platform is just a transport pipe.** It relays messages to the Hermes *gateway* process running on the host machine. The platform does NOT store your conversation.
2. **All chat history lives in one local SQLite DB:** `~/.hermes/state.db` (plus `state.db-wal` / `state.db-shm`). This holds CLI, Telegram, Discord, cron — every session — each tagged with a `source` column (`cli`, `telegram`, `discord`, ...). Location is overridable via `HERMES_HOME`.
3. **"Where Hermes works" ≠ "where Hermes remembers."** The desktop app / terminal sets a *working directory* per project (e.g. `~/Documents/Projects/Upwork`), so files you create land there. But the *conversation* always goes to the global `~/.hermes/state.db`, never the project folder. A project folder may contain a `.hermes/desktop-attachments/` dir — that is only scratch space for drag-in files, NOT the session store.
4. **The gateway must be running for the bot to respond.** If the host is off or the gateway process died, the bot is silent and nothing new is stored. For "always reachable on my phone," install it as a service (see below).

## Platform recommendation (phone + cheap + light → Telegram)
The platform is NOT where cost/performance comes from. Cost = model tokens + tool calls (identical on every platform). The platform is a free, thin relay. So pick the free, lightest, most phone-native option:

| Platform | Free? | Voice memo→text | Setup overhead | Notes |
|---|---|---|---|---|
| **Telegram** | Yes | ✅ auto-transcribe | Lowest (1 BotFather token) | Most mature adapter; images/files/threads/streaming/typing |
| Discord | Yes | ✅ | Medium (server+invite) | Most features but heavier |
| Signal | Yes | ❌ | Medium (phone #) | No voice |
| WhatsApp | Yes* | ❌ | High (needs 2nd phone #) | Bot mode = extra number cost |
| Slack | Yes | ✅ | Medium | Workspace needed |
| SMS / Email | **No** | ❌ | Needs paid provider (Twilio) | Avoid if cost matters |

→ **Default to Telegram.** Full-featured, free, lightest setup, best mobile app.

## Telegram setup (verified on macOS)
```bash
# 1. In Telegram, message @BotFather → /newbot → get token (looks like 123456789:ABC...)
# 2. Interactive wizard (writes ~/.hermes/.env):
hermes gateway setup          # pick Telegram, paste token + your numeric user ID
# 3. Run it. As a launchd service so it survives restarts/logout:
hermes gateway install        # macOS: user service
hermes gateway start
```
- Find your numeric user ID via @userinfobot or @get_id_bot (NOT your @username).
- Approve a pairing code from terminal: `hermes pairing approve telegram <CODE>` (codes expire 1h).
- The `.env` keys: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USERS` (comma-sep numeric IDs), optionally `TELEGRAM_HOME_CHANNEL`.
- Set the bot's home channel once by DMing the bot `/sethome` (required for handoff target).

## Cross-platform handoff (desktop ⇄ phone)
A session is one record in `state.db`. **Handoff is a transfer, not a live mirror** — one session binds to one active channel at a time. You CAN ping-pong, but not truly simultaneously type into both.
- Desktop → Telegram: `/handoff telegram` (from a CLI/TUI session; may not surface in the desktop composer — fallback: `hermes chat` then `/handoff telegram`).
- Telegram → desktop: `hermes -r "<title>"` or `/resume <title>`.
- History is continuous both ways (same session id). Gateway + home channel must be configured first.

## Pitfalls
- **Handoff ≠ mirror.** Don't promise "both inputs at once." It's switch-between-as-you-move, not two parallel live streams.
- **Local DB = single point.** If the host dies, the bot dies and history is whatever was last written. For resilience, run the gateway as a service and/or on a cheap always-on host.
- **Don't confuse project `.hermes/` with the session store.** `Project/.hermes/desktop-attachments/` is file-staging only.
- **Don't convert gateway to a service mid-conversation.** `hermes gateway install` stops the manual gateway first — do it after the chat wraps, or the live session disrupts.
- **WhatsApp/Signal caveats:** no voice memo transcription; WhatsApp needs a second phone number (extra cost).

## Verification commands (run these, don't assume)
```bash
hermes gateway status                       # is it running? PID? service or manual?
ls -la ~/.hermes/state.db*                  # confirm the session store exists
# redact secrets when showing config:
python3 - <<'PY'
import os
p=os.path.expanduser("~/.hermes/.env")
if os.path.exists(p):
    for l in open(p):
        if l.strip().startswith("TELEGRAM"):
            k,v=l.strip().split("=",1); print(f"{k}=<set, {len(v)} chars>")
PY
```
See `references/session-storage.md` for the `state.db` schema highlights and how to query/resume Telegram sessions.
