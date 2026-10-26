# VERITAS-600: Trade Finance Legal & Domain Specification

> **Governing Standards:** ICC Uniform Customs and Practice for Documentary Credits (UCP 600), International Standard Banking Practice (ISBP 745), SWIFT Standards MT, and Wolfsberg Group TBML Principles.  
> **Repository:** [VERITAS-600](https://github.com/sakibul-shovon/VERITAS-600)  
> **Production Instance:** [https://veritas.165.99.219.253.sslip.io](https://veritas.165.99.219.253.sslip.io)

---

## 1. The Documentary Credit Examination Mandate

Letters of Credit (LCs) represent the primary risk-mitigation instrument for global merchandise trade, settling over **$3 Trillion** annually. An issuing bank irrevocably undertakes to pay the beneficiary provided that complying documents are presented to the bank's counters.

Under **UCP 600 Art. 4** and **Art. 5**, documentary credit operations deal exclusively in **documents, not goods, services, or performance to which the documents may relate**. Banks examine documents solely on their face to ascertain whether or not they constitute a complying presentation.

```
+------------------------------------------------------------------------------------+
|                         THE 5-BANKING-DAY EXAMINATION CLOCK                        |
|                               (UCP 600 Art. 14(b))                                 |
+------------------------------------------------------------------------------------+
| Day of Presentation (Day 0)                                                        |
|   |                                                                                |
|   +--> Day 1 (Banking Day): OCR Intake & Federated Verification                    |
|   +--> Day 2 (Banking Day): Deterministic Math & Legal Adjudication                 |
|   +--> Day 3 (Banking Day): Bank Officer Sign-Off & Disposition Decision           |
|   +--> Day 4 (Banking Day): Final Action (Honour or Refusal)                       |
|   +--> Day 5 (Banking Day): ABSOLUTE DEADLINE (Preclusion Cliff)                   |
|          |                                                                         |
|          +---> If Single MT734 Notice with ALL discrepancies NOT dispatched:       |
|                BANK IS LEGALLY PRECLUDED FROM REFUSING (UCP 600 Art. 16(f))        |
|                Total balance-sheet loss on defective/fraudulent shipment!          |
+------------------------------------------------------------------------------------+
```

---

## 2. Canonical ICC Legal Articles Enforced in Code

### UCP 600 Article 6(d)(i) — Credit Expiry
* **Legal Rule:** A credit must state an expiry date for presentation. An expiry date stated for honour or negotiation will be deemed to be an expiry date for presentation.
* **Engine Implementation:** `apps/api/engines/ucp600_deterministic.py`
* **Rule Logic:**
  $$\text{Presentation Date} \le \text{Expiry Date}$$
* **Failure Verdict:** `DISCREPANT` (Permanent lock).

### UCP 600 Article 10(c) & 10(e) — Amendments & Partial Acceptance
* **Legal Rule:**
  * **Art. 10(c):** The terms and conditions of the original credit remain in force for the beneficiary until the beneficiary communicates its acceptance of the amendment, or presents documents complying with the credit and the amendment.
  * **Art. 10(e):** Partial acceptance of an amendment is not allowed and will be deemed to be a notification of rejection of the amendment.
* **Engine Implementation:** `apps/api/memory/amendment_memory.py`
* **Rule Logic:** Pending/unaccepted amendments are quarantined. Only fully accepted MT707 amendments merge into the active baseline. Partial compliance triggers automatic rejection.

### UCP 600 Article 14(b) & Article 16(f) — The 5-Banking-Day Preclusion Rule
* **Legal Rule:**
  * **Art. 14(b):** A nominated bank acting on its nomination, a confirming bank, if any, and the issuing bank shall each have a maximum of five banking days following the day of presentation to determine if a presentation is complying.
  * **Art. 16(c):** When an issuing bank decides to refuse, it must give a single notice to that effect by telecommunication (SWIFT MT734).
  * **Art. 16(f):** If an issuing bank fails to act in accordance with the provisions of this article, it shall be **precluded from claiming that the documents do not constitute a complying presentation**.
* **Engine Implementation:** Header bar 5-banking-day countdown clock and `apps/api/engines/decision_engine.py`.

### UCP 600 Article 14(c) — 21-Day Presentation Window
* **Legal Rule:** A presentation including one or more original transport documents must be made by or on behalf of the beneficiary not later than 21 calendar days after the date of shipment, but in no event later than the expiry date of the credit.
* **Engine Implementation:** `apps/api/engines/ucp600_deterministic.py`
* **Rule Logic:**
  $$\text{Presentation Date} - \text{Shipment Date} \le 21\text{ calendar days}$$
* **Advisory Calculation:** If an initial presentation is discrepant but $\le 19\text{ days}$ have elapsed, VERITAS-600 computes the exact financial demurrage savings achievable if the beneficiary re-presents corrected documents within the remaining window.

### UCP 600 Article 14(d) — Documentary Consistency & Weight Reconciliation
* **Legal Rule:** Data in a document, when read in context with the credit, the document itself and international standard banking practice, need not be identical to, but must not conflict with, data in that document, any other stipulated document or the credit.
* **Engine Implementation:** Cross-document reconciliation between Packing List and Bill of Lading gross weights with commercial rounding tolerance ($\le 0.1\%$ or $0.5\text{ kg}$).

### UCP 600 Article 14(e) — General Description of Goods on Transport Documents
* **Legal Rule:** In documents other than the commercial invoice, the description of the goods, services or performance, if stated, may be in **general terms not conflicting** with their description in the credit.
* **Engine Implementation:** `apps/api/engines/ucp600_legal_adjudicator.py`
* **Example:** Bill of Lading stating `"Industrial Servo Motors"` against an MT700 description of `"Industrial AC Servo Machine Model X-200"` is legally compliant and protected from wrongful dishonor.

### UCP 600 Article 14(j) — Consignee & Notify Party Address Details
* **Legal Rule:** When the address and contact details of the applicant appear as part of the consignee or notify party details on a transport document, they **must be the same as those stated in the credit**.
* **Engine Implementation:** `apps/api/engines/ucp600_legal_adjudicator.py` flags subtle address mutations in notify boxes that legacy models overlook.

### UCP 600 Article 18(b) & 18(c) — Commercial Invoice Standards
* **Legal Rule:**
  * **Art. 18(b):** An issuing bank may accept a commercial invoice issued for an amount in excess of the amount permitted by the credit, but its decision will be binding upon all parties.
  * **Art. 18(c):** The description of the goods, services or performance in a commercial invoice **must correspond with that in the credit**.
* **Engine Implementation:** Enforces invoice drawing limits and strictly validates goods nomenclature on the invoice.

### UCP 600 Article 20(a)(ii) — Bill of Lading Shipment & On-Board Date
* **Legal Rule:** A bill of lading must indicate that the goods have been shipped on board a named vessel at the port of loading by pre-printed wording, or by an on-board notation indicating the date on which the goods have been shipped on board.
* **Engine Implementation:** `apps/api/engines/ucp600_deterministic.py` ensures $\text{On-Board Date} \le \text{Latest Shipment Date}$.

### UCP 600 Article 28(c), 28(e) & 28(f)(ii) — Insurance Document Standards
* **Legal Rule:**
  * **Art. 28(c):** Cover notes will not be accepted.
  * **Art. 28(e):** The date of the insurance document must be no later than the date of shipment, unless it appears from the insurance document that the cover is effective from a date not later than the date of shipment.
  * **Art. 28(f)(ii):** The insurance must cover at least **110% of the CIF or CIP value of the goods**.
* **Engine Implementation:**
  $$\text{Required Coverage} = 1.10 \times \text{Invoice Amount (CIF/CIP)}$$
  Rejects all cover notes (with Unicode homoglyph normalization) and calculates exact dollar shortfalls.

### ISBP 745 Paragraph A23 — Typographical Errors
* **Legal Rule:** A misspelling or typing error that does not affect the meaning of a word or the sentence in which it occurs does **not** make a document discrepant.
* **Engine Implementation:** `apps/api/engines/ucp600_legal_adjudicator.py` protects typos like `"Mashine"` vs `"Machine"`, preventing wrongful dishonor litigation.

---

## 3. Trade-Based Money Laundering (TBML) & Sanctions Integration

Documentary compliance under UCP 600 is deliberately isolated from the underlying contract. Criminal syndicates exploit this rule by submitting completely matching documents that conceal illicit transfers:

1. **Unit Price Anomaly Detection ($Z$-Score):**
   Using customs trade statistics from historical Parquet lakehouses:
   $$Z = \frac{\text{Unit Price} - \mu_{\text{HS-Code}}}{\sigma_{\text{HS-Code}}}$$
   Under Wolfsberg Group standard deviation thresholds, a $Z \ge +3.0$ indicates an extreme outlier consistent with capital flight or over-invoicing.
2. **Sanctions & Beneficial Ownership:**
   Cross-references vessel IMO numbers, shippers, notify parties, and ultimate beneficial owners (UBOs) against global OpenSanctions databases.
3. **Regulatory Compliance Freeze vs. SWIFT MT734 Refusal:**
   If a presentation violates AML/Sanctions laws, issuing a standard UCP 600 MT734 refusal violates international AML regulations by tipping off criminals. VERITAS-600 generates an immediate **Compliance Hold & AML Escalation Dossier** and freezes payment authorization.
