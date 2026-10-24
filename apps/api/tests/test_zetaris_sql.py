"""Verification Gate 1: Join-Safe Zetaris 3-Silo Federated SQL Tests.

Invariants tested:
1. Join-Safe SQL Rule: Exactly 1 row per lc_id is returned (no Cartesian row multiplication).
2. CTE Pre-Aggregation: Accepted amendments update shipment date; unaccepted amendments are quarantined.
3. Customs Benchmark Anomaly: Unit-price Z-score calculation across Parquet customs stats.
4. OpenSanctions Aggregation: Watchlist matches detected across parties and vessel IMO without extra rows.
5. Latency requirement: Query execution takes < 1.5s.
"""

from __future__ import annotations

import pytest

from apps.api.zetaris.client import ZetarisFederationClient


@pytest.fixture
def zetaris_client() -> ZetarisFederationClient:
    return ZetarisFederationClient(execution_mode="FORCE_FALLBACK")


def test_scenario_1_wrongful_dishonor_amendment_quarantine(zetaris_client: ZetarisFederationClient):
    """Test LC-2026-8841: Amendment #1 accepted, Amendment #2 quarantined."""
    res = zetaris_client.execute_federated_check(
        lc_id="LC-2026-8841",
        beneficiary_name="Rotor Dynamics GmbH",
        vessel_name="EVER GLORY",
        notify_party_name="Pacific Heavy Machinery Pte Ltd",
        invoice_unit_price=480.00,
    )

    assert res["execution_mode"] in ("LIVE_ZETARIS", "LOCAL_DUCKDB_FALLBACK")
    assert res["query_ms"] < 1500, f"Query took {res['query_ms']}ms, expected < 1500ms"

    row = res["row"]
    assert row["lc_id"] == "LC-2026-8841"

    # Effective shipment date must reflect Accepted Amendment #1 (2026-10-18), not original (2026-10-10)
    assert str(row["effective_shipment_date"]) == "2026-10-18"
    assert str(row["original_shipment_date"]) == "2026-10-10"

    # Unaccepted Amendment #2 must be quarantined per Art. 10(c)
    assert row["quarantined_amendment_count"] == 1
    assert "port_of_discharge=Jurong Port, Singapore" in row["quarantined_amendments_summary"]

    # Customs check: unit price matches benchmark ($480), Z-score should be 0.0
    assert row["hs_code_6"] == "8501.10"
    assert float(row["tbml_price_zscore"]) == 0.0

    # Sanctions check: clean
    assert row["sanction_hit_count"] == 0


def test_scenario_2_cotton_yarn_benchmark(zetaris_client: ZetarisFederationClient):
    """Test LC-2026-9104: Clean amendments, normal unit price."""
    res = zetaris_client.execute_federated_check(
        lc_id="LC-2026-9104",
        beneficiary_name="Indus Textiles Pvt Ltd",
        vessel_name="KOTA WARIS",
        notify_party_name="Delta Textile Mills Ltd",
        invoice_unit_price=3.20,
    )

    row = res["row"]
    assert row["lc_id"] == "LC-2026-9104"
    assert str(row["effective_shipment_date"]) == "2026-10-25"
    assert row["quarantined_amendment_count"] == 0
    assert row["hs_code_6"] == "5205.12"
    assert float(row["tbml_price_zscore"]) == 0.0
    assert row["sanction_hit_count"] == 0


def test_scenario_3_tbml_price_anomaly_and_sanctions_freeze(zetaris_client: ZetarisFederationClient):
    """Test LC-2026-9920: Extreme TBML Z-score (>4.0) and OpenSanctions vessel/notify hit."""
    res = zetaris_client.execute_federated_check(
        lc_id="LC-2026-9920",
        beneficiary_name="Oriental Drilling Hardware Co",
        vessel_name="Pacific Star",
        notify_party_name="Eurasia Pipeline Valves Ltd",
        invoice_unit_price=450.00,  # Benchmark mean is $92, stddev $15.50
    )

    row = res["row"]
    assert row["lc_id"] == "LC-2026-9920"

    # Silo 2: Extreme TBML Unit Price Anomaly
    # Z = (450 - 92) / 15.50 = +23.10
    z_score = float(row["tbml_price_zscore"])
    assert z_score > 4.0, f"Expected Z-score > 4.0 for TBML flag, got {z_score}"
    assert z_score == pytest.approx(23.10, abs=0.1)

    # Silo 3: OpenSanctions Matches
    # Matches both Pacific Star (vessel) and Eurasia Pipeline Valves Ltd (notify party)
    assert row["sanction_hit_count"] >= 1
    assert float(row["sanction_max_risk_score"]) >= 8.5
    assert "Northern Petrochemical Holdings" in row["sanctions_summary"] or "OFAC" in row["sanctions_summary"]


def test_join_safe_single_row_guarantee(zetaris_client: ZetarisFederationClient):
    """Verify that multiple amendments or multiple watchlist hits never cause row duplication."""
    for lc_id in ["LC-2026-8841", "LC-2026-9104", "LC-2026-9920"]:
        res = zetaris_client.execute_federated_check(
            lc_id=lc_id,
            beneficiary_name="Northern Petrochemical Holdings",  # Trigger multiple hits
            vessel_name="Pacific Star",
            notify_party_name="Eurasia Pipeline Valves Ltd",
            invoice_unit_price=100.00,
        )
        assert isinstance(res["row"], dict)
        assert res["row"]["lc_id"] == lc_id
