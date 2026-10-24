"""Artifact Generator Engine for Trade Finance Bank Operations.

Generates:
1. Formal SWIFT MT734 (Advice of Refusal) compliant with SWIFT FIN standards & UCP 600 Art. 16(c).
2. Financial Crime Escalation Dossier (SAR/OFAC Freeze) for Action 3.
3. Settlement Authorization Voucher for Action 1.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from apps.api.engines.decision_engine import BankDecision


class ArtifactGenerator:
    """Generates bank-ready operational artifacts matching international standards."""

    def generate_artifact(
        self,
        decision: BankDecision,
        active_lc: dict[str, Any],
        presentation: dict[str, Any],
    ) -> str:
        """Generate formatted artifact based on decision action."""
        if decision.recommended_action == "ISSUE_MT734_REFUSAL":
            return self.generate_swift_mt734(decision, active_lc, presentation)
        elif decision.recommended_action == "COMPLIANCE_HOLD_AML":
            return self.generate_aml_dossier(decision, active_lc, presentation)
        else:
            return self.generate_settlement_voucher(decision, active_lc, presentation)

    def generate_swift_mt734(
        self,
        decision: BankDecision,
        active_lc: dict[str, Any],
        presentation: dict[str, Any],
    ) -> str:
        """Generate formal SWIFT MT734 Notice of Refusal text."""
        today_swift = datetime.now(UTC).strftime("%y%m%d")
        lc_id = decision.lc_id
        currency = active_lc.get("currency", "USD")
        amount = float(presentation.get("invoice_amount", active_lc.get("amount", 0.0)))
        amount_swift = f"{amount:,.2f}".replace(",", "").replace(".", ",")

        # Format discrepancies
        discrepancies_formatted = "\n".join(f"+ {d}" for d in decision.discrepancies)

        # Demurrage Advisory text
        advisory_text = ""
        if decision.demurrage_savings_advisory:
            adv = decision.demurrage_savings_advisory
            advisory_text = f"""
----------------------------------------------------------------------
BANK TRADE ADVISORY — PRE-EXPIRY CURE VS. APPLICANT WAIVER COMPARISON:
- Remaining Presentation Window (UCP 600 Art. 14(c)): {adv.get('days_remaining_in_window')} calendar days.
- Beneficiary 48-Hour Cured Re-Presentation Demurrage: ${adv.get('cured_demurrage_cost', 0):,.2f}
- Standard 8-Day Applicant Waiver Demurrage Exposure:  ${adv.get('waiver_demurrage_cost', 0):,.2f}
>>> ESTIMATED BENEFICIARY PORT DEMURRAGE SAVINGS:    ${adv.get('net_savings_usd', 0):,.2f} USD <<<
----------------------------------------------------------------------"""

        mt734 = f"""{'{1:F01ECOMUS33AXXX0000000000}{2:I734GTBKSGSGAXXXN}{4:'}
:20:REF-{lc_id}-{today_swift}
:21:{presentation.get('invoice_no', 'PRES-001')}
:32A:{today_swift}{currency}{amount_swift}
:77J:DISCREPANCIES NOTED PURSUANT TO ICC UCP 600 ART. 16(c)(ii):
{discrepancies_formatted}
:77B:DISPOSAL OF DOCUMENTS PURSUANT TO UCP 600 ART. 16(c)(iii)(a):
WE ARE HOLDING THE DOCUMENTS AT YOUR RISK AND DISPOSAL PENDING YOUR
INSTRUCTIONS, OR UNTIL RECEIPT OF ACCEPTABLE RE-PRESENTATION PRIOR
TO THE EXPIRY OF THE ARTICLE 14(c) PRESENTATION PERIOD.{advisory_text}
{'-}'}"""
        return mt734.strip()

    def generate_aml_dossier(
        self,
        decision: BankDecision,
        active_lc: dict[str, Any],
        presentation: dict[str, Any],
    ) -> str:
        """Generate Financial Crime Escalation Dossier for AML/Sanctions block."""
        now_str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        lc_id = decision.lc_id
        amount = presentation.get("invoice_amount", active_lc.get("amount", 0.0))

        flags_formatted = "\n".join(f"  [!] {f}" for f in decision.regulatory_flags)

        dossier = f"""================================================================================
VERITAS-600 FINANCIAL CRIME COMPLIANCE — REGULATORY FREEZE DOSSIER
CONFIDENTIAL // FOR EXAMINING BANK AML & SANCTIONS ESCALATION ONLY
================================================================================
CASE REFERENCE:       SAR-OFAC-{lc_id}-{datetime.now(UTC).strftime('%Y%m%d%H%M')}
STATUS:               PAYMENT BLOCKED / REGULATORY COMPLIANCE HOLD
TIMESTAMP:            {now_str}
LC IDENTIFIER:        {lc_id}
PRESENTED DRAWING:    USD {amount:,.2f}
BENEFICIARY:          {active_lc.get('beneficiary_name')}
APPLICANT / NOTIFY:   {presentation.get('bl_notify_party', active_lc.get('applicant_name'))}
CARRYING VESSEL:      {presentation.get('bl_vessel', 'N/A')}

CROSS-SILO INTELLIGENCE HIT SUMMARY:
{flags_formatted}

LEGAL DIRECTIVE:
1. Pursuant to Financial Crime and OFAC Regulatory Mandates, NO PAYMENT IS AUTHORIZED.
2. Standard documentary refusal notice (SWIFT MT734) is expressly SUPPRESSED to prevent
   inadvertent tipping-off under Anti-Money Laundering statutory guidelines.
3. Documents and transaction record frozen pending SAR filing and Compliance Officer sign-off.
================================================================================
Generated by VERITAS-600 Zetaris Federated Compliance Layer"""
        return dossier.strip()

    def generate_settlement_voucher(
        self,
        decision: BankDecision,
        active_lc: dict[str, Any],
        presentation: dict[str, Any],
    ) -> str:
        """Generate Settlement Authorization Voucher for clean/protected honour."""
        now_str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        lc_id = decision.lc_id
        amount = presentation.get("invoice_amount", active_lc.get("amount", 0.0))

        citations_str = ", ".join(decision.legal_citations)

        voucher = f"""================================================================================
VERITAS-600 DOCUMENTARY CREDIT SETTLEMENT AUTHORIZATION VOUCHER
================================================================================
AUTHORIZATION REF:    HONOUR-{lc_id}-{datetime.now(UTC).strftime('%y%m%d%H%M')}
TIMESTAMP:            {now_str}
LC IDENTIFIER:        {lc_id}
BENEFICIARY:          {active_lc.get('beneficiary_name')}
DRAWING AMOUNT:       {active_lc.get('currency', 'USD')} {amount:,.2f}
APPLICANT:            {active_lc.get('applicant_name')}

LEGAL ADJUDICATION BASIS:
- All required documents presented in full compliance with UCP 600.
- Statutory Citations Applied: {citations_str}
- Zero discrepancies identified. Harmless typographical errors protected under ISBP 745 Para A23.

SETTLEMENT STATUS:    PROPOSED - PENDING HUMAN EXAMINER AUTHORIZATION
DISPATCH STATUS:      AWAITING SIGN-OFF (NOT DISPATCHED)
RECOMMENDED ACTION:   APPROVE_HONOUR
================================================================================"""
        return voucher.strip()

    def generate_authorized_voucher(
        self,
        decision: BankDecision,
        active_lc: dict[str, Any],
        presentation: dict[str, Any],
        signer_name: str,
        signature_token: str,
    ) -> str:
        voucher = self.generate_settlement_voucher(decision, active_lc, presentation)
        voucher = voucher.replace(
            "SETTLEMENT STATUS:    PROPOSED - PENDING HUMAN EXAMINER AUTHORIZATION\nDISPATCH STATUS:      AWAITING SIGN-OFF (NOT DISPATCHED)\nRECOMMENDED ACTION:   APPROVE_HONOUR",
            f"SETTLEMENT STATUS:    AUTHORIZED BY HUMAN EXAMINER ({signer_name})\nDISPATCH STATUS:      AUTHORIZED_NOT_DISPATCHED (EXTERNAL GATEWAY NOT CONNECTED)\nCRYPTOGRAPHIC SEAL:   {signature_token}",
        )
        return voucher
