# Session storage reference — `~/.hermes/state.db`

SQLite (WAL mode). Single file holds every session across CLI, Telegram, Discord, cron, etc. Overridable via `HERMES_HOME`.

## Key tables
- `sessions` — metadata: `id`, `source` (cli/telegram/discord/...), `user_id`, `model`, `title` (unique non-null), `parent_session_id` (lineage on compression split), token counts, timestamps, estimated/actual cost.
- `messages` — full history: `session_id`, `role`, `content`, `tool_calls` (JSON), `tool_name`, `timestamp` (epoch float).
- `messages_fts` / `messages_fts_trigram` — FTS5 full-text search (trigram tokenizer powers CJK/substring search).

## Source tags (per platform)
`cli`, `telegram`, `discord`, `slack`, `whatsapp`, `signal`, `matrix`, `mattermost`, `email`, `sms`, `bluebubbles`, `cron`, `batch`, `api-server`, `webhook`, `acp`, ...

## Gateway session IDs
- CLI/TUI: 6-char hex suffix, e.g. `20250305_091523_a1b2c3`
- Gateway (Telegram etc.): 8-char suffix, e.g. `20250305_091523_a1b2c3d4`

## Resume / search a Telegram session
```bash
hermes -c "<title>"                 # resume most-recent titled session by name
hermes -r "<title>"                 # or by ID / title
hermes -r 20250305_091523_a1b2c3d4  # by full/unique-prefix ID
```
In Telegram/Discord: `/resume <name>`, `/title <name>`, `/usage`, `/compress`, `/new`.

## Pruning / privacy
- `hermes sessions prune` — delete old *ended* sessions from storage (use sparingly).
- `db.delete_session()` / `db.clear_messages()` (programmatic).
- Compression (`/compress`) shrinks live context; it is NOT a privacy delete.
- Back up `~/.hermes/state.db*` to preserve history; deleting it wipes all sessions.

## How multi-platform chat actually flows
```
phone → Telegram servers (transport only) → Gateway on host → ~/.hermes/state.db
```
Telegram never stores the conversation. The gateway process on the host does all the work and persistence. If the gateway is down, the bot is silent.
