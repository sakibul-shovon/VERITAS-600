"""Stateful Amendment Memory & UCP 600 Art. 10 Resolver.

Implements UCP 600 Art. 10(c) & 10(e) rules:
- Art. 10(c): Terms of the original credit remain in force until beneficiary communicates
  acceptance or presents documents complying with the amendment.
- Art. 10(e): Partial acceptance of an amendment is NOT allowed and is deemed rejection.
- Computes SHA-256 audit hash of active term lineage.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Dict, List, Literal, Optional, Tuple

AcceptanceStatus = Literal["ACCEPTED", "REJECTED", "UNACCEPTED_PENDING"]


@dataclass
class TermRecord:
    field_key: str
    value: Any
    source_doc: str  # e.g., 'MT700' or 'AMD-8841-01'
    status: AcceptanceStatus
    sequence_no: int
    effective_date: str


@dataclass
class AmendmentResolution:
    active_terms: Dict[str, Any]
    active_terms_sha256: str
    accepted_amendments: List[Dict[str, Any]]
    quarantined_amendments: List[Dict[str, Any]]
    implicit_acceptance_detected: bool
    partial_acceptance_violation: bool
    violation_details: Optional[str] = None


class AmendmentMemoryEngine:
    """Stateful memory resolver governing MT700 base terms and MT707 amendments."""

    def __init__(self):
        pass

    def build_active_state(
        self,
        base_lc: Dict[str, Any],
        amendments: List[Dict[str, Any]],
        presentation_fields: Optional[Dict[str, Any]] = None,
    ) -> AmendmentResolution:
        """Resolve active terms under UCP 600 Art. 10(c) and 10(e).

        Args:
            base_lc: Dictionary of original MT700 master fields.
            amendments: Ordered list of amendment records.
            presentation_fields: Optional extracted document fields from presentation.
        """
        # 1. Initialize active terms with baseline MT700
        active_terms = dict(base_lc)
        accepted_list: List[Dict[str, Any]] = []
        quarantined_list: List[Dict[str, Any]] = []

        # Sort amendments by sequence number
        sorted_amds = sorted(amendments, key=lambda x: x.get("sequence_no", 0))

        # Track unaccepted amendments grouped by amendment_id
        pending_by_id: Dict[str, List[Dict[str, Any]]] = {}

        for amd in sorted_amds:
            status = amd.get("beneficiary_acceptance_status", "UNACCEPTED_PENDING")
            field = amd["amended_field"]
            new_val = amd["new_value"]

            if status == "ACCEPTED":
                active_terms[field] = new_val
                accepted_list.append(amd)
            elif status == "UNACCEPTED_PENDING":
                quarantined_list.append(amd)
                amd_id = amd.get("amendment_id", f"AMD-{amd.get('sequence_no')}")
                pending_by_id.setdefault(amd_id, []).append(amd)
            elif status == "REJECTED":
                # Rejected amendments do not modify active terms
                pass

        # 2. Evaluate Art. 10(c) & 10(e) if presentation fields are provided
        implicit_acceptance_detected = False
        partial_acceptance_violation = False
        violation_details = None

        if presentation_fields and pending_by_id:
            for amd_id, items in pending_by_id.items():
                matches = []
                conflicts = []

                for item in items:
                    field = item["amended_field"]
                    new_val = str(item["new_value"]).strip().lower()
                    old_val = str(item["old_value"]).strip().lower()

                    # Map LC fields to presentation fields
                    pres_val = None
                    if field == "latest_shipment_date" and "bl_on_board_date" in presentation_fields:
                        pres_val = str(presentation_fields["bl_on_board_date"]).strip().lower()
                        # If shipment is past old latest date but within new latest date, implicit acceptance
                        if pres_val > old_val and pres_val <= new_val:
                            matches.append(field)
                        elif pres_val <= old_val:
                            # Adhered to original
                            pass
                        else:
                            conflicts.append(field)

                    elif field == "port_of_discharge" and "port_of_discharge" in presentation_fields:
                        pres_val = str(presentation_fields["port_of_discharge"]).strip().lower()
                        if pres_val == new_val:
                            matches.append(field)
                        elif pres_val == old_val:
                            pass
                        else:
                            conflicts.append(field)

                    elif field == "unit_price" and "invoice_unit_price" in presentation_fields:
                        pres_val = str(presentation_fields["invoice_unit_price"]).strip().lower()
                        if pres_val == new_val:
                            matches.append(field)
                        elif pres_val == old_val:
                            pass
                        else:
                            conflicts.append(field)

                # Check Art. 10(e): Partial acceptance prohibited
                if len(matches) > 0 and len(matches) < len(items):
                    partial_acceptance_violation = True
                    unmatched = [it["amended_field"] for it in items if it["amended_field"] not in matches]
                    violation_details = (
                        f"Partial acceptance of amendment {amd_id} detected: presentation conforms to {matches} "
                        f"while retaining original/non-conforming values for {unmatched}. "
                        f"Prohibited under UCP 600 Art. 10(e)."
                    )
                elif len(matches) == len(items) and len(items) > 0:
                    # Full implicit acceptance via documents under Art. 10(c)
                    implicit_acceptance_detected = True
                    for item in items:
                        active_terms[item["amended_field"]] = item["new_value"]

        # 3. Compute immutable SHA-256 fingerprint of resolved active terms
        normalized_json = json.dumps(active_terms, sort_keys=True, default=str)
        audit_hash = hashlib.sha256(normalized_json.encode("utf-8")).hexdigest()

        return AmendmentResolution(
            active_terms=active_terms,
            active_terms_sha256=audit_hash,
            accepted_amendments=accepted_list,
            quarantined_amendments=quarantined_list,
            implicit_acceptance_detected=implicit_acceptance_detected,
            partial_acceptance_violation=partial_acceptance_violation,
            violation_details=violation_details,
        )
