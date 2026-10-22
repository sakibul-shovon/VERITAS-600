"""Tests for Stateful Amendment Memory (UCP 600 Art. 10(c) & 10(e))."""

from __future__ import annotations

import json
from pathlib import Path
import pytest
from apps.api.memory.amendment_memory import AmendmentMemoryEngine

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
PRESENTATIONS_DIR = ROOT_DIR / "data" / "presentations"


@pytest.fixture
def memory_engine() -> AmendmentMemoryEngine:
    return AmendmentMemoryEngine()


def test_scenario_1_amendment_lifecycle(memory_engine: AmendmentMemoryEngine):
    """Test LC-2026-8841: Amendment #1 accepted, Amendment #2 quarantined."""
    with open(PRESENTATIONS_DIR / "LC-2026-8841.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    master = data["master"]
    amendments = data["amendments"]
    presentation = data["presentation"]

    resolution = memory_engine.build_active_state(
        base_lc=master,
        amendments=amendments,
        presentation_fields=presentation,
    )

    # 1. Accepted Amendment #1 overrides original date
    assert resolution.active_terms["latest_shipment_date"] == "2026-10-18"
    assert len(resolution.accepted_amendments) == 1
    assert resolution.accepted_amendments[0]["amendment_id"] == "AMD-8841-01"

    # 2. Unaccepted Amendment #2 is quarantined
    assert len(resolution.quarantined_amendments) == 1
    assert resolution.quarantined_amendments[0]["amendment_id"] == "AMD-8841-02"
    # Port of discharge in active terms remains original Singapore
    assert resolution.active_terms["port_of_discharge"] == "Singapore"

    # 3. No partial acceptance violation because presentation adhered to original port
    assert not resolution.partial_acceptance_violation
    assert resolution.active_terms_sha256 is not None
    assert len(resolution.active_terms_sha256) == 64


def test_art_10_e_partial_acceptance_prohibition(memory_engine: AmendmentMemoryEngine):
    """Test UCP 600 Art. 10(e): Partial acceptance of multi-item amendment is prohibited."""
    base_lc = {
        "lc_id": "LC-TEST-10E",
        "latest_shipment_date": "2026-10-01",
        "unit_price": 500.0,
        "port_of_discharge": "Singapore",
    }
    # Single multi-field amendment
    amendment = [
        {
            "amendment_id": "AMD-TEST-01",
            "lc_id": "LC-TEST-10E",
            "sequence_no": 1,
            "amended_field": "latest_shipment_date",
            "old_value": "2026-10-01",
            "new_value": "2026-10-20",
            "beneficiary_acceptance_status": "UNACCEPTED_PENDING",
            "effective_date": "2026-09-20",
        },
        {
            "amendment_id": "AMD-TEST-01",
            "lc_id": "LC-TEST-10E",
            "sequence_no": 1,
            "amended_field": "unit_price",
            "old_value": "500.0",
            "new_value": "450.0",
            "beneficiary_acceptance_status": "UNACCEPTED_PENDING",
            "effective_date": "2026-09-20",
        },
    ]

    # Beneficiary presents documents shipping on Oct 15 (invoking shipment extension)
    # but bills at original $500.0 (rejecting price cut)
    presentation = {
        "bl_on_board_date": "2026-10-15",
        "invoice_unit_price": "500.0",  # old price
    }

    resolution = memory_engine.build_active_state(
        base_lc=base_lc,
        amendments=amendment,
        presentation_fields=presentation,
    )

    # Partial acceptance must be flagged
    assert resolution.partial_acceptance_violation
    assert "Prohibited under UCP 600 Art. 10(e)" in str(resolution.violation_details)


def test_art_10_c_full_implicit_acceptance(memory_engine: AmendmentMemoryEngine):
    """Test UCP 600 Art. 10(c): Presentation conforming to all changes implicitly accepts."""
    base_lc = {
        "lc_id": "LC-TEST-10C",
        "latest_shipment_date": "2026-10-01",
        "port_of_discharge": "Singapore",
    }
    amendment = [
        {
            "amendment_id": "AMD-TEST-10C",
            "lc_id": "LC-TEST-10C",
            "sequence_no": 1,
            "amended_field": "latest_shipment_date",
            "old_value": "2026-10-01",
            "new_value": "2026-10-20",
            "beneficiary_acceptance_status": "UNACCEPTED_PENDING",
            "effective_date": "2026-09-20",
        },
        {
            "amendment_id": "AMD-TEST-10C",
            "lc_id": "LC-TEST-10C",
            "sequence_no": 1,
            "amended_field": "port_of_discharge",
            "old_value": "Singapore",
            "new_value": "Jurong Port",
            "beneficiary_acceptance_status": "UNACCEPTED_PENDING",
            "effective_date": "2026-09-20",
        },
    ]

    presentation = {
        "bl_on_board_date": "2026-10-15",
        "port_of_discharge": "jurong port",
    }

    resolution = memory_engine.build_active_state(
        base_lc=base_lc,
        amendments=amendment,
        presentation_fields=presentation,
    )

    assert resolution.implicit_acceptance_detected
    assert not resolution.partial_acceptance_violation
    assert resolution.active_terms["latest_shipment_date"] == "2026-10-20"
    assert resolution.active_terms["port_of_discharge"] == "Jurong Port"
