# Verified Workspace Mechanics — exact command outputs

Captured on this machine (macOS 15.6, Hermes via `nous` provider). Use as the
ground-truth reference when re-verifying after a Hermes update changes behavior.

## terminal.cwd default resolution

`hermes config get terminal.cwd` returned `.` → Desktop app launched in home `~`
(`/Users/<you>`), NOT the Hermes home dir. Setting it:

```
$ hermes config set terminal.cwd /Users/<you>/hermes-home
✓ Set terminal.cwd = /Users/<you>/hermes-home in /Users/<you>/.hermes/config.yaml

$ hermes config get terminal.cwd
/Users/<you>/hermes-home
```

Docs (config page, "Working Directory" section) confirm the resolution table:
- CLI: current launch dir
- Messaging gateway / cron: `terminal.cwd`; if unset, home `~`
- (Desktop behaves like the gateway fallback when cwd is `.` → home `~`)

## Project system

```
$ hermes project list
* upwork                   Upwork  [1 folder(s)]
  wifi-sense-through-wall-human-pose-presence-detection WiFi-Sense...  [1 folder(s)]
  hermes-home              hermes-home  [1 folder(s)]
```

```
$ hermes project show hermes-home
hermes-home  [p_6ef8f088]
  name:    hermes-home
  primary: /Users/<you>/hermes-home
  folders:
    * /Users/<you>/hermes-home
```

Note: `n8n-docker` was NOT in this list — it was a loose folder at home root,
not a registered project. A folder must be `hermes project create`d + folder-added
to be switchable.

## Context-file discovery

Verified via the official context-files doc:
- Priority: `.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules` (first wins)
- `SOUL.md` loads only from `HERMES_HOME`, independently of cwd
- Outside a git repo, only the cwd itself is checked (parents never consulted)
- Progressive discovery: reading subfolders during a session loads their context

Creating `~/hermes-home/AGENTS.md` (1448 bytes) made it auto-load from the next
new session onward (context loads at session STARTUP, not retroactively in the
current session).

## Escape hatch

`hermes chat --no-restore-cwd` — launches with zero cwd/Home-Base framing.

## Relocate-before-move safety check (P2/P3)

```
$ docker ps --filter "name=n8n" --format "{{.Names}} {{.Status}}"
n8n-docker-n8n-runner-1 Up 2 days
n8n-docker-n8n-1 Up 2 days
n8n-docker-postgres-1 Up 2 days (healthy)
```

n8n compose used ONLY relative mounts + named volumes (no hardcoded absolute
host paths), so a stop → mv → `docker compose up` would have worked — but the
running containers justified cancelling the move. Always check first.
