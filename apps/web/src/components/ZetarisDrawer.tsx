"use client";

import React, { useEffect, useRef } from "react";
import { ChevronDown, Database, Layers, ShieldCheck, Terminal, X } from "lucide-react";

interface ZetarisDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  telemetryMode: string;
  queryMs: number;
}

const FEDERATED_SQL = `WITH accepted_shipment_amd AS (
    SELECT lc_id, new_value AS effective_shipment_date
    FROM postgres_trade.lc_amendments
    WHERE amended_field = 'latest_shipment_date'
      AND beneficiary_acceptance_status = 'ACCEPTED'
    ORDER BY sequence_no DESC LIMIT 1
),
unaccepted_amendments_agg AS (
    SELECT lc_id, COUNT(*) AS quarantined_count,
           STRING_AGG(amended_field || '=' || new_value, '; ')
             AS quarantined_amendments_summary
    FROM postgres_trade.lc_amendments
    WHERE beneficiary_acceptance_status = 'UNACCEPTED_PENDING'
    GROUP BY lc_id
),
sanctions_hits_agg AS (
    SELECT COUNT(*) AS hit_count, MAX(risk_score) AS max_risk_score,
           STRING_AGG(matched_name || ' (Parent: ' ||
             COALESCE(parent_company_name, 'N/A') || ')', '; ')
             AS sanctions_summary
    FROM opensanctions_entities.watchlist
    WHERE lookup_name IN (:beneficiary_name, :vessel_name, :notify_party_name)
)
SELECT lc.lc_id, lc.applicant_name, lc.beneficiary_name, lc.amount,
       COALESCE(amd_acc.effective_shipment_date,
         CAST(lc.latest_shipment_date AS VARCHAR)) AS effective_shipment_date,
       cust.mean_unit_price_usd,
       ROUND((:invoice_unit_price - cust.mean_unit_price_usd) /
         NULLIF(cust.stddev_unit_price_usd, 0), 2) AS tbml_price_zscore,
       sanc.hit_count AS sanction_hit_count, sanc.sanctions_summary
FROM postgres_trade.lc_master lc
LEFT JOIN accepted_shipment_amd amd_acc ON lc.lc_id = amd_acc.lc_id
LEFT JOIN unaccepted_amendments_agg amd_unacc ON lc.lc_id = amd_unacc.lc_id
LEFT JOIN parquet_customs.hs_benchmarks cust ON lc.hs_code_6 = cust.hs_code_6
CROSS JOIN sanctions_hits_agg sanc
WHERE lc.lc_id = :lc_id;`;

export default function ZetarisDrawer({
  isOpen,
  onClose,
  telemetryMode,
  queryMs,
}: ZetarisDrawerProps) {
  const closeButtonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!isOpen) return;

    const previouslyFocused = document.activeElement as HTMLElement | null;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    closeButtonRef.current?.focus();

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = previousOverflow;
      previouslyFocused?.focus();
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const isFallback = telemetryMode.includes("FALLBACK");

  return (
    <div className="proof-drawer-backdrop" onMouseDown={onClose}>
      <aside
        aria-labelledby="zetaris-proof-title"
        aria-modal="true"
        className="proof-drawer"
        onMouseDown={(event) => event.stopPropagation()}
        role="dialog"
      >
        <header className="proof-drawer-header">
          <div className="proof-drawer-kicker">
            <Database aria-hidden="true" />
            Federation proof / Zetaris
          </div>
          <button
            ref={closeButtonRef}
            aria-label="Close federation proof"
            className="proof-drawer-close"
            onClick={onClose}
            type="button"
          >
            <X aria-hidden="true" />
          </button>
        </header>

        <div className="proof-drawer-body">
          <section className="proof-drawer-intro">
            <p>IN-SITU / THREE-SILO EVIDENCE</p>
            <h2 id="zetaris-proof-title">One query.<br />No ETL detour.</h2>
            <p className="proof-drawer-lead">
              The examination joins the active credit, customs benchmarks, and
              sanctions evidence while preserving one result row per LC.
            </p>
          </section>

          <section aria-label="Observed query telemetry" className="proof-telemetry">
            <div>
              <span>Observed runtime</span>
              <strong>{queryMs}<small> ms</small></strong>
            </div>
            <div>
              <span>Execution source</span>
              <strong className={isFallback ? "fallback" : "live"}>{telemetryMode}</strong>
            </div>
          </section>

          <div className="proof-silos">
            <article>
              <span>01 / PostgreSQL OLTP</span>
              <h3>Credit & amendments</h3>
              <p>Accepted and pending amendments are pre-aggregated in CTEs to prevent row multiplication.</p>
            </article>
            <article>
              <span>02 / Parquet customs</span>
              <h3>Price distribution</h3>
              <p>Six-digit HS-code benchmarks provide the observed TBML price anomaly Z-score.</p>
            </article>
            <article>
              <span>03 / OpenSanctions</span>
              <h3>Entity watchlist</h3>
              <p>Vessel, beneficiary, and parent-company matches are reduced to a single evidence record.</p>
            </article>
          </div>

          <div className="proof-invariant">
            <ShieldCheck aria-hidden="true" />
            <div>
              <span>JOIN-SAFE INVARIANT</span>
              <strong>Exactly one federated row per credit.</strong>
            </div>
          </div>

          <details className="proof-sql">
            <summary>
              <span><Terminal aria-hidden="true" /> Inspect join-safe SQL</span>
              <ChevronDown aria-hidden="true" />
            </summary>
            <div className="proof-sql-meta">
              <Layers aria-hidden="true" />
              apps/api/zetaris/sql/federated_check.sql
            </div>
            <pre>{FEDERATED_SQL}</pre>
          </details>
        </div>
      </aside>
    </div>
  );
}
