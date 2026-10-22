"""Append-Only Event Hash Chain for Examination Runs.

Ensures that examination events cannot be inserted, deleted, or reordered after emission.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List, Optional

from apps.api.audit.canonical_json import canonical_sha256, canonicalize_json


@dataclass
class ChainEvent:
    sequence_no: int
    event_type: str
    stage_id: Optional[str]
    payload: Dict[str, Any]
    prev_hash: str
    event_hash: str
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @classmethod
    def create(
        cls,
        sequence_no: int,
        event_type: str,
        stage_id: Optional[str],
        payload: Dict[str, Any],
        prev_hash: str,
    ) -> ChainEvent:
        canonical_p = canonicalize_json(payload)
        header = f"{sequence_no}:{event_type}:{stage_id or ''}:{prev_hash}:{canonical_p}"
        event_hash = hashlib.sha256(header.encode("utf-8")).hexdigest()
        return cls(
            sequence_no=sequence_no,
            event_type=event_type,
            stage_id=stage_id,
            payload=payload,
            prev_hash=prev_hash,
            event_hash=event_hash,
        )


class RunHashChain:
    """Maintains an append-only hash chain of examination events."""

    GENESIS_HASH = "0" * 64

    def __init__(self, run_id: str):
        self.run_id = run_id
        self.events: List[ChainEvent] = []

    @property
    def latest_hash(self) -> str:
        return self.events[-1].event_hash if self.events else self.GENESIS_HASH

    def append_event(self, event_type: str, payload: Dict[str, Any], stage_id: Optional[str] = None) -> ChainEvent:
        seq = len(self.events) + 1
        prev = self.latest_hash
        event = ChainEvent.create(
            sequence_no=seq,
            event_type=event_type,
            stage_id=stage_id,
            payload=payload,
            prev_hash=prev,
        )
        self.events.append(event)
        return event

    def verify_integrity(self) -> bool:
        """Verify that every event correctly links to its predecessor."""
        expected_prev = self.GENESIS_HASH
        for event in self.events:
            if event.prev_hash != expected_prev:
                return False
            # Recompute hash
            canonical_p = canonicalize_json(event.payload)
            header = f"{event.sequence_no}:{event.event_type}:{event.stage_id or ''}:{event.prev_hash}:{canonical_p}"
            expected_hash = hashlib.sha256(header.encode("utf-8")).hexdigest()
            if event.event_hash != expected_hash:
                return False
            expected_prev = event.event_hash
        return True

    def to_list(self) -> List[Dict[str, Any]]:
        return [asdict(e) for e in self.events]
