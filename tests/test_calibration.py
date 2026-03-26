from __future__ import annotations

from uncommon_route.calibration import (
    InMemoryRouteCalibrationStorage,
    RouteConfidenceCalibrator,
)
from uncommon_route.router.api import route
from uncommon_route.router.types import RoutingFeatures, Tier
from uncommon_route.stats import RouteRecord


def _record(
    *,
    confidence: float,
    signal: str,
    tier: str,
    step_type: str = "general",
    feature_tags: list[str] | None = None,
    complexity: float = 0.33,
    feedback_from_tier: str | None = None,
    feedback_to_tier: str | None = None,
    feedback_action: str | None = None,
    feedback_submitted_at: float = 0.0,
) -> RouteRecord:
    source_tier = feedback_from_tier or tier
    target_tier = feedback_to_tier
    if target_tier is None:
        if signal == "weak":
            target_tier = {
                "SIMPLE": "MEDIUM",
                "MEDIUM": "COMPLEX",
                "COMPLEX": "COMPLEX",
            }.get(source_tier, "MEDIUM")
        elif signal == "strong":
            target_tier = {
                "SIMPLE": "SIMPLE",
                "MEDIUM": "SIMPLE",
                "COMPLEX": "MEDIUM",
            }.get(source_tier, "MEDIUM")
        else:
            target_tier = source_tier
    return RouteRecord(
        timestamp=1.0,
        model="test/model",
        tier=tier,
        decision_tier=tier,
        confidence=confidence,
        raw_confidence=confidence,
        method="pool",
        estimated_cost=0.01,
        mode="auto",
        step_type=step_type,
        feature_tags=feature_tags or [],
        complexity=complexity,
        feedback_signal=signal,
        feedback_action=feedback_action or ("reinforced" if signal == "ok" else "updated"),
        feedback_from_tier=source_tier,
        feedback_to_tier=target_tier,
        feedback_submitted_at=feedback_submitted_at,
    )


def test_route_confidence_calibrator_is_inactive_without_labels() -> None:
    calibrator = RouteConfidenceCalibrator(
        storage=InMemoryRouteCalibrationStorage(),
        min_examples=2,
    )

    estimate = calibrator.calibrate(
        0.83,
        mode="auto",
        tier="MEDIUM",
        complexity=0.4,
    )

    assert estimate.confidence == estimate.raw_confidence == 0.83
    assert estimate.source == "classifier"


def test_route_confidence_calibrator_learns_from_labeled_route_traces() -> None:
    calibrator = RouteConfidenceCalibrator(
        storage=InMemoryRouteCalibrationStorage(),
        min_examples=4,
        min_tag_examples=2,
        prior_strength=2.0,
    )
    records = []
    for _ in range(6):
        records.append(
            _record(
                confidence=0.95,
                signal="weak",
                tier="MEDIUM",
                step_type="tool-followup",
                feature_tags=["step:tool-followup", "tier-floor:MEDIUM", "tool-results"],
                complexity=0.4,
            )
        )
    for _ in range(6):
        records.append(
            _record(
                confidence=0.60,
                signal="ok",
                tier="SIMPLE",
                step_type="general",
                complexity=0.1,
            )
        )

    snapshot = calibrator.fit_from_route_records(records)
    difficult_followup = calibrator.calibrate(
        0.95,
        mode="auto",
        tier="MEDIUM",
        complexity=0.4,
        step_type="tool-followup",
        feature_tags=("step:tool-followup", "tier-floor:MEDIUM", "tool-results"),
    )
    simple_case = calibrator.calibrate(
        0.60,
        mode="auto",
        tier="SIMPLE",
        complexity=0.1,
    )

    assert snapshot.active
    assert snapshot.labeled_examples == 12
    assert difficult_followup.source == "route_calibrated"
    assert difficult_followup.confidence < difficult_followup.raw_confidence
    assert simple_case.confidence > simple_case.raw_confidence
    assert "step:tool-followup" in difficult_followup.applied_adjustments
    assert "feature:step:tool-followup" not in difficult_followup.applied_adjustments


def test_route_uses_calibrated_route_confidence() -> None:
    calibrator = RouteConfidenceCalibrator(
        storage=InMemoryRouteCalibrationStorage(),
        min_examples=4,
        min_tag_examples=2,
        prior_strength=2.0,
    )
    records = []
    for _ in range(6):
        records.append(
            _record(
                confidence=1.0,
                signal="weak",
                tier="MEDIUM",
                step_type="tool-followup",
                feature_tags=["step:tool-followup", "tier-floor:MEDIUM", "tool-results"],
                complexity=0.4,
            )
        )
    for _ in range(6):
        records.append(
            _record(
                confidence=0.55,
                signal="ok",
                tier="SIMPLE",
                complexity=0.1,
            )
        )
    calibrator.fit_from_route_records(records)

    decision = route(
        "Which migration failed?",
        routing_features=RoutingFeatures(
            step_type="tool-followup",
            has_tool_results=True,
            tier_floor=Tier.MEDIUM,
        ),
        route_confidence_calibrator=calibrator,
    )

    # tier_floor is ignored; classifier judges this as SIMPLE
    assert decision.tier is Tier.SIMPLE
    assert decision.confidence_source == "route_calibrated"
    assert decision.calibration_version
    assert decision.calibration_sample_count == 12
    assert decision.calibration_temperature == calibrator.snapshot().temperature
    assert "step:tool-followup" in decision.calibration_applied_tags


def test_route_passes_streaming_context_into_calibration() -> None:
    calibrator = RouteConfidenceCalibrator(
        storage=InMemoryRouteCalibrationStorage(),
        min_examples=4,
        min_tag_examples=2,
        prior_strength=2.0,
    )
    records = []
    for _ in range(6):
        records.append(
            RouteRecord(
                timestamp=1.0,
                model="test/model",
                tier="SIMPLE",
                decision_tier="SIMPLE",
                confidence=0.9,
                raw_confidence=0.9,
                method="pool",
                estimated_cost=0.01,
                mode="auto",
                streaming=True,
                feedback_signal="weak",
            )
        )
    for _ in range(6):
        records.append(
            RouteRecord(
                timestamp=1.0,
                model="test/model",
                tier="SIMPLE",
                decision_tier="SIMPLE",
                confidence=0.6,
                raw_confidence=0.6,
                method="pool",
                estimated_cost=0.01,
                mode="auto",
                streaming=False,
                feedback_signal="ok",
            )
        )
    calibrator.fit_from_route_records(records)

    decision = route(
        "Say hi",
        routing_features=RoutingFeatures(streaming=True),
        route_confidence_calibrator=calibrator,
    )

    assert "streaming" in decision.calibration_applied_tags


def test_route_confidence_calibrator_distinguishes_upgrade_vs_downgrade_pressure() -> None:
    calibrator = RouteConfidenceCalibrator(
        storage=InMemoryRouteCalibrationStorage(),
        min_examples=6,
        min_tag_examples=2,
        prior_strength=1.0,
        min_holdout_examples=20,
    )
    records = []
    for _ in range(6):
        records.append(
            _record(
                confidence=0.92,
                signal="weak",
                tier="MEDIUM",
                complexity=0.66,
                feedback_from_tier="MEDIUM",
                feedback_to_tier="COMPLEX",
            )
        )
    for _ in range(6):
        records.append(
            _record(
                confidence=0.92,
                signal="strong",
                tier="MEDIUM",
                complexity=0.34,
                feedback_from_tier="MEDIUM",
                feedback_to_tier="SIMPLE",
            )
        )
    for _ in range(6):
        records.append(
            _record(
                confidence=0.70,
                signal="ok",
                tier="MEDIUM",
                complexity=0.50,
            )
        )

    calibrator.fit_from_route_records(records)

    upgrade_pressure = calibrator.calibrate(
        0.92,
        mode="auto",
        tier="MEDIUM",
        complexity=0.66,
    )
    downgrade_pressure = calibrator.calibrate(
        0.92,
        mode="auto",
        tier="MEDIUM",
        complexity=0.34,
    )
    centered = calibrator.calibrate(
        0.70,
        mode="auto",
        tier="MEDIUM",
        complexity=0.50,
    )

    assert upgrade_pressure.confidence < centered.confidence
    assert downgrade_pressure.confidence < centered.confidence
    assert "pressure:upgrade" in upgrade_pressure.applied_adjustments
    assert "pressure:downgrade" in downgrade_pressure.applied_adjustments


def test_route_confidence_calibrator_rejects_overfit_with_holdout_gate() -> None:
    calibrator = RouteConfidenceCalibrator(
        storage=InMemoryRouteCalibrationStorage(),
        now_fn=lambda: 200.0,
        min_examples=4,
        min_tag_examples=2,
        prior_strength=1.0,
        holdout_fraction=0.25,
        min_holdout_examples=2,
    )
    records = []
    for idx in range(6):
        records.append(
            _record(
                confidence=0.90,
                signal="weak",
                tier="SIMPLE",
                complexity=0.30,
                feedback_submitted_at=float(idx + 1),
            )
        )
    for idx in range(2):
        records.append(
            _record(
                confidence=0.90,
                signal="ok",
                tier="SIMPLE",
                complexity=0.30,
                feedback_submitted_at=float(100 + idx),
            )
        )

    snapshot = calibrator.fit_from_route_records(records)
    estimate = calibrator.calibrate(
        0.90,
        mode="auto",
        tier="SIMPLE",
        complexity=0.30,
    )

    assert snapshot.selected_strategy == "raw"
    assert calibrator.status()["active"] is False
    assert snapshot.holdout_examples == 2
    assert estimate.source == "classifier"


def test_route_confidence_calibrator_marks_stale_snapshots_inactive() -> None:
    storage = InMemoryRouteCalibrationStorage()
    builder = RouteConfidenceCalibrator(
        storage=storage,
        now_fn=lambda: 100.0,
        min_examples=2,
        min_tag_examples=1,
        max_label_age_s=10.0,
        min_holdout_examples=20,
    )
    builder.fit_from_route_records(
        [
            _record(
                confidence=0.80,
                signal="ok",
                tier="SIMPLE",
                feedback_submitted_at=95.0,
            ),
            _record(
                confidence=0.90,
                signal="weak",
                tier="SIMPLE",
                feedback_submitted_at=96.0,
            ),
        ]
    )

    stale = RouteConfidenceCalibrator(
        storage=storage,
        now_fn=lambda: 200.0,
        min_examples=2,
        min_tag_examples=1,
        max_label_age_s=10.0,
        min_holdout_examples=20,
    )
    estimate = stale.calibrate(
        0.90,
        mode="auto",
        tier="SIMPLE",
        complexity=0.30,
    )

    assert stale.status()["stale"] is True
    assert stale.status()["active"] is False
    assert estimate.source == "classifier"
