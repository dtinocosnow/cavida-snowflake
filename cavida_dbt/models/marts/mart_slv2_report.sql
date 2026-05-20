SELECT
    ar.reference_date,
    ar.asset_class,
    ar.instrument_count,
    ar.total_market_value,
    ar.total_accrued_interest,
    ar.total_value,
    ROUND(ar.total_value / NULLIF(SUM(ar.total_value) OVER (PARTITION BY ar.reference_date), 0) * 100, 2) AS pct_portfolio
FROM {{ ref('int_asset_reconciliation') }} ar
