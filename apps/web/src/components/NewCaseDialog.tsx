"use client";

import React, { FormEvent, useEffect, useRef, useState } from "react";
import { FilePlus2, Loader2, X } from "lucide-react";
import { createExaminationCase } from "@/lib/api";

type NewCaseDialogProps = {
  open: boolean;
  onClose: () => void;
  onCreated: (caseData: any) => void;
};

const INITIAL_FORM = {
  lc_id: "",
  applicant_name: "",
  applicant_address_strict: "",
  beneficiary_name: "",
  issuing_bank: "",
  currency: "USD",
  amount: "",
  tolerance_pct: "0",
  incoterm: "CIF",
  hs_code_6: "",
  goods_description_strict: "",
  unit_price: "",
  quantity: "",
  port_of_loading: "",
  port_of_discharge: "",
  latest_shipment_date: "",
  expiry_date: "",
  presentation_period_days: "21",
  daily_demurrage_usd: "0",
};

export default function NewCaseDialog({ open, onClose, onCreated }: NewCaseDialogProps) {
  const [form, setForm] = useState(INITIAL_FORM);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!open) return;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    window.setTimeout(() => closeRef.current?.focus(), 0);
    const onKeyDown = (event: KeyboardEvent) => { if (event.key === "Escape" && !busy) onClose(); };
    window.addEventListener("keydown", onKeyDown);
    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [open, busy, onClose]);

  if (!open) return null;

  const update = (key: keyof typeof INITIAL_FORM, value: string) => setForm((current) => ({ ...current, [key]: value }));

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const result = await createExaminationCase({
        ...form,
        lc_id: form.lc_id.trim().toUpperCase(),
        amount: Number(form.amount),
        tolerance_pct: Number(form.tolerance_pct),
        unit_price: Number(form.unit_price),
        quantity: Number(form.quantity),
        presentation_period_days: Number(form.presentation_period_days),
        daily_demurrage_usd: Number(form.daily_demurrage_usd),
      });
      setForm(INITIAL_FORM);
      onCreated(result);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Case creation failed.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="case-dialog-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget && !busy) onClose(); }}>
      <section className="case-dialog" role="dialog" aria-modal="true" aria-labelledby="new-case-title">
        <header>
          <div><span>NEW EXAMINATION</span><h2 id="new-case-title">Create a real case workspace</h2><p>Enter the credit baseline first. Documents and extracted presentation fields are added next.</p></div>
          <button ref={closeRef} type="button" onClick={onClose} disabled={busy} aria-label="Close new case dialog"><X /></button>
        </header>
        <form onSubmit={submit}>
          <div className="case-form-grid">
            <label><span>LC / case ID</span><input required pattern="[A-Za-z0-9-]{3,32}" value={form.lc_id} onChange={(e) => update("lc_id", e.target.value)} placeholder="LC-2026-10001" /></label>
            <label><span>Issuing bank</span><input value={form.issuing_bank} onChange={(e) => update("issuing_bank", e.target.value)} placeholder="Bank name" /></label>
            <label><span>Applicant</span><input required value={form.applicant_name} onChange={(e) => update("applicant_name", e.target.value)} /></label>
            <label><span>Beneficiary</span><input required value={form.beneficiary_name} onChange={(e) => update("beneficiary_name", e.target.value)} /></label>
            <label className="case-form-span"><span>Applicant address — strict transport-document reference</span><input required value={form.applicant_address_strict} onChange={(e) => update("applicant_address_strict", e.target.value)} /></label>
            <label><span>Currency</span><input required maxLength={3} value={form.currency} onChange={(e) => update("currency", e.target.value.toUpperCase())} /></label>
            <label><span>Credit amount</span><input required type="number" min="0.01" step="0.01" value={form.amount} onChange={(e) => update("amount", e.target.value)} /></label>
            <label><span>Quantity</span><input required type="number" min="1" value={form.quantity} onChange={(e) => update("quantity", e.target.value)} /></label>
            <label><span>Unit price</span><input required type="number" min="0.01" step="0.01" value={form.unit_price} onChange={(e) => update("unit_price", e.target.value)} /></label>
            <label><span>Incoterm</span><select value={form.incoterm} onChange={(e) => update("incoterm", e.target.value)}><option>CIF</option><option>CIP</option><option>FOB</option><option>CFR</option><option>EXW</option></select></label>
            <label><span>HS code (6 digit)</span><input required value={form.hs_code_6} onChange={(e) => update("hs_code_6", e.target.value)} placeholder="848180" /></label>
            <label className="case-form-span"><span>Strict goods description</span><textarea required rows={3} value={form.goods_description_strict} onChange={(e) => update("goods_description_strict", e.target.value)} /></label>
            <label><span>Port of loading</span><input required value={form.port_of_loading} onChange={(e) => update("port_of_loading", e.target.value)} /></label>
            <label><span>Port of discharge</span><input required value={form.port_of_discharge} onChange={(e) => update("port_of_discharge", e.target.value)} /></label>
            <label><span>Latest shipment date</span><input required type="date" value={form.latest_shipment_date} onChange={(e) => update("latest_shipment_date", e.target.value)} /></label>
            <label><span>Credit expiry date</span><input required type="date" value={form.expiry_date} onChange={(e) => update("expiry_date", e.target.value)} /></label>
          </div>
          {error && <p className="case-dialog-error" role="alert">{error}</p>}
          <footer>
            <p><b>Next:</b> upload documents, review extraction, then unlock the audit.</p>
            <div><button type="button" onClick={onClose} disabled={busy}>Cancel</button><button type="submit" disabled={busy}>{busy ? <Loader2 className="spin" /> : <FilePlus2 />} Create case & add documents</button></div>
          </footer>
        </form>
      </section>
    </div>
  );
}
