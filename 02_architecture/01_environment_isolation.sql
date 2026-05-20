----------------------------------------------------------------------
-- CAVIDA DEMO V2 — Architecture: Environment Isolation
-- REQ 3: Storage/compute separation + Dev/Test/Prod promotion
----------------------------------------------------------------------

USE ROLE ACCOUNTADMIN;
USE DATABASE CAVIDA_DEMO;

-- ============================================================
-- DEMO 1: Storage/Compute Separation
-- Each environment has its OWN warehouse (compute)
-- All share the SAME storage (database)
-- ============================================================

SHOW WAREHOUSES LIKE 'CAVIDA%';

-- Different sizes for different workloads:
-- DEV  = XSMALL (cheap experimentation)
-- TEST = XSMALL (QA validation)
-- PROD = SMALL  (business queries)
-- ETL  = MEDIUM (pipeline batch processing)

-- Scale compute instantly without touching data:
ALTER WAREHOUSE CAVIDA_PROD_WH SET WAREHOUSE_SIZE = 'MEDIUM';
ALTER WAREHOUSE CAVIDA_PROD_WH SET WAREHOUSE_SIZE = 'SMALL';

-- ============================================================
-- DEMO 2: Zero-Copy Clone — instant environment promotion
-- ============================================================

-- Clone PROD to TEST (instant, zero storage cost)
CREATE OR REPLACE SCHEMA CAVIDA_DEMO.TEST CLONE CAVIDA_DEMO.PROD
  COMMENT = 'QA environment — zero-copy clone from PROD';

-- This is INSTANT regardless of data size
-- No storage duplication until data diverges

-- Verify clone
SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, ROW_COUNT, BYTES
FROM CAVIDA_DEMO.INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA IN ('PROD', 'TEST')
  AND TABLE_NAME LIKE 'SLV2%'
ORDER BY TABLE_SCHEMA, TABLE_NAME;

-- ============================================================
-- DEMO 3: Independent compute per environment
-- ============================================================

-- Run same query on DEV warehouse (XSMALL)
USE WAREHOUSE CAVIDA_DEV_WH;
SELECT COUNT(*), SUM(sum_total) AS total_portfolio FROM CAVIDA_DEMO.RAW.SLV2_INVESTMENT_PORTFOLIO;

-- Run same query on PROD warehouse (SMALL)
USE WAREHOUSE CAVIDA_PROD_WH;
SELECT COUNT(*), SUM(sum_total) AS total_portfolio FROM CAVIDA_DEMO.RAW.SLV2_INVESTMENT_PORTFOLIO;

-- KEY POINT: Same data, different compute — no data movement
-- Unlike SAS where compute and storage are tightly coupled
