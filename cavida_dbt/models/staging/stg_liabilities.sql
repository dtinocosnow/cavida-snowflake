SELECT
    input_id,
    reference_date,
    risk_agility_input_file,
    math_provisions,
    insured_capital,
    record_count
FROM {{ source('bronze', 'SLV2_RISK_AGILITY_INPUTS_LIABILITIES') }}
