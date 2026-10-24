"""File-backed case and document intake storage for the local examination runtime.

Seeded golden scenarios remain immutable. User-created cases and evidence overlays are
stored below ``data/runtime_cases`` so a backend restart does not discard examiner work.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import threading
from collections.abc import Iterable
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

CASE_ID_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9-]{2,31}$")
DOCUMENT_TYPES = {
    "commercial_invoice",
    "bill_of_lading",
    "packing_list",
    "insurance",
    "other",
}

NUMERIC_PRESENTATION_FIELDS = {
    "invoice_amount",
    "invoice_unit_price",
    "packing_gross_weight_kg",
    "bl_gross_weight_kg",
    "insurance_amount",
}

FIELD_TO_PRESENTATION = {
    "commercial_invoice": {
        "invoice_no": "invoice_no",
        "invoice_date": "invoice_date",
        "goods_description": "invoice_goods_description",
        "unit_price": "invoice_unit_price",
        "invoice_unit_price": "invoice_unit_price",
        "total_amount": "invoice_amount",
        "invoice_amount": "invoice_amount",
    },
    "bill_of_lading": {
        "bl_no": "bl_no",
        "vessel": "bl_vessel",
        "goods_description": "bl_goods_description",
        "on_board_date": "bl_on_board_date",
        "gross_weight": "bl_gross_weight_kg",
        "notify_party": "bl_notify_party",
    },
    "packing_list": {"packing_gross_weight": "packing_gross_weight_kg"},
    "insurance": {
        "insurance_doc_type": "insurance_doc_type",
        "insurance_amount": "insurance_amount",
        "effective_date": "insurance_effective_date",
    },
}


class CaseStore:
    """Small, deterministic local store used by the API and replaceable by PostgreSQL."""

    def __init__(self, seed_dir: Path, runtime_dir: Path):
        self.seed_dir = Path(seed_dir)
        self.runtime_dir = Path(runtime_dir)
        self._lock = threading.Lock()

    @staticmethod
    def validate_case_id(lc_id: str) -> str:
        normalized = lc_id.strip().upper()
        if not CASE_ID_PATTERN.fullmatch(normalized):
            raise ValueError("Case ID must contain 3-32 uppercase letters, numbers, or hyphens.")
        return normalized

    def _case_dir(self, lc_id: str) -> Path:
        return self.runtime_dir / self.validate_case_id(lc_id)

    def _runtime_case_path(self, lc_id: str) -> Path:
        return self._case_dir(lc_id) / "case.json"

    def _seed_path(self, lc_id: str) -> Path:
        return self.seed_dir / f"{self.validate_case_id(lc_id)}.json"

    def exists(self, lc_id: str) -> bool:
        return self._runtime_case_path(lc_id).exists() or self._seed_path(lc_id).exists()

    def list_case_ids(self) -> list[str]:
        ids = {path.stem for path in self.seed_dir.glob("LC-*.json")}
        if self.runtime_dir.exists():
            ids.update(path.parent.name for path in self.runtime_dir.glob("*/case.json"))
        return sorted(ids)

    def load(self, lc_id: str) -> dict[str, Any]:
        runtime_path = self._runtime_case_path(lc_id)
        source = runtime_path if runtime_path.exists() else self._seed_path(lc_id)
        if not source.exists():
            raise FileNotFoundError(lc_id)
        with source.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        data.setdefault("case_source", "USER_CREATED" if source == runtime_path else "SAMPLE_CASE")
        data.setdefault("evidence_status", "SAMPLE_READY" if source != runtime_path else "AWAITING_DOCUMENTS")
        data.setdefault("evidence_documents", [])
        return data

    def _write_case(self, lc_id: str, data: dict[str, Any]) -> None:
        case_dir = self._case_dir(lc_id)
        case_dir.mkdir(parents=True, exist_ok=True)
        target = case_dir / "case.json"
        temporary = target.with_suffix(".tmp")
        temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        temporary.replace(target)

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        lc_id = self.validate_case_id(str(payload["lc_id"]))
        if self.exists(lc_id):
            raise FileExistsError(lc_id)

        quantity = int(payload["quantity"])
        amount = float(payload["amount"])
        unit_price = float(payload.get("unit_price") or (amount / quantity if quantity else 0))
        master = {
            "lc_id": lc_id,
            "swift_mt700_raw": payload.get("swift_mt700_raw") or f":20:{lc_id}\n:32B:{payload['currency']}{amount:.2f}",
            "issuing_bank": payload.get("issuing_bank") or "User supplied issuing bank",
            "applicant_name": payload["applicant_name"],
            "applicant_address_strict": payload["applicant_address_strict"],
            "beneficiary_name": payload["beneficiary_name"],
            "currency": payload["currency"],
            "amount": amount,
            "credit_amount": amount,
            "tolerance_pct": float(payload.get("tolerance_pct", 0)),
            "incoterm": payload["incoterm"],
            "hs_code_6": payload["hs_code_6"],
            "goods_description_strict": payload["goods_description_strict"],
            "unit_price": unit_price,
            "quantity": quantity,
            "port_of_loading": payload["port_of_loading"],
            "port_of_discharge": payload["port_of_discharge"],
            "latest_shipment_date": payload["latest_shipment_date"],
            "expiry_date": payload["expiry_date"],
            "presentation_period_days": int(payload.get("presentation_period_days", 21)),
            "insurance_min_pct": 110.0,
            "daily_demurrage_usd": float(payload.get("daily_demurrage_usd", 0)),
        }
        data = {
            "master": master,
            "amendments": [],
            "presentation": {
                "invoice_no": "",
                "invoice_date": "",
                "invoice_amount": amount,
                "invoice_unit_price": unit_price,
                "invoice_goods_description": "",
                "bl_no": "",
                "bl_vessel": "",
                "bl_goods_description": "",
                "bl_on_board_date": None,
                "bl_gross_weight_kg": None,
                "bl_notify_party": "",
                "packing_gross_weight_kg": None,
                "insurance_doc_type": "",
                "insurance_amount": None,
                "insurance_effective_date": None,
                "presentation_date": payload.get("presentation_date") or payload["expiry_date"],
            },
            "case_source": "USER_CREATED",
            "evidence_status": "AWAITING_DOCUMENTS",
            "evidence_documents": [],
            "approval_receipt": None,
            "created_at": datetime.now(UTC).isoformat(),
        }
        self._write_case(lc_id, data)
        return data

    def record_document(
        self,
        lc_id: str,
        document_type: str,
        original_filename: str,
        content_type: str,
        content: bytes,
        extraction: dict[str, Any],
    ) -> dict[str, Any]:
        if document_type not in DOCUMENT_TYPES:
            raise ValueError("Unsupported document type.")
        data = deepcopy(self.load(lc_id))
        digest = hashlib.sha256(content).hexdigest()
        extension = Path(original_filename).suffix.lower()[:10]
        document_id = f"DOC-{digest[:16]}"
        docs_dir = self._case_dir(lc_id) / "documents"
        docs_dir.mkdir(parents=True, exist_ok=True)
        (docs_dir / f"{document_id}{extension}").write_bytes(content)

        record = {
            "document_id": document_id,
            "document_type": document_type,
            "filename": Path(original_filename).name,
            "content_type": content_type,
            "size_bytes": len(content),
            "source_digest_sha256": digest,
            "uploaded_at": datetime.now(UTC).isoformat(),
            "extraction": extraction,
            "review_status": "NEEDS_REVIEW" if extraction.get("fields") else "OCR_UNAVAILABLE",
        }
        documents = [doc for doc in data.get("evidence_documents", []) if doc.get("document_type") != document_type]
        documents.append(record)
        data["evidence_documents"] = documents
        data["evidence_status"] = "NEEDS_REVIEW" if any(doc["review_status"] == "NEEDS_REVIEW" for doc in documents) else "OCR_UNAVAILABLE"
        if data.get("case_source") == "SAMPLE_CASE":
            data["case_source"] = "SAMPLE_CASE_WITH_USER_EVIDENCE"
        self._write_case(lc_id, data)
        return record

    def accept_evidence(self, lc_id: str, reviewed_documents: Iterable[dict[str, Any]]) -> dict[str, Any]:
        with self._lock:
            data = deepcopy(self.load(lc_id))
            by_id = {doc["document_id"]: doc for doc in data.get("evidence_documents", [])}
            accepted_ids: list[str] = []

            for reviewed in reviewed_documents:
                document_id = reviewed.get("document_id")
                if document_id not in by_id:
                    raise ValueError(f"Unknown document '{document_id}'.")
                record = by_id[document_id]
                extracted_fields = record.get("extraction", {}).get("fields", {})
                reviewed_fields = reviewed.get("fields") or {
                    key: value.get("value") for key, value in extracted_fields.items()
                }
                mapping = FIELD_TO_PRESENTATION.get(record["document_type"], {})
                for field_key, value in reviewed_fields.items():
                    presentation_key = mapping.get(field_key)
                    if presentation_key:
                        if presentation_key in NUMERIC_PRESENTATION_FIELDS and value is not None:
                            if isinstance(value, dict):
                                raise ValueError(f"Numeric field '{field_key}' cannot be an object.")
                            try:
                                f_val = float(str(value).replace(",", "").strip())
                                if math.isnan(f_val) or math.isinf(f_val):
                                    raise ValueError(f"Numeric field '{field_key}' cannot be NaN or Infinity.")
                                if f_val < 0:
                                    raise ValueError(f"Numeric field '{field_key}' cannot be negative.")
                                value = f_val
                            except (ValueError, TypeError) as exc:
                                raise ValueError(f"Field '{field_key}' must be a valid finite number: {exc}")
                        data["presentation"][presentation_key] = value
                record["review_status"] = "ACCEPTED"
                record["reviewed_fields"] = reviewed_fields
                record["accepted_at"] = datetime.now(UTC).isoformat()
                accepted_ids.append(document_id)

            data["evidence_documents"] = list(by_id.values())
            accepted_types = {
                document["document_type"]
                for document in data["evidence_documents"]
                if document.get("review_status") == "ACCEPTED"
            }
            required_types = {"commercial_invoice", "bill_of_lading", "packing_list", "insurance"}
            missing_types = sorted(required_types - accepted_types) if data.get("case_source") == "USER_CREATED" else []
            data["missing_document_types"] = missing_types
            data["evidence_status"] = (
                "ACCEPTED" if accepted_ids and not missing_types else
                "NEEDS_REVIEW" if accepted_ids else
                data.get("evidence_status", "AWAITING_DOCUMENTS")
            )
            data["evidence_version"] = int(data.get("evidence_version", 0)) + 1
            data["evidence_accepted_at"] = datetime.now(UTC).isoformat()
            self._write_case(lc_id, data)
            return data

    def document_path(self, lc_id: str, document_id: str) -> Path:
        if not re.fullmatch(r"DOC-[a-f0-9]{16}", document_id):
            raise FileNotFoundError(document_id)
        matches = list((self._case_dir(lc_id) / "documents").glob(f"{document_id}.*"))
        if len(matches) != 1 or not matches[0].is_file():
            raise FileNotFoundError(document_id)
        return matches[0]

    def record_approval(self, lc_id: str, receipt_dict: dict[str, Any]) -> dict[str, Any]:
        """Persist authorized sign-off receipt to durable case storage."""
        with self._lock:
            data = deepcopy(self.load(lc_id))
            data["approval_receipt"] = receipt_dict
            data["authorized_at"] = datetime.now(UTC).isoformat()
            self._write_case(lc_id, data)
            return data
