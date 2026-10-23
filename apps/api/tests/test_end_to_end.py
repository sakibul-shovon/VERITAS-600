"""Verification Gate 4: End-to-End API & Golden Scenario Integration Tests.

Tests:
1. Health and sponsor telemetry check (GET /api/v1/health).
2. Scenarios list and metadata (GET /api/v1/scenarios).
3. End-to-End examination of LC-2026-8841 (Verdict: APPROVE_HONOUR).
4. End-to-End examination of LC-2026-9104 (Verdict: ISSUE_MT734_REFUSAL).
5. End-to-End examination of LC-2026-9920 (Verdict: COMPLIANCE_HOLD_AML).
6. Mandatory Human Examiner Sign-Off Gate (POST /api/v1/examine/{lc_id}/approve-action).
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from apps.api.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_api_health_and_telemetry(client: TestClient):
    """Test health endpoint exposes live vs fallback telemetry."""
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "sponsors" in data
    assert "zetaris" in data["sponsors"]
    assert "meterless" in data["sponsors"]
    assert "nvidia_nim" in data["sponsors"]


def test_api_scenarios_list(client: TestClient):
    """Test scenarios endpoint lists all 3 flagship LCs."""
    res = client.get("/api/v1/scenarios")
    assert res.status_code == 200
    scenarios = res.json()["scenarios"]
    assert len(scenarios) == 3
    lc_ids = [s["lc_id"] for s in scenarios]
    assert "LC-2026-8841" in lc_ids
    assert "LC-2026-9104" in lc_ids
    assert "LC-2026-9920" in lc_ids


def test_e2e_scenario_1_wrongful_dishonor_prevention(client: TestClient):
    """Test LC-2026-8841: Prevents wrongful dishonor, outputs APPROVE_HONOUR."""
    res = client.post("/api/v1/examine/LC-2026-8841?stream=false")
    assert res.status_code == 200
    data = res.json()

    decision = data["decision"]
    assert decision["recommended_action"] == "APPROVE_HONOUR"
    assert "ISBP 745 Para A23" in decision["legal_citations"]
    assert "UCP 600 Art. 14(e)" in decision["legal_citations"]
    assert decision["action_status"] == "PENDING_HUMAN_SIGN_OFF"

    # Artifact check
    artifact = data["generated_artifact"]
    assert "SETTLEMENT AUTHORIZATION VOUCHER" in artifact
    assert "USD 240,000.00" in artifact

    # Human Sign-Off Gate
    sig_res = client.post(
        "/api/v1/examine/LC-2026-8841/approve-action",
        json={
            "examiner_name": "Sarah Chen, Trade Officer",
            "comments": "Checked and approved",
            "run_id": data["run_id"],
            "decision_sha256": data["decision_sha256"],
            "expected_action": decision["recommended_action"],
        },
    )
    assert sig_res.status_code == 200
    sig_data = sig_res.json()
    assert sig_data["status"] == "AUTHORIZED_NOT_DISPATCHED"
    assert sig_data["dispatch_status"] == "NOT_CONNECTED"
    assert sig_data["human_approved_by"] == "Sarah Chen, Trade Officer"


def test_e2e_scenario_2_curable_mt734_and_demurrage_save(client: TestClient):
    """Test LC-2026-9104: Catches insurance shortfall and weight conflict, outputs MT734."""
    res = client.post("/api/v1/examine/LC-2026-9104?stream=false")
    assert res.status_code == 200
    data = res.json()

    decision = data["decision"]
    assert decision["recommended_action"] == "ISSUE_MT734_REFUSAL"
    assert len(decision["discrepancies"]) == 2

    # Demurrage advisory check
    advisory = decision["demurrage_savings_advisory"]
    assert advisory is not None
    assert advisory["net_savings_usd"] == 11100.00
    assert advisory["days_remaining_in_window"] == 11

    # Generated SWIFT MT734 message check
    artifact = data["generated_artifact"]
    assert ":77J:DISCREPANCIES NOTED" in artifact
    assert "UCP 600 Art. 28(f)(ii)" in artifact
    assert "UCP 600 Art. 14(d)" in artifact
    assert ":77B:DISPOSAL OF DOCUMENTS PURSUANT TO UCP 600 ART. 16(c)(iii)(a)" in artifact
    assert "$11,100.00 USD" in artifact


def test_e2e_scenario_3_tbml_sanctions_freeze(client: TestClient):
    """Test LC-2026-9920: Detects price anomaly and watchlist hit, outputs COMPLIANCE_HOLD_AML."""
    res = client.post("/api/v1/examine/LC-2026-9920?stream=false")
    assert res.status_code == 200
    data = res.json()

    decision = data["decision"]
    assert decision["recommended_action"] == "COMPLIANCE_HOLD_AML"
    assert len(decision["regulatory_flags"]) >= 1

    # Regulatory AML dossier check (MT734 suppressed)
    artifact = data["generated_artifact"]
    assert "REGULATORY FREEZE DOSSIER" in artifact
    assert "SAR-OFAC" in artifact
    assert "NO PAYMENT IS AUTHORIZED" in artifact
    assert "SWIFT MT734" in artifact and "SUPPRESSED" in artifact
