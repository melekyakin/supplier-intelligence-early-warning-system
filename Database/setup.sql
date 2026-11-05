-- Supplier Intelligence & Early Warning System
-- Complete database setup script
-- Execute with PostgreSQL psql from the project root.

\set ON_ERROR_STOP on

BEGIN;

-- 1. Schemas
\ir schema/00_create_schemas.sql

-- 2. Tables and sequence
\ir schema/01_create_raw_table.sql
\ir schema/02_create_staging_table.sql
\ir schema/03_create_notification_log.sql

-- 3. Analytical views
\ir views/01_supplier_performance.sql
\ir views/02_supplier_risk.sql
\ir views/03_supplier_alerts.sql

-- 4. Indexes
\ir indexes/01_create_indexes.sql

COMMIT;
