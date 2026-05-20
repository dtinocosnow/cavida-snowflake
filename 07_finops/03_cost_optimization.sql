----------------------------------------------------------------------
-- CAVIDA DEMO — Cost Optimization
-- REQ 36: Detection of idle resources, inefficient workloads
----------------------------------------------------------------------

USE ROLE ACCOUNTADMIN;

-- ============================================================
-- 1. Detect idle/underutilized warehouses
-- ============================================================

SELECT
    WAREHOUSE_NAME,
    AVG(AVG_RUNNING) AS AVG_QUERIES_RUNNING,
    AVG(AVG_QUEUED_LOAD) AS AVG_QUERIES_QUEUED,
    MAX(AVG_RUNNING) AS PEAK_QUERIES_RUNNING,
    COUNT(*) AS MEASUREMENT_POINTS
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_LOAD_HISTORY
WHERE WAREHOUSE_NAME LIKE 'CAVIDA%'
  AND START_TIME >= DATEADD(day, -7, CURRENT_DATE())
GROUP BY WAREHOUSE_NAME
ORDER BY AVG_QUERIES_RUNNING DESC;

-- ============================================================
-- 2. Detect expensive/slow queries
-- ============================================================

SELECT
    QUERY_ID,
    USER_NAME,
    WAREHOUSE_NAME,
    EXECUTION_STATUS,
    TOTAL_ELAPSED_TIME / 1000 AS ELAPSED_SEC,
    BYTES_SCANNED / POWER(1024, 3) AS GB_SCANNED,
    PARTITIONS_SCANNED,
    PARTITIONS_TOTAL,
    ROUND(PARTITIONS_SCANNED / NULLIF(PARTITIONS_TOTAL, 0) * 100, 1) AS PCT_SCANNED,
    BYTES_SPILLED_TO_LOCAL_STORAGE / POWER(1024, 2) AS MB_SPILLED_LOCAL,
    BYTES_SPILLED_TO_REMOTE_STORAGE / POWER(1024, 2) AS MB_SPILLED_REMOTE
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE WAREHOUSE_NAME LIKE 'CAVIDA%'
  AND START_TIME >= DATEADD(day, -7, CURRENT_DATE())
  AND TOTAL_ELAPSED_TIME > 10000
ORDER BY TOTAL_ELAPSED_TIME DESC
LIMIT 20;

-- ============================================================
-- 3. Storage optimization
-- ============================================================

SELECT
    TABLE_CATALOG || '.' || TABLE_SCHEMA || '.' || TABLE_NAME AS TABLE_FQN,
    ACTIVE_BYTES / POWER(1024, 2) AS ACTIVE_MB,
    TIME_TRAVEL_BYTES / POWER(1024, 2) AS TIME_TRAVEL_MB,
    FAILSAFE_BYTES / POWER(1024, 2) AS FAILSAFE_MB,
    RETAINED_FOR_CLONE_BYTES / POWER(1024, 2) AS CLONE_MB,
    (ACTIVE_BYTES + TIME_TRAVEL_BYTES + FAILSAFE_BYTES) / POWER(1024, 2) AS TOTAL_MB
FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS
WHERE TABLE_CATALOG = 'CAVIDA_DEMO'
  AND ACTIVE_BYTES > 0
ORDER BY TOTAL_MB DESC
LIMIT 20;

-- ============================================================
-- 4. Warehouse sizing recommendations
-- ============================================================

-- Queries that spill = warehouse too small
SELECT
    WAREHOUSE_NAME,
    WAREHOUSE_SIZE,
    COUNT(*) AS TOTAL_QUERIES,
    SUM(CASE WHEN BYTES_SPILLED_TO_LOCAL_STORAGE > 0 THEN 1 ELSE 0 END) AS SPILLING_QUERIES,
    ROUND(SPILLING_QUERIES / NULLIF(TOTAL_QUERIES, 0) * 100, 1) AS PCT_SPILLING
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE WAREHOUSE_NAME LIKE 'CAVIDA%'
  AND START_TIME >= DATEADD(day, -7, CURRENT_DATE())
GROUP BY WAREHOUSE_NAME, WAREHOUSE_SIZE
ORDER BY PCT_SPILLING DESC;
