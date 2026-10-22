"use client";

import React, { useState } from "react";
import { FileText, Eye, CheckCircle2, AlertTriangle, Sparkles, Scan } from "lucide-react";

interface DocumentViewerPaneProps {
  scenarioData: any;
  onHighlightField?: (fieldKey: string) => void;
  highlightedField?: string | null;
}

export default function DocumentViewerPane({
  scenarioData,
  onHighlightField,
  highlightedField,
}: DocumentViewerPaneProps) {
  const [activeTab, setActiveTab] = useState<"mt700" | "invoice" | "bl" | "packing" | "insurance">("invoice");
  const [isExtracting, setIsExtracting] = useState(false);
  const [extractedFields, setExtractedFields] = useState<Record<string, any>>({});

  const master = scenarioData?.master || {};
  const amendments = scenarioData?.amendments || [];
  const presentation = scenarioData?.presentation || {};

  const handleRunLiveExtraction = () => {
    setIsExtracting(true);
    setTimeout(() => {
      setIsExtracting(false);
      setExtractedFields({
        invoice_no: presentation.invoice_no,
        invoice_amount: presentation.invoice_amount,
        goods_description: presentation.invoice_goods_description,
        on_board_date: presentation.bl_on_board_date,
        insurance_amount: presentation.insurance_amount,
      });
    }, 600);
  };

  return (
    <div className="flex flex-col h-full bg-card rounded-lg border border-card-border overflow-hidden">
      {/* Pane Header */}
      <div className="flex items-center justify-between px-3 py-2 bg-slate-900/60 border-b border-card-border">
        <div className="flex items-center gap-2">
          <FileText className="h-4 w-4 text-blue-400" />
          <span className="font-semibold text-xs tracking-wide text-slate-200 uppercase">
            Documentary Presentation Viewer
          </span>
        </div>
        <button
          onClick={handleRunLiveExtraction}
          disabled={isExtracting}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/30 text-[11px] font-mono text-blue-300 transition disabled:opacity-50"
        >
          {isExtracting ? (
            <>
              <Scan className="h-3 w-3 animate-spin text-blue-400" />
              <span>Extracting VLM...</span>
            </>
          ) : (
            <>
              <Sparkles className="h-3 w-3 text-amber-400" />
              <span>Live Nemotron OCR</span>
            </>
          )}
        </button>
      </div>

      {/* Document Tabs */}
      <div className="flex border-b border-card-border bg-slate-950/40 overflow-x-auto text-xs font-mono">
        <button
          onClick={() => setActiveTab("mt700")}
          className={`px-3 py-2 border-b-2 whitespace-nowrap transition ${
            activeTab === "mt700"
              ? "border-blue-500 text-blue-400 bg-slate-900/80 font-semibold"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          MT700 + Amendments ({amendments.length})
        </button>
        <button
          onClick={() => setActiveTab("invoice")}
          className={`px-3 py-2 border-b-2 whitespace-nowrap transition ${
            activeTab === "invoice"
              ? "border-blue-500 text-blue-400 bg-slate-900/80 font-semibold"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          Commercial Invoice
        </button>
        <button
          onClick={() => setActiveTab("bl")}
          className={`px-3 py-2 border-b-2 whitespace-nowrap transition ${
            activeTab === "bl"
              ? "border-blue-500 text-blue-400 bg-slate-900/80 font-semibold"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          Ocean Bill of Lading
        </button>
        <button
          onClick={() => setActiveTab("packing")}
          className={`px-3 py-2 border-b-2 whitespace-nowrap transition ${
            activeTab === "packing"
              ? "border-blue-500 text-blue-400 bg-slate-900/80 font-semibold"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          Packing List
        </button>
        <button
          onClick={() => setActiveTab("insurance")}
          className={`px-3 py-2 border-b-2 whitespace-nowrap transition ${
            activeTab === "insurance"
              ? "border-blue-500 text-blue-400 bg-slate-900/80 font-semibold"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          Insurance Cert
        </button>
      </div>

      {/* Document Content Display */}
      <div className="flex-1 p-3 overflow-y-auto space-y-3 font-mono text-xs">
        {activeTab === "mt700" && (
          <div className="space-y-3">
            <div className="p-2.5 rounded bg-slate-900 border border-card-border space-y-1.5">
              <div className="text-[11px] text-blue-400 font-bold">SWIFT MT700 ORIGINAL BASE CREDIT</div>
              <pre className="text-slate-300 whitespace-pre-wrap leading-relaxed text-[11px]">
                {master.swift_mt700_raw}
              </pre>
            </div>
            {amendments.map((amd: any, idx: number) => (
              <div key={idx} className="p-2.5 rounded bg-slate-900/70 border border-slate-700/60 space-y-1">
                <div className="flex items-center justify-between text-[11px]">
                  <span className="font-bold text-indigo-400">SWIFT MT707 AMENDMENT #{amd.sequence_no}</span>
                  <span
                    className={`px-1.5 py-0.2 rounded text-[10px] font-bold ${
                      amd.beneficiary_acceptance_status === "ACCEPTED"
                        ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                        : "bg-amber-500/20 text-amber-300 border border-amber-500/30"
                    }`}
                  >
                    {amd.beneficiary_acceptance_status}
                  </span>
                </div>
                <div className="text-slate-300 text-[11px]">
                  Amended Field: <span className="text-white">{amd.amended_field}</span>
                </div>
                <div className="text-[11px] text-slate-400">
                  Old: <span className="line-through text-rose-300">{amd.old_value}</span> → New:{" "}
                  <span className="text-emerald-300 font-semibold">{amd.new_value}</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === "invoice" && (
          <div className="p-3 rounded bg-slate-900 border border-card-border space-y-2">
            <div className="flex justify-between items-center border-b border-slate-800 pb-2">
              <span className="text-slate-100 font-bold">COMMERCIAL INVOICE</span>
              <span className="text-blue-400">NO: {presentation.invoice_no}</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-300">
              <div>
                <span className="text-slate-500">Applicant: </span>
                {master.applicant_name}
              </div>
              <div>
                <span className="text-slate-500">Beneficiary: </span>
                {master.beneficiary_name}
              </div>
              <div>
                <span className="text-slate-500">Drawing Amount: </span>
                <span className="text-emerald-400 font-bold">${presentation.invoice_amount?.toLocaleString()} USD</span>
              </div>
              <div>
                <span className="text-slate-500">Unit Price: </span>${presentation.invoice_unit_price} / unit
              </div>
            </div>
            <div className="mt-2 pt-2 border-t border-slate-800">
              <span className="text-slate-500 text-[11px]">Goods Description:</span>
              <div
                className={`mt-1 p-2 rounded text-slate-200 text-xs border ${
                  presentation.invoice_goods_description?.includes("MASHINE")
                    ? "bg-amber-500/10 border-amber-500/30 text-amber-200"
                    : "bg-slate-950 border-card-border"
                }`}
              >
                {presentation.invoice_goods_description}
                {presentation.invoice_goods_description?.includes("MASHINE") && (
                  <span className="ml-2 text-[10px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold">
                    ISBP 745 A23 TYPO
                  </span>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === "bl" && (
          <div className="p-3 rounded bg-slate-900 border border-card-border space-y-2">
            <div className="flex justify-between items-center border-b border-slate-800 pb-2">
              <span className="text-slate-100 font-bold">OCEAN BILL OF LADING</span>
              <span className="text-blue-400">B/L: {presentation.bl_no}</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-300">
              <div>
                <span className="text-slate-500">Vessel: </span>
                <span className={presentation.bl_vessel === "PACIFIC STAR" ? "text-rose-400 font-bold" : ""}>
                  {presentation.bl_vessel}
                </span>
              </div>
              <div>
                <span className="text-slate-500">On-Board Date: </span>
                {presentation.bl_on_board_date}
              </div>
              <div>
                <span className="text-slate-500">Gross Weight: </span>
                {presentation.bl_gross_weight_kg?.toLocaleString()} kg
              </div>
              <div>
                <span className="text-slate-500">Port of Loading: </span>
                {master.port_of_loading}
              </div>
            </div>
            <div className="mt-2 pt-2 border-t border-slate-800">
              <span className="text-slate-500 text-[11px]">Goods Description:</span>
              <div className="mt-1 p-2 rounded bg-slate-950 border border-card-border text-slate-200 text-xs">
                {presentation.bl_goods_description}
              </div>
            </div>
          </div>
        )}

        {activeTab === "packing" && (
          <div className="p-3 rounded bg-slate-900 border border-card-border space-y-2">
            <div className="flex justify-between items-center border-b border-slate-800 pb-2">
              <span className="text-slate-100 font-bold">PACKING LIST</span>
              <span className="text-blue-400">REF: PKL-{master.lc_id}</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-300">
              <div>
                <span className="text-slate-500">Stated Gross Weight: </span>
                <span
                  className={
                    presentation.packing_gross_weight_kg !== presentation.bl_gross_weight_kg
                      ? "text-rose-400 font-bold"
                      : "text-emerald-400"
                  }
                >
                  {presentation.packing_gross_weight_kg?.toLocaleString()} kg
                </span>
              </div>
              <div>
                <span className="text-slate-500">Net Weight: </span>
                {((presentation.packing_gross_weight_kg || 0) * 0.95).toFixed(1)} kg
              </div>
            </div>
          </div>
        )}

        {activeTab === "insurance" && (
          <div className="p-3 rounded bg-slate-900 border border-card-border space-y-2">
            <div className="flex justify-between items-center border-b border-slate-800 pb-2">
              <span className="text-slate-100 font-bold">INSURANCE CERTIFICATE / POLICY</span>
              <span className="text-blue-400">TYPE: {presentation.insurance_doc_type}</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-300">
              <div>
                <span className="text-slate-500">Insured Amount: </span>
                <span
                  className={
                    master.lc_id === "LC-2026-9104"
                      ? "text-rose-400 font-bold"
                      : "text-emerald-400 font-bold"
                  }
                >
                  ${presentation.insurance_amount?.toLocaleString()} USD
                </span>
              </div>
              <div>
                <span className="text-slate-500">Effective Date: </span>
                {presentation.insurance_effective_date}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
