"use client";

import React, { useEffect, useReducer, useRef, useState } from "react";
import HeaderBar from "@/components/HeaderBar";
import MissionControl from "@/components/MissionControl";
import ZetarisDrawer from "@/components/ZetarisDrawer";
import NoticeRegion from "@/components/ui/NoticeRegion";
import { fetchHealth, fetchScenarios, fetchScenarioDetails, openExamineStream, approveHumanAction } from "@/lib/api";
import { LCScenarioSummary } from "@/lib/types";
import { examinationReducer, initialExaminationState } from "@/lib/examination-reducer";

const KNOWN_CASES = new Set(["LC-2026-8841", "LC-2026-9104", "LC-2026-9920"]);

export default function ExaminationPage() {
  const [selectedLcId, setSelectedLcId] = useState<string>("LC-2026-8841");
  const [scenarios, setScenarios] = useState<LCScenarioSummary[]>([]);
  const [scenarioData, setScenarioData] = useState<any>(null);
  const [sponsorHealth, setSponsorHealth] = useState<any>(null);
  const [loadNotice, setLoadNotice] = useState<string | undefined>(undefined);
  const [approvalReceipt, setApprovalReceipt] = useState<any>(null);

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
    }).catch((err) => {
      console.error("Scenarios error:", err);
      setLoadNotice("Case discovery is unavailable. Please retry when the API is running.");
    });
  }, []);

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
    const res = await approveHumanAction(selectedLcId, examinerName, comments);
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

  return (
    <div className={`exam-shell ${examination.phase === "streaming" ? "audit-active" : ""} flex flex-col min-h-[100dvh] bg-background font-sans`}>
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

      <MissionControl
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
      />

      <ZetarisDrawer
        isOpen={sqlDrawerOpen}
        onClose={() => setSqlDrawerOpen(false)}
        telemetryMode={examination.stages[2]?.execution_mode || "LOCAL_DUCKDB_FALLBACK"}
        queryMs={examination.stages[2]?.query_ms || 14}
      />
    </div>
  );
}
