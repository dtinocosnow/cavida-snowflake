----------------------------------------------------------------------
-- CAVIDA DEMO V2 — Security: Row Access Policies
-- REQ 21: Row-level security
----------------------------------------------------------------------

USE ROLE ACCOUNTADMIN;
USE DATABASE CAVIDA_DEMO;

-- ============================================================
-- DEMO 1: Show existing Row Access Policy
-- ============================================================

DESCRIBE ROW ACCESS POLICY CAVIDA_DEMO.REGULATORY.RAP_REFERENCE_PERIOD;

-- Policy logic:
-- ACCOUNTADMIN/DATA_STEWARD/ACTUARIO → ALL rows
-- ANALYST → only data from last 6 months

-- Applied to: RAW.SLV2_INVESTMENT_PORTFOLIO (reference_date column)

-- ============================================================
-- DEMO 2: Test RLS with different roles
-- ============================================================

-- As ACCOUNTADMIN (all periods)
USE ROLE ACCOUNTADMIN;
SELECT reference_date, COUNT(*) AS records
FROM CAVIDA_DEMO.RAW.SLV2_INVESTMENT_PORTFOLIO
GROUP BY 1 ORDER BY 1;

-- As ANALYST (only recent data)
USE ROLE CAVIDA_ANALYST;
USE WAREHOUSE CAVIDA_PROD_WH;
SELECT reference_date, COUNT(*) AS records
FROM CAVIDA_DEMO.RAW.SLV2_INVESTMENT_PORTFOLIO
GROUP BY 1 ORDER BY 1;
-- Only shows last 6 months!

-- Switch back
USE ROLE ACCOUNTADMIN;

-- ============================================================
-- DEMO 3: RLS is invisible and automatic
-- ============================================================

-- The analyst sees fewer rows but doesn't know WHY
-- No error, no visible filter — just restricted results
-- This is CRITICAL for regulatory compliance (data minimisation)

-- KEY DIFFERENTIATOR vs SAS:
-- SAS: Manual WHERE clauses or SAS/Secure product (costly)
-- Databricks: Unity Catalog row filters (newer, less mature)
-- Snowflake: Production-ready, declarative, zero-code enforcement
