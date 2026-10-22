"""Unit tests for Canonical JSON, Merkle Tree, Hash Chain, and Audit Verification."""

from __future__ import annotations

from decimal import Decimal
import pytest

from apps.api.audit.canonical_json import canonical_sha256, canonicalize_json
from apps.api.audit.hash_chain import RunHashChain
from apps.api.audit.merkle import MerkleTree
from apps.api.audit.verifier import AuditVerifier
from apps.api.domain.decisions import ActionType, AuthorityLevel, DecisionReceipt
from apps.api.domain.money import Money
from apps.api.rulepacks.ucp600_rules import RULES_REGISTRY, get_rule


def test_canonical_json_determinism():
    """Verify that dictionary key order does not alter canonical JSON or SHA-256."""
    d1 = {"b": 2, "a": 1, "c": {"y": "test", "x": Decimal("100.50")}}
    d2 = {"a": 1, "c": {"x": 100.5, "y": "test"}, "b": 2}

    assert canonicalize_json(d1) == canonicalize_json(d2)
    assert canonical_sha256(d1) == canonical_sha256(d2)


def test_merkle_tree_root_and_inclusion_proof():
    """Verify RFC 9162 Merkle tree construction and proof verification."""
    leaves = [
        "1111111111111111111111111111111111111111111111111111111111111111",
        "2222222222222222222222222222222222222222222222222222222222222222",
        "3333333333333333333333333333333333333333333333333333333333333333",
        "4444444444444444444444444444444444444444444444444444444444444444",
    ]

    tree = MerkleTree(leaves)
    assert len(tree.root_hex) == 64

    # Proof for leaf 1
    proof = tree.get_proof(1)
    assert MerkleTree.verify_proof(leaves[1], proof, tree.root_hex) is True

    # Mutated leaf must fail verification
    mutated_leaf = "5555555555555555555555555555555555555555555555555555555555555555"
    assert MerkleTree.verify_proof(mutated_leaf, proof, tree.root_hex) is False


def test_event_hash_chain_tamper_detection():
    """Verify that mutating any past event breaks hash chain integrity."""
    chain = RunHashChain(run_id="RUN-TEST-001")
    chain.append_event("STAGE_1", {"status": "ok"}, stage_id="TEMPORAL")
    chain.append_event("STAGE_2", {"status": "ok"}, stage_id="ZETARIS")
    chain.append_event("STAGE_3", {"status": "ok"}, stage_id="DETERMINISTIC")

    assert chain.verify_integrity() is True

    # Tamper with event 1 payload
    chain.events[0].payload["status"] = "tampered"
    assert chain.verify_integrity() is False


def test_decision_receipt_cryptographic_verification():
    """Verify DecisionReceipt signature token generation and verification."""
    receipt = DecisionReceipt.generate(
        run_id="RUN-LC-8841-01",
        lc_id="LC-2026-8841",
        action=ActionType.APPROVE_HONOUR,
        decision_sha256="abc123decisionhash",
        merkle_root_sha256="def456merkleroot",
        signer_name="Senior Examiner #482",
        signer_role=AuthorityLevel.DESK_HEAD,
        discrepancy_count=0,
    )

    assert receipt.signature_token.startswith("V600-SIG-")

    # Verify through AuditVerifier
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


def test_money_decimal_operations():
    """Verify Decimal-safe money operations."""
    m = Money.from_value("240000.00", "USD")
    ins_req = m.multiply_percentage(110.0)
    assert ins_req == Money.from_value("264000.00", "USD")

    # Percentage addition
    with_tolerance = m.add_percentage(5.0)
    assert with_tolerance == Money.from_value("252000.00", "USD")


def test_rules_registry_lookup():
    """Verify legal rulepack definitions."""
    rule = get_rule("UCP600-ART-28F2")
    assert rule is not None
    assert rule.citation == "UCP 600 Art. 28(f)(ii)"
    assert rule.hard_invariant_locked is True
