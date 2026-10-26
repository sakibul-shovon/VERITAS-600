const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL !== undefined
    ? process.env.NEXT_PUBLIC_API_URL
    : "http://localhost:8000";

async function readApiError(res: Response, fallback: string) {
  try {
    const body = await res.json();
    return body.detail || body.message || fallback;
  } catch {
    return fallback;
  }
}

export async function fetchHealth() {
  const res = await fetch(`${API_BASE_URL}/api/v1/health`);
  if (!res.ok) throw new Error("Failed to fetch API health");
  return res.json();
}

export async function fetchScenarios() {
  const res = await fetch(`${API_BASE_URL}/api/v1/scenarios`);
  if (!res.ok) throw new Error("Failed to fetch scenarios");
  return res.json();
}

export async function fetchScenarioDetails(lcId: string) {
  const res = await fetch(`${API_BASE_URL}/api/v1/scenarios/${lcId}`);
  if (!res.ok) throw new Error(`Failed to fetch scenario details for ${lcId}`);
  return res.json();
}

export async function extractDocuments(lcId: string) {
  const res = await fetch(`${API_BASE_URL}/api/v1/extract/${lcId}`, {
    method: "POST",
  });
  if (!res.ok) throw new Error(`Failed to extract documents for ${lcId}`);
  return res.json();
}

export async function createExaminationCase(payload: Record<string, unknown>) {
  const res = await fetch(`${API_BASE_URL}/api/v1/cases`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await readApiError(res, "Failed to create examination case"));
  return res.json();
}

export async function uploadCaseDocument(lcId: string, documentType: string, file: File) {
  const body = new FormData();
  body.append("document_type", documentType);
  body.append("file", file);
  const res = await fetch(`${API_BASE_URL}/api/v1/cases/${encodeURIComponent(lcId)}/documents`, {
    method: "POST",
    body,
  });
  if (!res.ok) throw new Error(await readApiError(res, "Document upload or extraction failed"));
  return res.json();
}

export async function acceptCaseEvidence(
  lcId: string,
  documents: Array<{ document_id: string; fields: Record<string, unknown> }>,
) {
  const res = await fetch(`${API_BASE_URL}/api/v1/cases/${encodeURIComponent(lcId)}/evidence/accept`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ documents }),
  });
  if (!res.ok) throw new Error(await readApiError(res, "Evidence review could not be accepted"));
  return res.json();
}

export function caseDocumentUrl(lcId: string, documentId: string) {
  return `${API_BASE_URL}/api/v1/cases/${encodeURIComponent(lcId)}/documents/${encodeURIComponent(documentId)}/content`;
}

export async function approveHumanAction(
  lcId: string,
  examinerName: string,
  comments: string,
  runId: string,
  decisionSha256: string,
  expectedAction: string,
) {
  const res = await fetch(`${API_BASE_URL}/api/v1/examine/${lcId}/approve-action`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      examiner_name: examinerName,
      comments,
      run_id: runId,
      decision_sha256: decisionSha256,
      expected_action: expectedAction,
    }),
  });
  if (!res.ok) throw new Error(await readApiError(res, "Failed to submit human examiner approval"));
  return res.json();
}

export function openExamineStream(
  lcId: string,
  onEvent: (event: string, data: any) => void,
  onError?: (err: any) => void
): EventSource {
  const es = new EventSource(`${API_BASE_URL}/api/v1/examine/${lcId}?stream=true`);

  es.addEventListener("stage_start", (e) => {
    try {
      onEvent("stage_start", JSON.parse(e.data));
    } catch (err) {
      console.error("Parse error on stage_start", err);
    }
  });

  es.addEventListener("stage_complete", (e) => {
    try {
      onEvent("stage_complete", JSON.parse(e.data));
    } catch (err) {
      console.error("Parse error on stage_complete", err);
    }
  });

  es.addEventListener("decision_ready", (e) => {
    try {
      onEvent("decision_ready", JSON.parse(e.data));
      es.close();
    } catch (err) {
      console.error("Parse error on decision_ready", err);
    }
  });

  es.onerror = (err) => {
    if (onError) onError(err);
    es.close();
  };

  return es;
}

export async function fetchEvalsResults() {
  const res = await fetch(`${API_BASE_URL}/api/v1/evals/results`);
  if (!res.ok) throw new Error("Failed to fetch evaluation benchmark results");
  return res.json();
}

export async function runEvalsBenchmark() {
  const res = await fetch(`${API_BASE_URL}/api/v1/evals/run`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to run evaluation benchmark");
  return res.json();
}
