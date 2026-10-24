"""Cryptographic Audit Verifier for VERITAS-600 Runs.

Validates that decision receipts match Merkle roots and that event hash chains are untampered.
"""

from __future__ import annotations

import hashlib

from apps.api.audit.merkle import MerkleTree


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
        """Verify that signature token matches run credentials using keyed HMAC-SHA256."""
        sig_payload = f"{run_id}:{lc_id}:{action}:{decision_sha256}:{merkle_root_sha256}:{signer_name}:{signed_at_utc}"
        import hmac

        from apps.api.config import get_settings
        settings = get_settings()
        secret = settings.ZTRV_HMAC_SECRET.encode("utf-8")
        mac = hmac.new(secret, sig_payload.encode("utf-8"), hashlib.sha256).hexdigest()
        expected_token = f"V600-SIG-{mac[:24].upper()}"
        return signature_token == expected_token

    @staticmethod
    def verify_evidence_inclusion(
        leaf_sha256: str,
        merkle_proof: list[tuple[str, str]],
        merkle_root_sha256: str,
    ) -> bool:
        """Verify that a specific evidence item is included in the Merkle tree."""
        return MerkleTree.verify_proof(leaf_sha256, merkle_proof, merkle_root_sha256)
