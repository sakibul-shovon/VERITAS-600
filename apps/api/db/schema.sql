-- ==============================================================================
-- VERITAS-600 Database Schema (PostgreSQL 16)
-- Operational Trade Database: LCs, MT707 Amendments, and Examination Audit Logs
-- ==============================================================================

CREATE TABLE IF NOT EXISTS lc_master (
    lc_id VARCHAR(32) PRIMARY KEY,
    swift_mt700_raw TEXT NOT NULL,
    issuing_bank VARCHAR(128) NOT NULL,
    applicant_name VARCHAR(128) NOT NULL,
    applicant_address_strict VARCHAR(256) NOT NULL,
    beneficiary_name VARCHAR(128) NOT NULL,
    currency VARCHAR(8) NOT NULL DEFAULT 'USD',
    amount NUMERIC(15, 2) NOT NULL,
    tolerance_pct NUMERIC(5, 2) NOT NULL DEFAULT 0.00,
    incoterm VARCHAR(16) NOT NULL,
    hs_code_6 VARCHAR(10) NOT NULL,
    goods_description_strict TEXT NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    port_of_loading VARCHAR(128) NOT NULL,
    port_of_discharge VARCHAR(128) NOT NULL,
    latest_shipment_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    presentation_period_days INTEGER NOT NULL DEFAULT 21,
    insurance_min_pct NUMERIC(6, 2) NOT NULL DEFAULT 110.00, -- UCP 600 Art. 28(f)(ii)
    daily_demurrage_usd NUMERIC(10, 2) NOT NULL DEFAULT 1850.00
);

CREATE TABLE IF NOT EXISTS lc_amendments (
    amendment_id VARCHAR(32) PRIMARY KEY,
    lc_id VARCHAR(32) REFERENCES lc_master(lc_id),
    sequence_no INTEGER NOT NULL,
    amended_field VARCHAR(64) NOT NULL,
    old_value TEXT NOT NULL,
    new_value TEXT NOT NULL,
    beneficiary_acceptance_status VARCHAR(24) NOT NULL CHECK (
        beneficiary_acceptance_status IN ('ACCEPTED', 'REJECTED', 'UNACCEPTED_PENDING')
    ),
    effective_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS examination_audit_log (
    run_id VARCHAR(64) PRIMARY KEY,
    lc_id VARCHAR(32) NOT NULL,
    executed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    active_terms_sha256 VARCHAR(64) NOT NULL,
    zetaris_execution_mode VARCHAR(32) NOT NULL, -- 'LIVE_ZETARIS' or 'LOCAL_DUCKDB_FALLBACK'
    zetaris_query_ms INTEGER NOT NULL,
    deterministic_result JSON NOT NULL,
    neural_adjudication_result JSON NOT NULL,
    recommended_action VARCHAR(48) NOT NULL,     -- 'APPROVE_HONOUR', 'ISSUE_MT734_REFUSAL', 'COMPLIANCE_HOLD_AML'
    human_approved_by VARCHAR(128) NULL,
    human_approved_at TIMESTAMPTZ NULL,
    generated_artifact_text TEXT NULL
);

CREATE INDEX IF NOT EXISTS idx_lc_amendments_lc_id ON lc_amendments(lc_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_lc_id ON examination_audit_log(lc_id);
