export type LCScenarioSummary = {
  lc_id: string;
  beneficiary: string;
  applicant: string;
  amount: number;
  currency: string;
  incoterm: string;
  target_verdict: string;
  primary_citation: string;
  latest_shipment_date: string;
  expiry_date: string;
  case_source?: "SAMPLE_CASE" | "USER_CREATED" | "SAMPLE_CASE_WITH_USER_EVIDENCE";
  evidence_status?: "SAMPLE_READY" | "AWAITING_DOCUMENTS" | "NEEDS_REVIEW" | "OCR_UNAVAILABLE" | "ACCEPTED";
};

export type ExtractedDocumentField = {
  field_key: string;
  value: string | number | boolean | null;
  confidence: number;
  bounding_box: number[];
  source_document: string;
  source_digest_sha256: string;
  page_number?: number;
};

export type EvidenceDocument = {
  document_id: string;
  document_type: string;
  filename: string;
  content_type: string;
  size_bytes: number;
  source_digest_sha256: string;
  uploaded_at: string;
  review_status: "NEEDS_REVIEW" | "OCR_UNAVAILABLE" | "ACCEPTED";
  reviewed_fields?: Record<string, unknown>;
  extraction: {
    document_type: string;
    document_id: string;
    fields: Record<string, ExtractedDocumentField>;
    raw_text: string;
    extraction_mode: "PDF_TEXT_LAYER" | "LIVE_NEMOTRON_VLM" | "CACHED_REPLAY" | "OCR_UNAVAILABLE" | "STRUCTURED_FIXTURE";
    source_digest_sha256: string;
    notice?: string;
  };
};

export type DeterministicCheck = {
  check_id: string;
  name: string;
  ucp_citation: string;
  passed: boolean;
  severity: string;
  details: string;
  computed_values: Record<string, any>;
};

export type LegalFinding = {
  divergence_item: string;
  source_documents: string[];
  verdict: string;
  is_discrepant: boolean;
  ucp_isbp_citation: string;
  legal_reasoning: string;
  confidence: number;
};

export type BankDecision = {
  lc_id: string;
  recommended_action: "APPROVE_HONOUR" | "ISSUE_MT734_REFUSAL" | "COMPLIANCE_HOLD_AML";
  action_title: string;
  action_summary: string;
  action_status: string;
  legal_citations: string[];
  discrepancies: string[];
  regulatory_flags: string[];
  demurrage_savings_advisory?: {
    days_remaining_in_window: number;
    daily_demurrage_usd: number;
    applicant_waiver_days: number;
    waiver_demurrage_cost: number;
    cured_re_presentation_days: number;
    cured_demurrage_cost: number;
    net_savings_usd: number;
    advisory: string;
  };
  execution_telemetry: {
    zetaris_mode: string;
    zetaris_query_ms: number;
    deterministic_passed: boolean;
    neural_status: string;
    hard_invariant_enforced: boolean;
    timestamp: string;
  };
  human_approved_by?: string;
  human_approved_at?: string;
};

export type PipelineStageUpdate = {
  stage: number;
  name?: string;
  active_terms?: Record<string, any>;
  active_terms_sha256?: string;
  quarantined_count?: number;
  token_savings_pct?: number;
  raw_prompt_tokens_est?: number;
  routed_tokens_actual?: number;
  tokens_saved?: number;
  routing_mode?: string;
  execution_mode?: string;
  query_ms?: number;
  tbml_price_zscore?: number;
  sanction_hit_count?: number;
  sanctions_summary?: string;
  all_passed?: boolean;
  failed_count?: number;
  checks?: DeterministicCheck[];
  overall_legal_status?: string;
  final_locked_verdict?: string;
  hard_invariant_enforced?: boolean;
  findings?: LegalFinding[];
  extracted_fields_count?: number;
  extraction_modes?: string[];
  decision?: BankDecision;
  generated_artifact?: string;
  run_id?: string;
  decision_sha256?: string;
  merkle_root_sha256?: string;
  duration_ms?: number;
  stage_duration_ms?: number;
  started_at?: string;
  completed_at?: string;
};
