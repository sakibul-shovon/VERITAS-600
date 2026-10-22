"""Bank-Officer Decision Engine with Mandatory Human-in-the-Loop Sign-Off.

Synthesizes:
1. Deterministic UCP 600 Math & Dates (ucp600_deterministic.py)
2. Neural Legal Reasoning & ISBP 745 Findings (ucp600_legal_adjudicator.py)
3. Cross-Silo Risk & Customs TBML Z-Scores (zetaris/client.py)

Produces 3 Mutually Exclusive Bank Actions:
[1] APPROVE_HONOUR: Settlement authorized.
[2] ISSUE_MT734_REFUSAL: Formal refusal under UCP 600 Art. 16(c)(iii) + Demurrage Advisory.
[3] COMPLIANCE_HOLD_AML: Regulatory freeze (SAR/OFAC block), suppressing invalid MT734.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional

from apps.api.engines.ucp600_deterministic import DeterministicEvaluation
from apps.api.engines.ucp600_legal_adjudicator import LegalAdjudicationResult

ActionType = Literal["APPROVE_HONOUR", "ISSUE_MT734_REFUSAL", "COMPLIANCE_HOLD_AML"]


@dataclass
class BankDecision:
    lc_id: str
    recommended_action: ActionType
    action_title: str
    action_summary: str
    action_status: str  # 'PENDING_HUMAN_SIGN_OFF' or 'APPROVED'
    legal_citations: List[str]
    discrepancies: List[str]
    regulatory_flags: List[str]
    demurrage_savings_advisory: Optional[Dict[str, Any]]
    execution_telemetry: Dict[str, Any]
    human_approved_by: Optional[str] = None
    human_approved_at: Optional[str] = None


class BankDecisionEngine:
    """Trade Finance Officer decision synthesiser and regulatory gate."""

    def evaluate(
        self,
        lc_id: str,
        active_lc: Dict[str, Any],
        presentation: Dict[str, Any],
        deterministic_eval: DeterministicEvaluation,
        legal_eval: LegalAdjudicationResult,
        federated_risk: Dict[str, Any],
    ) -> BankDecision:
        """Synthesize all engine findings into a single authoritative bank action."""
        fed_row = federated_risk.get("row", {})
        z_score = float(fed_row.get("tbml_price_zscore") or 0.0)
        sanction_hits = int(fed_row.get("sanction_hit_count") or 0)
        sanctions_summary = fed_row.get("sanctions_summary") or ""

        # Collect discrepancies
        discrepancies: List[str] = []
        citations: List[str] = []
        regulatory_flags: List[str] = []

        # 1. Deterministic Failures
        for check in deterministic_eval.checks:
            if not check.passed:
                discrepancies.append(f"{check.name}: {check.details} ({check.ucp_citation})")
                citations.append(check.ucp_citation)

        # 2. Neural Legal Discrepancies
        for finding in legal_eval.findings:
            if finding.is_discrepant:
                discrepancies.append(f"{finding.divergence_item}: {finding.legal_reasoning} ({finding.ucp_isbp_citation})")
                citations.append(finding.ucp_isbp_citation)
            elif finding.verdict == "COMPLIANT_PROTECTED":
                citations.append(finding.ucp_isbp_citation)

        # 3. Regulatory / TBML Anomaly Check
        is_tbml_anomaly = z_score > 4.0
        is_sanctions_hit = sanction_hits > 0

        if is_tbml_anomaly:
            regulatory_flags.append(
                f"Severe Trade-Based Money Laundering (TBML) Unit Price Anomaly: Z-score = +{z_score:.2f} "
                f"vs 6-digit HS customs distribution mean."
            )
        if is_sanctions_hit:
            regulatory_flags.append(
                f"OpenSanctions Watchlist Match ({sanction_hits} hit): {sanctions_summary}"
            )

        # ----------------------------------------------------------------------
        # Synthesize Final Action
        # ----------------------------------------------------------------------
        # Rule A: Financial Crime / Sanctions ALWAYS overrides documentary compliance
        if is_tbml_anomaly or is_sanctions_hit:
            action: ActionType = "COMPLIANCE_HOLD_AML"
            title = "COMPLIANCE HOLD & REGULATORY FREEZE (AML/OFAC)"
            summary = (
                "Settlement blocked immediately due to cross-silo financial crime indicators. "
                "Notice of Refusal (MT734) suppressed under international sanctions regulations; "
                "escalating to Financial Crime Compliance (SAR/OFAC Hold)."
            )
            citations.append("OFAC / Financial Crime Regulations (Non-MT734 Freeze)")

        # Rule B: Documentary Discrepancies Exist -> Issue MT734 Notice of Refusal
        elif len(discrepancies) > 0 or not deterministic_eval.all_passed or legal_eval.final_locked_verdict == "DISCREPANT":
            action = "ISSUE_MT734_REFUSAL"
            title = "ISSUE SWIFT MT734 NOTICE OF REFUSAL"
            summary = (
                f"Documentary discrepancies identified under ICC UCP 600. "
                f"Holding documents at presenting party's disposal under Art. 16(c)(iii)(a). "
                f"Demurrage-saving cure advisory attached."
            )
            citations.append("UCP 600 Art. 16(c)(iii)")

        # Rule C: All Checks Pass (or protected under ISBP A23 / Art. 14(e))
        else:
            action = "APPROVE_HONOUR"
            title = "APPROVE & HONOUR SETTLEMENT"
            summary = (
                "All presentation documents comply with UCP 600 and credit terms on their face. "
                "Typographical errors (if any) are legally protected under ISBP 745 Para A23. "
                "Authorizing release of funds to beneficiary."
            )
            citations.append("UCP 600 Art. 15(a)")

        telemetry = {
            "zetaris_mode": federated_risk.get("execution_mode", "LOCAL_DUCKDB_FALLBACK"),
            "zetaris_query_ms": federated_risk.get("query_ms", 12),
            "deterministic_passed": deterministic_eval.all_passed,
            "neural_status": legal_eval.overall_legal_status,
            "hard_invariant_enforced": legal_eval.hard_invariant_enforced,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        return BankDecision(
            lc_id=lc_id,
            recommended_action=action,
            action_title=title,
            action_summary=summary,
            action_status="PENDING_HUMAN_SIGN_OFF",
            legal_citations=list(dict.fromkeys(citations)),  # unique
            discrepancies=discrepancies,
            regulatory_flags=regulatory_flags,
            demurrage_savings_advisory=deterministic_eval.demurrage_analysis,
            execution_telemetry=telemetry,
        )
