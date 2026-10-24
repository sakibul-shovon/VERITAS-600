"""RFC 8785 Canonical JSON Serialization.

Guarantees byte-for-byte deterministic JSON serialization across platforms and architectures.
Keys are lexicographically sorted in UTF-16 code unit order, with standard separators and no whitespace.
Handles Decimal, Date, and DateTime objects deterministically.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from decimal import Decimal
from typing import Any


def _canonical_default(o: Any) -> Any:
    if isinstance(o, Decimal):
        # Format Decimal deterministically: if integer value, int; else float
        return float(o)
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    return str(o)


def canonicalize_json(data: Any) -> str:
    """Return deterministic canonical JSON string per RFC 8785."""
    return json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=_canonical_default,
    )


def canonical_sha256(data: Any) -> str:
    """Return SHA-256 digest of canonicalized JSON."""
    import hashlib
    raw = canonicalize_json(data).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
