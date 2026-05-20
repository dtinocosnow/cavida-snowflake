SELECT
    portfolio_id,
    reference_date,
    internal_fund_identifier,
    internal_fund_code,
    asset_solvency_ii_code,
    asset_class,
    instrument_name,
    counterparty,
    rating,
    currency,
    market_value,
    accrued_interest,
    sum_total,
    loaded_at
FROM {{ source('raw', 'SLV2_INVESTMENT_PORTFOLIO') }}
