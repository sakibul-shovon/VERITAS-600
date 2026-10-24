"""Canonical Evidence Models and Bounding Box Envelopes."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class BoundingBox:
    """Normalized spatial coordinates [ymin, xmin, ymax, xmax] in 0-1000 scale."""
    ymin: int
    xmin: int
    ymax: int
    xmax: int

    def to_list(self) -> list[int]:
        return [self.ymin, self.xmin, self.ymax, self.xmax]

    @classmethod
    def from_list(cls, coords: list[int]) -> BoundingBox:
        if len(coords) != 4:
            raise ValueError("Bounding box must have 4 integers [ymin, xmin, ymax, xmax]")
        return cls(ymin=coords[0], xmin=coords[1], ymax=coords[2], xmax=coords[3])


@dataclass
class EvidenceRecord:
    """A tamper-evident extracted document field linked to spatial coordinates."""
    evidence_id: str
    field_key: str
    source_document: str
    raw_value: Any
    normalized_value: Any
    confidence: float
    bounding_box: list[int]
    source_digest_sha256: str
    timestamp_utc: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def compute_sha256(self) -> str:
        """Deterministic digest of this evidence record."""
        canonical_str = (
            f"{self.evidence_id}:{self.field_key}:{self.source_document}:"
            f"{self.normalized_value}:{self.confidence}:{self.bounding_box}:{self.source_digest_sha256}"
        )
        return hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceManifest:
    """Collection of evidence records for an examination run."""
    run_id: str
    lc_id: str
    records: list[EvidenceRecord] = field(default_factory=list)

    def add_record(self, record: EvidenceRecord) -> None:
        self.records.append(record)

    def leaf_hashes(self) -> list[str]:
        return [r.compute_sha256() for r in self.records]

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "lc_id": self.lc_id,
            "record_count": len(self.records),
            "records": [r.to_dict() for r in self.records],
            "leaf_hashes": self.leaf_hashes(),
        }
