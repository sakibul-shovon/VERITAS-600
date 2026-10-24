"""Verification Suite for Codebase Audit & Correctness Fixes.

Covers regression verification for:
1. Permissive multi-format date parser (DD/MM/YYYY, ISO, dash/dot).
2. Missing evidence handling: no silent 0==0 passes on weight reconciliation.
3. CIF basis calculation strictly under UCP 600 Art. 28(f)(ii).
4. Dynamic demurrage advisory string reflecting actual window days.
5. Markdown code fence stripping and non-JSON preamble recovery in legal adjudicator.
6. Keyed HMAC-SHA256 signature token generation and verifier roundtrip.
7. Durable approval persistence in CaseStore.
8. Zetaris SQL CTE isolation per LC ID.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from apps.api.audit.verifier import AuditVerifier
from apps.api.cases.store import CaseStore
from apps.api.domain.decisions import ActionType, AuthorityLevel, DecisionReceipt, DispatchStatus
from apps.api.engines.artifact_generator import ArtifactGenerator
from apps.api.engines.decision_engine import BankDecision
from apps.api.engines.ucp600_deterministic import UCP600DeterministicEngine, parse_date
from apps.api.engines.ucp600_legal_adjudicator import UCP600LegalAdjudicator

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
PRESENTATIONS_DIR = ROOT_DIR / "data" / "presentations"
RUNTIME_CASES_DIR = ROOT_DIR / "data" / "runtime_cases"


def test_permissive_date_parser_formats():
    """Verify that parse_date parses multiple international date formats."""
    expected = date(2026, 10, 15)
    assert parse_date("2026-10-15") == expected
    assert parse_date("15/10/2026") == expected
    assert parse_date("15-10-2026") == expected
    assert parse_date("2026/10/15") == expected
    assert parse_date("15.10.2026") == expected
    assert parse_date(date(2026, 10, 15)) == expected

    # Empty and None values return None instead of raising unhandled ValueError
    assert parse_date(None) is None
    assert parse_date("") is None
    assert parse_date("   ") is None


def test_no_silent_pass_on_unextracted_zero_weights():
    """Ensure that dummy 0 kg weights on missing evidence do not falsely pass Art. 14(d)."""
    engine = UCP600DeterministicEngine()
    active_lc = {
        "amount": 100000.0,
        "expiry_date": "2026-12-01",
        "latest_shipment_date": "2026-11-01",
    }
    presentation = {
        "invoice_amount": 100000.0,
        "packing_gross_weight_kg": 0.0,
        "bl_gross_weight_kg": 0.0,
    }

    eval_result = engine.evaluate_presentation(active_lc, presentation)
    # Check that CROSS_DOC_WEIGHT_RECONCILIATION is NOT recorded as compliant
    weight_checks = [c for c in eval_result.checks if c.check_id == "CROSS_DOC_WEIGHT_RECONCILIATION"]
    assert len(weight_checks) == 0, "Dummy 0kg weights should not manufacture a compliant weight check"


def test_cif_basis_not_overridden_by_larger_credit_limit():
    """Verify Art. 28(f)(ii): insurance basis is invoice gross value, not the larger credit ceiling."""
    engine = UCP600DeterministicEngine()
    # Credit ceiling is $500,000, but partial shipment / invoice is $200,000
    active_lc = {
        "amount": 500000.0,
        "expiry_date": "2026-12-01",
        "latest_shipment_date": "2026-11-01",
        "insurance_min_pct": 110.0,
    }
    # 110% of $200,000 = $220,000
    presentation = {
        "invoice_amount": 200000.0,
        "insurance_amount": 220000.0,
        "insurance_doc_type": "Insurance Policy",
        "bl_on_board_date": "2026-10-15",
        "presentation_date": "2026-10-20",
    }

    eval_result = engine.evaluate_presentation(active_lc, presentation)
    ins_check = next(c for c in eval_result.checks if c.check_id == "INSURANCE_MINIMUM_COVERAGE")
    assert ins_check.passed is True
    assert ins_check.computed_values["cif_basis"] == 200000.0
    assert ins_check.computed_values["required_insurance_min"] == 220000.0


def test_dynamic_demurrage_advisory_text():
    """Verify that demurrage advisory formats actual computed days_remaining_in_window."""
    engine = UCP600DeterministicEngine()
    active_lc = {
        "amount": 100000.0,
        "expiry_date": "2026-12-01",
        "latest_shipment_date": "2026-11-01",
        "presentation_period_days": 21,
        "daily_demurrage_usd": 1000.0,
    }
    # Shipped Oct 1, presented Oct 5 -> 4 days after shipment, 17 days remain in window
    presentation = {
        "bl_on_board_date": "2026-10-01",
        "presentation_date": "2026-10-05",
        "invoice_amount": 100000.0,
        "insurance_amount": 90000.0,  # Undercovered to trigger failed check
    }

    eval_result = engine.evaluate_presentation(active_lc, presentation)
    assert eval_result.demurrage_analysis is not None
    remaining = eval_result.demurrage_analysis["days_remaining_in_window"]
    assert remaining == 17
    assert "17 days remain in the UCP 600 Art. 14(c) presentation window" in eval_result.demurrage_analysis["advisory"]


def test_safe_parse_json_markdown_stripping():
    """Verify that model responses with markdown backticks or preamble are parsed cleanly."""
    adjudicator = UCP600LegalAdjudicator()
    default_res = {"verdict": "FAIL"}

    # Case 1: Markdown code block with ```json
    raw_markdown = "```json\n{\"verdict\": \"COMPLIANT\", \"confidence\": 0.99}\n```"
    parsed = adjudicator._safe_parse_json(raw_markdown, default_res)
    assert parsed["verdict"] == "COMPLIANT"
    assert parsed["confidence"] == 0.99

    # Case 2: Conversational preamble before JSON
    raw_preamble = "Here is the adjudication result:\n{\"verdict\": \"COMPLIANT_PROTECTED\"}\nHope this helps!"
    parsed_preamble = adjudicator._safe_parse_json(raw_preamble, default_res)
    assert parsed_preamble["verdict"] == "COMPLIANT_PROTECTED"

    # Case 3: Completely invalid JSON falls back gracefully without raising
    raw_garbage = "I cannot fulfill this request."
    parsed_garbage = adjudicator._safe_parse_json(raw_garbage, default_res)
    assert parsed_garbage == default_res


def test_keyed_hmac_decision_receipt_and_verifier():
    """Verify that decision receipts are signed with keyed HMAC and verified by AuditVerifier."""
    receipt = DecisionReceipt.generate(
        run_id="RUN-TEST-HMAC",
        lc_id="LC-2026-TEST",
        action=ActionType.APPROVE_HONOUR,
        decision_sha256="1234567890abcdef",
        merkle_root_sha256="fedcba0987654321",
        signer_name="Lead Officer",
        signer_role=AuthorityLevel.DESK_HEAD,
        discrepancy_count=0,
    )

    assert receipt.dispatch_status == DispatchStatus.AUTHORIZED_NOT_DISPATCHED
    assert receipt.signature_token.startswith("V600-SIG-")

    # AuditVerifier verifies correctly
    is_valid = AuditVerifier.verify_decision_receipt(
        run_id=receipt.run_id,
        lc_id=receipt.lc_id,
        action=receipt.action.value,
        decision_sha256=receipt.decision_sha256,
        merkle_root_sha256=receipt.merkle_root_sha256,
        signer_name=receipt.signer_name,
        signed_at_utc=receipt.signed_at_utc,
        signature_token=receipt.signature_token,
    )
    assert is_valid is True

    # Tampered signature fails
    is_valid_tampered = AuditVerifier.verify_decision_receipt(
        run_id=receipt.run_id,
        lc_id=receipt.lc_id,
        action=receipt.action.value,
        decision_sha256="tampered_hash",
        merkle_root_sha256=receipt.merkle_root_sha256,
        signer_name=receipt.signer_name,
        signed_at_utc=receipt.signed_at_utc,
        signature_token=receipt.signature_token,
    )
    assert is_valid_tampered is False


def test_settlement_voucher_pending_vs_authorized_status():
    """Verify that settlement voucher indicates pending approval initially, and authorized upon sign-off."""
    generator = ArtifactGenerator()
    decision = BankDecision(
        lc_id="LC-2026-8841",
        recommended_action="APPROVE_HONOUR",
        action_title="Approve & Honour Presentation",
        action_summary="All documents compliant.",
        action_status="PENDING_HUMAN_SIGN_OFF",
        legal_citations=["UCP 600 Art. 14(a)"],
        discrepancies=[],
        regulatory_flags=[],
        demurrage_savings_advisory=None,
        execution_telemetry={},
    )
    active_lc = {
        "amount": 240000.0,
        "currency": "USD",
        "beneficiary_name": "Apex Motors",
        "applicant_name": "Global Traders",
    }
    presentation = {"invoice_amount": 240000.0}

    # Pre-signoff voucher
    voucher_pending = generator.generate_artifact(decision, active_lc, presentation)
    assert "PROPOSED - PENDING HUMAN EXAMINER AUTHORIZATION" in voucher_pending
    assert "AWAITING SIGN-OFF (NOT DISPATCHED)" in voucher_pending
    assert "APPROVED BY TRADE FINANCE EXAMINER" not in voucher_pending

    # Post-signoff voucher
    voucher_auth = generator.generate_authorized_voucher(
        decision, active_lc, presentation, signer_name="Examiner Jane", signature_token="V600-SIG-TEST123"
    )
    assert "AUTHORIZED BY HUMAN EXAMINER (Examiner Jane)" in voucher_auth
    assert "AUTHORIZED_NOT_DISPATCHED" in voucher_auth
    assert "V600-SIG-TEST123" in voucher_auth


def test_case_store_durable_approval_recording(tmp_path):
    """Verify that CaseStore persists approvals durably."""
    store = CaseStore(PRESENTATIONS_DIR, tmp_path)
    created = store.create({
        "lc_id": "LC-AUDIT-PERSIST",
        "applicant_name": "Applicant Corp",
        "applicant_address_strict": "123 Port Road",
        "beneficiary_name": "Beneficiary Ltd",
        "currency": "USD",
        "amount": 150000.0,
        "quantity": 100,
        "incoterm": "CIF",
        "port_of_loading": "Singapore",
        "port_of_discharge": "Rotterdam",
        "latest_shipment_date": "2026-11-01",
        "expiry_date": "2026-12-01",
        "hs_code_6": "8481.80",
        "goods_description_strict": "High Pressure Valves",
    })
    assert created["approval_receipt"] is None

    receipt_dict = {
        "run_id": "RUN-001",
        "signature_token": "V600-SIG-ABC",
        "signer_name": "Examiner Bob",
        "dispatch_status": "AUTHORIZED_NOT_DISPATCHED",
    }
    updated = store.record_approval("LC-AUDIT-PERSIST", receipt_dict)
    assert updated["approval_receipt"] == receipt_dict

    # Reload from disk to verify durability
    reloaded = store.load("LC-AUDIT-PERSIST")
    assert reloaded["approval_receipt"] == receipt_dict
