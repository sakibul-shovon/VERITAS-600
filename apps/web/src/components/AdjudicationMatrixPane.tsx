"use client";

import React, { useState } from "react";
import {
  Activity,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Play,
  RotateCcw,
  Sparkles,
  GitBranch,
  Database,
  ArrowRight,
  ShieldCheck,
  Scale,
} from "lucide-react";
import { DeterministicCheck, LegalFinding, PipelineStageUpdate } from "@/lib/types";

interface AdjudicationMatrixPaneProps {
  stages: Record<number, PipelineStageUpdate>;
  isExamining: boolean;
  onStartExamination: () => void;
  selectedLcId: string;
}

export default function AdjudicationMatrixPane({
  stages,
  isExamining,
  onStartExamination,
  selectedLcId,
}: AdjudicationMatrixPaneProps) {
  const [activeSection, setActiveSection] = useState<"checks" | "amendments" | "federation">("checks");

  const stage1 = stages[1];
  const stage2 = stages[2];
  const stage3 = stages[3];
  const stage4 = stages[4];
  const stage5 = stages[5];

  const checks: DeterministicCheck[] = stage3?.checks || [];
  const findings: LegalFinding[] = stage4?.findings || [];

  return (
    <div className="flex flex-col h-full bg-card rounded-lg border border-card-border overflow-hidden">
      {/* Pane Header */}
      <div className="flex items-center justify-between px-3 py-2 bg-slate-900/60 border-b border-card-border">
        <div className="flex items-center gap-2">
          <Activity className="h-4 w-4 text-emerald-400" />
          <span className="font-semibold text-xs tracking-wide text-slate-200 uppercase">
            Adjudication Reasoning Matrix
          </span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={onStartExamination}
            disabled={isExamining}
            className="flex items-center gap-1.5 px-3 py-1 rounded bg-emerald-600 hover:bg-emerald-500 text-white font-mono text-xs font-semibold shadow-md shadow-emerald-600/20 transition disabled:opacity-50"
          >
            {isExamining ? (
              <>
                <RotateCcw className="h-3.5 w-3.5 animate-spin" />
                <span>Auditing Stream...</span>
              </>
            ) : (
              <>
                <Play className="h-3.5 w-3.5 fill-current" />
                <span>Examine Presentation</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Sub-Navigation Tabs */}
      <div className="flex border-b border-card-border bg-slate-950/40 text-xs font-mono">
        <button
          onClick={() => setActiveSection("checks")}
          className={`flex-1 py-1.5 border-b-2 text-center transition ${
            activeSection === "checks"
              ? "border-emerald-500 text-emerald-400 bg-slate-900/80 font-semibold"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          Rules Matrix ({checks.length + findings.length})
        </button>
        <button
          onClick={() => setActiveSection("amendments")}
          className={`flex-1 py-1.5 border-b-2 text-center transition ${
            activeSection === "amendments"
              ? "border-emerald-500 text-emerald-400 bg-slate-900/80 font-semibold"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          Art. 10 Amendment Memory
        </button>
        <button
          onClick={() => setActiveSection("federation")}
          className={`flex-1 py-1.5 border-b-2 text-center transition ${
            activeSection === "federation"
              ? "border-emerald-500 text-emerald-400 bg-slate-900/80 font-semibold"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          Zetaris 3-Silo Risk
        </button>
      </div>

      {/* Content Area */}
      <div className="flex-1 p-3 overflow-y-auto space-y-3 font-mono text-xs">
        {activeSection === "checks" && (
          <div className="space-y-2.5">
            {/* Stage Summary Status Banner */}
            <div className="flex items-center justify-between p-2 rounded bg-slate-900/90 border border-card-border text-[11px]">
              <div className="flex items-center gap-1.5">
                <span className="text-slate-400">Hard Invariant Status:</span>
                <span className="text-emerald-400 font-bold">LOCKED & ENFORCED</span>
              </div>
              <div className="text-slate-400 text-[10px]">
                Deterministic Python Math + Nemotron Legal Reasoning
              </div>
            </div>

            {/* Deterministic Symbolic Checks */}
            <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5 mt-2">
              <Scale className="h-3.5 w-3.5 text-blue-400" />
              <span>Deterministic Symbolic Validations (Python)</span>
            </div>

            {checks.length === 0 ? (
              <div className="p-4 text-center text-slate-500 bg-slate-950/40 rounded border border-card-border">
                Click &quot;Examine Presentation&quot; above to execute UCP 600 audit pipeline.
              </div>
            ) : (
              checks.map((chk, idx) => (
                <div
                  key={idx}
                  className={`p-2.5 rounded border transition ${
                    chk.passed
                      ? "bg-slate-900/80 border-slate-800 text-slate-300"
                      : "bg-rose-950/20 border-rose-500/40 text-rose-200"
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center gap-2">
                      {chk.passed ? (
                        <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" />
                      ) : (
                        <XCircle className="h-4 w-4 text-rose-400 shrink-0" />
                      )}
                      <div>
                        <span className="font-semibold text-slate-200">{chk.name}</span>
                        <span className="ml-2 text-[10px] px-1.5 py-0.2 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                          {chk.ucp_citation}
                        </span>
                      </div>
                    </div>
                    <span
                      className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                        chk.passed ? "text-emerald-400 bg-emerald-500/10" : "text-rose-400 bg-rose-500/20"
                      }`}
                    >
                      {chk.passed ? "PASSED" : "DISCREPANT"}
                    </span>
                  </div>
                  <p className="mt-1 text-[11px] text-slate-400 pl-6 leading-relaxed">{chk.details}</p>
                </div>
              ))
            )}

            {/* Neural Legal Adjudication Findings */}
            <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5 mt-4">
              <Sparkles className="h-3.5 w-3.5 text-amber-400" />
              <span>Neural Legal Semantic Adjudication (Nemotron)</span>
            </div>

            {findings.map((find, idx) => (
              <div
                key={idx}
                className={`p-2.5 rounded border transition ${
                  find.is_discrepant
                    ? "bg-rose-950/20 border-rose-500/40 text-rose-200"
                    : "bg-slate-900/80 border-slate-800 text-slate-300"
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex items-center gap-2">
                    {find.is_discrepant ? (
                      <XCircle className="h-4 w-4 text-rose-400 shrink-0" />
                    ) : (
                      <ShieldCheck className="h-4 w-4 text-emerald-400 shrink-0" />
                    )}
                    <div>
                      <span className="font-semibold text-slate-200">{find.divergence_item}</span>
                      <span className="ml-2 text-[10px] px-1.5 py-0.2 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20">
                        {find.ucp_isbp_citation}
                      </span>
                    </div>
                  </div>
                  <span
                    className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                      find.is_discrepant
                        ? "text-rose-400 bg-rose-500/20"
                        : "text-emerald-300 bg-emerald-500/10 border border-emerald-500/20"
                    }`}
                  >
                    {find.verdict}
                  </span>
                </div>
                <p className="mt-1 text-[11px] text-slate-300 pl-6 leading-relaxed">{find.legal_reasoning}</p>
              </div>
            ))}
          </div>
        )}

        {/* Section 2: Art. 10 Amendment Memory Timeline */}
        {activeSection === "amendments" && (
          <div className="space-y-3">
            <div className="p-2.5 rounded bg-slate-900 border border-card-border space-y-1">
              <div className="flex items-center justify-between">
                <span className="font-bold text-indigo-400 text-[11px]">ACTIVE TERM SNAPSHOT</span>
                <span className="text-[10px] font-mono text-slate-500">
                  SHA-256: {stage1?.active_terms_sha256?.slice(0, 16)}...
                </span>
              </div>
              <p className="text-[11px] text-slate-400">
                UCP 600 Art. 10(c) & 10(e) guarantees terms of the original credit remain in force
                until acceptance, and prevents invalid partial acceptance.
              </p>
            </div>

            <div className="p-3 rounded bg-slate-900/60 border border-card-border space-y-2">
              <div className="text-slate-300 font-semibold text-[11px]">Active Shipment & Destination State:</div>
              <div className="grid grid-cols-2 gap-2 text-[11px]">
                <div className="p-2 rounded bg-slate-950">
                  <span className="text-slate-500">Latest Shipment: </span>
                  <span className="text-emerald-400 font-bold">{stage1?.active_terms?.latest_shipment_date || "N/A"}</span>
                </div>
                <div className="p-2 rounded bg-slate-950">
                  <span className="text-slate-500">Port of Discharge: </span>
                  <span className="text-slate-200">{stage1?.active_terms?.port_of_discharge || "N/A"}</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Section 3: Zetaris 3-Silo Risk Drawer */}
        {activeSection === "federation" && (
          <div className="space-y-3">
            <div className="p-3 rounded bg-slate-900 border border-card-border space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-cyan-400 text-[11px]">SILO 2: CUSTOMS HS-6 PRICE ANOMALY</span>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded font-bold ${
                    (stage2?.tbml_price_zscore || 0) > 4.0
                      ? "bg-rose-500/20 text-rose-300 border border-rose-500/40"
                      : "bg-emerald-500/20 text-emerald-300"
                  }`}
                >
                  Z-SCORE: +{stage2?.tbml_price_zscore || 0.0}
                </span>
              </div>
              <p className="text-[11px] text-slate-400">
                Evaluated against historical Customs Parquet unit-price distribution (Mean ± StdDev).
                Scores above +4.0 indicate extreme Trade-Based Money Laundering (TBML) over-invoicing.
              </p>
            </div>

            <div className="p-3 rounded bg-slate-900 border border-card-border space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-purple-400 text-[11px]">SILO 3: OPENSANCTIONS WATCHLIST</span>
                <span
                  className={`text-[10px] px-2 py-0.5 rounded font-bold ${
                    (stage2?.sanction_hit_count || 0) > 0
                      ? "bg-rose-500/20 text-rose-300 border border-rose-500/40"
                      : "bg-emerald-500/20 text-emerald-300"
                  }`}
                >
                  HITS: {stage2?.sanction_hit_count || 0}
                </span>
              </div>
              <p className="text-[11px] text-slate-300">
                {stage2?.sanctions_summary || "No active OFAC/EU watchlist hits detected for parties or vessels."}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
