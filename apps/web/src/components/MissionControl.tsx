"use client";

import React, { useEffect, useMemo, useState } from "react";
import {
  Activity,
  ArrowRight,
  BadgeCheck,
  BookOpenCheck,
  Bot,
  Calculator,
  Check,
  CheckCircle2,
  ChevronRight,
  CircleDot,
  Database,
  FileSearch,
  FileText,
  Fingerprint,
  GitBranch,
  LayoutDashboard,
  LockKeyhole,
  Network,
  Play,
  RotateCcw,
  Scale,
  ShieldCheck,
  Sparkles,
  UserCheck,
} from "lucide-react";
import DocumentViewerPane from "@/components/DocumentViewerPane";
import AdjudicationMatrixPane from "@/components/AdjudicationMatrixPane";
import DecisionActionPane from "@/components/DecisionActionPane";
import EvidenceIntake from "@/components/EvidenceIntake";
import { ExaminationPhase } from "@/lib/examination-reducer";
import { BankDecision, DeterministicCheck, PipelineStageUpdate } from "@/lib/types";

type WorkspaceId = "overview" | "evidence" | "agents" | "rules" | "federation" | "decision" | "audit";

type MissionControlProps = {
  selectedLcId: string;
  scenarioData: any;
  stages: Record<number, PipelineStageUpdate>;
  phase: ExaminationPhase;
  decision?: BankDecision;
  generatedArtifact?: string;
  approvalReceipt?: any;
  onStartExamination: () => void;
  onApproveAction: (examinerName: string, comments: string) => Promise<any>;
  onOpenFederationProof: () => void;
  onEvidenceAccepted: (updated: any) => void;
  canRun: boolean;
  openEvidenceSignal: number;
};

const NAV_ITEMS: Array<{ id: WorkspaceId; label: string; eyebrow: string; icon: React.ElementType }> = [
  { id: "overview", label: "Case overview", eyebrow: "Mission control", icon: LayoutDashboard },
  { id: "evidence", label: "Evidence room", eyebrow: "Documents + OCR", icon: FileSearch },
  { id: "agents", label: "Agent run", eyebrow: "Live orchestration", icon: Network },
  { id: "rules", label: "Rule analysis", eyebrow: "Math + legal", icon: Scale },
  { id: "federation", label: "Federation", eyebrow: "Three data silos", icon: Database },
  { id: "decision", label: "Decision studio", eyebrow: "Action + sign-off", icon: UserCheck },
  { id: "audit", label: "Audit receipt", eyebrow: "Proof + lineage", icon: Fingerprint },
];

const AGENTS = [
  { stage: 1, owner: "Meterless / Memory", role: "Resolve active terms", icon: GitBranch, tone: "sage" },
  { stage: 2, owner: "Zetaris", role: "Federate three silos", icon: Database, tone: "blue" },
  { stage: 3, owner: "Python", role: "Lock math and dates", icon: Calculator, tone: "copper" },
  { stage: 4, owner: "Nemotron", role: "Interpret semantics", icon: Sparkles, tone: "violet" },
  { stage: 5, owner: "Policy / Human", role: "Recommend, then authorize", icon: ShieldCheck, tone: "gold" },
] as const;

function isStageComplete(stageNumber: number, stages: Record<number, PipelineStageUpdate>, decision?: BankDecision) {
  const stage = stages[stageNumber];
  if (!stage) return false;
  if (stageNumber === 1) return Boolean(stage.active_terms || stages[2]);
  if (stageNumber === 2) return Boolean(stage.execution_mode || stages[3]);
  if (stageNumber === 3) return Boolean(stage.checks || stages[4]);
  if (stageNumber === 4) return Boolean(stage.findings || stage.final_locked_verdict || stages[5]);
  return Boolean(stage.decision || decision);
}

function getCurrentStage(stages: Record<number, PipelineStageUpdate>) {
  const available = Object.keys(stages).map(Number);
  return available.length ? Math.max(...available) : 0;
}

function stageSummary(stageNumber: number, stage?: PipelineStageUpdate, decision?: BankDecision) {
  if (!stage) return "Waiting for structured input";
  const duration = stage.duration_ms ? ` · ${stage.duration_ms} ms` : "";
  if (stageNumber === 1) return stage.active_terms ? `${stage.token_savings_pct ?? 0}% saved: ${stage.routed_tokens_actual ?? "—"} routed vs ${stage.raw_prompt_tokens_est ?? "—"} baseline tokens${duration}` : "Resolving amendment state";
  if (stageNumber === 2) return stage.execution_mode ? `${stage.execution_mode} · ${stage.query_ms ?? "—"} ms${duration}` : "Querying data silos";
  if (stageNumber === 3) return stage.checks ? `${stage.checks.length} checks · ${stage.failed_count ?? 0} locked failures${duration}` : "Executing deterministic rules";
  if (stageNumber === 4) return `${stage.final_locked_verdict || stage.overall_legal_status || "Adjudicating legal semantics"}${duration}`;
  return `${decision?.recommended_action || "Human gate remains locked"}${duration}`;
}

function formatValue(value: unknown) {
  if (typeof value === "number") {
    if (Math.abs(value) >= 1000) return value.toLocaleString(undefined, { maximumFractionDigits: 2 });
    return value.toLocaleString(undefined, { maximumFractionDigits: 2 });
  }
  if (typeof value === "boolean") return value ? "TRUE" : "FALSE";
  return String(value ?? "—");
}

function AgentNetwork({ stages, phase, decision }: Pick<MissionControlProps, "stages" | "phase" | "decision">) {
  const currentStage = getCurrentStage(stages);
  const running = phase === "streaming";
  const completeRun = phase === "recommended" || phase === "authorized";

  return (
    <section className={`agent-network ${running ? "is-running" : ""} ${completeRun ? "is-complete" : ""}`} aria-label="Live five-agent execution graph">
      <div className="network-source-row" aria-label="Evidence sources">
        <span><FileText /> Documentary credit</span>
        <span><Database /> Customs benchmark</span>
        <span><BadgeCheck /> Sanctions intelligence</span>
        <i aria-hidden="true">STRUCTURED EVIDENCE IN</i>
      </div>
      <div className="agent-rail">
        {AGENTS.map((agent, index) => {
          const complete = isStageComplete(agent.stage, stages, decision);
          const active = running && currentStage === agent.stage && !complete;
          const state = complete ? "complete" : active ? "active" : "queued";
          const Icon = agent.icon;
          return (
            <React.Fragment key={agent.stage}>
              <article className={`agent-node ${state} tone-${agent.tone}`} style={{ "--agent-delay": `${index * 180}ms` } as React.CSSProperties} aria-current={active ? "step" : undefined}>
                <div className="agent-node-orbit" aria-hidden="true"><span /><span /></div>
                <div className="agent-node-icon"><Icon /></div>
                <div className="agent-node-copy">
                  <small>AGENT {String(agent.stage).padStart(2, "0")}</small>
                  <h3>{agent.owner}</h3>
                  <p>{agent.role}</p>
                  <b>{active ? "Processing evidence…" : complete ? stageSummary(agent.stage, stages[agent.stage], decision) : "Awaiting handoff"}</b>
                </div>
                <span className="agent-state-mark" aria-label={state}>{complete ? <Check /> : active ? <CircleDot /> : String(agent.stage)}</span>
              </article>
              {index < AGENTS.length - 1 && (
                <div className={`agent-link ${complete ? "complete" : active ? "active" : "queued"}`} style={{ "--agent-delay": `${index * 180 + 90}ms` } as React.CSSProperties} aria-hidden="true">
                  <span className="evidence-packet" />
                  <ArrowRight />
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
      <div className="network-invariant">
        <LockKeyhole />
        <div><b>Hard invariant enforced</b><span>Neural interpretation is downstream of deterministic truth and cannot reverse a failed check.</span></div>
        <span className="invariant-lock">IMMUTABLE</span>
      </div>
    </section>
  );
}

function CalculationBoard({ checks }: { checks: DeterministicCheck[] }) {
  if (!checks.length) {
    return (
      <div className="calculation-empty">
        <Calculator />
        <span>DETERMINISTIC ENGINE IDLE</span>
        <h3>Run the examination to reveal every calculation.</h3>
        <p>Python—not the language model—owns amounts, tolerances, dates, coverage thresholds and cross-document reconciliation.</p>
      </div>
    );
  }

  return (
    <div className="calculation-grid">
      {checks.map((check, index) => (
        <article key={check.check_id || `${check.name}-${index}`} className={`calculation-card ${check.passed ? "passed" : "failed"}`}>
          <div className="calculation-card-head">
            <span>{String(index + 1).padStart(2, "0")}</span>
            <b>{check.ucp_citation}</b>
            <i>{check.passed ? "PASSED" : "LOCKED DISCREPANCY"}</i>
          </div>
          <h3>{check.name}</h3>
          <div className="calculation-values">
            {Object.entries(check.computed_values || {}).map(([key, value]) => (
              <div key={key}><span>{key.replaceAll("_", " ")}</span><strong>{formatValue(value)}</strong></div>
            ))}
          </div>
          <p>{check.details}</p>
        </article>
      ))}
    </div>
  );
}

function FederationWorkspace({ stage, onOpenProof }: { stage?: PipelineStageUpdate; onOpenProof: () => void }) {
  const hasResult = Boolean(stage?.execution_mode);
  const anomaly = Number(stage?.tbml_price_zscore || 0) > 4;
  const sanctions = Number(stage?.sanction_hit_count || 0) > 0;

  return (
    <div className="federation-workspace">
      <div className="federation-map" aria-label="Three-silo federation map">
        <article><span>01 / OLTP</span><Database /><h3>PostgreSQL</h3><p>LC master, amendments and examination state.</p><b>{hasResult ? "SOURCE RESOLVED" : "WAITING"}</b></article>
        <div className="federation-join"><span /><i>JOIN-SAFE CTE</i><span /></div>
        <article className={anomaly ? "risk" : ""}><span>02 / PARQUET</span><Activity /><h3>Customs HS-6</h3><p>{hasResult ? "Z-score = (invoice unit price − HS-6 market mean) ÷ market standard deviation. Above 4 is flagged for review." : "Historical unit-price distribution will explain the TBML signal."}</p><b>{hasResult ? `Z-SCORE ${Number(stage?.tbml_price_zscore || 0).toFixed(2)} · ${anomaly ? "ABOVE 4 THRESHOLD" : "WITHIN THRESHOLD"}` : "WAITING"}</b></article>
        <div className="federation-join"><span /><i>ONE ROW / LC</i><span /></div>
        <article className={sanctions ? "risk" : ""}><span>03 / API DATA</span><BadgeCheck /><h3>OpenSanctions</h3><p>Entity, party and vessel watchlist screening.</p><b>{hasResult ? `${stage?.sanction_hit_count || 0} MATCHES` : "WAITING"}</b></article>
      </div>
      <div className="federation-result-card">
        <div><small>OBSERVED EXECUTION</small><strong>{stage?.execution_mode || "NOT YET OBSERVED"}</strong></div>
        <div><small>QUERY LATENCY</small><strong>{stage?.query_ms !== undefined ? `${stage.query_ms} ms` : "—"}</strong></div>
        <div><small>OUTPUT CARDINALITY</small><strong>{hasResult ? "EXACTLY 1 ROW" : "—"}</strong></div>
        <button type="button" onClick={onOpenProof}>Inspect query & provenance <ChevronRight /></button>
      </div>
    </div>
  );
}

function AuditWorkspace({ stages, decision, receipt, phase }: { stages: Record<number, PipelineStageUpdate>; decision?: BankDecision; receipt?: any; phase: ExaminationPhase }) {
  const stage1 = stages[1];
  const stage5: any = stages[5];
  const authorized = phase === "authorized";
  const proofRows = [
    { label: "Active terms fingerprint", value: stage1?.active_terms_sha256, ready: Boolean(stage1?.active_terms_sha256) },
    { label: "Decision digest", value: stage5?.decision_sha256, ready: Boolean(stage5?.decision_sha256) },
    { label: "Evidence Merkle root", value: receipt?.decision_receipt?.merkle_root_sha256 || stage5?.merkle_root_sha256, ready: Boolean(receipt?.decision_receipt?.merkle_root_sha256 || stage5?.merkle_root_sha256) },
    { label: "Human signature token", value: receipt?.audit_receipt_hash || receipt?.decision_receipt?.signature_token, ready: Boolean(receipt?.audit_receipt_hash || receipt?.decision_receipt?.signature_token) },
  ];

  return (
    <div className="audit-workspace">
      <div className={`seal-visual ${authorized ? "sealed" : "locked"}`} aria-label={authorized ? "Decision cryptographically sealed" : "Human authorization pending"}>
        <div className="seal-rings"><span /><span /><span /></div>
        {authorized ? <Fingerprint /> : <LockKeyhole />}
        <small>{authorized ? "VERITAS AUTHORITY SEAL" : "AUTHORITY GATE"}</small>
        <strong>{authorized ? "SEALED" : "LOCKED"}</strong>
        <p>{authorized ? receipt?.status || "AUTHORIZED_NOT_DISPATCHED" : decision ? "Recommendation ready for examiner sign-off" : "Complete the agent run before authorization"}</p>
      </div>
      <div className="proof-ledger">
        <div className="proof-ledger-head"><span>CHAIN OF CUSTODY</span><b>{proofRows.filter((row) => row.ready).length} / {proofRows.length} PROOFS READY</b></div>
        {proofRows.map((row, index) => (
          <div className={`proof-row ${row.ready ? "ready" : "pending"}`} key={row.label}>
            <span>{row.ready ? <CheckCircle2 /> : <CircleDot />}</span>
            <div><small>PROOF {String(index + 1).padStart(2, "0")}</small><b>{row.label}</b><code>{row.value || "Awaiting upstream evidence"}</code></div>
          </div>
        ))}
        <div className="proof-authority"><UserCheck /><div><b>Human authority remains final</b><span>The system recommends. An examiner explicitly authorizes the operational action.</span></div></div>
      </div>
    </div>
  );
}

export default function MissionControl({
  selectedLcId,
  scenarioData,
  stages,
  phase,
  decision,
  generatedArtifact,
  approvalReceipt,
  onStartExamination,
  onApproveAction,
  onOpenFederationProof,
  onEvidenceAccepted,
  canRun,
  openEvidenceSignal,
}: MissionControlProps) {
  const [activeWorkspace, setActiveWorkspace] = useState<WorkspaceId>("overview");
  const currentStage = getCurrentStage(stages);
  const checks = stages[3]?.checks || [];
  const completedStages = AGENTS.filter((agent) => isStageComplete(agent.stage, stages, decision)).length;
  const master = scenarioData?.master || {};
  const isRunning = phase === "streaming";
  const evidenceStatus = scenarioData?.evidence_status || (scenarioData && !scenarioData.case_source ? "SAMPLE_READY" : "AWAITING_DOCUMENTS");
  const evidenceCount = scenarioData?.evidence_documents?.length || (scenarioData?.case_source === "SAMPLE_CASE" ? 5 : 0);
  const ready = ["SAMPLE_READY", "ACCEPTED"].includes(evidenceStatus);

  useEffect(() => {
    if (phase === "authorized") setActiveWorkspace("audit");
  }, [phase]);

  useEffect(() => {
    const requestedWorkspace = new URLSearchParams(window.location.search).get("workspace") as WorkspaceId | null;
    setActiveWorkspace(requestedWorkspace && NAV_ITEMS.some((item) => item.id === requestedWorkspace) ? requestedWorkspace : "overview");
  }, [selectedLcId]);

  useEffect(() => {
    if (openEvidenceSignal > 0) setActiveWorkspace("evidence");
  }, [openEvidenceSignal]);

  const workspaceMeta = useMemo(() => NAV_ITEMS.find((item) => item.id === activeWorkspace) || NAV_ITEMS[0], [activeWorkspace]);

  const navStatus = (id: WorkspaceId) => {
    if (id === "evidence") return scenarioData ? "ready" : "pending";
    if (id === "agents") return isRunning ? "active" : completedStages === 5 ? "ready" : "pending";
    if (id === "rules") return stages[3] || stages[4] ? "ready" : "pending";
    if (id === "federation") return stages[2]?.execution_mode ? "ready" : "pending";
    if (id === "decision") return decision ? "ready" : "locked";
    if (id === "audit") return phase === "authorized" ? "ready" : "locked";
    return "ready";
  };

  const runAndOpenAgents = () => {
    setActiveWorkspace(canRun ? "agents" : "evidence");
    onStartExamination();
  };

  return (
    <div className="mission-control">
      <aside className="mission-sidebar" aria-label="Examination workspaces">
        <div className="mission-sidebar-brand"><Bot /><div><span>VERITAS OS</span><b>Examination system</b></div></div>
        <nav>
          {NAV_ITEMS.map((item, index) => {
            const Icon = item.icon;
            const status = navStatus(item.id);
            return (
              <button
                type="button"
                key={item.id}
                onClick={() => setActiveWorkspace(item.id)}
                className={`${activeWorkspace === item.id ? "active" : ""} status-${status}`}
                aria-current={activeWorkspace === item.id ? "page" : undefined}
              >
                <span className="nav-index">{String(index + 1).padStart(2, "0")}</span>
                <Icon />
                <span className="nav-copy"><b>{item.label}</b><small>{status === "locked" ? "Run required" : item.eyebrow}</small></span>
                <span className="nav-status" aria-label={status}>{status === "ready" ? <Check /> : status === "active" ? <Activity /> : status === "locked" ? <LockKeyhole /> : <CircleDot />}</span>
              </button>
            );
          })}
        </nav>
        <div className="mission-sidebar-foot">
          <span><i className={isRunning ? "live" : ""} /> {isRunning ? `AGENT ${currentStage} ACTIVE` : `${completedStages}/5 AGENTS COMPLETE`}</span>
          <p>Every handoff is bounded, observable and audit-linked.</p>
        </div>
      </aside>

      <main id="main-content" className="mission-stage">
        <header className="mission-commandbar">
          <div>
            <span className="mission-breadcrumb">EXAMINATION / {workspaceMeta.label.toUpperCase()}</span>
            <h1>{selectedLcId}</h1>
            <p>{master.applicant_name || "Loading applicant evidence"} <ArrowRight /> {master.beneficiary_name || "Loading beneficiary"}</p>
          </div>
          <div className="mission-case-facts">
            <span><small>CREDIT</small><b>{master.credit_amount || master.amount ? `$${Number(master.credit_amount || master.amount).toLocaleString()}` : "—"}</b></span>
            <span><small>WORKFLOW</small><b>{phase.replaceAll("_", " ").toUpperCase()}</b></span>
          </div>
          <button type="button" onClick={runAndOpenAgents} disabled={isRunning || !canRun} className="primary-audit-action" title={!canRun ? "Upload and accept reviewed evidence before running the audit" : undefined}>
            {isRunning ? <RotateCcw /> : <Play />}
            <span><small>{!canRun ? "EVIDENCE REVIEW REQUIRED" : isRunning ? "FIVE AGENTS EXECUTING" : completedStages ? "RUN AGAIN" : "START BOUNDED AUDIT"}</small><b>{!canRun ? "Complete document review" : isRunning ? `Stage ${currentStage} is analyzing` : "Run examination"}</b></span>
            <ChevronRight />
          </button>
        </header>

        {decision && activeWorkspace !== "decision" && activeWorkspace !== "audit" && (
          <button type="button" className="recommendation-banner" onClick={() => setActiveWorkspace("decision")}>
            <BadgeCheck /><span><small>RECOMMENDATION READY</small><b>{decision.action_title}</b></span><i>{decision.recommended_action}</i><ChevronRight />
          </button>
        )}

        <div className="mission-workspace" key={activeWorkspace}>
          {activeWorkspace === "overview" && (
            <div className="overview-workspace">
              <ol className="examiner-journey" aria-label="How to complete an examination">
                <li className={scenarioData ? "complete" : "active"}><span>1</span><div><b>Create or select a case</b><small>Confirm the credit baseline</small></div></li>
                <li className={canRun ? "complete" : "active"}><span>2</span><div><b>Add and review documents</b><small>Accept OCR evidence</small></div></li>
                <li className={completedStages === 5 ? "complete" : canRun ? "active" : "pending"}><span>3</span><div><b>Run the bounded audit</b><small>Watch five accountable stages</small></div></li>
                <li className={phase === "authorized" ? "complete" : decision ? "active" : "pending"}><span>4</span><div><b>Review and authorize</b><small>Human sign-off stays final</small></div></li>
              </ol>
              <section className="overview-hero">
                <div className="overview-hero-copy">
                  <span>AGENTIC TRADE FINANCE / LIVE CASE</span>
                  <h2>One presentation.<br />Five bounded agents.<br /><em>One accountable decision.</em></h2>
                  <p>Follow evidence from source documents through federation, deterministic validation, legal interpretation and a mandatory human authority gate.</p>
                  <div><button type="button" onClick={runAndOpenAgents} disabled={!canRun}><Play /> {canRun ? "Run bounded audit" : "Review evidence first"}</button><button type="button" onClick={() => setActiveWorkspace("evidence")}>Open evidence room <ArrowRight /></button></div>
                </div>
                <div className="overview-scorecard">
                  <span>CASE READINESS</span>
                  <strong>{ready ? "READY" : evidenceStatus.replaceAll("_", " ")}</strong>
                  <div><i style={{ width: ready ? "100%" : evidenceCount ? "50%" : "15%" }} /></div>
                  <dl>
                    <div><dt>Agents complete</dt><dd>{completedStages} / 5</dd></div>
                    <div><dt>Evidence documents</dt><dd>{evidenceCount}</dd></div>
                    <div><dt>Rules evaluated</dt><dd>{checks.length || "—"}</dd></div>
                    <div><dt>Human authority</dt><dd>{phase === "authorized" ? "SEALED" : "LOCKED"}</dd></div>
                  </dl>
                  <p className="readiness-reason">{ready ? "Required evidence is available for a bounded run." : "Readiness stays locked until required documents are extracted and examiner-accepted."}</p>
                </div>
              </section>
              <AgentNetwork stages={stages} phase={phase} decision={decision} />
              <section className="module-launchpad" aria-label="Open examination modules">
                {NAV_ITEMS.slice(1).map((item, index) => {
                  const Icon = item.icon;
                  const status = navStatus(item.id);
                  return <button type="button" key={item.id} onClick={() => setActiveWorkspace(item.id)}><span>{String(index + 1).padStart(2, "0")}</span><Icon /><div><small>{status.toUpperCase()}</small><b>{item.label}</b><p>{item.eyebrow}</p></div><ChevronRight /></button>;
                })}
              </section>
            </div>
          )}

          {activeWorkspace === "evidence" && (
            <section className="dedicated-workspace">
              <div className="workspace-intro"><div><span>SOURCE EVIDENCE</span><h2>Evidence room</h2></div><p>Open each instrument, run extraction, and inspect spatial anchors without leaving the case.</p></div>
              <EvidenceIntake lcId={selectedLcId} scenarioData={scenarioData} onEvidenceAccepted={onEvidenceAccepted} />
              <div className="workspace-component document-workspace"><DocumentViewerPane scenarioData={scenarioData} /></div>
            </section>
          )}

          {activeWorkspace === "agents" && (
            <section className="dedicated-workspace">
              <div className="workspace-intro"><div><span>LIVE ORCHESTRATION</span><h2>Agent execution graph</h2></div><p>Animated handoffs represent real SSE stage transitions—not decorative simulated activity.</p></div>
              <AgentNetwork stages={stages} phase={phase} decision={decision} />
              <div className="agent-event-ledger">
                <div className="event-ledger-head"><span>STRUCTURED EVENT STREAM</span><b>{isRunning ? "RECEIVING" : completedStages ? "RUN COMPLETE" : "IDLE"}</b></div>
                {AGENTS.map((agent) => {
                  const complete = isStageComplete(agent.stage, stages, decision);
                  const active = isRunning && currentStage === agent.stage && !complete;
                  return <div key={agent.stage} className={`${complete ? "complete" : active ? "active" : "queued"}`}><span>{String(agent.stage).padStart(2, "0")}</span><i /><div><b>{agent.owner}</b><small>{stageSummary(agent.stage, stages[agent.stage], decision)}</small></div><em>{complete ? "OUTPUT RECEIVED" : active ? "PROCESSING" : "QUEUED"}</em></div>;
                })}
              </div>
            </section>
          )}

          {activeWorkspace === "rules" && (
            <section className="dedicated-workspace">
              <div className="workspace-intro"><div><span>NEURO-SYMBOLIC SPLIT</span><h2>Calculation & rule analysis</h2></div><p>Backend-computed values remain visibly separate from Nemotron’s bounded semantic findings.</p></div>
              <CalculationBoard checks={checks} />
              <div className="workspace-component rules-workspace"><AdjudicationMatrixPane stages={stages} isExamining={isRunning} onStartExamination={runAndOpenAgents} selectedLcId={selectedLcId} /></div>
            </section>
          )}

          {activeWorkspace === "federation" && (
            <section className="dedicated-workspace">
              <div className="workspace-intro"><div><span>IN-SITU FEDERATION</span><h2>Three silos. Zero ETL.</h2></div><p>The runtime mode shown here is observed from the actual run and never presented as live cloud when fallback executes.</p></div>
              <FederationWorkspace stage={stages[2]} onOpenProof={onOpenFederationProof} />
            </section>
          )}

          {activeWorkspace === "decision" && (
            <section className="dedicated-workspace">
              <div className="workspace-intro"><div><span>POLICY RECOMMENDATION</span><h2>Decision studio & human gate</h2></div><p>The system may recommend and prepare an artifact. Only the examiner can authorize dispatch.</p></div>
              <div className="workspace-component decision-workspace"><DecisionActionPane decision={decision} generatedArtifact={generatedArtifact} onApproveAction={onApproveAction} approvalReceipt={approvalReceipt} /></div>
            </section>
          )}

          {activeWorkspace === "audit" && (
            <section className="dedicated-workspace">
              <div className="workspace-intro"><div><span>CRYPTOGRAPHIC PROVENANCE</span><h2>Audit receipt & evidence lineage</h2></div><p>Terms, evidence, rules, recommendation and human authorization converge in one verifiable chain of custody.</p></div>
              <AuditWorkspace stages={stages} decision={decision} receipt={approvalReceipt} phase={phase} />
              {!decision && <button type="button" className="audit-next-action" onClick={runAndOpenAgents}><Play /> Run examination to build the proof chain</button>}
              {decision && phase !== "authorized" && <button type="button" className="audit-next-action" onClick={() => setActiveWorkspace("decision")}><UserCheck /> Open mandatory human sign-off</button>}
            </section>
          )}
        </div>
      </main>
    </div>
  );
}
