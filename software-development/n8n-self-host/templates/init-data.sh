#!/bin/bash
set -e;

# Creates the non-root Postgres user n8n actually connects as.
# Mounted into the postgres container at /docker-entrypoint-initdb.d/init-data.sh
# so it runs ONCE during first cluster initialization. Without this, the
# POSTGRES_NON_ROOT_USER is never created and n8n gets
# "password authentication failed for user \"<nonroot>\"".

if [ -n "${POSTGRES_NON_ROOT_USER:-}" ] && [ -n "${POSTGRES_NON_ROOT_PASSWORD:-}" ]; then
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
		CREATE USER ${POSTGRES_NON_ROOT_USER} WITH PASSWORD '${POSTGRES_NON_ROOT_PASSWORD}';
		GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_NON_ROOT_USER};
		GRANT CREATE ON SCHEMA public TO ${POSTGRES_NON_ROOT_USER};
	EOSQL
else
	echo "SETUP INFO: No Environment variables given!"
fi
