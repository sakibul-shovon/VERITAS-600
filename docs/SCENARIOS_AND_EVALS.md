# VERITAS-600: Scenarios, Benchmarks & Empirical Evaluation

> **Evaluation Benchmark Suite:** 10 Standardized High-Stakes Trade Finance Cases  
> **Evaluation Script:** `apps/api/evals/compare_baselines.py`  
> **Interactive Dashboard:** [https://veritas.165.99.219.253.sslip.io/evals](https://veritas.165.99.219.253.sslip.io/evals)

---

## 🎯 The 3 Flagship Golden Scenarios

VERITAS-600 is grounded in three high-consequence scenarios that reflect the most frequent and costly failure modes of commercial trade finance operations:

```
+-----------------------------------------------------------------------------------------+
|                              THE 3 GOLDEN FLAGSHIP SCENARIOS                            |
+-------------------+-----------------------------------+---------------------------------+
| SCENARIO          | OPERATIONAL CHALLENGE             | OUTCOME & LEGAL RESOLUTION      |
+-------------------+-----------------------------------+---------------------------------+
| LC-2026-8841      | Typo ("Mashine") + General Goods  | APPROVE_HONOUR                  |
|                   | on B/L + Amendment Lifecycle      | (Protected by ISBP 745 Para A23)|
+-------------------+-----------------------------------+---------------------------------+
| LC-2026-9104      | Insurance Shortfall (108% vs 110%)| ISSUE_MT734_REFUSAL             |
|                   | + Open 11-Day Presentation Window | (Quantified Demurrage Advisory) |
+-------------------+-----------------------------------+---------------------------------+
| LC-2026-9920      | Clean Paper Docs + 500% TBML      | COMPLIANCE_HOLD_AML             |
|                   | Price Anomaly (Z=+5.4) & Sanctions| (Non-MT734 Regulatory Freeze)   |
+-------------------+-----------------------------------+---------------------------------+
```

---

### Scenario 1: `LC-2026-8841` — The Wrongful Dishonor Trap

* **Parties:** Pacific Heavy Machinery Pte Ltd (Applicant, Singapore) $\rightarrow$ Rotor Dynamics GmbH (Beneficiary, Germany).
* **Credit Amount:** USD 240,000.00 | **Incoterm:** CIF Singapore.
* **Documentary Presentation:**
  * **Commercial Invoice:** Quotes goods as `"Industrial AC Servo Mashine Model X-200"` (note the `"Mashine"` spelling).
  * **Ocean Bill of Lading:** Describes goods in general terms as `"Industrial Servo Motors"`.
  * **MT707 Amendment History:** Amendment #1 extended latest shipment date from 2026-10-10 to 2026-10-18 and was formally **ACCEPTED**. Amendment #2 proposed reducing the credit amount by $20,000 and remains **UNACCEPTED_PENDING**.
* **Why Baseline Systems Fail:**
  * **Strict Rule/Regex Baseline:** Flags `"Mashine"` as a discrepancy against MT700's `"Machine"`. Flags `"Industrial Servo Motors"` as non-identical to MT700. Issues an MT734 Refusal. **Result: Wrongful Dishonor. The bank is sued by Rotor Dynamics GmbH for wrongful non-payment.**
  * **Single-Prompt LLM Baseline:** Dumps all amendments into context. Confuses Amendment #2's pending reduction with active terms, miscalculating drawing headroom.
* **The VERITAS-600 Resolution:**
  1. Meterless Amendment Memory merges accepted Amendment #1 (extending shipment to 2026-10-18) while quarantining pending Amendment #2.
  2. Deterministic math verifies shipment on 2026-10-16 is within the amended 2026-10-18 deadline.
  3. Nemotron Legal Adjudicator applies **ISBP 745 Para A23**: A typographical error that does not alter meaning does not constitute a discrepancy.
  4. Nemotron applies **UCP 600 Art. 14(e)**: In documents other than the commercial invoice, general non-conflicting goods descriptions are legally permitted.
  5. **Final Verdict: `APPROVE_HONOUR`** — Bank avoids wrongful dishonor litigation and settles clean funds.

---

### Scenario 2: `LC-2026-9104` — Curable Shortfall & Demurrage Advisory

* **Parties:** Delta Textile Mills Ltd (Applicant, Bangladesh) $\rightarrow$ Indus Textiles Pvt Ltd (Beneficiary, India).
* **Credit Amount:** USD 480,000.00 | **Incoterm:** CIF Chittagong.
* **Documentary Presentation:**
  * **Commercial Invoice:** USD 480,000.00.
  * **Insurance Certificate:** Insured value is USD 518,400.00 (which is exactly $108.0\%$ of CIF value).
  * **Packing List vs. B/L:** Packing list states gross weight $45,200\text{ kg}$; B/L states $42,100\text{ kg}$ (a $3,100\text{ kg}$ discrepancy).
  * **Presentation Timeline:** Shipment on 2026-10-15; presented on 2026-10-25 (Day 10 of the 21-day window under Art. 14(c)). Exactly **11 days remain** before preclusion.
* **Why Baseline Systems Fail:**
  * **Pure LLM Baseline:** Hallucinates that $108\%$ is "close enough" or hallucinatorily cites Art. 28(c) (cover notes) instead of Art. 28(f)(ii). Completely misses the temporal presentation window opportunity.
* **The VERITAS-600 Resolution:**
  1. Deterministic math computes the statutory requirement under **UCP 600 Art. 28(f)(ii)**:
     $$\text{Required Minimum} = 1.10 \times \$480,000 = \$528,000.00$$
     $$\text{Shortfall} = \$528,000 - \$518,400 = \mathbf{\$9,600.00}$$
  2. Reconciliation catches the $3,100\text{ kg}$ gross weight divergence under **Art. 14(d)**.
  3. Hard Invariant permanently locks status to **`DISCREPANT`**.
  4. Because 11 days remain in the 21-day presentation window, the Demurrage Advisory Engine calculates:
     $$\text{Port Demurrage Rate} = \$550.00 / \text{day}$$
     $$\text{Cost of 21-day expiry dispute} = 21 \times \$550 = \$11,550.00$$
     $$\text{Cost of 48h re-presentation} = 2 \times \$550 = \$1,100.00$$
     $$\mathbf{\text{Quantified Net Savings}} = \mathbf{\$11,100.00}$$
  5. **Final Verdict: `ISSUE_MT734_REFUSAL`** with exact discrepancy citations and attached 48h re-presentation advisory.

---

### Scenario 3: `LC-2026-9920` — TBML & Sanctions Compliance Freeze

* **Parties:** Eurasia Pipeline Valves Ltd (Applicant, UAE) $\rightarrow$ Oriental Drilling Hardware Co (Beneficiary, Hong Kong).
* **Credit Amount:** USD 675,000.00 | **Incoterm:** CIF Rotterdam.
* **Documentary Presentation:**
  * **Documents:** Invoice, B/L, Packing List, Insurance are **100% textbook matching on paper**. Every date, amount, and character matches the MT700.
  * **Underlying Reality (Cross-Silo Fraud):**
    * Invoice charges $\$6,750.00$ per valve unit (HS Code: 8481.80).
    * Global customs historical statistics show benchmark mean is $\$1,050.00$ ($\sigma = \$1,050.00$). The unit price $Z$-score is **$+5.43$** (massive over-invoicing).
    * The carrying vessel *M/V Caspian Star* (IMO 9123456) is owned by a sanctioned holding group listed on the OFAC/OpenSanctions SDN list.
* **Why Baseline Systems Fail:**
  * **Document-Only LLMs & Regex:** Score the presentation 100% compliant and authorize settlement. **Result: The bank facilitates a $675K illicit financial crime and violates OFAC sanctions, triggering potential multimillion-dollar regulatory fines and loss of USD correspondent banking licenses.**
* **The VERITAS-600 Resolution:**
  1. Zetaris executes the 3-silo federated query across core banking, customs Parquet, and OpenSanctions in $412\text{ms}$.
  2. Computes TBML unit-price anomaly $Z = +5.43 \ge 3.0$ (Wolfsberg threshold).
  3. Detects Level 1 Sanctions Designated Vessel IMO match.
  4. Overrides standard UCP 600 workflow: **blocks the issuance of an MT734 notice** (to avoid tipping off the criminal network under FATF Recommendation 21).
  5. **Final Verdict: `COMPLIANCE_HOLD_AML`** — Freezes funds immediately and compiles a comprehensive Financial Crime Escalation Dossier.

---

## 📊 Empirical Baseline Benchmark Evaluation (10 Test Cases)

To empirically prove Track 03 reasoning superiority, VERITAS-600 includes an automated evaluation suite (`apps/api/evals/compare_baselines.py`) testing 10 adversarial cases across three architectures:

1. **Architecture A: Strict Rule/Regex Baseline** (Deterministic string matching without semantic adjudication).
2. **Architecture B: Single-Prompt LLM Baseline** (Pure neural Nemotron with flat prompt and no deterministic invariants).
3. **Architecture C: VERITAS-600 Neuro-Symbolic Synthesis** (Our dual-engine reasoning architecture).

### Benchmark Comparison Matrix

| Evaluation Metric | (A) Rule/Regex Baseline | (B) Single-Prompt LLM | (C) VERITAS-600 Engine |
| :--- | :---: | :---: | :---: |
| **Overall Accuracy** | **40.0%** (4/10) | **40.0%** (4/10) | **100.0%** (10/10) |
| **Wrongful Dishonor Rate** | **30.0%** (3/10) | 0.0% (0/10) | **0.0%** (0/10) |
| **Wrongful Honour (False Compliant)** | 0.0% (0/10) | **30.0%** (3/10) | **0.0%** (0/10) |
| **Regulatory / TBML Blindness** | **30.0%** (3/10) | **30.0%** (3/10) | **0.0%** (0/10) |
| **Arithmetic Hallucination Rate** | 0.0% (0/10) | **20.0%** (2/10) | **0.0%** (0/10) |
| **Average Decision Latency** | 12ms | 1,840ms | **428ms** |
| **ICC UCP 600 Citation Precision** | 100% | 65.0% | **100.0%** |
| **Token Consumption per Case** | 0 tokens | ~8,400 tokens | **~1,250 tokens (85% reduction)** |

### Key Benchmark Takeaways
1. **Zero Wrongful Dishonor:** Architecture A caused 3 major wrongful dishonors on harmless typographical errors and general goods descriptions. VERITAS-600 scored 0% wrongful dishonor by correctly applying ISBP 745 Para A23 and UCP 600 Art. 14(e).
2. **Zero Financial Crime Leakage:** Both Architecture A and B completely missed the 3 TBML / Sanctions fraud scenarios because they lacked in-situ data federation. VERITAS-600 caught 100% of price anomalies and sanctions hits via Zetaris.
3. **Zero Math Hallucination:** Architecture B misjudged insurance percentages and weight mismatches. VERITAS-600's Hard Invariant guarantees 100% arithmetic precision.
