"""Benchmark runner for UncommonRoute classification and routing quality.

Usage:
    python -m bench.run                          # 运行手写数据集 benchmark
    python -m bench.run --data bench/data/dev.jsonl  # 运行指定 JSONL 数据集
    python -m bench.run --baseline               # 运行并设为 baseline
    python -m bench.run --compare path/to/old.json   # 和指定文件对比
"""

from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from bench.dataset import DATASET, TestCase
from bench.evaluate import (
    collapse_tier,
    compute_metrics,
    evaluate_dataset,
    fit_temperature_scaling,
)
from uncommon_route.router.types import ScoringConfig

RESULTS_DIR = Path(__file__).parent / "results"
BENCH_VIEWS = ("route", "classifier")
PRIMARY_VIEW = "route"


def _config_hash(config: ScoringConfig) -> str:
    return hashlib.md5(
        json.dumps(asdict(config), sort_keys=True).encode(),
    ).hexdigest()[:8]


def _dataset_fingerprint(dataset: list[TestCase]) -> str:
    serialized = [asdict(test_case) for test_case in dataset]
    return hashlib.md5(
        json.dumps(serialized, ensure_ascii=False, sort_keys=True).encode("utf-8"),
    ).hexdigest()[:12]


def _build_result(dataset: list[TestCase], config: ScoringConfig) -> dict:
    views: dict[str, dict] = {}
    for view in BENCH_VIEWS:
        evals = evaluate_dataset(dataset, config, view=view)
        metrics = compute_metrics(evals)
        metrics["posthoc_temperature"] = fit_temperature_scaling(evals)
        views[view] = metrics

    primary = views[PRIMARY_VIEW]
    feature_annotated = sum(1 for tc in dataset if tc.routing_features)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config_hash": _config_hash(config),
        "dataset": {
            "total": len(dataset),
            "langs": sorted({tc.lang for tc in dataset}),
            "feature_annotated": feature_annotated,
            "fingerprint": _dataset_fingerprint(dataset),
        },
        "views": views,
        "summary": primary["summary"],
        "per_tier": primary["per_tier"],
        "per_lang": primary["per_lang"],
        "per_category": primary["per_category"],
        "per_feature_slice": primary["per_feature_slice"],
        "calibration": primary["calibration"],
    }


def _pct(n: float) -> str:
    return f"{n * 100:.1f}%"


def _delta(curr: float, base: float) -> str:
    diff = curr - base
    sign = "+" if diff >= 0 else ""
    return f"{sign}{diff * 100:.1f}pp"


def _baseline_view(baseline: dict | None, view: str) -> dict | None:
    if baseline is None:
        return None
    if "views" in baseline:
        return baseline["views"].get(view)
    if view == PRIMARY_VIEW:
        return {
            "summary": baseline.get("summary", {}),
            "per_tier": baseline.get("per_tier", {}),
            "per_category": baseline.get("per_category", {}),
            "calibration": baseline.get("calibration", {}),
            "posthoc_temperature": baseline.get("posthoc_temperature"),
        }
    return None


def _baseline_is_comparable(current: dict, baseline: dict | None) -> bool:
    if baseline is None:
        return False
    current_dataset = current.get("dataset", {})
    baseline_dataset = baseline.get("dataset", {})

    current_fingerprint = current_dataset.get("fingerprint")
    baseline_fingerprint = baseline_dataset.get("fingerprint")
    if current_fingerprint and baseline_fingerprint:
        return current_fingerprint == baseline_fingerprint

    return (
        current_dataset.get("total") == baseline_dataset.get("total")
        and current_dataset.get("langs") == baseline_dataset.get("langs")
        and current_dataset.get("feature_annotated", 0) == baseline_dataset.get("feature_annotated", 0)
    )


def _print_view_block(name: str, result: dict, baseline: dict | None = None) -> None:
    title = "最终路由视角" if name == "route" else "原始分类视角"
    summary = result["summary"]
    calibration = result["calibration"]
    calibrated = result["posthoc_temperature"]["calibrated"]
    baseline_summary = baseline["summary"] if baseline else None

    print(f"  {title}:")
    acc_delta = f" ({_delta(summary['accuracy'], baseline_summary['accuracy'])})" if baseline_summary else ""
    f1_delta = f" ({_delta(summary['weighted_f1'], baseline_summary['weighted_f1'])})" if baseline_summary else ""
    ece_delta = ""
    if baseline and baseline.get("calibration"):
        ece_delta = f" ({_delta(calibration['ece'], baseline['calibration']['ece'])})"

    print(f"    准确率:    {_pct(summary['accuracy'])}{acc_delta}    ({summary['correct']}/{summary['total']})")
    print(f"    加权 F1:   {_pct(summary['weighted_f1'])}{f1_delta}")
    print(f"    模糊分类:  {summary['ambiguous']}")
    print(f"    平均置信度: {_pct(summary['avg_confidence'])}")
    print(f"    ECE:       {_pct(calibration['ece'])}{ece_delta}")
    print(
        "    温度校准: "
        f"T={result['posthoc_temperature']['temperature']:.2f} "
        f"| ECE {_pct(calibration['ece'])} -> {_pct(calibrated['ece'])}"
    )

    print()
    print("    ┌───────────┬───────────┬────────┬────────┐")
    print("    │   Tier    │ Precision │ Recall │   F1   │")
    print("    ├───────────┼───────────┼────────┼────────┤")
    for tier_name, metrics in result["per_tier"].items():
        precision = _pct(metrics["precision"]).rjust(6)
        recall = _pct(metrics["recall"]).rjust(5)
        f1 = _pct(metrics["f1"]).rjust(5)
        suffix = ""
        if baseline and tier_name in baseline.get("per_tier", {}):
            suffix = f" {_delta(metrics['f1'], baseline['per_tier'][tier_name]['f1'])}"
        print(f"    │ {tier_name:<9} │ {precision}    │ {recall}  │ {f1}  │{suffix}")
    print("    └───────────┴───────────┴────────┴────────┘")

    failed = [
        (category, values) for category, values in sorted(result["per_category"].items()) if values["accuracy"] < 1.0
    ]
    if failed:
        failed.sort(key=lambda item: item[1]["accuracy"])
        print()
        print("    未通过的类别:")
        for category, values in failed[:12]:
            baseline_category = baseline["per_category"].get(category) if baseline else None
            delta = f" ({_delta(values['accuracy'], baseline_category['accuracy'])})" if baseline_category else ""
            print(
                f"      ✗ {category:<28} "
                f"{values['correct']}/{values['total']} {_pct(values['accuracy'])}{delta} "
                f"[{values['expected_tier']}]"
            )

    interesting_slices = [
        (name, metrics) for name, metrics in sorted(result["per_feature_slice"].items()) if name != "unannotated"
    ]
    if interesting_slices:
        print()
        print("    Feature slices:")
        for slice_name, metrics in interesting_slices:
            print(f"      - {slice_name:<24} {metrics['correct']}/{metrics['total']} {_pct(metrics['accuracy'])}")

    print()


def _print_summary(result: dict, baseline: dict | None = None) -> None:
    comparable_baseline = baseline if _baseline_is_comparable(result, baseline) else None

    print()
    print("╔═══════════════════════════════════════╗")
    print("║   UncommonRoute Benchmark             ║")
    print("╚═══════════════════════════════════════╝")
    print()
    print(
        "  数据集: "
        f"{result['dataset']['total']} 条 | "
        f"语言: {', '.join(result['dataset']['langs'])} | "
        f"feature 标注: {result['dataset']['feature_annotated']} | "
        f"config: {result['config_hash']} | "
        f"dataset: {result['dataset']['fingerprint']}"
    )
    print()

    if baseline and comparable_baseline is None:
        print("  基线已忽略: dataset 指纹不一致，旧结果不可直接比较。")
        print()

    for view in BENCH_VIEWS:
        _print_view_block(view, result["views"][view], _baseline_view(comparable_baseline, view))


def _load_jsonl_as_testcases(path: Path) -> list[TestCase]:
    cases = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            row = line.strip()
            if not row:
                continue
            data = json.loads(row)
            cases.append(
                TestCase(
                    prompt=data["prompt"],
                    expected_tier=collapse_tier(data["expected_tier"]),
                    category=data["category"],
                    lang=data["lang"],
                    system_prompt=data.get("system_prompt"),
                    expected_classifier_tier=(
                        collapse_tier(data["expected_classifier_tier"])
                        if data.get("expected_classifier_tier")
                        else None
                    ),
                    routing_features=data.get("routing_features"),
                )
            )
    return cases


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    args = sys.argv[1:]
    is_baseline = "--baseline" in args
    compare_path = None
    data_path = None
    for index, arg in enumerate(args):
        if arg == "--compare" and index + 1 < len(args):
            compare_path = args[index + 1]
        elif arg == "--data" and index + 1 < len(args):
            data_path = Path(args[index + 1])

    dataset = _load_jsonl_as_testcases(data_path) if data_path else DATASET
    config = ScoringConfig()
    result = _build_result(dataset, config)

    ts = result["timestamp"].replace(":", "-").replace(".", "-")
    result_path = RESULTS_DIR / f"{ts}.json"
    result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    baseline: dict | None = None
    baseline_path = RESULTS_DIR / "baseline.json"
    if compare_path:
        baseline = json.loads(Path(compare_path).read_text())
    elif baseline_path.exists() and not is_baseline:
        baseline = json.loads(baseline_path.read_text())

    _print_summary(result, baseline)

    if is_baseline:
        baseline_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"  ✓ 已保存为 baseline ({baseline_path})")
        print()

    latest_path = RESULTS_DIR / "latest.json"
    latest_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"  结果已保存: {result_path}")
    print()

    if result["summary"]["accuracy"] < 0.7:
        sys.exit(1)


if __name__ == "__main__":
    main()
