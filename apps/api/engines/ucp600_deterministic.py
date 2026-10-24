"""Deterministic UCP 600 Symbolic Engine.

Handles all mathematical calculations, temporal verifications, financial tolerances,
insurance coverage requirements, and physical weight cross-checks.

HARD INVARIANT RULE:
A neural LLM verdict can NEVER override a failed deterministic check.
If any check in this engine fails, the presentation is permanently locked to DISCREPANT.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any


@dataclass
class DeterministicCheckResult:
    check_id: str
    name: str
    ucp_citation: str
    passed: bool
    severity: str  # 'COMPLIANT' or 'FATAL_DISCREPANCY'
    details: str
    computed_values: dict[str, Any]


@dataclass
class DeterministicEvaluation:
    all_passed: bool
    failed_checks_count: int
    checks: list[DeterministicCheckResult]
    demurrage_analysis: dict[str, Any] | None = None


def parse_date(date_val: Any) -> date | None:
    """Parse date from string or date/datetime object across common trade formats.

    Supports ISO (YYYY-MM-DD), slash-delimited (DD/MM/YYYY, MM/DD/YYYY, YYYY/MM/DD),
    dash-delimited (DD-MM-YYYY), and dot-delimited formats.
    Returns None if date_val is None or empty.
    """
    if date_val is None:
        return None
    if isinstance(date_val, date) and not isinstance(date_val, datetime):
        return date_val
    if isinstance(date_val, datetime):
        return date_val.date()
    date_str = str(date_val).strip()
    if not date_str:
        return None

    formats = (
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%d.%m.%Y",
        "%Y.%m.%d",
    )
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(date_str).date()
    except Exception:
        pass
    raise ValueError(f"Unable to parse date string: '{date_str}'")


class UCP600DeterministicEngine:
    """Pure Python Symbolic Engine for ICC UCP 600 validation."""

    def evaluate_presentation(
        self,
        active_lc: dict[str, Any],
        presentation: dict[str, Any],
    ) -> DeterministicEvaluation:
        """Run all deterministic mathematical, temporal, insurance, and weight checks."""
        results: list[DeterministicCheckResult] = []

        # ----------------------------------------------------------------------
        # 1. Temporal Checks
        # ----------------------------------------------------------------------
        pres_date_val = presentation.get("presentation_date")
        pres_date = parse_date(pres_date_val) if pres_date_val else date.today()
        if not pres_date:
            pres_date = date.today()

        expiry_date = parse_date(active_lc.get("expiry_date"))
        if not expiry_date:
            raise ValueError(f"Active LC missing valid expiry_date: {active_lc.get('expiry_date')}")

        latest_shipment_date = parse_date(active_lc.get("latest_shipment_date")) or expiry_date

        bl_board_raw = presentation.get("bl_on_board_date")
        has_bl_on_board = bool(bl_board_raw and str(bl_board_raw).strip())
        bl_date = parse_date(bl_board_raw) if has_bl_on_board else None
        shipment_date = bl_date or latest_shipment_date

        # Check 1.1: Presentation Date <= Expiry Date (Art. 6(d)(i))
        passed_expiry = pres_date <= expiry_date
        results.append(
            DeterministicCheckResult(
                check_id="TEMPORAL_EXPIRY_DATE",
                name="Presentation Within Expiry Date",
                ucp_citation="UCP 600 Art. 6(d)(i)",
                passed=passed_expiry,
                severity="COMPLIANT" if passed_expiry else "FATAL_DISCREPANCY",
                details=(
                    f"Presentation date ({pres_date}) is within LC expiry date ({expiry_date})"
                    if passed_expiry
                    else f"Presentation date ({pres_date}) is past LC expiry date ({expiry_date})"
                ),
                computed_values={"presentation_date": str(pres_date), "expiry_date": str(expiry_date)},
            )
        )

        # Check 1.2: 21-Day Presentation Window (Art. 14(c))
        presentation_period = int(active_lc.get("presentation_period_days", 21))
        max_presentation_date = shipment_date + timedelta(days=presentation_period)
        days_after_shipment = (pres_date - shipment_date).days
        days_remaining_in_window = (max_presentation_date - pres_date).days
        passed_window = pres_date <= max_presentation_date

        results.append(
            DeterministicCheckResult(
                check_id="TEMPORAL_21_DAY_WINDOW",
                name="21-Day Presentation Window",
                ucp_citation="UCP 600 Art. 14(c)",
                passed=passed_window,
                severity="COMPLIANT" if passed_window else "FATAL_DISCREPANCY",
                details=(
                    f"Presented {days_after_shipment} days after shipment date ({shipment_date}). "
                    f"{max(0, days_remaining_in_window)} days remain in presentation period."
                    if passed_window
                    else f"Late presentation: presented {days_after_shipment} days after shipment. "
                    f"Maximum allowed is {presentation_period} days ({max_presentation_date})."
                ),
                computed_values={
                    "shipment_date": str(shipment_date),
                    "presentation_date": str(pres_date),
                    "days_after_shipment": days_after_shipment,
                    "days_remaining_in_window": max(0, days_remaining_in_window),
                },
            )
        )

        # Check 1.3: Shipment Date <= Effective Latest Shipment Date (Art. 20(a)(ii))
        if bl_date is not None:
            passed_shipment = bl_date <= latest_shipment_date
            details = (
                f"Bill of Lading on-board date ({bl_date}) is on or before latest shipment date ({latest_shipment_date})"
                if passed_shipment
                else f"Late shipment: Bill of Lading on-board date ({bl_date}) exceeds latest shipment date ({latest_shipment_date})"
            )
            computed_shipment = str(bl_date)
        elif "bl_on_board_date" in presentation and not has_bl_on_board:
            # Document record present but no date extracted
            passed_shipment = False
            details = "Transport document missing mandatory on-board notation/date under UCP 600 Art. 20(a)(ii)"
            computed_shipment = "MISSING"
        else:
            passed_shipment = shipment_date <= latest_shipment_date
            details = f"Shipment inferred within latest date ({latest_shipment_date})"
            computed_shipment = str(shipment_date)

        results.append(
            DeterministicCheckResult(
                check_id="TEMPORAL_LATEST_SHIPMENT",
                name="On-Board Date vs Latest Shipment Date",
                ucp_citation="UCP 600 Art. 20(a)(ii)",
                passed=passed_shipment,
                severity="COMPLIANT" if passed_shipment else "FATAL_DISCREPANCY",
                details=details,
                computed_values={"bl_on_board_date": computed_shipment, "latest_shipment_date": str(latest_shipment_date)},
            )
        )

        # ----------------------------------------------------------------------
        # 2. Financial & Quantity Math
        # ----------------------------------------------------------------------
        lc_amount = float(active_lc["amount"])
        tolerance_pct = float(active_lc.get("tolerance_pct", 0.0))
        max_allowed_amount = round(lc_amount * (1.0 + tolerance_pct / 100.0), 2)
        invoice_amount = float(presentation.get("invoice_amount", 0.0))

        # Check 2.1: Invoice Amount <= Credit Limit (Art. 18(b))
        passed_amount = invoice_amount <= max_allowed_amount
        results.append(
            DeterministicCheckResult(
                check_id="FINANCIAL_INVOICE_AMOUNT",
                name="Invoice Amount vs LC Drawing Limit",
                ucp_citation="UCP 600 Art. 18(b)",
                passed=passed_amount,
                severity="COMPLIANT" if passed_amount else "FATAL_DISCREPANCY",
                details=(
                    f"Invoice amount (${invoice_amount:,.2f}) within credit limit (${max_allowed_amount:,.2f})"
                    if passed_amount
                    else f"Invoice amount (${invoice_amount:,.2f}) exceeds credit limit (${max_allowed_amount:,.2f})"
                ),
                computed_values={"invoice_amount": invoice_amount, "max_allowed_amount": max_allowed_amount},
            )
        )

        # Check 2.2: Unit Price Math Consistency
        inv_qty = presentation.get("invoice_quantity")
        inv_unit_price = presentation.get("invoice_unit_price")
        if inv_qty and inv_unit_price:
            expected_total = round(float(inv_qty) * float(inv_unit_price), 2)
            passed_unit_math = abs(invoice_amount - expected_total) <= 0.05
            results.append(
                DeterministicCheckResult(
                    check_id="FINANCIAL_UNIT_PRICE_MATH",
                    name="Unit Price Arithmetic Consistency",
                    ucp_citation="UCP 600 Art. 18(a)(iii)",
                    passed=passed_unit_math,
                    severity="COMPLIANT" if passed_unit_math else "FATAL_DISCREPANCY",
                    details=(
                        f"Invoice total matches quantity ({inv_qty}) x unit price (${inv_unit_price}) = ${expected_total:,.2f}"
                        if passed_unit_math
                        else f"Arithmetic error in invoice: {inv_qty} x ${inv_unit_price} = ${expected_total:,.2f}, but total is stated as ${invoice_amount:,.2f}"
                    ),
                    computed_values={"quantity": inv_qty, "unit_price": inv_unit_price, "expected_total": expected_total},
                )
            )

        # ----------------------------------------------------------------------
        # 3. Insurance Coverage & Document Type (Art. 28)
        # ----------------------------------------------------------------------
        insurance_doc_type = str(presentation.get("insurance_doc_type", "Insurance Certificate")).strip()
        insurance_amount = float(presentation.get("insurance_amount", 0.0))
        min_insured_pct = float(active_lc.get("insurance_min_pct", 110.0))

        # Check 3.1: Reject Cover Notes (Art. 28(c))
        is_cover_note = "cover note" in insurance_doc_type.lower()
        passed_doc_type = not is_cover_note
        results.append(
            DeterministicCheckResult(
                check_id="INSURANCE_DOCUMENT_TYPE",
                name="Insurance Document Type (Cover Notes Prohibited)",
                ucp_citation="UCP 600 Art. 28(c)",
                passed=passed_doc_type,
                severity="COMPLIANT" if passed_doc_type else "FATAL_DISCREPANCY",
                details=(
                    f"Presented valid insurance document type: '{insurance_doc_type}'"
                    if passed_doc_type
                    else "Cover Notes are expressly prohibited and not acceptable under UCP 600 Art. 28(c)"
                ),
                computed_values={"presented_doc_type": insurance_doc_type},
            )
        )

        # Check 3.2: Minimum 110% Coverage of CIF/CIP Value (Art. 28(f)(ii))
        # UCP 600 Art. 28(f)(ii): Basis is CIF/CIP value of goods, or gross invoice/honour value if CIF not stated.
        cif_basis = invoice_amount if invoice_amount > 0 else float(active_lc.get("amount", 0.0))
        required_insurance_min = round(cif_basis * (min_insured_pct / 100.0), 2)
        insurance_shortfall = round(max(0.0, required_insurance_min - insurance_amount), 2)
        actual_coverage_pct = round((insurance_amount / cif_basis) * 100.0, 2) if cif_basis > 0 else 0.0
        passed_insurance_min = insurance_amount >= required_insurance_min

        results.append(
            DeterministicCheckResult(
                check_id="INSURANCE_MINIMUM_COVERAGE",
                name="110% CIF/CIP Minimum Insurance Coverage",
                ucp_citation="UCP 600 Art. 28(f)(ii)",
                passed=passed_insurance_min,
                severity="COMPLIANT" if passed_insurance_min else "FATAL_DISCREPANCY",
                details=(
                    f"Insured amount (${insurance_amount:,.2f}) covers {actual_coverage_pct:.1f}% of CIF value (${cif_basis:,.2f}), exceeding {min_insured_pct}% minimum requirement (${required_insurance_min:,.2f})"
                    if passed_insurance_min
                    else f"Insurance under-covered: Presented ${insurance_amount:,.2f} ({actual_coverage_pct:.1f}% of CIF value), creating a ${insurance_shortfall:,.2f} shortfall against the {min_insured_pct}% minimum (${required_insurance_min:,.2f})"
                ),
                computed_values={
                    "cif_basis": cif_basis,
                    "insurance_amount": insurance_amount,
                    "required_insurance_min": required_insurance_min,
                    "shortfall_usd": insurance_shortfall,
                    "actual_coverage_pct": actual_coverage_pct,
                },
            )
        )

        # Check 3.3: Insurance Date Prior to or On Shipment Date (Art. 28(e))
        ins_date_raw = (
            presentation.get("insurance_issue_date")
            or presentation.get("insurance_effective_date")
            or presentation.get("insurance_date")
        )
        if ins_date_raw and str(ins_date_raw).strip():
            ins_eff_date = parse_date(ins_date_raw)
            if ins_eff_date and shipment_date:
                passed_ins_date = ins_eff_date <= shipment_date
                results.append(
                    DeterministicCheckResult(
                        check_id="INSURANCE_EFFECTIVE_DATE",
                        name="Insurance Date Prior to Shipment",
                        ucp_citation="UCP 600 Art. 28(e)",
                        passed=passed_ins_date,
                        severity="COMPLIANT" if passed_ins_date else "FATAL_DISCREPANCY",
                        details=(
                            f"Insurance document/effective date ({ins_eff_date}) is on or before shipment date ({shipment_date})"
                            if passed_ins_date
                            else f"Insurance date ({ins_eff_date}) is later than shipment date ({shipment_date})"
                        ),
                        computed_values={"insurance_effective_date": str(ins_eff_date), "shipment_date": str(shipment_date)},
                    )
                )

        # ----------------------------------------------------------------------
        # 4. Cross-Document Weight Matching (Art. 14(d))
        # ----------------------------------------------------------------------
        packing_gross_wt = presentation.get("packing_gross_weight_kg")
        bl_gross_wt = presentation.get("bl_gross_weight_kg")

        if packing_gross_wt is not None and bl_gross_wt is not None:
            packing_wt = float(packing_gross_wt)
            bl_wt = float(bl_gross_wt)
            # Only perform cross-reconciliation if at least one weight is non-zero (avoid 0==0 silent pass)
            if packing_wt > 0 or bl_wt > 0:
                weight_diff = abs(packing_wt - bl_wt)
                # Allow rounding / minor tolerance (0.1% or 0.5 kg)
                allowed_tol = max(0.5, 0.001 * max(packing_wt, bl_wt))
                passed_weight = weight_diff <= allowed_tol

                results.append(
                    DeterministicCheckResult(
                        check_id="CROSS_DOC_WEIGHT_RECONCILIATION",
                        name="Gross Weight Consistency (Packing List vs B/L)",
                        ucp_citation="UCP 600 Art. 14(d)",
                        passed=passed_weight,
                        severity="COMPLIANT" if passed_weight else "FATAL_DISCREPANCY",
                        details=(
                            f"Gross weight matches across Packing List and Bill of Lading ({bl_wt:,.2f} kg)"
                            if passed_weight
                            else f"Weight conflict: Packing List states {packing_wt:,.2f} kg while Bill of Lading states {bl_wt:,.2f} kg (Variance: {weight_diff:,.2f} kg)"
                        ),
                        computed_values={
                            "packing_gross_weight_kg": packing_wt,
                            "bl_gross_weight_kg": bl_wt,
                            "weight_diff_kg": weight_diff,
                        },
                    )
                )

        # ----------------------------------------------------------------------
        # Demurrage Savings Advisory Calculation (For Curable Discrepancies)
        # ----------------------------------------------------------------------
        failed_checks = [c for c in results if not c.passed]
        demurrage_analysis = None

        if failed_checks and days_remaining_in_window > 0:
            daily_demurrage = float(active_lc.get("daily_demurrage_usd", 1850.0))
            # Option A: Beneficiary Cures & Re-presents within 48h (2 days)
            cured_turnaround_days = 2
            # Option B: Bank waits for Applicant Waiver (typical 6 to 8 banking days)
            applicant_waiver_days = 8

            waiver_demurrage_cost = round(applicant_waiver_days * daily_demurrage, 2)
            cured_demurrage_cost = round(cured_turnaround_days * daily_demurrage, 2)
            net_savings = round(waiver_demurrage_cost - cured_demurrage_cost, 2)

            demurrage_analysis = {
                "days_remaining_in_window": days_remaining_in_window,
                "daily_demurrage_usd": daily_demurrage,
                "applicant_waiver_days": applicant_waiver_days,
                "waiver_demurrage_cost": waiver_demurrage_cost,
                "cured_re_presentation_days": cured_turnaround_days,
                "cured_demurrage_cost": cured_demurrage_cost,
                "net_savings_usd": net_savings,
                "advisory": (
                    f"{max(0, days_remaining_in_window)} days remain in the UCP 600 Art. 14(c) presentation window. "
                    f"Re-presenting cured documents within 48h saves ${net_savings:,.2f} "
                    f"in port demurrage vs waiting for applicant waiver."
                ),
            }

        return DeterministicEvaluation(
            all_passed=len(failed_checks) == 0,
            failed_checks_count=len(failed_checks),
            checks=results,
            demurrage_analysis=demurrage_analysis,
        )
