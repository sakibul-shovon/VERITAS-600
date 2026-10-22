"""ICC UCP 600 & ISBP 745 Rule Registry.

Provides structured, immutable legal rule definitions with stable rule IDs,
exact official citations, severity categories, and adjudication engine bindings.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class RuleCategory(str, Enum):
    DETERMINISTIC_MATH = "DETERMINISTIC_MATH"
    DETERMINISTIC_TEMPORAL = "DETERMINISTIC_TEMPORAL"
    DETERMINISTIC_DOCUMENT = "DETERMINISTIC_DOCUMENT"
    STATEFUL_AMENDMENT = "STATEFUL_AMENDMENT"
    SEMANTIC_ADJUDICATION = "SEMANTIC_ADJUDICATION"
    REGULATORY_AML = "REGULATORY_AML"


class RuleSeverity(str, Enum):
    FATAL_DISCREPANCY = "FATAL_DISCREPANCY"
    CURABLE_DISCREPANCY = "CURABLE_DISCREPANCY"
    PROTECTED_VARIANCE = "PROTECTED_VARIANCE"
    MANDATORY_REGULATORY_FREEZE = "MANDATORY_REGULATORY_FREEZE"


@dataclass(frozen=True)
class LegalRule:
    rule_id: str
    citation: str
    title: str
    category: RuleCategory
    severity: RuleSeverity
    official_summary: str
    hard_invariant_locked: bool = True


RULES_REGISTRY: Dict[str, LegalRule] = {
    "UCP600-ART-6D1": LegalRule(
        rule_id="UCP600-ART-6D1",
        citation="UCP 600 Art. 6(d)(i)",
        title="Presentation Expiry Date Limit",
        category=RuleCategory.DETERMINISTIC_TEMPORAL,
        severity=RuleSeverity.FATAL_DISCREPANCY,
        official_summary="Credit must state an expiry date for presentation. A presentation after expiry date is non-compliant.",
    ),
    "UCP600-ART-10C": LegalRule(
        rule_id="UCP600-ART-10C",
        citation="UCP 600 Art. 10(c)",
        title="Implicit Amendment Acceptance",
        category=RuleCategory.STATEFUL_AMENDMENT,
        severity=RuleSeverity.PROTECTED_VARIANCE,
        official_summary="Presentation of complying documents under amended terms constitutes deemed acceptance of amendment.",
        hard_invariant_locked=False,
    ),
    "UCP600-ART-10E": LegalRule(
        rule_id="UCP600-ART-10E",
        citation="UCP 600 Art. 10(e)",
        title="Partial Acceptance Prohibition",
        category=RuleCategory.STATEFUL_AMENDMENT,
        severity=RuleSeverity.FATAL_DISCREPANCY,
        official_summary="Partial acceptance of an amendment is not allowed and will be deemed to be notification of rejection of the amendment.",
    ),
    "UCP600-ART-14B": LegalRule(
        rule_id="UCP600-ART-14B",
        citation="UCP 600 Art. 14(b)",
        title="5-Banking-Day Examination Window",
        category=RuleCategory.DETERMINISTIC_TEMPORAL,
        severity=RuleSeverity.FATAL_DISCREPANCY,
        official_summary="Issuing/Nominated bank has a maximum of five banking days following day of presentation to examine documents.",
    ),
    "UCP600-ART-14C": LegalRule(
        rule_id="UCP600-ART-14C",
        citation="UCP 600 Art. 14(c)",
        title="21-Day Presentation Period Limit",
        category=RuleCategory.DETERMINISTIC_TEMPORAL,
        severity=RuleSeverity.FATAL_DISCREPANCY,
        official_summary="Presentation must be made no later than 21 calendar days after date of shipment, but within credit expiry.",
    ),
    "UCP600-ART-14D": LegalRule(
        rule_id="UCP600-ART-14D",
        citation="UCP 600 Art. 14(d)",
        title="Cross-Document Data Consistency",
        category=RuleCategory.DETERMINISTIC_DOCUMENT,
        severity=RuleSeverity.CURABLE_DISCREPANCY,
        official_summary="Data in a document, when read in context with the credit and other documents, need not be identical, but must not conflict.",
    ),
    "UCP600-ART-14E": LegalRule(
        rule_id="UCP600-ART-14E",
        citation="UCP 600 Art. 14(e)",
        title="General Goods Description on Non-Invoice Documents",
        category=RuleCategory.SEMANTIC_ADJUDICATION,
        severity=RuleSeverity.PROTECTED_VARIANCE,
        official_summary="In documents other than invoice, goods description may be in general terms not conflicting with credit description.",
        hard_invariant_locked=False,
    ),
    "UCP600-ART-14J": LegalRule(
        rule_id="UCP600-ART-14J",
        citation="UCP 600 Art. 14(j)",
        title="Mandatory Consignee/Notify Address Conformity",
        category=RuleCategory.SEMANTIC_ADJUDICATION,
        severity=RuleSeverity.FATAL_DISCREPANCY,
        official_summary="When applicant address appears as consignee or notify details on transport document, it must be the same as in credit.",
    ),
    "UCP600-ART-16C3": LegalRule(
        rule_id="UCP600-ART-16C3",
        citation="UCP 600 Art. 16(c)(iii)",
        title="Single Notice of Refusal & Disposal Mandate",
        category=RuleCategory.DETERMINISTIC_DOCUMENT,
        severity=RuleSeverity.FATAL_DISCREPANCY,
        official_summary="Notice of refusal must state all discrepancies and state document disposal status (holding, returning, or acting on instructions).",
    ),
    "UCP600-ART-18B": LegalRule(
        rule_id="UCP600-ART-18B",
        citation="UCP 600 Art. 18(b)",
        title="Commercial Invoice Amount Cap",
        category=RuleCategory.DETERMINISTIC_MATH,
        severity=RuleSeverity.FATAL_DISCREPANCY,
        official_summary="Commercial invoice must not be issued for an amount in excess of the amount permitted by the credit.",
    ),
    "UCP600-ART-18C": LegalRule(
        rule_id="UCP600-ART-18C",
        citation="UCP 600 Art. 18(c)",
        title="Strict Invoice Goods Description",
        category=RuleCategory.SEMANTIC_ADJUDICATION,
        severity=RuleSeverity.FATAL_DISCREPANCY,
        official_summary="Description of goods in commercial invoice must correspond with that in the credit without omission of critical specs.",
    ),
    "UCP600-ART-20A2": LegalRule(
        rule_id="UCP600-ART-20A2",
        citation="UCP 600 Art. 20(a)(ii)",
        title="On Board Date Within Latest Shipment Date",
        category=RuleCategory.DETERMINISTIC_TEMPORAL,
        severity=RuleSeverity.FATAL_DISCREPANCY,
        official_summary="Date of issuance of transport document is deemed shipment date unless an on board notation with date is present.",
    ),
    "UCP600-ART-28C": LegalRule(
        rule_id="UCP600-ART-28C",
        citation="UCP 600 Art. 28(c)",
        title="Cover Notes Explicitly Prohibited",
        category=RuleCategory.DETERMINISTIC_DOCUMENT,
        severity=RuleSeverity.FATAL_DISCREPANCY,
        official_summary="Cover notes issued by brokers will not be accepted as insurance documents.",
    ),
    "UCP600-ART-28E": LegalRule(
        rule_id="UCP600-ART-28E",
        citation="UCP 600 Art. 28(e)",
        title="Insurance Date Prior to or On Shipment Date",
        category=RuleCategory.DETERMINISTIC_TEMPORAL,
        severity=RuleSeverity.FATAL_DISCREPANCY,
        official_summary="Date of insurance document must be no later than date of shipment, unless cover is effective from shipment date.",
    ),
    "UCP600-ART-28F2": LegalRule(
        rule_id="UCP600-ART-28F2",
        citation="UCP 600 Art. 28(f)(ii)",
        title="Minimum Insurance Coverage 110% CIF",
        category=RuleCategory.DETERMINISTIC_MATH,
        severity=RuleSeverity.FATAL_DISCREPANCY,
        official_summary="Insurance must cover at least 110% of CIF or CIP value of goods.",
    ),
    "UCP600-ART-30B": LegalRule(
        rule_id="UCP600-ART-30B",
        citation="UCP 600 Art. 30(b)",
        title="5% Quantity Tolerance on Bulk Goods",
        category=RuleCategory.DETERMINISTIC_MATH,
        severity=RuleSeverity.PROTECTED_VARIANCE,
        official_summary="Tolerance of +/- 5% in quantity of goods allowed provided quantity not stated in units of packaging and drawings within credit amount.",
        hard_invariant_locked=False,
    ),
    "ISBP745-PARA-A23": LegalRule(
        rule_id="ISBP745-PARA-A23",
        citation="ISBP 745 Para A23",
        title="Harmless Typographical Errors Protection",
        category=RuleCategory.SEMANTIC_ADJUDICATION,
        severity=RuleSeverity.PROTECTED_VARIANCE,
        official_summary="Typographical errors that do not alter the meaning of the word or sentence do not constitute a discrepancy.",
        hard_invariant_locked=False,
    ),
    "TBML-CUSTOMS-PRICE": LegalRule(
        rule_id="TBML-CUSTOMS-PRICE",
        citation="FATF / Wolfsberg TBML Benchmark",
        title="Trade-Based Money Laundering Price Anomaly (+3.0σ)",
        category=RuleCategory.REGULATORY_AML,
        severity=RuleSeverity.MANDATORY_REGULATORY_FREEZE,
        official_summary="Invoice unit price exceeding +3.0σ from customs historical benchmark requires mandatory AML compliance hold.",
    ),
    "OFAC-SDN-WATCHLIST": LegalRule(
        rule_id="OFAC-SDN-WATCHLIST",
        citation="UN / OFAC / EU Sanctions Regulations",
        title="Designated Watchlist Entity or Sanctioned Vessel Match",
        category=RuleCategory.REGULATORY_AML,
        severity=RuleSeverity.MANDATORY_REGULATORY_FREEZE,
        official_summary="Positive match against sanctioned entity or blocked vessel requires immediate freezing and compliance escalation.",
    ),
}


def get_rule(rule_id: str) -> Optional[LegalRule]:
    return RULES_REGISTRY.get(rule_id)
