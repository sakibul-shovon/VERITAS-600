"""Real-document intake, evidence review, and approval-binding tests."""

from __future__ import annotations

from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from apps.api import main


@pytest.fixture
def client(tmp_path, monkeypatch) -> TestClient:
    monkeypatch.setattr(main.case_store, "runtime_dir", tmp_path / "runtime_cases")
    main._RUN_STORE.clear()
    return TestClient(main.app)


def make_text_pdf(lines: list[str]) -> bytes:
    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)
    font = DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
    })
    page[NameObject("/Resources")] = DictionaryObject({
        NameObject("/Font"): DictionaryObject({NameObject("/F1"): writer._add_object(font)}),
    })
    commands = ["BT", "/F1 12 Tf", "50 740 Td"]
    for index, line in enumerate(lines):
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        if index:
            commands.append("0 -22 Td")
        commands.append(f"({escaped}) Tj")
    commands.append("ET")
    stream = DecodedStreamObject()
    stream.set_data("\n".join(commands).encode("latin-1"))
    page[NameObject("/Contents")] = writer._add_object(stream)
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def case_payload(lc_id: str) -> dict:
    return {
        "lc_id": lc_id,
        "applicant_name": "Atlas Imports Ltd",
        "applicant_address_strict": "17 Port Road, Singapore",
        "beneficiary_name": "Northstar Machines GmbH",
        "issuing_bank": "Evidence Bank",
        "currency": "USD",
        "amount": 240000,
        "incoterm": "CIF",
        "hs_code_6": "848180",
        "goods_description_strict": "Industrial valve assemblies Model V-600",
        "unit_price": 480,
        "quantity": 500,
        "port_of_loading": "Hamburg",
        "port_of_discharge": "Singapore",
        "latest_shipment_date": "2026-11-15",
        "expiry_date": "2026-12-15",
    }


def test_user_case_acceptance_requires_complete_document_set(client: TestClient):
    create = client.post("/api/v1/cases", json=case_payload("LC-USER-1001"))
    assert create.status_code == 201
    assert create.json()["evidence_status"] == "AWAITING_DOCUMENTS"

    pdf = make_text_pdf([
        "INVOICE NO: INV-1001",
        "INVOICE DATE: 2026-11-10",
        "GOODS DESCRIPTION: Industrial valve assemblies Model V-600",
        "UNIT PRICE: USD 480.00",
        "TOTAL AMOUNT: USD 240000.00",
    ])
    uploaded = client.post(
        "/api/v1/cases/LC-USER-1001/documents",
        data={"document_type": "commercial_invoice"},
        files={"file": ("invoice.pdf", pdf, "application/pdf")},
    )
    assert uploaded.status_code == 201
    document = uploaded.json()["document"]
    assert document["extraction"]["extraction_mode"] == "PDF_TEXT_LAYER"
    assert document["extraction"]["fields"]["total_amount"]["value"] == 240000.0

    reviewed_fields = {
        key: field["value"] for key, field in document["extraction"]["fields"].items()
    }
    accepted = client.post(
        "/api/v1/cases/LC-USER-1001/evidence/accept",
        json={"documents": [{"document_id": document["document_id"], "fields": reviewed_fields}]},
    )
    assert accepted.status_code == 200
    assert accepted.json()["evidence_status"] == "NEEDS_REVIEW"
    assert set(accepted.json()["missing_document_types"]) == {"bill_of_lading", "packing_list", "insurance"}

    blocked = client.post("/api/v1/examine/LC-USER-1001?stream=false")
    assert blocked.status_code == 409


def test_real_pdf_evidence_flows_into_calculations(client: TestClient):
    lc_id = "LC-USER-2001"
    assert client.post("/api/v1/cases", json=case_payload(lc_id)).status_code == 201
    pdf_documents = {
        "commercial_invoice": [
            "INVOICE NO: INV-REAL-2001",
            "INVOICE DATE: 2026-11-10",
            "GOODS DESCRIPTION: Industrial valve assemblies Model V-600",
            "UNIT PRICE: USD 480.00",
            "TOTAL AMOUNT: USD 240000.00",
        ],
        "bill_of_lading": [
            "B/L NO: BL-REAL-2001",
            "VESSEL: MV Aurora",
            "GOODS DESCRIPTION: Industrial valve assemblies",
            "ON BOARD DATE: 2026-11-12",
            "GROSS WEIGHT: 12500",
            "NOTIFY PARTY: Atlas Imports Ltd, 17 Port Road, Singapore",
        ],
        "packing_list": ["PACKING LIST", "GROSS WEIGHT: 12500"],
        "insurance": [
            "INSURANCE CERTIFICATE",
            "INSURED AMOUNT: USD 264000.00",
            "EFFECTIVE DATE: 2026-11-11",
        ],
    }

    reviews = []
    for document_type, lines in pdf_documents.items():
        response = client.post(
            f"/api/v1/cases/{lc_id}/documents",
            data={"document_type": document_type},
            files={"file": (f"{document_type}.pdf", make_text_pdf(lines), "application/pdf")},
        )
        assert response.status_code == 201
        document = response.json()["document"]
        assert document["extraction"]["extraction_mode"] == "PDF_TEXT_LAYER"
        assert document["extraction"]["source_digest_sha256"] == document["source_digest_sha256"]
        reviews.append({
            "document_id": document["document_id"],
            "fields": {key: item["value"] for key, item in document["extraction"]["fields"].items()},
        })

    accepted = client.post(f"/api/v1/cases/{lc_id}/evidence/accept", json={"documents": reviews})
    assert accepted.status_code == 200
    accepted_data = accepted.json()
    assert accepted_data["evidence_status"] == "ACCEPTED"
    assert accepted_data["presentation"]["invoice_amount"] == 240000.0
    assert accepted_data["presentation"]["insurance_amount"] == 264000.0
    assert accepted_data["presentation"]["bl_on_board_date"] == "2026-11-12"
    assert accepted_data["presentation"]["packing_gross_weight_kg"] == 12500.0

    run = client.post(f"/api/v1/examine/{lc_id}?stream=false")
    assert run.status_code == 200
    payload = run.json()
    insurance_check = next(check for check in payload["deterministic"]["checks"] if check["check_id"] == "INSURANCE_MINIMUM_COVERAGE")
    assert insurance_check["passed"] is True
    assert insurance_check["computed_values"]["actual_coverage_pct"] == 110.0
    assert payload["extraction_provenance"]["modes"] == ["PDF_TEXT_LAYER"]


def test_image_upload_never_falls_back_to_fixture_ocr(client: TestClient, monkeypatch):
    client.post("/api/v1/cases", json=case_payload("LC-USER-1002"))
    monkeypatch.setattr(main.extractor.nim_client, "api_key", "")
    image = BytesIO()
    from PIL import Image
    Image.new("RGB", (64, 64), "white").save(image, format="PNG")

    uploaded = client.post(
        "/api/v1/cases/LC-USER-1002/documents",
        data={"document_type": "insurance"},
        files={"file": ("insurance.png", image.getvalue(), "image/png")},
    )
    assert uploaded.status_code == 201
    extraction = uploaded.json()["document"]["extraction"]
    assert extraction["extraction_mode"] == "OCR_UNAVAILABLE"
    assert extraction["fields"] == {}


def test_scanned_pdf_is_rendered_for_vision_without_fixture_fallback(client: TestClient, monkeypatch):
    client.post("/api/v1/cases", json=case_payload("LC-USER-1003"))
    monkeypatch.setattr(main.extractor.nim_client, "api_key", "")
    from PIL import Image, ImageDraw
    scan = Image.new("RGB", (900, 1200), "white")
    ImageDraw.Draw(scan).text((80, 100), "INSURANCE CERTIFICATE\nINSURED AMOUNT: USD 264000.00", fill="black")
    pdf = BytesIO()
    scan.save(pdf, format="PDF")

    uploaded = client.post(
        "/api/v1/cases/LC-USER-1003/documents",
        data={"document_type": "insurance"},
        files={"file": ("insurance-scan.pdf", pdf.getvalue(), "application/pdf")},
    )
    assert uploaded.status_code == 201
    extraction = uploaded.json()["document"]["extraction"]
    assert extraction["extraction_mode"] == "OCR_UNAVAILABLE"
    assert "credentials are not configured" in extraction["notice"]
    assert "page rendering is unavailable" not in extraction["notice"]


def test_approval_rejects_missing_and_stale_run_bindings(client: TestClient):
    missing = client.post(
        "/api/v1/examine/LC-2026-9104/approve-action",
        json={
            "examiner_name": "Sarah Chen",
            "comments": "Reviewed",
            "run_id": "RUN-NOT-FOUND",
            "decision_sha256": "0" * 64,
            "expected_action": "ISSUE_MT734_REFUSAL",
        },
    )
    assert missing.status_code == 409

    run = client.post("/api/v1/examine/LC-2026-9104?stream=false").json()
    stale = client.post(
        "/api/v1/examine/LC-2026-9104/approve-action",
        json={
            "examiner_name": "Sarah Chen",
            "comments": "Reviewed",
            "run_id": run["run_id"],
            "decision_sha256": "f" * 64,
            "expected_action": run["decision"]["recommended_action"],
        },
    )
    assert stale.status_code == 409
