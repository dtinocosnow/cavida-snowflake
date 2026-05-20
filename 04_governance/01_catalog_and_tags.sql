----------------------------------------------------------------------
-- CAVIDA DEMO V2 — Governance: Catalog & Tags
-- REQ 13: Data catalog, business glossary, search
----------------------------------------------------------------------

USE ROLE ACCOUNTADMIN;
USE DATABASE CAVIDA_DEMO;

-- ============================================================
-- DEMO 1: Tag-based governance (classification)
-- ============================================================

-- Tags created in REGULATORY schema
SHOW TAGS IN SCHEMA CAVIDA_DEMO.REGULATORY;

-- Data Domain tags applied to tables
SELECT * FROM TABLE(INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS(
  'CAVIDA_DEMO.RAW.SLV2_INVESTMENT_PORTFOLIO', 'TABLE'));

-- ============================================================
-- DEMO 2: Semantic View as Business Glossary
-- ============================================================

-- The semantic view acts as a live business glossary
DESCRIBE SEMANTIC VIEW CAVIDA_DEMO.SEMANTIC.SLV2_ANALYTICS;

-- Show all dimensions with descriptions
SHOW SEMANTIC DIMENSIONS IN CAVIDA_DEMO.SEMANTIC.SLV2_ANALYTICS;

-- Show all metrics with business definitions
SHOW SEMANTIC METRICS IN CAVIDA_DEMO.SEMANTIC.SLV2_ANALYTICS;

-- ============================================================
-- DEMO 3: Object search and discovery
-- ============================================================

-- Find all SLV2 tables
SHOW TABLES LIKE 'SLV2%' IN DATABASE CAVIDA_DEMO;

-- Table comments for discoverability
SELECT table_schema, table_name, comment
FROM CAVIDA_DEMO.INFORMATION_SCHEMA.TABLES
WHERE table_name LIKE 'SLV2%'
ORDER BY table_schema, table_name;

-- KEY DIFFERENTIATOR vs SAS:
-- SAS requires SAS Information Catalog (separate license)
-- Snowflake: Tags + Semantic Views + Horizon Catalog = native, no extra cost
