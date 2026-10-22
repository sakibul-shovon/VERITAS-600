"""Verification Gate 3: Legal Adjudicator, Document Extraction & Hard Invariant Tests.

Invariants tested:
1. ISBP 745 Para A23: Harmless typographical error ('Mashine') is legally protected.
2. UCP 600 Art. 14(e): General goods description on B/L is legally protected.
3. UCP 600 Art. 14(j): Address mutation in Consignee/Notify box is a fatal discrepancy.
4. UCP 600 Art. 18(c): Commercial invoice description must correspond with credit.
5. Hard Invariant Rule: Neural verdict can NEVER override a failed deterministic check.
6. DocumentExtractor: Generates valid normalized bounding boxes [ymin, xmin, ymax, xmax].
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from apps.api.engines.document_extractor import DocumentExtractor
from apps.api.engines.ucp600_deterministic import DeterministicCheckResult, DeterministicEvaluation
from apps.api.engines.ucp600_legal_adjudicator import UCP600LegalAdjudicator
from apps.api.inference.meterless_router import MeterlessRouter

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
PRESENTATIONS_DIR = ROOT_DIR / "data" / "presentations"


@pytest.fixture
def adjudicator() -> UCP600LegalAdjudicator:
    return UCP600LegalAdjudicator()


@pytest.fixture
def extractor() -> DocumentExtractor:
    return DocumentExtractor()


@pytest.fixture
def router() -> MeterlessRouter:
    return MeterlessRouter()


def test_scenario_1_isbp_a23_and_art_14e_protections(adjudicator: UCP600LegalAdjudicator):
    """Test LC-2026-8841: 'Mashine' typo protected under A23 and 'Servo Motors' protected under 14(e)."""
    with open(PRESENTATIONS_DIR / "LC-2026-8841.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    res = adjudicator.adjudicate_presentation(data["master"], data["presentation"])

    # Must be protected, not discrepant
    assert res.overall_legal_status == "COMPLIANT_PROTECTED"
    assert res.final_locked_verdict == "COMPLIANT"
    assert len(res.findings) >= 2

    findings_by_doc = {f.divergence_item: f for f in res.findings}

    # Invoice typo finding
    inv_finding = findings_by_doc["Commercial Invoice Goods Description"]
    assert inv_finding.verdict == "COMPLIANT_PROTECTED"
    assert "ISBP 745 Para A23" in inv_finding.ucp_isbp_citation
    assert inv_finding.is_discrepant is False
    assert "wrongful dishonor" in inv_finding.legal_reasoning.lower() or "typo" in inv_finding.legal_reasoning.lower()

    # B/L general description finding
    bl_finding = findings_by_doc["Ocean Bill of Lading Goods Description"]
    assert bl_finding.verdict == "COMPLIANT_PROTECTED"
    assert "UCP 600 Art. 14(e)" in bl_finding.ucp_isbp_citation
    assert bl_finding.is_discrepant is False


def test_consignee_address_mutation_art_14_j(adjudicator: UCP600LegalAdjudicator):
    """Test UCP 600 Art. 14(j): Address mutation in Consignee/Notify box is discrepant."""
    active_lc = {
        "applicant_name": "Pacific Heavy Machinery Pte Ltd",
        "applicant_address_strict": "82 Shenton Way, Singapore 079120",
    }
    presentation = {
        "bl_notify_party": "Pacific Heavy Machinery Pte Ltd, Wrong Address 99 Orchard Road, Singapore",
    }

    res = adjudicator.adjudicate_presentation(active_lc, presentation)
    assert res.overall_legal_status == "DISCREPANT"
    assert res.final_locked_verdict == "DISCREPANT"

    notify_finding = res.findings[0]
    assert notify_finding.is_discrepant is True
    assert "UCP 600 Art. 14(j)" in notify_finding.ucp_isbp_citation


def test_hard_invariant_rule_enforcement(adjudicator: UCP600LegalAdjudicator):
    """Hard Invariant Rule: Neural engine CANNOT override a failed deterministic check."""
    # Presentation has compliant descriptions (so neural findings pass)
    active_lc = {
        "goods_description_strict": "INDUSTRIAL PUMPS",
        "applicant_address_strict": "100 Port Road",
    }
    presentation = {
        "invoice_goods_description": "INDUSTRIAL PUMPS",
        "bl_goods_description": "PUMPS",
    }

    # But deterministic evaluation has a failed check (e.g. 108% insurance shortfall)
    failed_det_eval = DeterministicEvaluation(
        all_passed=False,
        failed_checks_count=1,
        checks=[
            DeterministicCheckResult(
                check_id="INSURANCE_MINIMUM_COVERAGE",
                name="Insurance Coverage",
                ucp_citation="UCP 600 Art. 28(f)(ii)",
                passed=False,
                severity="FATAL_DISCREPANCY",
                details="Insurance covers 108% instead of required 110%",
                computed_values={"shortfall_usd": 9600.0},
            )
        ],
    )

    res = adjudicator.adjudicate_presentation(active_lc, presentation, deterministic_eval=failed_det_eval)

    # Invariant assertion: final verdict MUST be DISCREPANT, override blocked!
    assert res.hard_invariant_enforced is True
    assert res.final_locked_verdict == "DISCREPANT"


def test_document_extractor_bounding_boxes(extractor: DocumentExtractor):
    """Test that DocumentExtractor returns normalized bounding boxes for invoice and B/L."""
    res_inv = extractor.extract_document("Commercial Invoice", "...", "LC-2026-8841")
    assert res_inv.document_type == "Commercial Invoice"
    assert "invoice_no" in res_inv.fields
    assert "total_amount" in res_inv.fields

    box = res_inv.fields["total_amount"].bounding_box
    assert len(box) == 4
    # Bounding boxes must be [ymin, xmin, ymax, xmax] in 0-1000 scale
    assert 0 <= box[0] <= 1000 and 0 <= box[2] <= 1000

    res_bl = extractor.extract_document("Ocean Bill of Lading", "...", "LC-2026-8841")
    assert res_bl.document_type == "Ocean Bill of Lading"
    assert "on_board_date" in res_bl.fields
    assert "gross_weight" in res_bl.fields


def test_meterless_router_markovian_chunks(router: MeterlessRouter):
    """Test that MeterlessRouter chunks LC into 6 stages and computes token savings."""
    with open(PRESENTATIONS_DIR / "LC-2026-8841.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = router.route_markovian_chunks(data["master"], data["amendments"], data["presentation"])
    assert len(chunks) == 6

    stage_ids = [c.stage_id for c in chunks]
    assert stage_ids == [
        "TEMPORAL",
        "FINANCIAL",
        "INSURANCE",
        "PHYSICAL_RECONCILIATION",
        "LEGAL_ADJUDICATION",
        "FEDERATED_RISK",
    ]

    telemetry = router.compute_telemetry(data, chunks, start_time_sec=1.0)
    assert telemetry.token_reduction_pct > 0.0
    assert telemetry.routing_mode == "MARKOVIAN_6_CHUNK"
