"use client";

import React, { useEffect, useReducer, useRef, useState } from "react";
import HeaderBar from "@/components/HeaderBar";
import DocumentViewerPane from "@/components/DocumentViewerPane";
import AdjudicationMatrixPane from "@/components/AdjudicationMatrixPane";
import DecisionActionPane from "@/components/DecisionActionPane";
import ZetarisDrawer from "@/components/ZetarisDrawer";
import { fetchHealth, fetchScenarios, fetchScenarioDetails, openExamineStream, approveHumanAction } from "@/lib/api";
import { LCScenarioSummary } from "@/lib/types";
import { examinationReducer, initialExaminationState } from "@/lib/examination-reducer";
import NoticeRegion from "@/components/ui/NoticeRegion";

const KNOWN_CASES = new Set(["LC-2026-8841", "LC-2026-9104", "LC-2026-9920"]);

export default function ExaminationPage() {
  const [selectedLcId, setSelectedLcId] = useState<string>("LC-2026-8841");
  const [scenarios, setScenarios] = useState<LCScenarioSummary[]>([]);
  const [scenarioData, setScenarioData] = useState<any>(null);
  const [sponsorHealth, setSponsorHealth] = useState<any>(null);
  const [loadNotice, setLoadNotice] = useState<string | undefined>(undefined);

  const [examination, dispatch] = useReducer(examinationReducer, initialExaminationState);
  const [sqlDrawerOpen, setSqlDrawerOpen] = useState<boolean>(false);
  const streamRef = useRef<EventSource | null>(null);
  const runTokenRef = useRef(0);

  useEffect(() => {
    const requestedCase = new URLSearchParams(window.location.search).get("case");
    if (requestedCase && KNOWN_CASES.has(requestedCase)) setSelectedLcId(requestedCase);

    fetchHealth().then(setSponsorHealth).catch((err) => console.error("Health check error:", err));
    fetchScenarios().then((res) => {
      const availableScenarios = res.scenarios || [];
      setScenarios(availableScenarios);
      if (availableScenarios.length === 0) setLoadNotice("No examination cases are currently available from the API.");
    }).catch((err) => { console.error("Scenarios error:", err); setLoadNotice("Case discovery is unavailable. Please retry when the API is running."); });
  }, []);

  useEffect(() => () => streamRef.current?.close(), []);

  useEffect(() => {
    if (!selectedLcId) return;
    runTokenRef.current += 1;
    streamRef.current?.close();
    dispatch({ type: "CASE_SELECTED" });
    setScenarioData(null);
    fetchScenarioDetails(selectedLcId).then((data) => { setScenarioData(data); setLoadNotice(undefined); }).catch((err) => { console.error("Scenario details error:", err); setLoadNotice("The selected case could not be loaded. You can choose another available case or retry shortly."); });
  }, [selectedLcId]);

  const handleStartExamination = () => {
    streamRef.current?.close();
    const token = ++runTokenRef.current;
    const caseAtStart = selectedLcId;
    dispatch({ type: "RUN_STARTED" });

    streamRef.current = openExamineStream(
      selectedLcId,
      (event, data) => {
        if (token !== runTokenRef.current || caseAtStart !== selectedLcId) return;
        if (event === "stage_start") {
          dispatch({ type: "STAGE_RECEIVED", stage: { stage: data.stage, name: data.name } });
        } else if (event === "stage_complete") {
          dispatch({ type: "STAGE_RECEIVED", stage: data });
        } else if (event === "decision_ready") {
          dispatch({ type: "RECOMMENDATION_RECEIVED", stage: data, decision: data.decision, artifact: data.generated_artifact });
          streamRef.current?.close();
        }
      },
      (err) => {
        console.error("SSE stream error:", err);
        if (token === runTokenRef.current) dispatch({ type: "STREAM_INTERRUPTED", message: "The examination stream was interrupted. Completed evidence remains visible; you may run the case again." });
      }
    );
  };

  const handleApproveAction = async (examinerName: string, comments: string) => {
    const res = await approveHumanAction(selectedLcId, examinerName, comments);
    if (examination.decision) {
      dispatch({ type: "AUTHORIZED", decision: {
        ...examination.decision,
        action_status: "APPROVED",
        human_approved_by: examinerName,
        human_approved_at: res.human_approved_at || new Date().toISOString(),
      } });
    }
    return res;
  };

  return (
    <div className={`exam-shell ${examination.phase === "streaming" ? "audit-active" : ""} flex flex-col min-h-[100dvh] bg-background text-slate-100 font-sans`}>
      <HeaderBar
        scenarios={scenarios}
        selectedLcId={selectedLcId}
        onSelectScenario={setSelectedLcId}
        sponsorHealth={sponsorHealth}
        onToggleSqlDrawer={() => setSqlDrawerOpen((open) => !open)}
        sqlDrawerOpen={sqlDrawerOpen}
      />

      <div className="exam-context-strip" aria-live="polite">
        <span>ACTIVE PRESENTATION</span>
        <strong>{selectedLcId}</strong>
        <i />
        <span>{scenarioData?.master?.applicant_name || "Loading applicant evidence"}</span>
        <i />
        <span>{scenarioData?.master?.beneficiary_name || "Preparing document set"}</span>
        <b>{examination.phase === "streaming" ? "AUDIT STREAM ACTIVE" : examination.phase === "recommended" ? "RECOMMENDATION READY" : examination.phase === "authorized" ? "ACTION AUTHORIZED" : "READY FOR EXAMINATION"}</b>
      </div>
      <NoticeRegion message={examination.error || loadNotice} />

      <section className="case-masthead" aria-labelledby="case-title">
        <div><p>DOCUMENTARY CREDIT / ACTIVE EXAMINATION</p><h1 id="case-title">{selectedLcId}</h1><span>{scenarioData?.master?.applicant_name || "Loading applicant"} <b>→</b> {scenarioData?.master?.beneficiary_name || "Loading beneficiary"}</span></div>
        <dl><div><dt>CREDIT AMOUNT</dt><dd>{scenarioData?.master?.credit_amount ? `$${Number(scenarioData.master.credit_amount).toLocaleString()}` : "—"}</dd></div><div><dt>GOVERNING TERMS</dt><dd>{scenarioData?.master?.incoterm || "UCP 600"}</dd></div><div><dt>EXAMINATION STATUS</dt><dd>{examination.phase.replace("_", " ")}</dd></div></dl>
      </section>

      <div className="agentic-heading"><div><span>AGENTIC ORCHESTRATION</span><h2>Five bounded owners. One auditable decision.</h2></div><p>Each agent owns a limited stage and hands structured evidence forward. No model can overwrite a failed deterministic check.</p></div>
      <ol className="decision-spine" aria-label="Agentic examination decision spine">
        {[
          { owner: "METERLESS / MEMORY", label: "Resolve active terms" },
          { owner: "ZETARIS", label: "Federate three silos" },
          { owner: "PYTHON", label: "Lock math and dates" },
          { owner: "NEMOTRON", label: "Interpret legal semantics" },
          { owner: "POLICY → HUMAN", label: "Recommend, then authorize" },
        ].map((agent, index) => {
          const complete = Boolean(examination.stages[index + 1]);
          return <li key={agent.owner} className={complete ? "complete" : examination.phase === "streaming" && index === Object.keys(examination.stages).length ? "active" : ""}><span>{String(index + 1).padStart(2, "0")} / {agent.owner}</span><b>{agent.label}</b><small>{complete ? "Structured output received" : index === 4 ? "Human gate locked" : examination.phase === "streaming" && index === Object.keys(examination.stages).length ? "Agent active" : "Awaiting handoff"}</small></li>;
        })}
      </ol>

      <main id="main-content" className="exam-workspace flex-1 grid grid-cols-1 md:grid-cols-12 gap-2 p-2.5 overflow-auto">
        <section className="exam-document-slot md:col-span-4 h-full overflow-hidden">
          <DocumentViewerPane scenarioData={scenarioData} />
        </section>
        <section className="exam-matrix-slot md:col-span-5 h-full overflow-hidden">
          <AdjudicationMatrixPane
            stages={examination.stages}
            isExamining={examination.phase === "streaming"}
            onStartExamination={handleStartExamination}
            selectedLcId={selectedLcId}
          />
        </section>
        <section className="exam-decision-slot md:col-span-3 h-full overflow-hidden">
          <DecisionActionPane
            decision={examination.decision}
            generatedArtifact={examination.generatedArtifact}
            onApproveAction={handleApproveAction}
          />
        </section>
      </main>

      <ZetarisDrawer
        isOpen={sqlDrawerOpen}
        onClose={() => setSqlDrawerOpen(false)}
        telemetryMode={examination.stages[2]?.execution_mode || "LOCAL_DUCKDB_FALLBACK"}
        queryMs={examination.stages[2]?.query_ms || 14}
      />
    </div>
  );
}
