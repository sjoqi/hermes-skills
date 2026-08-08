# n8n via Docker Compose — reference

## Official source (fetch, don't reconstruct)
Repo: `n8n-io/n8n-hosting`, path `docker-compose/withPostgres/`.
- Raw compose: `https://raw.githubusercontent.com/n8n-io/n8n-hosting/main/docker-compose/withPostgres/docker-compose.yml`
- Raw init script: `.../withPostgres/init-data.sh`
- Raw `.env`: `.../withPostgres/.env`
- Raw README: `.../withPostgres/README.md`

## What the official compose contains (and why)
- `postgres:16` with healthcheck `pg_isready -U $POSTGRES_USER -d $POSTGRES_DB`.
- `init-data.sh` mounted to `/docker-entrypoint-initdb.d/` — creates `POSTGRES_NON_ROOT_USER` and grants DB + schema perms. **This is why the split-user pattern works; a hand-written compose without it fails auth.**
- `n8n` service: `DB_*` env from the non-root user; `N8N_RUNNERS_MODE=external` + `N8N_RUNNERS_AUTH_TOKEN` + broker on 5679 (internal only, NOT exposed to host).
- `n8n-runner` service: executes Code nodes in a sandbox (security isolation). Port 5679 is internal Docker networking — never expose to host.
- Named volumes `db_storage`, `n8n_storage` (not bind mounts).

## Our additions to the official (it omits these)
- `N8N_ENCRYPTION_KEY` — encrypts stored credentials. Generate: `openssl rand -base64 48`. Back up separately.
- `GENERIC_TIMEZONE` — e.g. `Asia/Jakarta`. Drives scheduled workflow timing.
- `N8N_SECURE_COOKIE=false` for localhost; set `true` + `N8N_HOST`/`N8N_PROTOCOL=https` for a client domain (pair with a reverse proxy + TLS).
- Pin `N8N_VERSION` (e.g. `2.8.4`) for clients instead of `stable`.

## Gotchas that broke the first run (with fixes)
1. Hand-written compose used a non-root user the stock image never created → `password authentication failed for user "n8n"`. Fix: use the official `init-data.sh`.
2. Mixed-case generated username (`u189F33d0YODB7wo`) → Postgres stored it lowercase → n8n sent verbatim → auth fail. Fix: **lowercase-only usernames** (passwords may stay mixed-case).
3. Changed creds but old volume still had old owner → had to `docker compose down -v` + wipe.

## Verify after `up`
```
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5678   # expect 200
docker logs n8n-docker-n8n-1 --tail 10   # look for "Editor is now accessible" / auth errors
docker ps --filter name=n8n-docker
```

## Client-domain checklist (defer until localhost works)
- `N8N_SECURE_COOKIE=true`, `N8N_PROTOCOL=https`, `N8N_HOST=their.domain`.
- Reverse proxy (Caddy/Nginx) with TLS; never expose 5678 over http.
- Pin `N8N_VERSION` to a tested release.
- Back up volumes + encryption key offsite.
