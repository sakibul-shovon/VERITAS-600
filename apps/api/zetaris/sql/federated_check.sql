-- ==============================================================================
-- Zetaris Join-Safe 3-Silo Federated Check Query
-- Silo 1: postgres_trade (OLTP)
-- Silo 2: parquet_customs (Lakehouse HS-6 benchmark stats)
-- Silo 3: opensanctions_entities (Watchlist JSON/REST)
-- CTE Pre-Aggregation guarantees EXACTLY 1 row per lc_id
-- ==============================================================================

WITH accepted_shipment_amd AS (
    SELECT
        lc_id,
        new_value AS effective_shipment_date
    FROM postgres_trade.lc_amendments
    WHERE amended_field = 'latest_shipment_date'
      AND beneficiary_acceptance_status = 'ACCEPTED'
      AND lc_id = :lc_id
    ORDER BY sequence_no DESC
    LIMIT 1
),
unaccepted_amendments_agg AS (
    SELECT
        lc_id,
        COUNT(*) AS quarantined_count,
        STRING_AGG(amended_field || '=' || new_value, '; ') AS quarantined_amendments_summary
    FROM postgres_trade.lc_amendments
    WHERE beneficiary_acceptance_status = 'UNACCEPTED_PENDING'
      AND lc_id = :lc_id
    GROUP BY lc_id
),
sanctions_hits_agg AS (
    SELECT
        COUNT(*) AS hit_count,
        MAX(risk_score) AS max_risk_score,
        STRING_AGG(
            matched_name || ' (Parent: ' || COALESCE(parent_company_name, 'N/A') || ' | ' || sanction_program || ')',
            '; '
        ) AS sanctions_summary
    FROM opensanctions_entities.watchlist
    WHERE lookup_name IN (:beneficiary_name, :vessel_name, :notify_party_name)
)
SELECT
    lc.lc_id,
    lc.applicant_name,
    lc.beneficiary_name,
    lc.amount AS lc_amount,
    lc.unit_price AS lc_unit_price,
    lc.latest_shipment_date AS original_shipment_date,
    COALESCE(amd_acc.effective_shipment_date, CAST(lc.latest_shipment_date AS VARCHAR)) AS effective_shipment_date,
    COALESCE(amd_unacc.quarantined_count, 0) AS quarantined_amendment_count,
    amd_unacc.quarantined_amendments_summary,
    -- Silo 2: Parquet Customs HS-Code Unit Price Benchmark
    cust.hs_code_6,
    cust.description AS hs_description,
    cust.mean_unit_price_usd,
    cust.stddev_unit_price_usd,
    ROUND((:invoice_unit_price - cust.mean_unit_price_usd) / NULLIF(cust.stddev_unit_price_usd, 0), 2) AS tbml_price_zscore,
    -- Silo 3: Aggregated OpenSanctions Watchlist Hits
    COALESCE(sanc.hit_count, 0) AS sanction_hit_count,
    COALESCE(sanc.max_risk_score, 0.0) AS sanction_max_risk_score,
    sanc.sanctions_summary
FROM postgres_trade.lc_master lc
LEFT JOIN accepted_shipment_amd amd_acc
    ON lc.lc_id = amd_acc.lc_id
LEFT JOIN unaccepted_amendments_agg amd_unacc
    ON lc.lc_id = amd_unacc.lc_id
LEFT JOIN parquet_customs.hs_benchmarks cust
    ON lc.hs_code_6 = cust.hs_code_6
CROSS JOIN sanctions_hits_agg sanc
WHERE lc.lc_id = :lc_id;
