----------------------------------------------------------------------
-- CAVIDA DEMO V2 — Time Travel & Dataset Versioning
-- REQ 6: Historical state access, rollback, time-travel
----------------------------------------------------------------------

USE ROLE ACCOUNTADMIN;
USE DATABASE CAVIDA_DEMO;
USE WAREHOUSE CAVIDA_PROD_WH;

-- ============================================================
-- DEMO 1: Query data as it existed in the past
-- ============================================================

-- Current count
SELECT COUNT(*) AS current_records FROM RAW.SLV2_INVESTMENT_PORTFOLIO;

-- Make a change (simulate accidental deletion)
DELETE FROM RAW.SLV2_INVESTMENT_PORTFOLIO WHERE asset_class = 'Cash';

SELECT COUNT(*) AS after_delete FROM RAW.SLV2_INVESTMENT_PORTFOLIO;

-- TIME TRAVEL: See data as it was 5 minutes ago
SELECT COUNT(*) AS before_delete
FROM RAW.SLV2_INVESTMENT_PORTFOLIO AT(OFFSET => -300);

-- RESTORE: Undo the deletion instantly
INSERT INTO RAW.SLV2_INVESTMENT_PORTFOLIO
SELECT * FROM RAW.SLV2_INVESTMENT_PORTFOLIO AT(OFFSET => -300)
WHERE asset_class = 'Cash';

SELECT COUNT(*) AS restored FROM RAW.SLV2_INVESTMENT_PORTFOLIO;

-- ============================================================
-- DEMO 2: Clone from specific point in time (backup)
-- ============================================================

CREATE OR REPLACE TABLE RAW.SLV2_PORTFOLIO_BACKUP
  CLONE RAW.SLV2_INVESTMENT_PORTFOLIO AT(OFFSET => -60);

-- Zero storage cost until data diverges

-- ============================================================
-- DEMO 3: UNDROP — recover dropped objects
-- ============================================================

-- Accidentally drop a table
DROP TABLE PROD.SLV2_REPORT_STATUS;

-- Recover it immediately
UNDROP TABLE PROD.SLV2_REPORT_STATUS;

-- Works for tables, schemas, and entire databases
-- Retention: 90 days on Business Critical

-- ============================================================
-- DEMO 4: 90-Day retention (Business Critical)
-- ============================================================

SHOW TABLES LIKE 'SLV2%' IN SCHEMA CAVIDA_DEMO.RAW;
-- retention_time = 90 days on Enterprise/BC edition

-- KEY DIFFERENTIATOR vs SAS:
-- SAS has NO built-in time travel
-- BigQuery: 7 days max
-- Databricks: Delta Lake has versioning but requires manual management
-- Snowflake: Native, automatic, up to 90 days, zero config
