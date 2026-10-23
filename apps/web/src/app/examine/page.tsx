"use client";

import React, { useEffect, useReducer, useRef, useState } from "react";
import { ArrowRight, FilePlus2, FlaskConical, ShieldCheck } from "lucide-react";
import HeaderBar from "@/components/HeaderBar";
import MissionControl from "@/components/MissionControl";
import ZetarisDrawer from "@/components/ZetarisDrawer";
import NoticeRegion from "@/components/ui/NoticeRegion";
import NewCaseDialog from "@/components/NewCaseDialog";
import { fetchHealth, fetchScenarios, fetchScenarioDetails, openExamineStream, approveHumanAction } from "@/lib/api";
import { LCScenarioSummary } from "@/lib/types";
import { examinationReducer, initialExaminationState } from "@/lib/examination-reducer";

export default function ExaminationPage() {
  const [selectedLcId, setSelectedLcId] = useState<string>("");
  const [scenarios, setScenarios] = useState<LCScenarioSummary[]>([]);
  const [scenarioData, setScenarioData] = useState<any>(null);
  const [sponsorHealth, setSponsorHealth] = useState<any>(null);
  const [loadNotice, setLoadNotice] = useState<string | undefined>(undefined);
  const [approvalReceipt, setApprovalReceipt] = useState<any>(null);
  const [darkMode, setDarkMode] = useState(false);
  const [newCaseOpen, setNewCaseOpen] = useState(false);
  const [openEvidenceSignal, setOpenEvidenceSignal] = useState(0);

  const [examination, dispatch] = useReducer(examinationReducer, initialExaminationState);
  const [sqlDrawerOpen, setSqlDrawerOpen] = useState<boolean>(false);
  const streamRef = useRef<EventSource | null>(null);
  const runTokenRef = useRef(0);
  const effectiveEvidenceStatus = scenarioData?.evidence_status || (scenarioData && !scenarioData.case_source ? "SAMPLE_READY" : undefined);

  useEffect(() => {
    const requestedCase = new URLSearchParams(window.location.search).get("case");
    if (requestedCase && /^[A-Z0-9-]{3,32}$/i.test(requestedCase)) setSelectedLcId(requestedCase.toUpperCase());
    const storedTheme = window.localStorage.getItem("veritas-examine-theme");
    setDarkMode(storedTheme === "dark");

    fetchHealth().then(setSponsorHealth).catch((err) => console.error("Health check error:", err));
    fetchScenarios().then((res) => {
      const availableScenarios = res.scenarios || [];
      setScenarios(availableScenarios);
      if (availableScenarios.length === 0) setLoadNotice("No examination cases are currently available from the API.");
    }).catch((err) => {
      console.error("Scenarios error:", err);
      setLoadNotice("Case discovery is unavailable. Please retry when the API is running.");
    });
  }, []);

  const toggleTheme = () => setDarkMode((current) => {
    const next = !current;
    window.localStorage.setItem("veritas-examine-theme", next ? "dark" : "light");
    return next;
  });

  useEffect(() => () => streamRef.current?.close(), []);

  useEffect(() => {
    if (!selectedLcId) return;
    runTokenRef.current += 1;
    streamRef.current?.close();
    dispatch({ type: "CASE_SELECTED" });
    setApprovalReceipt(null);
    setScenarioData(null);
    fetchScenarioDetails(selectedLcId).then((data) => {
      setScenarioData(data);
      setLoadNotice(undefined);
    }).catch((err) => {
      console.error("Scenario details error:", err);
      setLoadNotice("The selected case could not be loaded. You can choose another available case or retry shortly.");
    });
  }, [selectedLcId]);

  const handleStartExamination = () => {
    const evidenceStatus = scenarioData?.evidence_status || "SAMPLE_READY";
    if (!["SAMPLE_READY", "ACCEPTED"].includes(evidenceStatus)) {
      setLoadNotice("Review and accept the uploaded evidence before starting the examination.");
      setOpenEvidenceSignal((value) => value + 1);
      return;
    }
    streamRef.current?.close();
    const token = ++runTokenRef.current;
    const caseAtStart = selectedLcId;
    setApprovalReceipt(null);
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
        if (token === runTokenRef.current) {
          dispatch({ type: "STREAM_INTERRUPTED", message: "The examination stream was interrupted. Completed evidence remains visible; you may run the case again." });
        }
      }
    );
  };

  const handleApproveAction = async (examinerName: string, comments: string) => {
    const finalStage = examination.stages[5];
    if (!finalStage?.run_id || !finalStage?.decision_sha256 || !examination.decision) {
      throw new Error("The signed run identity is unavailable. Run the examination again before authorizing.");
    }
    const res = await approveHumanAction(
      selectedLcId,
      examinerName,
      comments,
      finalStage.run_id,
      finalStage.decision_sha256,
      examination.decision.recommended_action,
    );
    setApprovalReceipt(res);
    if (examination.decision) {
      dispatch({
        type: "AUTHORIZED",
        decision: {
          ...examination.decision,
          action_status: "APPROVED",
          human_approved_by: examinerName,
          human_approved_at: res.human_approved_at || new Date().toISOString(),
        },
      });
    }
    return res;
  };

  const handleCaseCreated = async (caseData: any) => {
    const lcId = caseData.master.lc_id;
    setNewCaseOpen(false);
    setSelectedLcId(lcId);
    setScenarioData(caseData);
    setOpenEvidenceSignal((value) => value + 1);
    try {
      const result = await fetchScenarios();
      setScenarios(result.scenarios || []);
    } catch {
      setLoadNotice("The case was created, but the case list could not be refreshed.");
    }
  };

  const handleEvidenceAccepted = (updated: any) => {
    setScenarioData((current: any) => current ? {
      ...current,
      presentation: updated.presentation,
      evidence_status: updated.evidence_status,
      evidence_version: updated.evidence_version,
      evidence_documents: updated.documents,
    } : current);
    setLoadNotice(undefined);
  };

  return (
    <div className={`exam-shell ${darkMode ? "exam-dark" : ""} ${examination.phase === "streaming" ? "audit-active" : ""} flex flex-col min-h-[100dvh] bg-background font-sans`}>
      <HeaderBar
        scenarios={scenarios}
        selectedLcId={selectedLcId}
        onSelectScenario={setSelectedLcId}
        sponsorHealth={sponsorHealth}
        onToggleSqlDrawer={() => setSqlDrawerOpen((open) => !open)}
        sqlDrawerOpen={sqlDrawerOpen}
        darkMode={darkMode}
        onToggleTheme={toggleTheme}
        onNewCase={() => setNewCaseOpen(true)}
      />

      <div className="exam-context-strip" aria-live="polite">
        <span>{selectedLcId ? "ACTIVE PRESENTATION" : "NEW EXAMINATION"}</span>
        <strong>{selectedLcId || "NO CASE SELECTED"}</strong>
        <i />
        <span>{scenarioData?.master?.applicant_name || "Loading applicant evidence"}</span>
        <i />
        <span>{scenarioData?.master?.beneficiary_name || "Preparing document set"}</span>
        <b>{!selectedLcId ? "CREATE OR OPEN A CASE" : examination.phase === "streaming" ? "AUDIT STREAM ACTIVE" : examination.phase === "recommended" ? "RECOMMENDATION READY" : examination.phase === "authorized" ? "ACTION AUTHORIZED" : "READY FOR EXAMINATION"}</b>
      </div>
      <NoticeRegion message={examination.error || loadNotice} />

      {!selectedLcId ? (
        <main className="case-start-screen" id="main-content">
          <section className="case-start-hero">
            <span>EXAMINER-GUIDED WORKFLOW</span>
            <h1>Start with your case.<br /><em>Not a pre-filled demo.</em></h1>
            <p>Create an LC baseline, upload the actual PDF or image evidence, verify every extracted value, then run the bounded five-stage examination.</p>
            <button type="button" onClick={() => setNewCaseOpen(true)}><FilePlus2 /> Create a new examination <ArrowRight /></button>
          </section>
          <section className="case-start-paths" aria-label="Available ways to begin">
            <article><ShieldCheck /><div><small>PRODUCTION PATH</small><h2>Use your own documents</h2><p>No sample evidence is substituted. Text PDFs are parsed directly; scans and images use configured vision OCR. You approve extracted values before calculations can run.</p></div></article>
            <article><FlaskConical /><div><small>OPTIONAL SANDBOX</small><h2>Explore a labelled sample</h2><p>Choose a SAMPLE case from the header only when you want to inspect the workflow without uploading documents.</p>{scenarios.length > 0 && <button type="button" onClick={() => setSelectedLcId(scenarios.find((item) => item.case_source === "SAMPLE_CASE")?.lc_id || scenarios[0].lc_id)}>Open a sample case <ArrowRight /></button>}</div></article>
          </section>
        </main>
      ) : <MissionControl
        selectedLcId={selectedLcId}
        scenarioData={scenarioData}
        stages={examination.stages}
        phase={examination.phase}
        decision={examination.decision}
        generatedArtifact={examination.generatedArtifact}
        approvalReceipt={approvalReceipt}
        onStartExamination={handleStartExamination}
        onApproveAction={handleApproveAction}
        onOpenFederationProof={() => setSqlDrawerOpen(true)}
        onEvidenceAccepted={handleEvidenceAccepted}
        canRun={Boolean(effectiveEvidenceStatus && ["SAMPLE_READY", "ACCEPTED"].includes(effectiveEvidenceStatus))}
        openEvidenceSignal={openEvidenceSignal}
      />}

      <ZetarisDrawer
        isOpen={sqlDrawerOpen}
        onClose={() => setSqlDrawerOpen(false)}
        telemetryMode={examination.stages[2]?.execution_mode || "LOCAL_DUCKDB_FALLBACK"}
        queryMs={examination.stages[2]?.query_ms || 14}
      />
      <NewCaseDialog open={newCaseOpen} onClose={() => setNewCaseOpen(false)} onCreated={handleCaseCreated} />
    </div>
  );
}
