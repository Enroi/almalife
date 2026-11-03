#!/usr/bin/env bash

echo "${POSTGRES_USER}"

# ------------------------------------------------------------------------
# Создание examples базы данных
# ------------------------------------------------------------------------
set -e

psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" --dbname "${POSTGRES_DB}" <<-EOSQL

  CREATE OR REPLACE FUNCTION add_uuid_pk()
  RETURNS event_trigger AS \$\$
  DECLARE
      obj record;
  BEGIN
      FOR obj IN SELECT * FROM pg_event_trigger_ddl_commands()
      LOOP
          -- Только таблицы в схеме public
          IF obj.object_type = 'table' AND obj.schema_name = 'public' THEN

              -- 1. Проверяем, нет ли уже колонки с именем "uuid"
              IF NOT EXISTS (
                  SELECT 1
                  FROM pg_attribute a
                  WHERE a.attrelid = obj.object_identity::regclass
                    AND a.attname = 'uuid'
                    AND a.attnum > 0
                    AND NOT a.attisdropped
              ) THEN

                  -- 2. Проверяем, нет ли уже первичного ключа
                  IF NOT EXISTS (
                      SELECT 1
                      FROM pg_constraint c
                      WHERE c.conrelid = obj.object_identity::regclass
                        AND c.contype = 'p'
                  ) THEN
                      EXECUTE format(
                          'ALTER TABLE %s ADD COLUMN uuid uuid DEFAULT gen_random_uuid() PRIMARY KEY',
                          obj.object_identity
                      );
                  END IF;

              END IF;
          END IF;
      END LOOP;
  END;
  \$\$ LANGUAGE plpgsql;

  CREATE EVENT TRIGGER add_uuid_pk_on_create
      ON ddl_command_end
      WHEN TAG IN ('CREATE TABLE')
      EXECUTE FUNCTION add_uuid_pk();

  CREATE DATABASE sources;
  CREATE DATABASE results;
EOSQL
