"""Unit and Integration Tests for Baseline Comparison Suite & Evals API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from apps.api.evals.compare_baselines import BaselineComparisonSuite
from apps.api.main import app

client = TestClient(app)


def test_baseline_suite_loads_all_10_scenarios() -> None:
    suite = BaselineComparisonSuite()
    scenarios = suite.load_all_scenarios()
    assert len(scenarios) == 10, f"Expected 10 scenarios, found {len(scenarios)}"
    lc_ids = [s["master"]["lc_id"] for s in scenarios]
    assert "LC-2026-8841" in lc_ids
    assert "LC-2026-9104" in lc_ids
    assert "LC-2026-9920" in lc_ids
    assert "LC-EVAL-0004" in lc_ids
    assert "LC-EVAL-0010" in lc_ids


def test_regex_baseline_failure_modes() -> None:
    suite = BaselineComparisonSuite()
    scenarios = {s["master"]["lc_id"]: s for s in suite.load_all_scenarios()}

    # LC-2026-8841: Regex fails on typo 'Mashine'
    res_8841 = suite.evaluate_regex_baseline(scenarios["LC-2026-8841"])
    assert res_8841.verdict == "ISSUE_MT734_REFUSAL"
    assert not res_8841.is_correct
    assert "Wrongful Dishonor" in (res_8841.failure_mode or "")

    # LC-2026-9920: Regex passes face-valid docs, missing customs / OFAC
    res_9920 = suite.evaluate_regex_baseline(scenarios["LC-2026-9920"])
    assert res_9920.verdict == "APPROVE_HONOUR"
    assert not res_9920.is_correct
    assert "Leakage" in (res_9920.failure_mode or "")


def test_single_prompt_llm_failure_modes() -> None:
    suite = BaselineComparisonSuite()
    scenarios = {s["master"]["lc_id"]: s for s in suite.load_all_scenarios()}

    # LC-2026-9104: LLM excuses 108% insurance shortfall
    res_9104 = suite.evaluate_single_prompt_llm(scenarios["LC-2026-9104"])
    assert res_9104.verdict == "APPROVE_HONOUR"
    assert not res_9104.is_correct
    assert "Hallucinatory Flattery" in (res_9104.failure_mode or "")

    # LC-2026-9920: LLM context boundary blindspot
    res_9920 = suite.evaluate_single_prompt_llm(scenarios["LC-2026-9920"])
    assert res_9920.verdict == "APPROVE_HONOUR"
    assert not res_9920.is_correct
    assert "Blindspot" in (res_9920.failure_mode or "")


def test_veritas_600_achieves_perfect_accuracy() -> None:
    suite = BaselineComparisonSuite()
    results = suite.run_benchmark()

    veritas = results["architectures"]["veritas_600"]
    assert veritas["accuracy_pct"] == 100.0, f"Expected 100% accuracy, got {veritas['accuracy_pct']}"
    assert veritas["correct_count"] == 10
    assert veritas["wrongful_dishonor_rate_pct"] == 0.0
    assert veritas["sanctions_leakage_rate_pct"] == 0.0
    assert veritas["hard_invariant_compliance"] == 100.0
    assert veritas["demurrage_savings_usd"] == 11100.0


def test_evals_api_endpoints() -> None:
    # 1. Trigger live benchmark
    post_res = client.post("/api/v1/evals/run")
    assert post_res.status_code == 200
    data = post_res.json()
    assert data["total_scenarios"] == 10
    assert "architectures" in data
    assert data["architectures"]["veritas_600"]["accuracy_pct"] == 100.0

    # 2. Query cached results
    get_res = client.get("/api/v1/evals/results")
    assert get_res.status_code == 200
    get_data = get_res.json()
    assert get_data["total_scenarios"] == 10
    assert len(get_data["rows"]) == 10
