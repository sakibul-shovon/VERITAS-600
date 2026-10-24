"use client";

import React, { useState } from "react";
import {
  FileCheck2,
  FileX,
  AlertOctagon,
  CheckCircle,
  Copy,
  Check,
  Send,
  DollarSign,
  UserCheck,
} from "lucide-react";
import { BankDecision } from "@/lib/types";

interface DecisionActionPaneProps {
  decision?: BankDecision;
  generatedArtifact?: string;
  onApproveAction: (examinerName: string, comments: string) => Promise<any>;
  approvalReceipt?: any;
}

export default function DecisionActionPane({
  decision,
  generatedArtifact,
  onApproveAction,
  approvalReceipt,
}: DecisionActionPaneProps) {
  const [copied, setCopied] = useState(false);
  const [isSigning, setIsSigning] = useState(false);
  const [signedSuccess, setSignedSuccess] = useState(false);
  const [receipt, setReceipt] = useState<any>(null);
  const [signError, setSignError] = useState<string | undefined>(undefined);
  const [examinerName, setExaminerName] = useState("");
  const [comments, setComments] = useState("");

  const handleCopyArtifact = () => {
    if (!generatedArtifact) return;
    navigator.clipboard.writeText(generatedArtifact);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSignOff = async () => {
    setSignError(undefined);
    if (!examinerName.trim()) { setSignError("Enter the examining officer’s name before authorizing this action."); return; }
    setIsSigning(true);
    try {
      const res = await onApproveAction(examinerName, comments);
      if (res) setReceipt(res);
      setSignedSuccess(true);
    } catch (err) {
      console.error(err);
      setSignError("Authorization was not accepted by the server. Your entered details have been kept; review and try again.");
    } finally {
      setIsSigning(false);
    }
  };

  const getActionTheme = () => {
    switch (decision?.recommended_action) {
      case "APPROVE_HONOUR":
        return {
          bg: "bg-emerald-950/20 border-emerald-500/30",
          badge: "bg-emerald-500/20 text-emerald-300 border-emerald-500/40",
          icon: FileCheck2,
          iconColor: "text-emerald-400",
        };
      case "ISSUE_MT734_REFUSAL":
        return {
          bg: "bg-amber-950/20 border-amber-500/30",
          badge: "bg-amber-500/20 text-amber-300 border-amber-500/40",
          icon: FileX,
          iconColor: "text-amber-400",
        };
      case "COMPLIANCE_HOLD_AML":
        return {
          bg: "bg-rose-950/30 border-rose-500/40",
          badge: "bg-rose-500/20 text-rose-300 border-rose-500/40",
          icon: AlertOctagon,
          iconColor: "text-rose-400",
        };
      default:
        return {
          bg: "bg-slate-900 border-card-border",
          badge: "bg-slate-800 text-slate-400 border-slate-700",
          icon: FileCheck2,
          iconColor: "text-slate-400",
        };
    }
  };

  const theme = getActionTheme();
  const Icon = theme.icon;
  const isAuthorized = signedSuccess || decision?.action_status === "APPROVED";
  const effectiveReceipt = receipt || approvalReceipt;

  return (
    <div className="exam-pane exam-decision-pane flex flex-col h-full bg-card rounded-lg border border-card-border overflow-hidden">
      {/* Pane Header */}
      <div className="flex items-center justify-between px-3 py-2 bg-slate-900/60 border-b border-card-border">
        <div className="flex items-center gap-2">
          <UserCheck className="h-4 w-4 text-purple-400" />
          <span className="font-semibold text-xs tracking-wide text-slate-200 uppercase">
            Decision Docket & Human Gate
          </span>
        </div>
      </div>

      <div className="flex-1 p-3 overflow-y-auto space-y-3 font-mono text-xs">
        {/* Recommended Action Card */}
        {decision ? (
          <div className={`p-3 rounded-lg border ${theme.bg} space-y-2`}>
            <div className="flex items-start justify-between gap-2">
              <div className="flex items-center gap-2">
                <Icon className={`h-5 w-5 ${theme.iconColor}`} />
                <div>
                  <h3 className="font-bold text-slate-100 text-xs tracking-wide">{decision.action_title}</h3>
                  <div className="text-[10px] text-slate-400 mt-0.5">
                    Action Type: <span className="font-bold text-slate-300">{decision.recommended_action}</span>
                  </div>
                </div>
              </div>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${theme.badge}`}>
                {isAuthorized ? "AUTHORIZED (NOT DISPATCHED)" : "AWAITING SIGN-OFF"}
              </span>
            </div>
            <p className="text-[11px] text-slate-300 leading-relaxed border-t border-slate-800/80 pt-2">
              {decision.action_summary}
            </p>
          </div>
        ) : (
          <div className="p-4 text-center text-slate-500 bg-slate-950/40 rounded border border-card-border">
            Awaiting presentation examination to formulate bank action.
          </div>
        )}

        {/* Demurrage Savings Advisory Card (for MT734) */}
        {decision?.demurrage_savings_advisory && (
          <div className="p-3 rounded bg-amber-950/20 border border-amber-500/30 space-y-2">
            <div className="flex items-center gap-2 text-amber-300 font-bold text-[11px]">
              <DollarSign className="h-4 w-4 text-amber-400" />
              <span>CURE VS WAIVER DEMURRAGE ADVISORY</span>
            </div>
            <p className="text-[11px] text-slate-300">
              {decision.demurrage_savings_advisory.advisory}
            </p>
            <div className="grid grid-cols-2 gap-2 text-[11px] pt-1 border-t border-amber-500/20">
              <div>
                <span className="text-slate-400">48h Re-Presentation Demurrage: </span>
                <span className="text-emerald-400 font-bold">
                  ${decision.demurrage_savings_advisory.cured_demurrage_cost.toLocaleString()}
                </span>
              </div>
              <div>
                <span className="text-slate-400">Net Estimated Savings: </span>
                <span className="text-amber-300 font-bold">
                  ${decision.demurrage_savings_advisory.net_savings_usd.toLocaleString()} USD
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Generated Artifact Preview */}
        {generatedArtifact && (
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold text-slate-400 uppercase">
                Generated Bank Operational Artifact
              </span>
              <button
                onClick={handleCopyArtifact}
                className="flex items-center gap-1 text-[11px] text-slate-400 hover:text-slate-200"
              >
                {copied ? <Check className="h-3 w-3 text-emerald-400" /> : <Copy className="h-3 w-3" />}
                <span>{copied ? "Copied" : "Copy"}</span>
              </button>
            </div>
            <div className="p-2.5 rounded bg-slate-950 border border-card-border overflow-x-auto max-h-56">
              <pre className="text-[11px] text-slate-300 font-mono whitespace-pre leading-relaxed">
                {generatedArtifact}
              </pre>
            </div>
          </div>
        )}

        {/* Human-in-the-Loop Sign-Off Gate */}
        {decision && (
          <div className="p-3 rounded-lg bg-slate-900 border border-card-border space-y-2 mt-4">
            <div className="flex items-center gap-2 text-indigo-300 font-bold text-xs">
              <UserCheck className="h-4 w-4" />
              <span>Mandatory Human Examiner Sign-Off</span>
            </div>
            <p className="text-[11px] text-slate-400">
              Pursuant to bank governance mandates, every final action requires explicit human verification
              before settlement release, MT734 dispatch, or AML filing.
            </p>

            {isAuthorized ? (
              <div className="p-3 rounded bg-emerald-950/30 border border-emerald-500/40 text-emerald-200 text-xs space-y-2">
                <div className="flex items-center gap-2 font-bold text-emerald-300">
                  <CheckCircle className="h-4 w-4 text-emerald-400 shrink-0" />
                  <span>Dual-Control Execution Authorized & Sealed</span>
                </div>
                <div className="text-[11px] text-slate-300 space-y-1 font-mono bg-slate-950/70 p-2 rounded border border-emerald-500/20">
                  <div>
                    <span className="text-slate-400">Authorized By: </span>
                    <span className="text-slate-100 font-bold">{examinerName}</span>
                  </div>
                  <div>
                    <span className="text-slate-400">Signature Token: </span>
                    <span className="text-blue-300 font-bold break-all">
                      {effectiveReceipt?.audit_receipt_hash || effectiveReceipt?.decision_receipt?.signature_token || "V600-SIG-SEALED"}
                    </span>
                  </div>
                  {effectiveReceipt?.decision_receipt?.merkle_root_sha256 && (
                    <div>
                      <span className="text-slate-400">Merkle Root: </span>
                      <span className="text-purple-300 text-[10px] break-all">
                        {effectiveReceipt.decision_receipt.merkle_root_sha256.slice(0, 32)}...
                      </span>
                    </div>
                  )}
                  <div className="flex items-center justify-between pt-1 border-t border-slate-800 text-[10px]">
                    <span className="text-slate-400">Dispatch Status:</span>
                    <span className="text-emerald-400 font-bold">AUTHORIZED — NOT DISPATCHED</span>
                  </div>
                  <div className="text-[10px] text-slate-400">External SWIFT / AML dispatch is not connected in this runtime.</div>
                </div>
              </div>
            ) : (
              <div className="space-y-2 pt-1">
                {signError && <p className="text-[11px] text-rose-300 border border-rose-500/40 bg-rose-950/30 rounded p-2" role="alert">{signError}</p>}
                <label className="signoff-field"><span>Examiner name and officer ID</span><input
                    type="text"
                    value={examinerName}
                    onChange={(e) => setExaminerName(e.target.value)}
                    placeholder="e.g. Sarah Chen · TF-482"
                    autoComplete="name"
                  /></label>
                <label className="signoff-field"><span>Review comments</span><textarea
                    value={comments}
                    onChange={(e) => setComments(e.target.value)}
                    placeholder="Record what you verified, any escalation, and why this action is authorized."
                    rows={4}
                  /></label>
                <button
                  onClick={handleSignOff}
                  disabled={isSigning}
                  className="w-full py-2 rounded bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-xs shadow-md shadow-blue-500/20 transition flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  <Send className="h-3.5 w-3.5" />
                  <span>{isSigning ? "Authorizing & sealing…" : "Authorize action & seal receipt"}</span>
                </button>
                <p className="signoff-disclaimer">This records authorization only. It does not transmit SWIFT, release settlement, or file an AML report.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
