----------------------------------------------------------------------
-- CAVIDA DEMO — Resource Monitors & Cost Control
-- REQ 34: Cost visibility, reporting, cost-limiting mechanisms
----------------------------------------------------------------------

USE ROLE ACCOUNTADMIN;

-- ============================================================
-- 1. Resource Monitors (credit quotas per warehouse)
-- ============================================================

CREATE OR REPLACE RESOURCE MONITOR CAVIDA_DEV_MONITOR
  WITH CREDIT_QUOTA = 100
  FREQUENCY = MONTHLY
  START_TIMESTAMP = IMMEDIATELY
  TRIGGERS
    ON 75 PERCENT DO NOTIFY
    ON 90 PERCENT DO SUSPEND
    ON 100 PERCENT DO SUSPEND_IMMEDIATE;

CREATE OR REPLACE RESOURCE MONITOR CAVIDA_PROD_MONITOR
  WITH CREDIT_QUOTA = 500
  FREQUENCY = MONTHLY
  START_TIMESTAMP = IMMEDIATELY
  TRIGGERS
    ON 50 PERCENT DO NOTIFY
    ON 80 PERCENT DO NOTIFY
    ON 95 PERCENT DO SUSPEND
    ON 100 PERCENT DO SUSPEND_IMMEDIATE;

CREATE OR REPLACE RESOURCE MONITOR CAVIDA_ETL_MONITOR
  WITH CREDIT_QUOTA = 300
  FREQUENCY = MONTHLY
  START_TIMESTAMP = IMMEDIATELY
  TRIGGERS
    ON 75 PERCENT DO NOTIFY
    ON 95 PERCENT DO SUSPEND
    ON 100 PERCENT DO SUSPEND_IMMEDIATE;

-- Assign monitors to warehouses
ALTER WAREHOUSE CAVIDA_DEV_WH SET RESOURCE_MONITOR = CAVIDA_DEV_MONITOR;
ALTER WAREHOUSE CAVIDA_PROD_WH SET RESOURCE_MONITOR = CAVIDA_PROD_MONITOR;
ALTER WAREHOUSE CAVIDA_ETL_WH SET RESOURCE_MONITOR = CAVIDA_ETL_MONITOR;

-- ============================================================
-- 2. Auto-suspend configuration (cost optimization)
-- ============================================================

-- Already configured in warehouse creation:
-- DEV: 60s auto-suspend
-- TEST: 60s auto-suspend
-- PROD: 120s auto-suspend
-- ETL: 60s auto-suspend

SHOW WAREHOUSES LIKE 'CAVIDA%';

-- ============================================================
-- 3. Cost visibility queries
-- ============================================================

-- Credits consumed per warehouse (last 30 days)
SELECT WAREHOUSE_NAME,
       SUM(CREDITS_USED) AS TOTAL_CREDITS,
       SUM(CREDITS_USED) * 5.20 AS ESTIMATED_COST_EUR
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE WAREHOUSE_NAME LIKE 'CAVIDA%'
  AND START_TIME >= DATEADD(day, -30, CURRENT_DATE())
GROUP BY WAREHOUSE_NAME
ORDER BY TOTAL_CREDITS DESC;

SELECT 'Resource monitors configured' AS STATUS;
