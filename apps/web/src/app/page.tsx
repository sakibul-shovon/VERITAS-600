"use client";

import React, { useState, useEffect } from "react";
import HeaderBar from "@/components/HeaderBar";
import DocumentViewerPane from "@/components/DocumentViewerPane";
import AdjudicationMatrixPane from "@/components/AdjudicationMatrixPane";
import DecisionActionPane from "@/components/DecisionActionPane";
import ZetarisDrawer from "@/components/ZetarisDrawer";
import { fetchHealth, fetchScenarios, fetchScenarioDetails, openExamineStream, approveHumanAction } from "@/lib/api";
import { LCScenarioSummary, BankDecision, PipelineStageUpdate } from "@/lib/types";

export default function TerminalPage() {
  const [selectedLcId, setSelectedLcId] = useState<string>("LC-2026-8841");
  const [scenarios, setScenarios] = useState<LCScenarioSummary[]>([]);
  const [scenarioData, setScenarioData] = useState<any>(null);
  const [sponsorHealth, setSponsorHealth] = useState<any>(null);

  const [stages, setStages] = useState<Record<number, PipelineStageUpdate>>({});
  const [decision, setDecision] = useState<BankDecision | undefined>(undefined);
  const [generatedArtifact, setGeneratedArtifact] = useState<string | undefined>(undefined);
  const [isExamining, setIsExamining] = useState<boolean>(false);
  const [sqlDrawerOpen, setSqlDrawerOpen] = useState<boolean>(false);

  // Load health & scenarios on mount
  useEffect(() => {
    fetchHealth()
      .then(setSponsorHealth)
      .catch((err) => console.error("Health check error:", err));

    fetchScenarios()
      .then((res) => {
        setScenarios(res.scenarios || []);
      })
      .catch((err) => console.error("Scenarios error:", err));
  }, []);

  // Load active scenario details on switch
  useEffect(() => {
    if (!selectedLcId) return;
    setStages({});
    setDecision(undefined);
    setGeneratedArtifact(undefined);

    fetchScenarioDetails(selectedLcId)
      .then(setScenarioData)
      .catch((err) => console.error("Scenario details error:", err));
  }, [selectedLcId]);

  // Handle Examination Stream
  const handleStartExamination = () => {
    setStages({});
    setDecision(undefined);
    setGeneratedArtifact(undefined);
    setIsExamining(true);

    openExamineStream(
      selectedLcId,
      (event, data) => {
        if (event === "stage_start") {
          setStages((prev) => ({
            ...prev,
            [data.stage]: { stage: data.stage, name: data.name },
          }));
        } else if (event === "stage_complete") {
          setStages((prev) => ({
            ...prev,
            [data.stage]: { ...(prev[data.stage] || {}), ...data },
          }));
        } else if (event === "decision_ready") {
          setStages((prev) => ({
            ...prev,
            [data.stage]: { ...(prev[data.stage] || {}), ...data },
          }));
          setDecision(data.decision);
          setGeneratedArtifact(data.generated_artifact);
          setIsExamining(false);
        }
      },
      (err) => {
        console.error("SSE stream error:", err);
        setIsExamining(false);
      }
    );
  };

  const handleApproveAction = async (examinerName: string, comments: string) => {
    await approveHumanAction(selectedLcId, examinerName, comments);
    if (decision) {
      setDecision({
        ...decision,
        action_status: "APPROVED",
        human_approved_by: examinerName,
        human_approved_at: new Date().toISOString(),
      });
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background text-slate-100 overflow-hidden font-sans">
      {/* Top Header Bar */}
      <HeaderBar
        scenarios={scenarios}
        selectedLcId={selectedLcId}
        onSelectScenario={setSelectedLcId}
        sponsorHealth={sponsorHealth}
        onToggleSqlDrawer={() => setSqlDrawerOpen((o) => !o)}
        sqlDrawerOpen={sqlDrawerOpen}
      />

      {/* 3-Pane Compliance Workbench Layout */}
      <main className="flex-1 grid grid-cols-1 md:grid-cols-12 gap-2 p-2.5 overflow-hidden">
        {/* Left Pane: Document Presentation Viewer (3.5 cols) */}
        <section className="md:col-span-4 h-full overflow-hidden">
          <DocumentViewerPane scenarioData={scenarioData} />
        </section>

        {/* Center Pane: Adjudication Reasoning Matrix (5 cols) */}
        <section className="md:col-span-5 h-full overflow-hidden">
          <AdjudicationMatrixPane
            stages={stages}
            isExamining={isExamining}
            onStartExamination={handleStartExamination}
            selectedLcId={selectedLcId}
          />
        </section>

        {/* Right Pane: Bank Examiner Decision & Action (3 cols) */}
        <section className="md:col-span-3 h-full overflow-hidden">
          <DecisionActionPane
            decision={decision}
            generatedArtifact={generatedArtifact}
            onApproveAction={handleApproveAction}
          />
        </section>
      </main>

      {/* Expandable Zetaris SQL Drawer */}
      <ZetarisDrawer
        isOpen={sqlDrawerOpen}
        onClose={() => setSqlDrawerOpen(false)}
        telemetryMode={stages[2]?.execution_mode || "LOCAL_DUCKDB_FALLBACK"}
        queryMs={stages[2]?.query_ms || 14}
      />
    </div>
  );
}
