SELECT
    input_id,
    reference_date,
    risk_agility_file,
    column_name,
    information,
    record_count,
    empty_count,
    status
FROM {{ source('bronze', 'SLV2_RISK_AGILITY_INPUTS_ASSETS') }}
