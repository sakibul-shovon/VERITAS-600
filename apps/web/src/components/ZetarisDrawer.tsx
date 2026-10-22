"use client";

import React from "react";
import { X, Database, Terminal, ShieldCheck, Layers } from "lucide-react";

interface ZetarisDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  telemetryMode: string;
  queryMs: number;
}

export default function ZetarisDrawer({
  isOpen,
  onClose,
  telemetryMode,
  queryMs,
}: ZetarisDrawerProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-x-0 bottom-0 z-50 bg-[#0B0F19] border-t-2 border-blue-500/40 shadow-2xl shadow-blue-500/10 p-4 max-h-[75vh] flex flex-col font-mono text-xs">
      <div className="flex items-center justify-between pb-3 border-b border-card-border">
        <div className="flex items-center gap-2">
          <Database className="h-4 w-4 text-cyan-400" />
          <span className="font-bold text-slate-100 text-sm tracking-wide">
            Zetaris In-Situ 3-Silo Federated SQL Inspector
          </span>
          <span className="text-[10px] px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30">
            {telemetryMode} ({queryMs}ms)
          </span>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-white transition"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto py-3 space-y-3">
        {/* Architecture explanation */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-[11px]">
          <div className="p-2.5 rounded bg-slate-900 border border-card-border space-y-1">
            <span className="text-cyan-400 font-bold">SILO 1 (PostgreSQL OLTP)</span>
            <p className="text-slate-400">
              Stores <code className="text-slate-200">lc_master</code> and <code className="text-slate-200">lc_amendments</code>.
              Amendments pre-aggregated in CTE to prevent Cartesian row multiplication.
            </p>
          </div>
          <div className="p-2.5 rounded bg-slate-900 border border-card-border space-y-1">
            <span className="text-emerald-400 font-bold">SILO 2 (Parquet Customs Lakehouse)</span>
            <p className="text-slate-400">
              Stores 6-digit HS-code price distributions (Mean ± StdDev). Computes live TBML price anomaly Z-score.
            </p>
          </div>
          <div className="p-2.5 rounded bg-slate-900 border border-card-border space-y-1">
            <span className="text-purple-400 font-bold">SILO 3 (OpenSanctions Watchlist)</span>
            <p className="text-slate-400">
              Evaluates vessel IMO numbers and beneficiary parent corporations in a single CTE join.
            </p>
          </div>
        </div>

        {/* Query display */}
        <div className="space-y-1">
          <div className="flex items-center gap-1.5 text-slate-400 text-[11px] font-bold">
            <Terminal className="h-3.5 w-3.5 text-blue-400" />
            <span>Join-Safe SQL Query (apps/api/zetaris/sql/federated_check.sql):</span>
          </div>
          <pre className="p-3 rounded bg-slate-950 border border-card-border text-slate-300 overflow-x-auto text-[11px] leading-relaxed">
{`WITH accepted_shipment_amd AS (
    SELECT lc_id, new_value AS effective_shipment_date
    FROM postgres_trade.lc_amendments
    WHERE amended_field = 'latest_shipment_date' AND beneficiary_acceptance_status = 'ACCEPTED'
    ORDER BY sequence_no DESC LIMIT 1
),
unaccepted_amendments_agg AS (
    SELECT lc_id, COUNT(*) AS quarantined_count,
           STRING_AGG(amended_field || '=' || new_value, '; ') AS quarantined_amendments_summary
    FROM postgres_trade.lc_amendments WHERE beneficiary_acceptance_status = 'UNACCEPTED_PENDING'
    GROUP BY lc_id
),
sanctions_hits_agg AS (
    SELECT COUNT(*) AS hit_count, MAX(risk_score) AS max_risk_score,
           STRING_AGG(matched_name || ' (Parent: ' || COALESCE(parent_company_name, 'N/A') || ')', '; ') AS sanctions_summary
    FROM opensanctions_entities.watchlist
    WHERE lookup_name IN (:beneficiary_name, :vessel_name, :notify_party_name)
)
SELECT lc.lc_id, lc.applicant_name, lc.beneficiary_name, lc.amount,
       COALESCE(amd_acc.effective_shipment_date, CAST(lc.latest_shipment_date AS VARCHAR)) AS effective_shipment_date,
       cust.mean_unit_price_usd,
       ROUND((:invoice_unit_price - cust.mean_unit_price_usd) / NULLIF(cust.stddev_unit_price_usd, 0), 2) AS tbml_price_zscore,
       sanc.hit_count AS sanction_hit_count, sanc.sanctions_summary
FROM postgres_trade.lc_master lc
LEFT JOIN accepted_shipment_amd amd_acc ON lc.lc_id = amd_acc.lc_id
LEFT JOIN unaccepted_amendments_agg amd_unacc ON lc.lc_id = amd_unacc.lc_id
LEFT JOIN parquet_customs.hs_benchmarks cust ON lc.hs_code_6 = cust.hs_code_6
CROSS JOIN sanctions_hits_agg sanc
WHERE lc.lc_id = :lc_id;`}
          </pre>
        </div>
      </div>
    </div>
  );
}
