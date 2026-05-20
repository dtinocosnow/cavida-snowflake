SELECT
    lr.reference_date,
    lr.risk_agility_input_file AS description,
    'Tier 1' AS tier,
    lr.total_math_provisions AS value,
    'Risk Agility' AS origin
FROM {{ ref('int_liability_reconciliation') }} lr
