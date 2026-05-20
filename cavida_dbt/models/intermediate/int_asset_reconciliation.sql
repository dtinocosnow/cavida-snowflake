SELECT
    p.reference_date,
    p.asset_class,
    COUNT(*) AS instrument_count,
    SUM(p.market_value) AS total_market_value,
    SUM(p.accrued_interest) AS total_accrued_interest,
    SUM(p.sum_total) AS total_value
FROM {{ ref('stg_investment_portfolio') }} p
GROUP BY p.reference_date, p.asset_class
