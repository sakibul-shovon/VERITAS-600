import { BankDecision, PipelineStageUpdate } from "@/lib/types";

export type ExaminationPhase = "idle" | "streaming" | "interrupted" | "failed" | "recommended" | "authorized";

export interface ExaminationState {
  phase: ExaminationPhase;
  stages: Record<number, PipelineStageUpdate>;
  decision?: BankDecision;
  generatedArtifact?: string;
  error?: string;
}

export type ExaminationAction =
  | { type: "CASE_SELECTED" }
  | { type: "RUN_STARTED" }
  | { type: "STAGE_RECEIVED"; stage: PipelineStageUpdate }
  | { type: "RECOMMENDATION_RECEIVED"; stage: PipelineStageUpdate; decision: BankDecision; artifact?: string }
  | { type: "STREAM_INTERRUPTED"; message: string }
  | { type: "AUTHORIZED"; decision: BankDecision };

export const initialExaminationState: ExaminationState = { phase: "idle", stages: {} };

export function examinationReducer(state: ExaminationState, action: ExaminationAction): ExaminationState {
  switch (action.type) {
    case "CASE_SELECTED":
    case "RUN_STARTED":
      return { ...initialExaminationState, phase: action.type === "RUN_STARTED" ? "streaming" : "idle" };
    case "STAGE_RECEIVED":
      return { ...state, stages: { ...state.stages, [action.stage.stage]: { ...(state.stages[action.stage.stage] || {}), ...action.stage } } };
    case "RECOMMENDATION_RECEIVED":
      return { ...state, phase: "recommended", stages: { ...state.stages, [action.stage.stage]: { ...(state.stages[action.stage.stage] || {}), ...action.stage } }, decision: action.decision, generatedArtifact: action.artifact };
    case "STREAM_INTERRUPTED":
      return { ...state, phase: "interrupted", error: action.message };
    case "AUTHORIZED":
      return { ...state, phase: "authorized", decision: action.decision, error: undefined };
    default:
      return state;
  }
}
