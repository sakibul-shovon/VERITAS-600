"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";
import { AlertTriangle, CheckCircle2, Eye, FileUp, Image as ImageIcon, Loader2, ScanLine, ShieldCheck } from "lucide-react";
import { acceptCaseEvidence, caseDocumentUrl, uploadCaseDocument } from "@/lib/api";
import { EvidenceDocument } from "@/lib/types";

type EvidenceIntakeProps = {
  lcId: string;
  scenarioData: any;
  onEvidenceAccepted: (updated: any) => void;
};

const DOCUMENT_OPTIONS = [
  ["commercial_invoice", "Commercial invoice"],
  ["bill_of_lading", "Ocean bill of lading"],
  ["packing_list", "Packing list"],
  ["insurance", "Insurance certificate / policy"],
] as const;

function fieldValue(document: EvidenceDocument, key: string) {
  const reviewed = document.reviewed_fields?.[key];
  if (reviewed !== undefined) return reviewed;
  return document.extraction.fields[key]?.value ?? "";
}

export default function EvidenceIntake({ lcId, scenarioData, onEvidenceAccepted }: EvidenceIntakeProps) {
  const [documentType, setDocumentType] = useState("commercial_invoice");
  const [file, setFile] = useState<File | null>(null);
  const [documents, setDocuments] = useState<EvidenceDocument[]>(scenarioData?.evidence_documents || []);
  const [selectedDocumentId, setSelectedDocumentId] = useState<string | null>(documents[0]?.document_id || null);
  const [drafts, setDrafts] = useState<Record<string, Record<string, unknown>>>({});
  const [busy, setBusy] = useState<"upload" | "accept" | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const nextDocuments: EvidenceDocument[] = scenarioData?.evidence_documents || [];
    setDocuments(nextDocuments);
    setSelectedDocumentId((current) => current && nextDocuments.some((doc) => doc.document_id === current) ? current : nextDocuments[0]?.document_id || null);
    const nextDrafts: Record<string, Record<string, unknown>> = {};
    nextDocuments.forEach((document) => {
      nextDrafts[document.document_id] = Object.fromEntries(
        Object.keys(document.extraction?.fields || {}).map((key) => [key, fieldValue(document, key)]),
      );
    });
    setDrafts(nextDrafts);
  }, [scenarioData]);

  const selectedDocument = useMemo(
    () => documents.find((document) => document.document_id === selectedDocumentId) || null,
    [documents, selectedDocumentId],
  );
  const reviewable = documents.filter((document) => Object.keys(document.extraction?.fields || {}).length > 0);
  const evidenceStatus = scenarioData?.evidence_status || "SAMPLE_READY";
  const isSample = String(scenarioData?.case_source || "SAMPLE_CASE").startsWith("SAMPLE_CASE");

  const handleUpload = async () => {
    if (!file) {
      setNotice("Choose a PDF, PNG, JPEG, or WebP document first.");
      inputRef.current?.focus();
      return;
    }
    setBusy("upload");
    setNotice(null);
    try {
      const response = await uploadCaseDocument(lcId, documentType, file);
      const record: EvidenceDocument = response.document;
      const next = [...documents.filter((document) => document.document_type !== record.document_type), record];
      setDocuments(next);
      setSelectedDocumentId(record.document_id);
      setDrafts((current) => ({
        ...current,
        [record.document_id]: Object.fromEntries(
          Object.entries(record.extraction.fields || {}).map(([key, field]) => [key, field.value]),
        ),
      }));
      setFile(null);
      if (inputRef.current) inputRef.current.value = "";
      setNotice(record.extraction.notice || "Document uploaded. Review every extracted field before accepting it.");
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Document upload failed.");
    } finally {
      setBusy(null);
    }
  };

  const handleAccept = async () => {
    if (!reviewable.length) {
      setNotice("No extracted fields are available to accept. Check the OCR mode and document quality.");
      return;
    }
    setBusy("accept");
    setNotice(null);
    try {
      const response = await acceptCaseEvidence(
        lcId,
        reviewable.map((document) => ({ document_id: document.document_id, fields: drafts[document.document_id] || {} })),
      );
      onEvidenceAccepted(response);
      setDocuments(response.documents || []);
      setNotice(response.evidence_status === "ACCEPTED"
        ? `Evidence version ${response.evidence_version} accepted. The examination can now use this reviewed snapshot.`
        : `Reviewed fields were saved. Still required: ${(response.missing_document_types || []).map((value: string) => value.replaceAll("_", " ")).join(", ")}.`);
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Evidence acceptance failed.");
    } finally {
      setBusy(null);
    }
  };

  return (
    <section className="evidence-intake" aria-labelledby="evidence-intake-title">
      <div className="evidence-intake-head">
        <div>
          <span>REAL DOCUMENT INTAKE</span>
          <h3 id="evidence-intake-title">Upload, extract, then verify.</h3>
          <p>{isSample ? "This is a labelled sample case. Uploading a real document creates a reviewed evidence overlay without altering the golden source file." : "This user-created case stays locked until extracted evidence is reviewed and accepted. Confidence below is extraction certainty—not a compliance verdict."}</p>
        </div>
        <div className={`evidence-status status-${evidenceStatus.toLowerCase()}`}>
          {evidenceStatus === "ACCEPTED" || evidenceStatus === "SAMPLE_READY" ? <CheckCircle2 /> : <AlertTriangle />}
          <span><small>EVIDENCE GATE</small><b>{evidenceStatus.replaceAll("_", " ")}</b></span>
        </div>
      </div>

      <div className="evidence-upload-row">
        <label>
          <span>Document type</span>
          <select value={documentType} onChange={(event) => setDocumentType(event.target.value)}>
            {DOCUMENT_OPTIONS.map(([value, label]) => <option value={value} key={value}>{label}</option>)}
          </select>
        </label>
        <label className="evidence-file-control">
          <span>PDF or image · maximum 12 MB</span>
          <input ref={inputRef} type="file" accept="application/pdf,image/png,image/jpeg,image/webp" onChange={(event) => setFile(event.target.files?.[0] || null)} />
        </label>
        <button type="button" onClick={handleUpload} disabled={busy !== null} className="evidence-upload-button">
          {busy === "upload" ? <Loader2 className="spin" /> : <FileUp />}
          <span><small>{file ? file.name : "NO FILE SELECTED"}</small><b>{busy === "upload" ? "Extracting document…" : "Upload & extract"}</b></span>
        </button>
      </div>

      {notice && <p className="evidence-intake-notice" role="status">{notice}</p>}

      {documents.length > 0 && (
        <div className="evidence-review-layout">
          <nav className="evidence-document-list" aria-label="Uploaded evidence documents">
            {documents.map((document) => (
              <button type="button" key={document.document_id} className={selectedDocumentId === document.document_id ? "active" : ""} onClick={() => setSelectedDocumentId(document.document_id)}>
                {document.content_type.startsWith("image/") ? <ImageIcon /> : <ScanLine />}
                <span><b>{document.filename}</b><small>{document.extraction.extraction_mode.replaceAll("_", " ")} · {document.review_status.replaceAll("_", " ")}</small></span>
                <Eye />
              </button>
            ))}
          </nav>

          {selectedDocument && (
            <div className="evidence-review-card">
              <div className="evidence-source-preview">
                {selectedDocument.content_type.startsWith("image/") ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={caseDocumentUrl(lcId, selectedDocument.document_id)} alt={`Uploaded ${selectedDocument.filename}`} />
                ) : (
                  <iframe src={caseDocumentUrl(lcId, selectedDocument.document_id)} title={`Uploaded ${selectedDocument.filename}`} />
                )}
              </div>
              <div className="evidence-field-review">
                <div className="evidence-field-review-head">
                  <div><span>EXTRACTION MODE</span><b>{selectedDocument.extraction.extraction_mode.replaceAll("_", " ")}</b></div>
                  <code title={selectedDocument.source_digest_sha256}>sha256:{selectedDocument.source_digest_sha256.slice(0, 14)}…</code>
                </div>
                {Object.entries(selectedDocument.extraction.fields || {}).length ? Object.entries(selectedDocument.extraction.fields).map(([key, field]) => (
                  <label key={key} className="evidence-field-input">
                    <span><b>{key.replaceAll("_", " ")}</b><small title="How certain the extractor is that this value was read correctly; it does not indicate UCP compliance.">Page {field.page_number || 1} · {Math.round(field.confidence * 100)}% extraction confidence</small></span>
                    <input
                      value={String(drafts[selectedDocument.document_id]?.[key] ?? "")}
                      onChange={(event) => setDrafts((current) => ({
                        ...current,
                        [selectedDocument.document_id]: { ...(current[selectedDocument.document_id] || {}), [key]: event.target.value },
                      }))}
                      aria-label={`Reviewed value for ${key.replaceAll("_", " ")}`}
                    />
                    <em title="Normalized coordinates">[{field.bounding_box.join(", ")}]</em>
                  </label>
                )) : (
                  <div className="evidence-ocr-unavailable"><AlertTriangle /><b>No trusted fields were extracted.</b><p>{selectedDocument.extraction.notice || "Configure live vision OCR or provide a text-based PDF."}</p></div>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {reviewable.length > 0 && (
        <button type="button" className="evidence-accept-button" onClick={handleAccept} disabled={busy !== null}>
          {busy === "accept" ? <Loader2 className="spin" /> : <ShieldCheck />}
          <span><small>HUMAN REVIEW GATE</small><b>{busy === "accept" ? "Sealing reviewed evidence…" : "Accept reviewed evidence snapshot"}</b></span>
        </button>
      )}
    </section>
  );
}
