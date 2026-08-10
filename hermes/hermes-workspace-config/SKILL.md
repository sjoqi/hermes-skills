---
name: hermes-workspace-config
description: >-
  Hermes default cwd, Project routing, AGENTS context loading.
version: 1
author: hermes-curator
license: MIT
metadata:
  hermes:
    tags: [hermes, config, workspace, projects, context-files]
    related_skills: [hermes-self-introspection, hermes-collab-setup, hermes-memory-setup]
---

# Hermes Workspace & Session-Start Configuration

## When to Use

Load this skill when the user asks any of:
- "where does Hermes start / what's my default directory"
- "change my default working directory" or "make Hermes open in my project"
- "why doesn't my AGENTS.md / CLAUDE.md load"
- wants to set up a Home Base launchpad (`~/hermes-home`)
- is about to relocate / rename / move a project folder (safety check first)
- asks how Projects relate to the working directory

Companion to `hermes-self-introspection` (the *methodology* — introspect before
guessing). This skill holds the *verified mechanics*. Re-verify against the live
CLI if Hermes has updated since capture (see `references/workspace-mechanics.md`).

How Hermes decides *where* a session begins and *which context files* load there.
All mechanics below were verified against the live CLI + docs on this machine —
not assumed.

## 1. Where a session starts (terminal.cwd)

`terminal.cwd` in `~/.hermes/config.yaml` is the single default. Resolves
differently per surface:

| Surface | Default when `terminal.cwd: .` | With `terminal.cwd: /abs/path` |
|---|---|---|
| **Desktop app** (Cmd+N) | User home `~` | That path |
| **CLI `hermes chat`** | Directory you launched from | That path |
| **Messaging gateway / cron** | Home `~` | That path |

Set it the right way (NEVER hand-edit config.yaml — stray indentation corrupts
it and breaks the live gateway):

```bash
hermes config set terminal.cwd /Users/<you>/hermes-home
hermes config get terminal.cwd          # verify it landed
```

## 2. The Project system

Projects are human-named workspaces that anchor session grouping and (when
kanban-bound) give deterministic worktree/branch conventions. Registered
projects are independent of the cwd default.

```bash
hermes project list          # lists projects; '*' = active, shows folder count
hermes project show <name>   # reveals primary folder (where context roots)
hermes project use <name>    # bind active session to that project's folder
hermes project use           # (no arg) clears the active project
```

Switching projects redirects the session to that project's primary folder, so
its context files load. Good pattern: keep `terminal.cwd` at a neutral Home Base
for chat + simple work, and `hermes project use <name>` (or `cd`) for focused
project work.

## 3. Context-file discovery (AGENTS.md / CLAUDE.md)

At session start Hermes loads the highest-priority context file from the working
directory: `.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules` (first match
wins). `SOUL.md` always loads from `HERMES_HOME`, independently.

- **Inside a git repo:** a merged chain from git-root down to cwd loads.
- **Outside a git repo:** only the working directory itself is checked — parents
  are NEVER consulted (so an `AGENTS.md` in `$HOME` can't leak into unrelated
  sessions).
- **Progressive discovery:** as the agent `cd`s into subfolders during a session,
  that folder's context file loads the moment it becomes relevant.

**Takeaway:** writing `AGENTS.md` at your `terminal.cwd` (e.g. `~/hermes-home`)
gives every new session automatic Home Base context. Keep it small (~1–1.5 KB)
and just point to INDEX/PLAYBOOK/GLOSSARY.

## 4. Escape hatch — truly blank session

```bash
hermes chat --no-restore-cwd   # start with zero cwd framing / Home Base context
```
Rarely needed, but useful when you want a chat with no project scaffolding.

## PITFALLS

**P1 — Never hand-edit config.yaml.** Use `hermes config set/get`. A stray
indent breaks the live gateway. (Also in memory as a hard invariant.)

**P2 — Check running containers before relocating a project folder.** Moving a
folder that holds live Docker containers silently breaks them. Before any `mv`:
```bash
docker ps --filter "name=<project>" --format "{{.Names}} {{.Status}}"
```
This session caught `n8n-docker` with 3 containers "Up 2 days" — relocation was
cancelled. Good thing we checked.

**P3 — Compose relative mounts make a MOVE safe ONLY when stopped.** n8n's
`docker-compose.yml` used only `./init-data.sh` and named volumes (`db_storage`,
`n8n_storage`) — no hardcoded absolute host paths. So after stopping containers,
a `mv` + `docker compose up` works unchanged. Verify there are no
`/abs/host/path` mounts before moving any compose stack.

**P4 — A "project" must be registered to switch to it.** A loose folder at home
root is NOT a project. `hermes project list` showed only `upwork`, `wifi-sense`,
`hermes-home`; `n8n-docker` was just a folder. To make a folder a switchable
project: `hermes project create` then add the folder.

## 5. Operating convention (G)

`~/hermes-home` is the neutral launchpad for ALL sessions (chat + simple work).
For focused project work, switch to the relevant registered project so its
context loads and files land correctly. Casual chat stays ephemeral — the agent
writes no files unless asked. (Also persisted in memory.)
