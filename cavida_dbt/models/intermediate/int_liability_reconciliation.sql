SELECT
    l.reference_date,
    l.risk_agility_input_file,
    SUM(l.math_provisions) AS total_math_provisions,
    SUM(l.insured_capital) AS total_insured_capital,
    SUM(l.record_count) AS total_records
FROM {{ ref('stg_liabilities') }} l
GROUP BY l.reference_date, l.risk_agility_input_file
