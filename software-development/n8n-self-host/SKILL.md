---
name: n8n-self-host
description: Self-host n8n via Docker Compose (n8n + Postgres), for learning AND client-ready deployments. Covers the official n8n-hosting withPostgres template, the stock-Postgres single-user auth trap, the MIXED-CASE USERNAME bug, the N8N_ENCRYPTION_KEY rule, healthcheck-gated startup, and client hardening (secure cookie, reverse proxy, version pinning). Load whenever the user wants to install/run/deploy n8n locally or for a client, or hits a Postgres "password authentication failed" / "role does not exist" error in a compose stack.
---

# Self-host n8n with Docker Compose

Use this for any "set up n8n" task — local learning OR a client production box. The recipe is the same; only the secrets, domain, and TLS differ.

## Mental model (teach this to the user)
- **Image** = frozen prebuilt blueprint (n8n ships `n8nio/n8n`, no local build needed).
- **Container** = running instance; **ephemeral** — dies with `docker compose down` unless state is in a **volume**.
- **Volume** (named `db_storage` / `n8n_storage`, or bind `./postgres-data` / `./n8n-data`) = the only thing that survives restarts. Back these up.
- **Compose file** = recipe for all services + how they connect.

You do NOT build an image. `docker run` / `docker compose up` auto-pulls the published `n8nio/n8n` (or `docker.n8n.io/n8nio/n8n` in the official file) image.

## Which compose recipe to use (RECOMMENDATION)
**Prefer the official n8n-hosting `withPostgres` template** — it is maintained upstream (n8n publishes it), includes the **n8n-runner** service (isolates untrusted Code nodes in a sandbox — important for client multi-tenant), and implements the split-user pattern CORRECTLY via a `init-data.sh` Postgres init hook. Get it from:
`https://github.com/n8n-io/n8n-hosting/tree/main/docker-compose/withPostgres`
(docker-compose.yml + init-data.sh + .env). Copy those 3 files, fill real secrets, add `N8N_ENCRYPTION_KEY` + `GENERIC_TIMEZONE` (the official `.env` omits them), run `docker compose up -d`.
The `templates/` here mirror that official file with those two gaps filled.

**Simpler alternative (pure learning, single `docker run`):** SQLite, no Postgres:
`docker run -it --rm -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n`. Fine to learn the UI; not for clients.

**Do NOT hand-write a compose from memory.** A hand-written split-user compose (root + non-root without the init hook) breaks exactly like the trap below — we hit this in-session and had to adopt the official file. Use the official one or the template here.

## BEFORE setup (checklist — do in order)
1. **Docker daemon must be running.** Verify with `docker info`. If `Cannot connect to the Docker daemon`, launch Docker Desktop first. (`docker compose` plugin is separate from the daemon — having the binary doesn't mean the daemon is up.)
2. **Choose DB:** SQLite (single `docker run`) = learning only. Postgres = anything real (concurrency, backups, scale). Default to Postgres for clients.
3. **Set `N8N_ENCRYPTION_KEY` BEFORE first run.** Generate: `openssl rand -base64 48`. It encrypts all credentials (API keys, tokens) at rest. If n8n starts without one, it bakes a random key into the volume — **lose the volume and you can never decrypt those credentials again.** Put it in `.env`, back it up in a password manager, never commit it.
4. **`.env` for all secrets; add `.env` to `.gitignore`.** Never hardcode creds in the compose file.
5. **Set `GENERIC_TIMEZONE`** to the user's zone. Scheduled workflows fire on this.
6. **Generate DB usernames LOWERCASE-ONLY** (mixed-case breaks Postgres auth — see below). Passwords may be mixed-case.

## The Postgres auth traps (CRITICAL — most common failures)
**Trap 1 — user never created.** The stock `postgres` image only auto-creates the SINGLE user named in `POSTGRES_USER`. It does NOT create a second "non-root" user even if you pass `POSTGRES_NON_ROOT_USER` — UNLESS you ship an init hook (`init-data.sh` mounted at `/docker-entrypoint-initdb.d/`) that runs `CREATE USER ...`. The official template does this; a hand-written one usually doesn't →
```
password authentication failed for user "n8n"
```
**Two correct patterns:**
1. **Official split-user** (recommended): keep `POSTGRES_USER=root` + `POSTGRES_NON_ROOT_USER=n8n`, and include `init-data.sh` so the non-root user is actually created. n8n uses `DB_POSTGRESDB_USER=${POSTGRES_NON_ROOT_USER}`.
2. **Single-user** (simpler): one app user the image creates; point both at it (`POSTGRES_USER=n8n`, no non-root vars).

**Trap 2 — MIXED-CASE USERNAME (bit us twice).** Postgres **folds unquoted identifiers to lowercase on CREATE** but auth lookups are case-sensitive per the exact string sent. If a generated username contains uppercase (e.g. `u189F33d0YODB7wo`), Postgres stores it as `u189f33d0yodb7wo`, but n8n sends the env var verbatim → `role "u189F33d0YODB7wo" does not exist` / auth failed. **Fix: generate usernames LOWERCASE-ONLY.** Passwords may stay mixed-case (they are quoted). The official `.env` example uses `changeUser` (lowercase) precisely to avoid this. Always `grep -i '[A-Z]'` your username vars after generating.

**Volume-reset trap:** if you change DB creds after Postgres has initialized its data dir, the OLD data dir still has the previous owner → auth keeps failing even with corrected env. Fix: `docker compose down -v` AND `rm -rf ./postgres-data ./n8n-data`, then `docker compose up -d` so Postgres re-initializes with the new user. See `references/postgres-auth-pitfall.md`.

## DURING setup (the working recipe)
- `depends_on: condition: service_healthy` + a Postgres `healthcheck` using `pg_isready` → n8n waits for DB readiness (avoids the start-before-DB race).
- `restart: unless-stopped` (or `always`) on all services.
- Named volumes (`db_storage`, `n8n_storage`) or bind mounts (`./postgres-data`, `./n8n-data`).
- Pin the n8n image for clients (`n8nio/n8n:2.x.x` or `${N8N_VERSION}`), not `:latest`, so updates can't surprise them. For local learning `:latest`/`stable` is fine.
- Include the **n8n-runner** service for Code-node isolation (present in the official template).

Known-good files: `templates/docker-compose.yml` and `templates/.env.example` (+ `init-data.sh`). Copy, fill secrets, run `docker compose up -d`.

### Verify it's actually up (don't trust "Started")
```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:5678   # expect 200
docker logs <n8n-container> --tail 20                                  # watch for DB migrations running, not auth errors
```

## AFTER setup (operations — the client-care part)
1. **First boot = create owner account** (email + password). That's admin. For a client: you create it, then create their limited-scope user.
2. **Back up three things:** the n8n volume, the postgres volume, and `N8N_ENCRYPTION_KEY` stored separately. Without the key, backups are undecryptable.
3. **Updates:** `docker compose pull && docker compose up -d`. Pin versions for clients; test on staging first.
4. **Client domain (not localhost):** set `N8N_SECURE_COOKIE=true`, `N8N_PROTOCOL=https`, `N8N_HOST=theirdomain.com`, and put it behind a reverse proxy (Caddy/Nginx) with TLS. Never expose port 5678 directly to the internet over http.
5. **Scale:** for many concurrent executions, add `N8N_EXECUTIONS_MODE=queue` + Redis.

## Uninstall / clean slate
Global npm installs land under **nvm**, not `~/.local` (this user's `npm root -g` points at a nonexistent `~/.local/lib` while the real install is at `~/.nvm/versions/node/<ver>/lib/node_modules/n8n`). To remove: `rm -rf` that dir + the `n8n` bin symlink, plus `~/.n8n` and `~/.cache/n8n`. For Docker: `docker compose down -v` + delete the project folder's data dirs.

## Teaching delivery (for user G — when they ask to LEARN)
G explicitly wants **step-by-step instructions they execute themselves**, not the agent doing it all and handing over notes. When the task is "teach me / guide me through setup":
- Give the numbered steps as the primary deliverable. Execute alongside them, but frame each as "you do X, then verify Y", and surface the WHY (the trap/rule) at each step.
- Still do the work to VERIFY it actually runs (curl/logs) — learning doesn't mean shipping an unproven recipe.
- Save a durable `README.md`/`references/` notes file they can re-read later (they asked for this).
- Prefer the official source file over a hand-written equivalent; if you deviate, say why.

## Client deployment checklist (localhost → production)
- [ ] `N8N_SECURE_COOKIE=true`, `N8N_PROTOCOL=https`, `N8N_HOST=their.domain` (no scheme).
- [ ] Reverse proxy (Caddy/Nginx) terminating TLS in front; never expose :5678 over http.
- [ ] Pin `N8N_VERSION` to a tested release (not `stable`) after staging validation.
- [ ] Back up `db_storage` + `n8n_storage` volumes AND `N8N_ENCRYPTION_KEY` (off-server; backups undecryptable without it).
- [ ] n8n-runner :5679 stays on the internal Docker network only.
- [ ] For high concurrency: `N8N_EXECUTIONS_MODE=queue` + Redis.
- [ ] Hand over a `README.md`: start/stop, backup location, encryption-key location, pinned version.

## Gotchas / pitfalls
- `docker compose up -d` detaches and returns immediately — it is NOT a long-lived foreground process; don't background-guard it as if it hangs.
- The firecrawl web tool was disabled this session; n8n docs are a JS SPA so `curl` of the HTML returns the shell only. Pull raw files from `raw.githubusercontent.com/n8n-io/n8n-hosting/...` instead. The compose recipe here is verified-working.
- Image pull can be slow (n8n layer ~315MB); poll `docker ps` / `docker logs` rather than assuming failure.
- `.env` files with secrets may be hidden by the host's secret-guard; inspect via terminal with values masked, never print raw secrets to chat.
