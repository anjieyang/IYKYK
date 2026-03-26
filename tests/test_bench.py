"""Benchmark integration tests for classifier and final routed decisions."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bench.dataset import DATASET, TestCase  # noqa: E402
from bench.evaluate import compute_metrics, evaluate_dataset, fit_temperature_scaling  # noqa: E402
from bench.run import _baseline_is_comparable, _build_result, _load_jsonl_as_testcases  # noqa: E402
from uncommon_route.router.classifier import classify  # noqa: E402
from uncommon_route.router.types import ScoringConfig, Tier  # noqa: E402

MIN_OVERALL_ACCURACY = 0.85
MIN_TIER_F1: dict[str, float] = {
    "SIMPLE": 0.80,
    "MEDIUM": 0.80,
    "COMPLEX": 0.80,
}
TIERS = [Tier.SIMPLE, Tier.MEDIUM, Tier.COMPLEX]


def _tier_f1(evals: list[dict]) -> dict[str, float]:
    metrics = compute_metrics(evals)
    return {tier.value: metrics["per_tier"][tier.value]["f1"] for tier in TIERS}


@pytest.fixture(scope="module")
def classifier_results() -> list[dict]:
    return evaluate_dataset(DATASET, ScoringConfig(), view="classifier")


@pytest.fixture(scope="module")
def route_results() -> list[dict]:
    return evaluate_dataset(DATASET, ScoringConfig(), view="route")


class TestClassifierBenchmarkAccuracy:
    """Regression guard for the raw classifier view."""

    def test_overall_accuracy(self, classifier_results: list[dict]) -> None:
        correct = sum(1 for e in classifier_results if e["correct"])
        accuracy = correct / len(classifier_results)
        assert accuracy >= MIN_OVERALL_ACCURACY, (
            f"Overall accuracy {accuracy:.3f} < {MIN_OVERALL_ACCURACY} ({correct}/{len(classifier_results)})"
        )

    def test_per_tier_f1(self, classifier_results: list[dict]) -> None:
        f1s = _tier_f1(classifier_results)
        for tier_name, threshold in MIN_TIER_F1.items():
            assert f1s[tier_name] >= threshold, f"{tier_name} F1 {f1s[tier_name]:.3f} < {threshold}"

    def test_no_extreme_confusion(self, classifier_results: list[dict]) -> None:
        """SIMPLE<->COMPLEX confusions should be rare (at most 3 each direction)."""
        simple_to_complex = sum(
            1 for item in classifier_results if item["expected"] == "SIMPLE" and item["resolved"] == "COMPLEX"
        )
        complex_to_simple = sum(
            1 for item in classifier_results if item["expected"] == "COMPLEX" and item["resolved"] == "SIMPLE"
        )
        assert simple_to_complex <= 3, f"SIMPLE -> COMPLEX confusions: {simple_to_complex} (max 3)"
        assert complex_to_simple <= 3, f"COMPLEX -> SIMPLE confusions: {complex_to_simple} (max 3)"


class TestFeatureAwareRoutingBenchmark:
    def test_route_view_applies_routing_features(self) -> None:
        """routing_features are passed through but don't override the classifier."""
        cases = [
            TestCase(
                "Which migration failed?",
                "SIMPLE",
                "tool-followup-floor",
                "en",
                routing_features={
                    "step_type": "tool-followup",
                    "has_tool_results": True,
                    "tier_floor": "MEDIUM",
                },
            ),
            TestCase(
                (
                    "Design a distributed consensus algorithm that handles Byzantine faults "
                    "with formal correctness proofs and implement it in Rust."
                ),
                "COMPLEX",
                "tool-selection-cap",
                "en",
                routing_features={
                    "step_type": "tool-selection",
                    "tool_names": ["bash"],
                    "needs_tool_calling": True,
                    "is_agentic": True,
                    "requested_max_output_tokens": 64,
                    "tier_cap": "MEDIUM",
                },
            ),
        ]

        classifier_view = evaluate_dataset(cases, ScoringConfig(), view="classifier")
        route_view = evaluate_dataset(cases, ScoringConfig(), view="route")

        for cv, rv in zip(classifier_view, route_view):
            assert rv["resolved"] == cv["resolved"], (
                f"route view resolved {rv['resolved']} != classifier {cv['resolved']}; "
                "tier_floor/tier_cap should not override"
            )

        assert route_view[0]["routing_features"]["tier_floor"] == "MEDIUM"
        assert route_view[1]["routing_features"]["tier_cap"] == "MEDIUM"

    def test_route_metrics_include_feature_slices_and_calibration(self, route_results: list[dict]) -> None:
        metrics = compute_metrics(route_results)

        assert metrics["summary"]["feature_annotated"] >= 3
        assert "annotated" in metrics["per_feature_slice"]
        assert "tier-floor:MEDIUM" in metrics["per_feature_slice"]
        assert "tier-cap:MEDIUM" in metrics["per_feature_slice"]
        assert 0.0 <= metrics["calibration"]["ece"] <= 1.0
        assert 0.0 <= metrics["calibration"]["avg_confidence"] <= 1.0

    def test_temperature_fit_does_not_worsen_ece(self, route_results: list[dict]) -> None:
        fit = fit_temperature_scaling(route_results)

        assert fit["temperature"] > 0.0
        assert fit["calibrated"]["ece"] <= fit["raw"]["ece"] + 1e-12

    def test_jsonl_loader_parses_optional_routing_fields(self, tmp_path: Path) -> None:
        dataset_path = tmp_path / "route-bench.jsonl"
        dataset_path.write_text(
            (
                '{"prompt":"Which migration failed?","expected_tier":"MEDIUM",'
                '"expected_classifier_tier":"SIMPLE","category":"tool-followup-floor","lang":"en",'
                '"routing_features":{"step_type":"tool-followup","has_tool_results":true,"tier_floor":"MEDIUM"}}\n'
            ),
            encoding="utf-8",
        )

        cases = _load_jsonl_as_testcases(dataset_path)

        assert len(cases) == 1
        assert cases[0].expected_classifier_tier == "SIMPLE"
        assert cases[0].routing_features == {
            "step_type": "tool-followup",
            "has_tool_results": True,
            "tier_floor": "MEDIUM",
        }

    def test_baseline_comparison_rejects_dataset_mismatch(self) -> None:
        result = _build_result(
            [TestCase("Which migration failed?", "MEDIUM", "tool-followup-floor", "en")],
            ScoringConfig(),
        )

        assert result["dataset"]["fingerprint"]
        assert _baseline_is_comparable(
            result,
            {"dataset": dict(result["dataset"])},
        )
        assert not _baseline_is_comparable(
            result,
            {"dataset": {**result["dataset"], "fingerprint": "stale-baseline"}},
        )


class TestClassifierSmoke:
    """Quick sanity checks for individual classifier stages."""

    def test_greeting_is_simple(self) -> None:
        assert classify("hello").tier == Tier.SIMPLE

    def test_empty_is_simple(self) -> None:
        assert classify("").tier == Tier.SIMPLE

    def test_code_snippet_question_not_reasoning(self) -> None:
        result = classify("What does this code do?\n```python\nprint('hello')\n```")
        assert result.tier in (Tier.SIMPLE, Tier.MEDIUM)

    def test_complex_requirements(self) -> None:
        prompt = (
            "Design a distributed caching system with TTL-based expiration, "
            "LRU eviction, cross-datacenter replication, automatic failover, "
            "write-behind caching with configurable flush intervals, "
            "and a RESTful management API with role-based access control."
        )
        assert classify(prompt).tier == Tier.COMPLEX

    def test_math_proof_is_complex(self) -> None:
        assert classify("Prove that sqrt(2) is irrational using proof by contradiction").tier == Tier.COMPLEX

    def test_chinese_greeting(self) -> None:
        result = classify("你好")
        assert result.tier == Tier.SIMPLE
        assert result.confidence > 0.0

    def test_confidence_range(self) -> None:
        result = classify("explain quicksort")
        assert 0.0 <= result.confidence <= 1.0
