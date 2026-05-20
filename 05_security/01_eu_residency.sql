----------------------------------------------------------------------
-- CAVIDA DEMO V2 — Security: EU Data Residency
-- REQ 17: EU data residency & sovereignty
----------------------------------------------------------------------

USE ROLE ACCOUNTADMIN;

-- ============================================================
-- DEMO 1: Account Region Verification
-- ============================================================

-- Verify region (must be EU)
SELECT CURRENT_REGION();
-- Expected: AWS_EU_CENTRAL_1 (Frankfurt)

SELECT CURRENT_ACCOUNT_NAME();
-- Account: SFSEEUROPE-DTINOCO_AWS

-- ============================================================
-- DEMO 2: Encryption (Business Critical Edition)
-- ============================================================

-- Business Critical = AES-256 encryption at rest + in transit
-- Support for customer-managed keys (Tri-Secret Secure)

SELECT SYSTEM$GET_SNOWFLAKE_PLATFORM_INFO();

-- ============================================================
-- DEMO 3: No Cross-Region Replication
-- ============================================================

-- Data stays in EU - no replication to other regions configured
SHOW REPLICATION ACCOUNTS;

-- ============================================================
-- DEMO 4: GDPR & Compliance Certifications
-- ============================================================

-- Snowflake Business Critical certifications:
-- SOC 1 Type II, SOC 2 Type II
-- ISO 27001, ISO 27017, ISO 27018
-- PCI DSS
-- GDPR compliant
-- HIPAA (Healthcare)

-- KEY DIFFERENTIATOR vs SAS:
-- Same EU hosting possible but Snowflake adds native encryption,
-- Tri-Secret Secure, and automated compliance without extra licensing
