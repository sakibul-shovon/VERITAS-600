"""Cryptographic Audit Verifier for VERITAS-600 Runs.

Validates that decision receipts match Merkle roots and that event hash chains are untampered.
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Tuple

from apps.api.audit.merkle import MerkleTree
from apps.api.audit.hash_chain import RunHashChain


class AuditVerifier:
    """Independent verification engine for trade finance runs."""

    @staticmethod
    def verify_decision_receipt(
        run_id: str,
        lc_id: str,
        action: str,
        decision_sha256: str,
        merkle_root_sha256: str,
        signer_name: str,
        signed_at_utc: str,
        signature_token: str,
    ) -> bool:
        """Verify that signature token matches run credentials."""
        sig_payload = f"{run_id}:{lc_id}:{action}:{decision_sha256}:{merkle_root_sha256}:{signer_name}:{signed_at_utc}"
        expected_token = f"V600-SIG-{hashlib.sha256(sig_payload.encode('utf-8')).hexdigest()[:24].upper()}"
        return signature_token == expected_token

    @staticmethod
    def verify_evidence_inclusion(
        leaf_sha256: str,
        merkle_proof: List[Tuple[str, str]],
        merkle_root_sha256: str,
    ) -> bool:
        """Verify that a specific evidence item is included in the Merkle tree."""
        return MerkleTree.verify_proof(leaf_sha256, merkle_proof, merkle_root_sha256)
