#!/bin/sh -e

# This script creates a PostgreSQL database and user for PyPnbPartKeepr.
# Usage: ./create_db.sh [-f|--force]
# -f, --force: Force recreation of the database and user.

if [ "$1" = "-f" ] || [ "$1" = "--force" ]; then
    FORCE=1
else
    FORCE=0
fi

DB_HOST=${DB_HOST:-"localhost"}
DB_PORT=${DB_PORT:-"5432"}
DB_USER=${DB_USER:-"partkeeprpsqluser"}
DB_PASS=${DB_PASS:-"PartKeeprPsqlPass"}
DB_DB=${DB_NAME:-"partkeeprpsqldb"}

echo "Creating PostgreSQL database and user for PyPnbPartKeepr."
echo "Using host: ${DB_HOST}, port: ${DB_PORT}, user: ${DB_USER}, database: ${DB_DB}"

export PGPASSWORD=postgres
CONN_ARGS="-U postgres -h ${DB_HOST} -p ${DB_PORT}"

if [ $FORCE -eq 1 ]; then
    echo "Force creation of the database and user."
    psql ${CONN_ARGS} -c "DROP DATABASE IF EXISTS ${DB_DB};"
fi

if ! psql ${CONN_ARGS} -tc "SELECT 1 FROM pg_database WHERE datname = '${DB_DB}'" | grep -q 1; then
    echo "Database ${DB_DB} does not exist, creating it."

    echo "Creating user ${DB_USER} with password."
    psql ${CONN_ARGS} -c "
    DROP USER IF EXISTS ${DB_USER};
    CREATE ROLE ${DB_USER} PASSWORD '${DB_PASS}' LOGIN;
    ALTER USER ${DB_USER} WITH PASSWORD '${DB_PASS}';
    "

    echo "Creating database ${DB_DB} with owner ${DB_USER}."
    psql ${CONN_ARGS} -c "
    CREATE DATABASE ${DB_DB} OWNER ${DB_USER};
    "
else
    echo "Database ${DB_DB} already exists, skipping creation."
fi
