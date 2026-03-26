"""Offline tuner for route-level boundaries and confidence calibration.

Usage:
    python -m bench.tune                # run grid search
    python -m bench.tune --fine         # finer grid (slower)
"""

from __future__ import annotations

import copy
import itertools
import json
import sys
from pathlib import Path

from bench.dataset import DATASET
from bench.evaluate import compute_metrics, evaluate_dataset, fit_temperature_scaling
from uncommon_route.router.types import ScoringConfig, Tier, TierBoundaries

TIERS = [Tier.SIMPLE, Tier.MEDIUM, Tier.COMPLEX]


def _route_metrics(config: ScoringConfig) -> tuple[float, float, dict[str, float], dict]:
    """Evaluate route-level accuracy and calibration for a config."""
    evals = evaluate_dataset(DATASET, config, view="route")
    metrics = compute_metrics(evals)
    tier_f1 = {tier.value: metrics["per_tier"][tier.value]["f1"] for tier in TIERS}
    return (
        metrics["summary"]["accuracy"],
        metrics["summary"]["weighted_f1"],
        tier_f1,
        metrics,
    )


def _grid_search_boundaries(base_config: ScoringConfig, fine: bool = False) -> ScoringConfig:
    """Search optimal route-level tier boundaries."""
    step = 0.01 if fine else 0.02

    sm_range = [round(x * step, 3) for x in range(-2, 8)]
    mc_range = [round(x * step + 0.06, 3) for x in range(0, 12)]

    best_score = 0.0
    best_config = base_config
    total = len(sm_range) * len(mc_range)

    print(f"  搜索 route tier boundaries ({total} 组合)...")

    for simple_medium, medium_complex in itertools.product(sm_range, mc_range):
        if simple_medium >= medium_complex:
            continue
        cfg = copy.deepcopy(base_config)
        cfg.tier_boundaries = TierBoundaries(
            simple_medium=simple_medium,
            medium_complex=medium_complex,
        )
        _, weighted_f1, _, _ = _route_metrics(cfg)
        if weighted_f1 > best_score:
            best_score = weighted_f1
            best_config = cfg

    bounds = best_config.tier_boundaries
    print(f"  最优 route boundaries: SM={bounds.simple_medium} MC={bounds.medium_complex} -> wF1={best_score:.3f}")
    return best_config


def _fit_route_temperature(config: ScoringConfig) -> dict:
    evals = evaluate_dataset(DATASET, config, view="route")
    return fit_temperature_scaling(evals)


def main() -> None:
    fine = "--fine" in sys.argv

    print()
    print("╔═══════════════════════════════════════╗")
    print("║   UncommonRoute Auto-Tuner            ║")
    print("╚═══════════════════════════════════════╝")
    print()

    base = ScoringConfig()
    acc0, wf1_0, tier_f1_0, base_metrics = _route_metrics(base)
    base_calibration = _fit_route_temperature(base)

    print(f"  当前 route 配置: accuracy={acc0:.3f} wF1={wf1_0:.3f} ECE={base_metrics['calibration']['ece']:.3f}")
    for tier in TIERS:
        print(f"    {tier.value}: F1={tier_f1_0[tier.value]:.3f}")
    print(
        "    温度校准: "
        f"T={base_calibration['temperature']:.2f} "
        f"NLL={base_calibration['raw']['nll']:.3f}->{base_calibration['calibrated']['nll']:.3f} "
        f"ECE={base_calibration['raw']['ece']:.3f}->{base_calibration['calibrated']['ece']:.3f}"
    )
    print()

    tuned = _grid_search_boundaries(base, fine=fine)
    print()

    acc, wf1, tier_f1, metrics = _route_metrics(tuned)
    calibration = _fit_route_temperature(tuned)

    print(f"  调优后 route 指标: accuracy={acc:.3f} wF1={wf1:.3f} ECE={metrics['calibration']['ece']:.3f}")
    for tier in TIERS:
        delta = tier_f1[tier.value] - tier_f1_0[tier.value]
        sign = "+" if delta >= 0 else ""
        print(f"    {tier.value}: F1={tier_f1[tier.value]:.3f} ({sign}{delta:.3f})")
    print(
        "    温度校准: "
        f"T={calibration['temperature']:.2f} "
        f"NLL={calibration['raw']['nll']:.3f}->{calibration['calibrated']['nll']:.3f} "
        f"ECE={calibration['raw']['ece']:.3f}->{calibration['calibrated']['ece']:.3f}"
    )
    print()

    improvement = wf1 - wf1_0
    ece_improvement = calibration["raw"]["ece"] - calibration["calibrated"]["ece"]
    sign = "+" if improvement >= 0 else ""
    if improvement > 0.005:
        print(f"  发现 route 指标改进: wF1 {sign}{improvement:.3f}")
    else:
        print("  route 边界已接近最优，wF1 没有显著提升。")
    if ece_improvement > 0.001:
        print(f"  发现可用校准改进: ECE -{ece_improvement:.3f}")
    print()

    out_path = Path(__file__).parent / "results" / "tuned-config.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(
            {
                "tier_boundaries": {
                    "simple_medium": tuned.tier_boundaries.simple_medium,
                    "medium_complex": tuned.tier_boundaries.medium_complex,
                },
                "metrics": {
                    "route": {
                        "accuracy": acc,
                        "weighted_f1": wf1,
                        "per_tier_f1": tier_f1,
                        "calibration": metrics["calibration"],
                    },
                },
                "route_confidence_calibration": {
                    "temperature": calibration["temperature"],
                    "raw": {
                        "nll": calibration["raw"]["nll"],
                        "ece": calibration["raw"]["ece"],
                        "brier": calibration["raw"]["brier"],
                    },
                    "calibrated": {
                        "nll": calibration["calibrated"]["nll"],
                        "ece": calibration["calibrated"]["ece"],
                        "brier": calibration["calibrated"]["brier"],
                    },
                },
            },
            indent=2,
        )
    )
    print(f"  配置已保存: {out_path}")
    print()


if __name__ == "__main__":
    main()
