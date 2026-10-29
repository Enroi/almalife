#!/usr/bin/env bash

echo "${PG_DB_USER}"

# ------------------------------------------------------------------------
# Создание examples базы данных
# ------------------------------------------------------------------------
set -e

psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" --dbname "${PG_DB_NAME}" <<-EOSQL
  CREATE DATABASE superset;
EOSQL
