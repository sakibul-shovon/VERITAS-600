"""UCP 600 & ISBP 745 Neural Legal Adjudicator Engine.

Uses NVIDIA Nemotron LLM to resolve lexical variations, evaluate typographical errors
under ISBP 745 Para A23, and verify general vs. strict descriptions under UCP 600 Art. 14(e) & 18(c).

ENFORCES THE HARD INVARIANT RULE:
A neural LLM verdict can NEVER override a failed deterministic check.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from typing import Any, Dict, List, Optional

from apps.api.engines.ucp600_deterministic import DeterministicEvaluation
from apps.api.inference.nim_client import NvidiaNimClient


@dataclass
class LegalFinding:
    divergence_item: str
    source_documents: List[str]
    verdict: str  # 'COMPLIANT_PROTECTED', 'COMPLIANT', 'DISCREPANT'
    is_discrepant: bool
    ucp_isbp_citation: str
    legal_reasoning: str
    confidence: float


@dataclass
class LegalAdjudicationResult:
    overall_legal_status: str  # 'COMPLIANT', 'COMPLIANT_PROTECTED', 'DISCREPANT'
    findings: List[LegalFinding]
    hard_invariant_enforced: bool
    final_locked_verdict: str  # 'COMPLIANT' or 'DISCREPANT'


class UCP600LegalAdjudicator:
    """Legal semantic judge powered by NVIDIA Nemotron with deterministic invariant guardrails."""

    def __init__(self, nim_client: Optional[NvidiaNimClient] = None):
        self.nim_client = nim_client or NvidiaNimClient()

    def adjudicate_presentation(
        self,
        active_lc: Dict[str, Any],
        presentation: Dict[str, Any],
        deterministic_eval: Optional[DeterministicEvaluation] = None,
    ) -> LegalAdjudicationResult:
        """Run legal adjudication across all textual and lexical fields.

        Enforces the Hard Invariant Rule: if deterministic checks failed,
        the final verdict is strictly locked to DISCREPANT.
        """
        findings: List[LegalFinding] = []

        # 1. Evaluate Goods Description: Commercial Invoice vs LC (Art. 18(c) & ISBP 745 A23)
        lc_goods = active_lc.get("goods_description_strict", "")
        inv_goods = presentation.get("invoice_goods_description", "")

        if inv_goods and lc_goods:
            prompt = (
                f"LETTER OF CREDIT GOODS SPECIFICATION:\n{lc_goods}\n\n"
                f"COMMERCIAL INVOICE GOODS DESCRIPTION:\n{inv_goods}\n\n"
                "Evaluate whether any discrepancy exists under UCP 600 Art. 18(c) (strict invoice description) "
                "or whether any typographical error is legally protected under ISBP 745 Para A23 "
                "(misspelling/typing error not altering word/sentence meaning). "
                "Output JSON with keys: verdict, ucp_isbp_citation, is_discrepancy, legal_reasoning, confidence."
            )
            res = self.nim_client.complete(prompt)
            data = json.loads(res["content"])
            findings.append(
                LegalFinding(
                    divergence_item="Commercial Invoice Goods Description",
                    source_documents=["MT700 Credit", "Commercial Invoice"],
                    verdict=data.get("verdict", "COMPLIANT"),
                    is_discrepant=data.get("is_discrepancy", False),
                    ucp_isbp_citation=data.get("ucp_isbp_citation", "ISBP 745 Para A23"),
                    legal_reasoning=data.get("legal_reasoning", ""),
                    confidence=float(data.get("confidence", 0.95)),
                )
            )

        # 2. Evaluate Ocean Bill of Lading Description (Art. 14(e))
        bl_goods = presentation.get("bl_goods_description", "")
        if bl_goods and lc_goods:
            prompt = (
                f"LETTER OF CREDIT GOODS SPECIFICATION:\n{lc_goods}\n\n"
                f"OCEAN BILL OF LADING GOODS DESCRIPTION:\n{bl_goods}\n\n"
                "Evaluate whether the goods description on this transport document is permissible in general terms "
                "not conflicting with the credit under UCP 600 Art. 14(e). "
                "Output JSON with keys: verdict, ucp_isbp_citation, is_discrepancy, legal_reasoning, confidence."
            )
            res = self.nim_client.complete(prompt)
            data = json.loads(res["content"])
            findings.append(
                LegalFinding(
                    divergence_item="Ocean Bill of Lading Goods Description",
                    source_documents=["MT700 Credit", "Ocean Bill of Lading"],
                    verdict=data.get("verdict", "COMPLIANT_PROTECTED"),
                    is_discrepant=data.get("is_discrepancy", False),
                    ucp_isbp_citation=data.get("ucp_isbp_citation", "UCP 600 Art. 14(e)"),
                    legal_reasoning=data.get("legal_reasoning", ""),
                    confidence=float(data.get("confidence", 0.98)),
                )
            )

        # 3. Evaluate Transport Document Consignee / Notify Box Address (Art. 14(j))
        bl_notify = presentation.get("bl_notify_party", "")
        applicant_address = active_lc.get("applicant_address_strict", "")
        if bl_notify and applicant_address:
            # If notify box contains applicant name/address, check strict address match
            prompt = (
                f"LC APPLICANT NAME & STRICT ADDRESS:\n{active_lc.get('applicant_name')}, {applicant_address}\n\n"
                f"BILL OF LADING NOTIFY PARTY BOX:\n{bl_notify}\n\n"
                "Evaluate under UCP 600 Art. 14(j). When the applicant address appears in the Consignee or Notify box, "
                "it must be the same as stated in the credit. Is this discrepant or compliant? "
                "Output JSON with keys: verdict, ucp_isbp_citation, is_discrepancy, legal_reasoning, confidence."
            )
            res = self.nim_client.complete(prompt)
            data = json.loads(res["content"])
            findings.append(
                LegalFinding(
                    divergence_item="Consignee / Notify Party Address Details",
                    source_documents=["MT700 Credit", "Ocean Bill of Lading Notify Box"],
                    verdict=data.get("verdict", "COMPLIANT"),
                    is_discrepant=data.get("is_discrepancy", False),
                    ucp_isbp_citation=data.get("ucp_isbp_citation", "UCP 600 Art. 14(j)"),
                    legal_reasoning=data.get("legal_reasoning", ""),
                    confidence=float(data.get("confidence", 0.95)),
                )
            )

        # Compute neural status
        has_neural_discrepancy = any(f.is_discrepant for f in findings)
        overall_legal_status = "DISCREPANT" if has_neural_discrepancy else "COMPLIANT_PROTECTED"

        # ----------------------------------------------------------------------
        # HARD INVARIANT RULE ENFORCEMENT
        # ----------------------------------------------------------------------
        hard_invariant_enforced = False
        final_verdict = overall_legal_status

        if deterministic_eval is not None and not deterministic_eval.all_passed:
            # Fatal deterministic check failed! Hard invariant locks verdict to DISCREPANT.
            final_verdict = "DISCREPANT"
            hard_invariant_enforced = True
        elif has_neural_discrepancy:
            final_verdict = "DISCREPANT"
        else:
            final_verdict = "COMPLIANT"

        return LegalAdjudicationResult(
            overall_legal_status=overall_legal_status,
            findings=findings,
            hard_invariant_enforced=hard_invariant_enforced,
            final_locked_verdict=final_verdict,
        )
