# The stock-Postgres single-user auth trap (reproduced + fixed)

## Symptom
n8n container logs循环 (retries then fails):
```
Initial database connection attempt 1 failed: password authentication failed for user "n8n". Retrying in 1000ms
Initial database connection attempt 2 failed: password authentication failed for user "n8n". Retrying in 2000ms
...
```
Meanwhile `curl localhost:5678` returns HTTP 000 (n8n never finishes booting).

## Root cause
Compose used:
```
POSTGRES_USER=root          # image creates THIS user
POSTGRES_NON_ROOT_USER=n8n  # image does NOT create this
```
n8n was pointed at `DB_POSTGRESDB_USER=n8n`, but that user was never created by
the standard `postgres` image (it only auto-provisions the single `POSTGRES_USER`).
Hence `password authentication failed for user "n8n"`.

## Fix (applied)
Collapse to ONE app user the image actually creates:
```env
POSTGRES_USER=n8n
POSTGRES_PASSWORD=<random>
POSTGRES_DB=n8n
```
n8n: `DB_POSTGRESDB_USER=${POSTGRES_USER}`, `DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}`.
Removed `POSTGRES_NON_ROOT_*` vars entirely.

## Volume-reset trap (same failure persists after the env fix)
The OLD `./postgres-data` was initialized with `root` as owner. Even after fixing
env, Postgres' on-disk cluster still has the previous owner → auth keeps failing.
Resolution:
```bash
docker compose down -v
rm -rf ./postgres-data ./n8n-data
docker compose up -d     # Postgres re-initializes cluster with the NEW user
```
After this, n8n connects (HTTP 200) and DB migrations run clean.

## Rule of thumb
Changing DB credentials in a compose stack is NOT enough if the data volume already
exists. Either wipe the volume or use `docker compose run postgres psql` to ALTER the
role. For greenfield client setups, set the correct single user BEFORE first `up`.
