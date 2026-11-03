#!/usr/bin/env bash

echo "${POSTGRES_USER}"

# ------------------------------------------------------------------------
# Создание examples базы данных
# ------------------------------------------------------------------------
set -e

psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" --dbname "${POSTGRES_DB}" <<-EOSQL
  CREATE DATABASE sources;
  CREATE DATABASE results;
EOSQL
