----------------------------------------------------------------------
-- CAVIDA DEMO V2 — Security: Dynamic Data Masking
-- REQ 21: Column-level security via masking policies
----------------------------------------------------------------------

USE ROLE ACCOUNTADMIN;
USE DATABASE CAVIDA_DEMO;

-- ============================================================
-- DEMO 1: Show existing masking policy
-- ============================================================

DESCRIBE MASKING POLICY CAVIDA_DEMO.REGULATORY.MASK_PII;

-- Policy logic:
-- ACCOUNTADMIN, CAVIDA_DATA_STEWARD, CAVIDA_ACTUARIO → see real data
-- All other roles → see '***MASKED***'

-- ============================================================
-- DEMO 2: Test masking with different roles
-- ============================================================

-- As ACCOUNTADMIN (full access)
USE ROLE ACCOUNTADMIN;
SELECT instrument_name, counterparty, rating
FROM CAVIDA_DEMO.BRONZE.SLV2_INVESTMENT_PORTFOLIO LIMIT 5;

-- As ANALYST (masked)
USE ROLE CAVIDA_ANALYST;
USE WAREHOUSE CAVIDA_PROD_WH;
SELECT instrument_name, counterparty, rating
FROM CAVIDA_DEMO.BRONZE.SLV2_INVESTMENT_PORTFOLIO LIMIT 5;

-- Switch back
USE ROLE ACCOUNTADMIN;

-- ============================================================
-- DEMO 3: Apply masking to sensitive columns
-- ============================================================

-- Apply to counterparty column (sensitive business relationship data)
ALTER TABLE CAVIDA_DEMO.BRONZE.SLV2_INVESTMENT_PORTFOLIO
  MODIFY COLUMN counterparty SET MASKING POLICY CAVIDA_DEMO.REGULATORY.MASK_PII;

-- Verify
SELECT instrument_name, counterparty FROM CAVIDA_DEMO.BRONZE.SLV2_INVESTMENT_PORTFOLIO LIMIT 3;

-- KEY DIFFERENTIATOR vs SAS:
-- SAS requires WHERE clauses in EVERY program or SAS/Secure (extra license)
-- Snowflake: Declarative policies applied once, enforced EVERYWHERE automatically
