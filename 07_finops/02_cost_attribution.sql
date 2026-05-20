----------------------------------------------------------------------
-- CAVIDA DEMO — Cost Attribution & Chargeback
-- REQ 35: Cost attribution, showback, chargeback
----------------------------------------------------------------------

USE ROLE ACCOUNTADMIN;
USE DATABASE CAVIDA_DEMO;

-- ============================================================
-- 1. Tags for cost attribution
-- ============================================================

CREATE TAG IF NOT EXISTS CAVIDA_DEMO.PROD.COST_CENTER
  COMMENT = 'Cost center for chargeback attribution';

CREATE TAG IF NOT EXISTS CAVIDA_DEMO.PROD.ENVIRONMENT
  ALLOWED_VALUES 'DEV', 'TEST', 'PROD', 'ETL'
  COMMENT = 'Environment tag for cost isolation';

-- Tag warehouses
ALTER WAREHOUSE CAVIDA_DEV_WH SET TAG CAVIDA_DEMO.PROD.ENVIRONMENT = 'DEV';
ALTER WAREHOUSE CAVIDA_DEV_WH SET TAG CAVIDA_DEMO.PROD.COST_CENTER = 'IT-DataPlatform';

ALTER WAREHOUSE CAVIDA_TEST_WH SET TAG CAVIDA_DEMO.PROD.ENVIRONMENT = 'TEST';
ALTER WAREHOUSE CAVIDA_TEST_WH SET TAG CAVIDA_DEMO.PROD.COST_CENTER = 'IT-QA';

ALTER WAREHOUSE CAVIDA_PROD_WH SET TAG CAVIDA_DEMO.PROD.ENVIRONMENT = 'PROD';
ALTER WAREHOUSE CAVIDA_PROD_WH SET TAG CAVIDA_DEMO.PROD.COST_CENTER = 'Business-Analytics';

ALTER WAREHOUSE CAVIDA_ETL_WH SET TAG CAVIDA_DEMO.PROD.ENVIRONMENT = 'ETL';
ALTER WAREHOUSE CAVIDA_ETL_WH SET TAG CAVIDA_DEMO.PROD.COST_CENTER = 'IT-DataEngineering';

-- ============================================================
-- 2. Cost attribution query (chargeback report)
-- ============================================================

SELECT
    w.WAREHOUSE_NAME,
    t.TAG_VALUE AS COST_CENTER,
    SUM(w.CREDITS_USED) AS TOTAL_CREDITS,
    ROUND(SUM(w.CREDITS_USED) * 5.20, 2) AS COST_EUR,
    MIN(w.START_TIME) AS PERIOD_START,
    MAX(w.END_TIME) AS PERIOD_END
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY w
LEFT JOIN SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES t
  ON t.OBJECT_NAME = w.WAREHOUSE_NAME
  AND t.TAG_NAME = 'COST_CENTER'
  AND t.DOMAIN = 'WAREHOUSE'
WHERE w.WAREHOUSE_NAME LIKE 'CAVIDA%'
  AND w.START_TIME >= DATEADD(day, -30, CURRENT_DATE())
GROUP BY w.WAREHOUSE_NAME, t.TAG_VALUE
ORDER BY COST_EUR DESC;

-- ============================================================
-- 3. Per-domain storage costs
-- ============================================================

SELECT
    TABLE_SCHEMA AS DOMAIN,
    COUNT(*) AS NUM_TABLES,
    ROUND(SUM(BYTES) / POWER(1024, 3), 4) AS STORAGE_GB,
    ROUND(SUM(BYTES) / POWER(1024, 3) * 23, 2) AS STORAGE_COST_EUR_MONTH
FROM CAVIDA_DEMO.INFORMATION_SCHEMA.TABLES
WHERE TABLE_CATALOG = 'CAVIDA_DEMO'
GROUP BY TABLE_SCHEMA
ORDER BY STORAGE_GB DESC;

SELECT 'Cost attribution configured' AS STATUS;
