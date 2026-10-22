"""Verification Gate 2: Deterministic UCP 600 Engine Tests.

Tests pure Python mathematical, calendar, tolerance, insurance, and weight checks.
Invariants tested:
1. Scenario 1 (LC-2026-8841): All deterministic checks pass.
2. Scenario 2 (LC-2026-9104): Catches exact $9,600 shortfall under Art. 28(f)(ii) and gross weight conflict under Art. 14(d).
3. Scenario 3 (LC-2026-9920): Deterministic checks pass on face (TBML/sanctions handled in Action Engine).
4. Cover note rejection under Art. 28(c).
5. Late presentation rejection under Art. 14(c).
6. Demurrage advisory correctly computes $11,100 savings for 48h re-presentation.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest
from apps.api.engines.ucp600_deterministic import UCP600DeterministicEngine
from apps.api.memory.amendment_memory import AmendmentMemoryEngine

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
PRESENTATIONS_DIR = ROOT_DIR / "data" / "presentations"


@pytest.fixture
def det_engine() -> UCP600DeterministicEngine:
    return UCP600DeterministicEngine()


@pytest.fixture
def memory_engine() -> AmendmentMemoryEngine:
    return AmendmentMemoryEngine()


def test_scenario_1_deterministic_all_pass(
    det_engine: UCP600DeterministicEngine,
    memory_engine: AmendmentMemoryEngine,
):
    """Test LC-2026-8841: All deterministic math, dates, and tolerances pass."""
    with open(PRESENTATIONS_DIR / "LC-2026-8841.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # First resolve active terms via amendment memory (latest_shipment_date updated to 2026-10-18)
    res_mem = memory_engine.build_active_state(data["master"], data["amendments"], data["presentation"])
    eval_result = det_engine.evaluate_presentation(res_mem.active_terms, data["presentation"])

    assert eval_result.all_passed is True
    assert eval_result.failed_checks_count == 0

    # Verify specific checks
    checks_by_id = {c.check_id: c for c in eval_result.checks}
    assert checks_by_id["TEMPORAL_EXPIRY_DATE"].passed is True
    assert checks_by_id["TEMPORAL_21_DAY_WINDOW"].passed is True
    assert checks_by_id["TEMPORAL_LATEST_SHIPMENT"].passed is True
    assert checks_by_id["FINANCIAL_INVOICE_AMOUNT"].passed is True
    assert checks_by_id["INSURANCE_MINIMUM_COVERAGE"].passed is True
    assert checks_by_id["CROSS_DOC_WEIGHT_RECONCILIATION"].passed is True


def test_scenario_2_curable_shortfall_and_weight_conflict(
    det_engine: UCP600DeterministicEngine,
    memory_engine: AmendmentMemoryEngine,
):
    """Test LC-2026-9104: Fails Art. 28(f)(ii) (exact $9,600 shortfall) and Art. 14(d) weight conflict."""
    with open(PRESENTATIONS_DIR / "LC-2026-9104.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    res_mem = memory_engine.build_active_state(data["master"], data["amendments"], data["presentation"])
    eval_result = det_engine.evaluate_presentation(res_mem.active_terms, data["presentation"])

    assert eval_result.all_passed is False
    assert eval_result.failed_checks_count == 2

    checks_by_id = {c.check_id: c for c in eval_result.checks}

    # 1. Insurance Coverage Shortfall Check (Art. 28(f)(ii))
    ins_check = checks_by_id["INSURANCE_MINIMUM_COVERAGE"]
    assert ins_check.passed is False
    assert ins_check.ucp_citation == "UCP 600 Art. 28(f)(ii)"
    assert ins_check.computed_values["shortfall_usd"] == 9600.00
    assert ins_check.computed_values["required_insurance_min"] == 528000.00
    assert ins_check.computed_values["actual_coverage_pct"] == 108.0

    # 2. Cross-Document Weight Conflict Check (Art. 14(d))
    wt_check = checks_by_id["CROSS_DOC_WEIGHT_RECONCILIATION"]
    assert wt_check.passed is False
    assert wt_check.ucp_citation == "UCP 600 Art. 14(d)"
    assert wt_check.computed_values["weight_diff_kg"] == 450.00

    # 3. Demurrage Analysis
    dem = eval_result.demurrage_analysis
    assert dem is not None
    assert dem["days_remaining_in_window"] == 11
    assert dem["net_savings_usd"] == 11100.00  # (8 - 2) * $1850 = $11,100


def test_scenario_3_paper_math_passes_on_face(
    det_engine: UCP600DeterministicEngine,
    memory_engine: AmendmentMemoryEngine,
):
    """Test LC-2026-9920: Paper dates and amounts are compliant on face."""
    with open(PRESENTATIONS_DIR / "LC-2026-9920.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    res_mem = memory_engine.build_active_state(data["master"], data["amendments"], data["presentation"])
    eval_result = det_engine.evaluate_presentation(res_mem.active_terms, data["presentation"])

    # On face, dates, amounts, 110% insurance, and weights pass
    assert eval_result.all_passed is True


def test_cover_note_prohibition_art_28_c(det_engine: UCP600DeterministicEngine):
    """Test UCP 600 Art. 28(c): Cover Notes are prohibited."""
    active_lc = {
        "amount": 100000.0,
        "expiry_date": "2026-12-01",
        "latest_shipment_date": "2026-11-01",
        "insurance_min_pct": 110.0,
    }
    presentation = {
        "presentation_date": "2026-10-15",
        "bl_on_board_date": "2026-10-10",
        "invoice_amount": 100000.0,
        "insurance_amount": 110000.0,
        "insurance_doc_type": "Cover Note",  # Prohibited!
    }

    eval_result = det_engine.evaluate_presentation(active_lc, presentation)
    assert eval_result.all_passed is False

    checks_by_id = {c.check_id: c for c in eval_result.checks}
    assert checks_by_id["INSURANCE_DOCUMENT_TYPE"].passed is False
    assert checks_by_id["INSURANCE_DOCUMENT_TYPE"].ucp_citation == "UCP 600 Art. 28(c)"


def test_late_presentation_art_14_c(det_engine: UCP600DeterministicEngine):
    """Test UCP 600 Art. 14(c): Presentation >21 days after shipment is discrepant."""
    active_lc = {
        "amount": 100000.0,
        "expiry_date": "2026-12-01",
        "latest_shipment_date": "2026-11-01",
        "presentation_period_days": 21,
    }
    presentation = {
        "bl_on_board_date": "2026-09-01",
        "presentation_date": "2026-09-25",  # 24 days later! (>21 days)
        "invoice_amount": 100000.0,
        "insurance_amount": 110000.0,
    }

    eval_result = det_engine.evaluate_presentation(active_lc, presentation)
    assert eval_result.all_passed is False

    checks_by_id = {c.check_id: c for c in eval_result.checks}
    assert checks_by_id["TEMPORAL_21_DAY_WINDOW"].passed is False
    assert checks_by_id["TEMPORAL_21_DAY_WINDOW"].ucp_citation == "UCP 600 Art. 14(c)"
