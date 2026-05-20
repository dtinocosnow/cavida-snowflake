SELECT
    process_id,
    reference_date,
    process_name,
    description,
    status,
    started_at,
    completed_at,
    pre_requisite,
    pre_req_status
FROM {{ source('raw', 'SLV2_TAGETIK_PROCESSES') }}
