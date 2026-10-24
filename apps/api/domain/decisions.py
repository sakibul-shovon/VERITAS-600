"""Decision Lattice and Authoritative Sign-Off Types."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class ActionType(str, Enum):
    APPROVE_HONOUR = "APPROVE_HONOUR"
    ISSUE_MT734_REFUSAL = "ISSUE_MT734_REFUSAL"
    COMPLIANCE_HOLD_AML = "COMPLIANCE_HOLD_AML"


class AuthorityLevel(str, Enum):
    MAKER = "MAKER"
    CHECKER = "CHECKER"
    DESK_HEAD = "DESK_HEAD"
    COMPLIANCE_OFFICER = "COMPLIANCE_OFFICER"


class DispatchStatus(str, Enum):
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED_QUEUED = "APPROVED_QUEUED"
    AUTHORIZED_NOT_DISPATCHED = "AUTHORIZED_NOT_DISPATCHED"
    ACKNOWLEDGED_DISPATCHED = "ACKNOWLEDGED_DISPATCHED"


@dataclass
class DecisionReceipt:
    """Cryptographically verifiable decision receipt signed by an authorized human."""
    run_id: str
    lc_id: str
    action: ActionType
    decision_sha256: str
    merkle_root_sha256: str
    signer_name: str
    signer_role: AuthorityLevel
    signed_at_utc: str
    dispatch_status: DispatchStatus
    outbox_receipt_id: str
    signature_token: str
    discrepancy_count: int
    regulatory_hold_active: bool

    @classmethod
    def generate(
        cls,
        run_id: str,
        lc_id: str,
        action: ActionType,
        decision_sha256: str,
        merkle_root_sha256: str,
        signer_name: str,
        signer_role: AuthorityLevel = AuthorityLevel.DESK_HEAD,
        discrepancy_count: int = 0,
        regulatory_hold_active: bool = False,
    ) -> DecisionReceipt:
        signed_at = datetime.now(UTC).isoformat()
        sig_payload = f"{run_id}:{lc_id}:{action.value}:{decision_sha256}:{merkle_root_sha256}:{signer_name}:{signed_at}"

        import hmac

        from apps.api.config import get_settings
        settings = get_settings()
        secret = settings.ZTRV_HMAC_SECRET.encode("utf-8")
        mac = hmac.new(secret, sig_payload.encode("utf-8"), hashlib.sha256).hexdigest()
        sig_token = f"V600-SIG-{mac[:24].upper()}"
        outbox_id = f"OUTBOX-{lc_id}-{datetime.now(UTC).strftime('%y%m%d%H%M%S')}"

        return cls(
            run_id=run_id,
            lc_id=lc_id,
            action=action,
            decision_sha256=decision_sha256,
            merkle_root_sha256=merkle_root_sha256,
            signer_name=signer_name,
            signer_role=signer_role,
            signed_at_utc=signed_at,
            dispatch_status=DispatchStatus.AUTHORIZED_NOT_DISPATCHED,
            outbox_receipt_id=outbox_id,
            signature_token=sig_token,
            discrepancy_count=discrepancy_count,
            regulatory_hold_active=regulatory_hold_active,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "lc_id": self.lc_id,
            "action": self.action.value if hasattr(self.action, "value") else str(self.action),
            "decision_sha256": self.decision_sha256,
            "merkle_root_sha256": self.merkle_root_sha256,
            "signer_name": self.signer_name,
            "signer_role": self.signer_role.value if hasattr(self.signer_role, "value") else str(self.signer_role),
            "signed_at_utc": self.signed_at_utc,
            "dispatch_status": self.dispatch_status.value if hasattr(self.dispatch_status, "value") else str(self.dispatch_status),
            "outbox_receipt_id": self.outbox_receipt_id,
            "signature_token": self.signature_token,
            "discrepancy_count": self.discrepancy_count,
            "regulatory_hold_active": self.regulatory_hold_active,
        }
