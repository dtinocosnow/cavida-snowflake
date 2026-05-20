SELECT
    r.reference_date,
    r.risk_agility_file,
    COUNT(*) AS total_entries,
    SUM(CASE WHEN r.information LIKE '%vazi%' THEN 1 ELSE 0 END) AS empty_records
FROM {{ ref('stg_risk_agility_inputs') }} r
GROUP BY r.reference_date, r.risk_agility_file
