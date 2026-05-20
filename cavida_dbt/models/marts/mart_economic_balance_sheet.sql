SELECT
    ar.reference_date,
    ar.asset_class AS asset_type,
    ar.asset_class AS reference_code,
    ar.asset_class AS subrubrica,
    ar.total_value AS saldo_periodo,
    LAG(ar.total_value) OVER (PARTITION BY ar.asset_class ORDER BY ar.reference_date) AS saldo_periodo_anterior,
    ar.total_value - COALESCE(LAG(ar.total_value) OVER (PARTITION BY ar.asset_class ORDER BY ar.reference_date), 0) AS variacao_absoluta,
    CASE
        WHEN LAG(ar.total_value) OVER (PARTITION BY ar.asset_class ORDER BY ar.reference_date) > 0
        THEN (ar.total_value - LAG(ar.total_value) OVER (PARTITION BY ar.asset_class ORDER BY ar.reference_date))
             / LAG(ar.total_value) OVER (PARTITION BY ar.asset_class ORDER BY ar.reference_date)
        ELSE NULL
    END AS variacao_percentual
FROM {{ ref('int_asset_reconciliation') }} ar
