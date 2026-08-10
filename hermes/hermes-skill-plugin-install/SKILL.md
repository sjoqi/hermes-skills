---
name: hermes-skill-plugin-install
description: "Install third-party Hermes skills and plugins from a GitHub repo into ~/.hermes. Covers the three install paths (single SKILL.md URL, hub `tap`+`install`, and `hermes plugins install owner/repo/subdir --enable` for plugin-packaged skills), how Hermes discovers them, how to verify the install actually loads, and a pre-enable safety review of plugin hooks. Load when the user says 'install this skill', pastes a github.com skill/plugin repo URL, or asks to add a Hermes extension."
metadata:
  hermes:
    tags: [hermes, skills, plugins, install, github, extension]
    category: hermes
---

# Install third-party Hermes skills & plugins

When a user points at a GitHub repo and says "install this skill" (or similar), the
repo is usually one of three shapes. Pick the path by shape — do NOT just copy the
repo into `~/.hermes/skills/`. (This was learned the hard way installing
witt3rd/oh-my-hermes, whose skills are nested under `plugins/omh/skills/`, not a
top-level `skills/` dir — the naive copy found nothing.)

## Step 0 — Inspect the repo shape first
Fetch the repo tree (GitHub API `git/trees/<branch>?recursive=1` or web_extract the
README) and look for:
- A top-level `skills/<name>/SKILL.md` (or flat `<name>/SKILL.md`) → **hub skill pack**.
- A `plugin.yaml` somewhere, often `plugins/<name>/plugin.yaml`, with skills nested
  under `plugins/<name>/skills/` → **Hermes plugin** (the OMH shape).
- A single `SKILL.md` file → **single skill**.

A plugin may ALSO ship its skills under `plugins/<name>/skills/`; in that case there
is no top-level `skills/` path, so the hub `tap` path finds nothing.

## Path A — Single skill from a URL
```bash
hermes skills install https://raw.githubusercontent.com/OWNER/REPO/main/path/to/SKILL.md
```
Works when you can point directly at a raw `SKILL.md`. `--name` overrides the skill
name if the frontmatter lacks `name:`.

## Path B — Hub skill pack (`skills/` layout)
```bash
hermes skills tap add OWNER/REPO
hermes skills install <skill-name> [--yes]
```
Only valid if the repo actually has the hub layout (`skills/<name>/SKILL.md`). Verify
the tree first; if there's no top-level `skills/`, use Path C.

## Path C — Plugin (with or without bundled skills) ← most "skill repos" that look like OMH
A Hermes plugin lives in a dir containing `plugin.yaml` + an `__init__.py` with a
`register(ctx)` entrypoint. The official installer clones the repo, extracts a
**subdirectory**, drops it in `~/.hermes/plugins/<name>/`, and `--enable` persists it
to `config.yaml` (`plugins.enabled`). It auto-detects `plugin.yaml` inside the subdir.
```bash
# subdir form: owner/repo/path/to/plugin
hermes plugins install OWNER/REPO/plugins/omh --enable
```
- Resolves `owner/repo/subdir` → clones repo, extracts `subdir`, lands at
  `~/.hermes/plugins/omh`.
- `--enable` writes `plugins: {enabled: [omh], disabled: []}` to
  `~/.hermes/config.yaml`. Without it the plugin is installed but inert (user plugins
  are opt-in).
- If the plugin's `register()` auto-installs bundled skills (copies
  `plugins/<name>/skills/*` → `~/.hermes/skills/<category>/`, skip-if-exists), those
  skills come along for free.

## Discovery facts (verified against Hermes source)
- **Skills**: anything under `~/.hermes/skills/` containing `SKILL.md` is
  auto-discovered via `rglob("SKILL.md")` — both flat (`skills/<name>/`) and
  category-nested (`skills/<cat>/<name>/`). They appear in the `<available_skills>`
  auto-index and load on relevance. No config entry needed.
- **Plugins**: opt-in. A user plugin only loads if its name is in `plugins.enabled`
  in `config.yaml`. Bundled/platform plugins auto-load; user-installed ones do not.
- A skill that calls a plugin-provided tool (e.g. `omh_state`) will **fail** unless the
  owning plugin is enabled. If skills reference an `omh`-style toolset, enable the
  plugin.

## Verify the install (do this — don't assume)
```bash
hermes skills list | grep -i <name>      # skill present + enabled
hermes plugins list | grep -i <name>     # plugin enabled, tools/hooks counted
```
Definitive load check (loads the real PluginManager) and the full expected-output
shape: see `references/verify-install.md`.

## Pre-enable safety review (untrusted plugin code)
User plugins execute code + hooks every session. Before `--enable`, read the hook
sources:
- `pre_llm_call` — must return `None` when no OMH marker is present (zero overhead in
  normal use).
- `pre_tool_call` — should be non-blocking (warn, not prevent).
- `on_session_end` — should only touch the plugin's own state dir.
Red flags: network egress, writes outside the plugin's `.omh/` state dir, prompt-cache
mutation on every turn, or `requires_env` secrets you can't satisfy. Hermes's venv
already ships pyyaml 6.x, so most plugin deps are satisfied.

## Pitfalls
- **Copying the whole repo into `~/.hermes/skills/` does nothing** — only dirs
  containing `SKILL.md` are scanned. The plugin's `plugin.yaml`/`__init__.py` are not
  skills.
- **`hermes skills install <repo-url>` fails for plugin-shaped repos** — it expects a
  `skills/` layout or a raw `SKILL.md`. Use Path C.
- **Plugin installed but skills still error on `omh_state`** → the plugin isn't
  enabled. Run `hermes plugins enable <name>` (or reinstall with `--enable`).
- **Pre-copying skills then installing the plugin**: the plugin's `_install_skills`
  skips dirs that already exist, so your manual copy wins (fine, but keep them
  identical).
- **Installed ≠ authored.** Skills installed via these paths have a *recent mtime* but
  are third-party work. Never republish them as the user's own — see
  `publishing-skills-to-public-repo` before pushing `~/.hermes/skills` anywhere public.

## Related skills
- `publishing-skills-to-public-repo` — the opposite direction: pushing skills OUT to a
  public GitHub repo, with PII screening and leak incident response.
