"""VERITAS-600 Data Seeding Script.

Seeds:
1. Customs HS-Code 6-digit price benchmark distributions (data/customs_parquet/hs_benchmarks.parquet)
2. Watchlist entities for sanctions / TBML (data/opensanctions/watchlist_entities.json)
3. 3 Flagship Golden Scenarios + 7 Evaluation Cases into presentations directory
4. DuckDB / PostgreSQL local database tables
"""

from __future__ import annotations

import json
from pathlib import Path
import duckdb
import pandas as pd

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = ROOT_DIR / "data"
CUSTOMS_DIR = DATA_DIR / "customs_parquet"
SANCTIONS_DIR = DATA_DIR / "opensanctions"
PRESENTATIONS_DIR = DATA_DIR / "presentations"
DB_DIR = ROOT_DIR / "apps" / "api" / "db"

CUSTOMS_DIR.mkdir(parents=True, exist_ok=True)
SANCTIONS_DIR.mkdir(parents=True, exist_ok=True)
PRESENTATIONS_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------------------------
# 1. HS-Code Customs Price Benchmarks (Parquet)
# ------------------------------------------------------------------------------
def seed_customs_parquet() -> Path:
    """Generate 6-digit HS-code historical unit-price stats."""
    parquet_path = CUSTOMS_DIR / "hs_benchmarks.parquet"
    benchmarks = [
        {
            "hs_code_6": "8481.80",
            "description": "Taps, cocks, valves for pipes, boiler shells, tanks, vats or the like",
            "mean_unit_price_usd": 92.00,
            "stddev_unit_price_usd": 15.50,
            "p5_unit_price_usd": 68.00,
            "p95_unit_price_usd": 125.00,
            "sample_size": 14250,
        },
        {
            "hs_code_6": "8501.10",
            "description": "Electric motors of an output not exceeding 37.5 W / Servo Motors",
            "mean_unit_price_usd": 480.00,
            "stddev_unit_price_usd": 45.00,
            "p5_unit_price_usd": 410.00,
            "p95_unit_price_usd": 560.00,
            "sample_size": 8900,
        },
        {
            "hs_code_6": "5205.12",
            "description": "Cotton yarn, single, of uncombed fibres, not for retail sale",
            "mean_unit_price_usd": 3.20,
            "stddev_unit_price_usd": 0.40,
            "p5_unit_price_usd": 2.50,
            "p95_unit_price_usd": 3.90,
            "sample_size": 32000,
        },
        {
            "hs_code_6": "8471.30",
            "description": "Portable automatic data processing machines weighing not more than 10 kg",
            "mean_unit_price_usd": 650.00,
            "stddev_unit_price_usd": 85.00,
            "p5_unit_price_usd": 510.00,
            "p95_unit_price_usd": 820.00,
            "sample_size": 54000,
        },
    ]

    df = pd.DataFrame(benchmarks)
    df.to_parquet(parquet_path, engine="pyarrow", index=False)
    print(f"Generated HS customs parquet at {parquet_path} ({len(df)} rows)")
    return parquet_path


# ------------------------------------------------------------------------------
# 2. Master LC and Amendments Definitions
# ------------------------------------------------------------------------------
SCENARIOS_DATA = [
    # Flagship 1: The Wrongful Dishonor Trap ($240,000 Industrial Servo Machines)
    {
        "master": {
            "lc_id": "LC-2026-8841",
            "swift_mt700_raw": ":27: 1/1\n:40A: IRREVOCABLE\n:20: LC-2026-8841\n:31C: 260901\n:31D: 261115 SINGAPORE\n:50: PACIFIC HEAVY MACHINERY PTE LTD, 82 SHENTON WAY, SINGAPORE 079120\n:59: ROTOR DYNAMICS GMBH, INDUSTRIESTRASSE 45, 70565 STUTTGART GERMANY\n:32B: USD 240000,00\n:39A: 0/0\n:44A: HAMBURG, GERMANY\n:44B: SINGAPORE\n:44C: 261010\n:45A: 500 UNITS INDUSTRIAL AC SERVO MACHINE MODEL X-200 AT USD 480.00 PER UNIT CIF SINGAPORE\n:46A: 1. SIGNED COMMERCIAL INVOICE IN 3 COPIES\n2. FULL SET CLEAN ON BOARD OCEAN BILLS OF LADING CONSIGNED TO ORDER OF ISSUING BANK\n3. PACKING LIST IN 2 COPIES\n4. INSURANCE POLICY COVERING ALL RISKS FOR 110PCT CIF VALUE\n:47A: ALL DOCUMENTS MUST MENTION LC NUMBER\n:48: 21 DAYS AFTER SHIPMENT DATE\n:49: WITHOUT",
            "issuing_bank": "Global Trade Bank Singapore",
            "applicant_name": "Pacific Heavy Machinery Pte Ltd",
            "applicant_address_strict": "82 Shenton Way, Singapore 079120",
            "beneficiary_name": "Rotor Dynamics GmbH",
            "currency": "USD",
            "amount": 240000.00,
            "tolerance_pct": 0.00,
            "incoterm": "CIF",
            "hs_code_6": "8501.10",
            "goods_description_strict": "500 UNITS INDUSTRIAL AC SERVO MACHINE MODEL X-200 AT USD 480.00 PER UNIT CIF SINGAPORE",
            "unit_price": 480.00,
            "quantity": 500,
            "port_of_loading": "Hamburg, Germany",
            "port_of_discharge": "Singapore",
            "latest_shipment_date": "2026-10-10",
            "expiry_date": "2026-11-15",
            "presentation_period_days": 21,
            "insurance_min_pct": 110.00,
            "daily_demurrage_usd": 1850.00,
        },
        "amendments": [
            {
                "amendment_id": "AMD-8841-01",
                "lc_id": "LC-2026-8841",
                "sequence_no": 1,
                "amended_field": "latest_shipment_date",
                "old_value": "2026-10-10",
                "new_value": "2026-10-18",
                "beneficiary_acceptance_status": "ACCEPTED",
                "effective_date": "2026-09-25",
            },
            {
                "amendment_id": "AMD-8841-02",
                "lc_id": "LC-2026-8841",
                "sequence_no": 2,
                "amended_field": "port_of_discharge",
                "old_value": "Singapore",
                "new_value": "Jurong Port, Singapore",
                "beneficiary_acceptance_status": "UNACCEPTED_PENDING",
                "effective_date": "2026-10-02",
            },
        ],
        "presentation": {
            "invoice_no": "INV-2026-771",
            "invoice_amount": 240000.00,
            "invoice_unit_price": 480.00,
            "invoice_quantity": 500,
            "invoice_goods_description": "500 UNITS INDUSTRIAL AC SERVO MASHINE MODEL X-200",  # harmless typo under ISBP 745 A23
            "bl_no": "MEDU987654321",
            "bl_goods_description": "INDUSTRIAL SERVO MOTORS",  # protected under UCP 600 Art. 14(e)
            "bl_on_board_date": "2026-10-16",  # adheres to Accepted Amd 1 (Oct 18)
            "bl_vessel": "EVER GLORY",
            "bl_notify_party": "Pacific Heavy Machinery Pte Ltd, 82 Shenton Way, Singapore 079120",
            "packing_gross_weight_kg": 18450.00,
            "bl_gross_weight_kg": 18450.00,
            "insurance_doc_type": "Insurance Certificate",
            "insurance_amount": 264000.00,  # 110% of $240,000 = $264,000 (compliant)
            "insurance_effective_date": "2026-10-14",
            "presentation_date": "2026-10-24",
        },
        "target_verdict": "APPROVE_HONOUR",
        "primary_citation": "ISBP 745 Para A23 & UCP 600 Art. 14(e)",
    },
    # Flagship 2: The Curable Discrepancy & Demurrage Save ($480,000 Cotton Yarn)
    {
        "master": {
            "lc_id": "LC-2026-9104",
            "swift_mt700_raw": ":20: LC-2026-9104\n:31D: 261120 CHITTAGONG\n:50: DELTA TEXTILE MILLS LTD, DHAKA BANGLADESH\n:59: INDUS TEXTILES PVT LTD, KARACHI PAKISTAN\n:32B: USD 480000,00\n:44C: 261025\n:45A: 150000 KGS 100PCT COTTON COMBED YARN AT USD 3.20 PER KG CIF CHITTAGONG\n:46A: INVOICE, BL, PACKING LIST, INSURANCE CERTIFICATE FOR 110PCT CIF VALUE\n:48: 21 DAYS",
            "issuing_bank": "Eastern Commercial Bank Ltd",
            "applicant_name": "Delta Textile Mills Ltd",
            "applicant_address_strict": "Planners Tower, Level 8, 13/A Sonargaon Road, Dhaka 1000",
            "beneficiary_name": "Indus Textiles Pvt Ltd",
            "currency": "USD",
            "amount": 480000.00,
            "tolerance_pct": 0.00,
            "incoterm": "CIF",
            "hs_code_6": "5205.12",
            "goods_description_strict": "150000 KGS 100PCT COTTON COMBED YARN AT USD 3.20 PER KG CIF CHITTAGONG",
            "unit_price": 3.20,
            "quantity": 150000,
            "port_of_loading": "Karachi, Pakistan",
            "port_of_discharge": "Chittagong, Bangladesh",
            "latest_shipment_date": "2026-10-25",
            "expiry_date": "2026-11-20",
            "presentation_period_days": 21,
            "insurance_min_pct": 110.00,
            "daily_demurrage_usd": 1850.00,
        },
        "amendments": [],
        "presentation": {
            "invoice_no": "IND-YARN-8802",
            "invoice_amount": 480000.00,
            "invoice_unit_price": 3.20,
            "invoice_quantity": 150000,
            "invoice_goods_description": "150000 KGS 100PCT COTTON COMBED YARN",
            "bl_no": "HLCUKAR261019",
            "bl_goods_description": "100PCT COTTON COMBED YARN IN 3000 CARTONS",
            "bl_on_board_date": "2026-10-20",
            "bl_vessel": "KOTA WARIS",
            "bl_notify_party": "Delta Textile Mills Ltd, Dhaka Bangladesh",
            "packing_gross_weight_kg": 24500.00,  # Conflict: 24,500 vs 24,050 kg (Art. 14(d))
            "bl_gross_weight_kg": 24050.00,
            "insurance_doc_type": "Insurance Certificate",
            "insurance_amount": 518400.00,  # 108% of CIF instead of 110% ($528,000 required). Shortfall = $9,600!
            "insurance_effective_date": "2026-10-18",
            "presentation_date": "2026-10-30",  # 10 days after shipment; 11 days remaining in 21-day window
        },
        "target_verdict": "ISSUE_MT734_REFUSAL",
        "primary_citation": "UCP 600 Art. 28(f)(ii) & Art. 14(d)",
    },
    # Flagship 3: The Cross-Silo TBML & Sanctions Freeze ($675,000 Precision Valves)
    {
        "master": {
            "lc_id": "LC-2026-9920",
            "swift_mt700_raw": ":20: LC-2026-9920\n:31D: 261130 DUBAI\n:50: EURASIA PIPELINE VALVES LTD, JAFZA DUBAI UAE\n:59: ORIENTAL DRILLING HARDWARE CO, SHANGHAI CHINA\n:32B: USD 675000,00\n:44C: 261031\n:45A: 1500 UNITS INDUSTRIAL HIGH PRESSURE BALL VALVES AT USD 450.00 PER UNIT CIF JEBEL ALI\n:46A: INVOICE, BL, PACKING LIST, INSURANCE POLICY",
            "issuing_bank": "Emirates Commercial Banking Corp",
            "applicant_name": "Eurasia Pipeline Valves Ltd",
            "applicant_address_strict": "Jafza View 18, 12th Floor, Jebel Ali Free Zone, Dubai UAE",
            "beneficiary_name": "Oriental Drilling Hardware Co",
            "currency": "USD",
            "amount": 675000.00,
            "tolerance_pct": 0.00,
            "incoterm": "CIF",
            "hs_code_6": "8481.80",
            "goods_description_strict": "1500 UNITS INDUSTRIAL HIGH PRESSURE BALL VALVES AT USD 450.00 PER UNIT CIF JEBEL ALI",
            "unit_price": 450.00,  # Customs benchmark mean is $92.00, stddev $15.50 -> Z-score = +23.1!
            "quantity": 1500,
            "port_of_loading": "Shanghai, China",
            "port_of_discharge": "Jebel Ali, Dubai",
            "latest_shipment_date": "2026-10-31",
            "expiry_date": "2026-11-30",
            "presentation_period_days": 21,
            "insurance_min_pct": 110.00,
            "daily_demurrage_usd": 2200.00,
        },
        "amendments": [],
        "presentation": {
            "invoice_no": "ODH-2026-VALV-99",
            "invoice_amount": 675000.00,
            "invoice_unit_price": 450.00,
            "invoice_quantity": 1500,
            "invoice_goods_description": "1500 UNITS INDUSTRIAL HIGH PRESSURE BALL VALVES",
            "bl_no": "COSCOSH261022",
            "bl_goods_description": "INDUSTRIAL HIGH PRESSURE BALL VALVES",
            "bl_on_board_date": "2026-10-22",
            "bl_vessel": "PACIFIC STAR",  # Watchlist Vessel Hit!
            "bl_notify_party": "Eurasia Pipeline Valves Ltd",  # Watchlist hit (controlled by Northern Petrochemical)
            "packing_gross_weight_kg": 12500.00,
            "bl_gross_weight_kg": 12500.00,
            "insurance_doc_type": "Insurance Policy",
            "insurance_amount": 742500.00,  # 110% of CIF ($675k) = $742.5k (compliant on face)
            "insurance_effective_date": "2026-10-21",
            "presentation_date": "2026-10-28",
        },
        "target_verdict": "COMPLIANCE_HOLD_AML",
        "primary_citation": "Regulatory AML / OFAC Freeze (Non-MT734)",
    },
]

# Additional 7 evaluation cases
EVAL_CASES = [
    {
        "lc_id": "LC-EVAL-0004",
        "title": "Prohibited Cover Note Rejection",
        "hs_code": "8501.10",
        "unit_price": 480.00,
        "amount": 240000.00,
        "insurance_doc_type": "Cover Note",  # Prohibited under Art. 28(c)
        "target_verdict": "ISSUE_MT734_REFUSAL",
        "citation": "UCP 600 Art. 28(c)",
    },
    {
        "lc_id": "LC-EVAL-0005",
        "title": "Late Presentation (>21 Days After Shipment)",
        "hs_code": "8501.10",
        "unit_price": 480.00,
        "amount": 240000.00,
        "shipment_date": "2026-09-01",
        "presentation_date": "2026-09-25",  # 24 days later! (>21 days)
        "target_verdict": "ISSUE_MT734_REFUSAL",
        "citation": "UCP 600 Art. 14(c)",
    },
    {
        "lc_id": "LC-EVAL-0006",
        "title": "Consignee Address Mismatch on B/L",
        "hs_code": "8501.10",
        "unit_price": 480.00,
        "amount": 240000.00,
        "consignee_box_address": "Wrong Address 99 Orchard Road, Singapore",
        "target_verdict": "ISSUE_MT734_REFUSAL",
        "citation": "UCP 600 Art. 14(j)",
    },
    {
        "lc_id": "LC-EVAL-0007",
        "title": "Partial Amendment Acceptance (Prohibited)",
        "hs_code": "8501.10",
        "unit_price": 480.00,
        "amount": 240000.00,
        "partial_amendment": True,  # Art. 10(e) partial acceptance
        "target_verdict": "ISSUE_MT734_REFUSAL",
        "citation": "UCP 600 Art. 10(e)",
    },
    {
        "lc_id": "LC-EVAL-0008",
        "title": "Valid Quantity Tolerance (+/- 5%)",
        "hs_code": "5205.12",
        "unit_price": 3.20,
        "amount": 460800.00,  # 144,000 kgs (-4% within 5% tolerance)
        "quantity_actual": 144000,
        "target_verdict": "APPROVE_HONOUR",
        "citation": "UCP 600 Art. 30(b)",
    },
    {
        "lc_id": "LC-EVAL-0009",
        "title": "Invoice Missing Mandatory Model Spec",
        "hs_code": "8501.10",
        "unit_price": 480.00,
        "amount": 240000.00,
        "invoice_goods": "Industrial Machine (Model omitted)",  # Art. 18(c) strict specification violated
        "target_verdict": "ISSUE_MT734_REFUSAL",
        "citation": "UCP 600 Art. 18(c)",
    },
    {
        "lc_id": "LC-EVAL-0010",
        "title": "Clean Presentation with Implicit Art. 10(c) Acceptance",
        "hs_code": "8501.10",
        "unit_price": 480.00,
        "amount": 240000.00,
        "target_verdict": "APPROVE_HONOUR",
        "citation": "UCP 600 Art. 10(c)",
    },
]


def seed_presentation_files() -> None:
    """Write presentations JSON for scenarios and evaluation cases."""
    for sc in SCENARIOS_DATA:
        lc_id = sc["master"]["lc_id"]
        filepath = PRESENTATIONS_DIR / f"{lc_id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(sc, f, indent=2)
        print(f"Written presentation packet: {filepath}")

    eval_filepath = PRESENTATIONS_DIR / "eval_scenarios.json"
    with open(eval_filepath, "w", encoding="utf-8") as f:
        json.dump(EVAL_CASES, f, indent=2)
    print(f"Written evaluation cases packet: {eval_filepath}")


def seed_duckdb_standby() -> Path:
    """Create local DuckDB database holding postgres_trade standby tables."""
    duckdb_path = DB_DIR / "veritas_standby.duckdb"
    con = duckdb.connect(str(duckdb_path))

    # Read and apply schema
    schema_path = DB_DIR / "schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    # Create tables
    con.execute(schema_sql)

    # Insert Scenarios
    for sc in SCENARIOS_DATA:
        m = sc["master"]
        con.execute(
            """
            INSERT OR REPLACE INTO lc_master (
                lc_id, swift_mt700_raw, issuing_bank, applicant_name,
                applicant_address_strict, beneficiary_name, currency, amount,
                tolerance_pct, incoterm, hs_code_6, goods_description_strict,
                unit_price, quantity, port_of_loading, port_of_discharge,
                latest_shipment_date, expiry_date, presentation_period_days,
                insurance_min_pct, daily_demurrage_usd
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                m["lc_id"],
                m["swift_mt700_raw"],
                m["issuing_bank"],
                m["applicant_name"],
                m["applicant_address_strict"],
                m["beneficiary_name"],
                m["currency"],
                m["amount"],
                m["tolerance_pct"],
                m["incoterm"],
                m["hs_code_6"],
                m["goods_description_strict"],
                m["unit_price"],
                m["quantity"],
                m["port_of_loading"],
                m["port_of_discharge"],
                m["latest_shipment_date"],
                m["expiry_date"],
                m["presentation_period_days"],
                m["insurance_min_pct"],
                m["daily_demurrage_usd"],
            ],
        )

        for amd in sc["amendments"]:
            con.execute(
                """
                INSERT OR REPLACE INTO lc_amendments (
                    amendment_id, lc_id, sequence_no, amended_field,
                    old_value, new_value, beneficiary_acceptance_status, effective_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    amd["amendment_id"],
                    amd["lc_id"],
                    amd["sequence_no"],
                    amd["amended_field"],
                    amd["old_value"],
                    amd["new_value"],
                    amd["beneficiary_acceptance_status"],
                    amd["effective_date"],
                ],
            )

    # Insert Evaluation Cases into lc_master
    for ec in EVAL_CASES:
        lc_id = ec["lc_id"]
        con.execute(
            """
            INSERT OR REPLACE INTO lc_master (
                lc_id, swift_mt700_raw, issuing_bank, applicant_name,
                applicant_address_strict, beneficiary_name, currency, amount,
                tolerance_pct, incoterm, hs_code_6, goods_description_strict,
                unit_price, quantity, port_of_loading, port_of_discharge,
                latest_shipment_date, expiry_date, presentation_period_days,
                insurance_min_pct, daily_demurrage_usd
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                lc_id,
                f":20: {lc_id}\n:31D: 261115 SINGAPORE\n:32B: USD {ec.get('amount', 240000.0)}\n:45A: {ec.get('title', 'Goods')}",
                "Global Trade Bank Singapore",
                "Pacific Heavy Machinery Pte Ltd",
                "82 Shenton Way, Singapore 079120",
                "Rotor Dynamics GmbH",
                "USD",
                float(ec.get("amount", 240000.0)),
                5.0 if ec.get("quantity_actual") else 0.0,
                "CIF",
                ec.get("hs_code", "8501.10"),
                "500 UNITS INDUSTRIAL AC SERVO MACHINE MODEL X-200 AT USD 480.00 PER UNIT CIF SINGAPORE",
                float(ec.get("unit_price", 480.0)),
                500 if not ec.get("quantity_actual") else 150000,
                "Hamburg, Germany",
                "Singapore",
                "2026-10-10",
                "2026-11-15",
                21,
                110.0,
                1850.0,
            ],
        )

        if ec.get("partial_amendment"):
            con.execute(
                """
                INSERT OR REPLACE INTO lc_amendments (
                    amendment_id, lc_id, sequence_no, amended_field,
                    old_value, new_value, beneficiary_acceptance_status, effective_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    f"AMD-{lc_id}-01",
                    lc_id,
                    1,
                    "amount",
                    "240000.0",
                    "220000.0",
                    "UNACCEPTED_PENDING",
                    "2026-10-01",
                ],
            )

    con.close()
    print(f"Seeded DuckDB standby database at {duckdb_path}")
    return duckdb_path


def main() -> None:
    print("=== Starting VERITAS-600 Phase 1 Data Seeding ===")
    seed_customs_parquet()
    seed_presentation_files()
    seed_duckdb_standby()
    print("=== Data Seeding Completed Successfully ===")


if __name__ == "__main__":
    main()
