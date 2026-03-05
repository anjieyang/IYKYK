"""Benchmark runner for UncommonRoute classifier.

Usage:
    python -m bench.run                          # 运行手写数据集 benchmark
    python -m bench.run --data bench/data/dev.jsonl  # 运行指定 JSONL 数据集
    python -m bench.run --baseline               # 运行并设为 baseline
    python -m bench.run --compare path/to/old.json   # 和指定文件对比
"""

from __future__ import annotations

import json
import sys
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from uncommon_route.router.classifier import classify
from uncommon_route.router.types import ScoringConfig, Tier
from bench.dataset import DATASET, TestCase

TIERS = [Tier.SIMPLE, Tier.MEDIUM, Tier.COMPLEX, Tier.REASONING]
RESULTS_DIR = Path(__file__).parent / "results"


@dataclass
class TierMetrics:
    precision: float
    recall: float
    f1: float
    support: int


def _evaluate(dataset: list[TestCase], config: ScoringConfig) -> list[dict]:
    results = []
    for tc in dataset:
        result = classify(tc.prompt, tc.system_prompt, config)
        resolved = result.tier.value if result.tier else "MEDIUM"
        results.append({
            "expected": tc.expected_tier,
            "actual": result.tier.value if result.tier else None,
            "resolved": resolved,
            "correct": resolved == tc.expected_tier,
            "score": result.score,
            "confidence": result.confidence,
            "category": tc.category,
            "lang": tc.lang,
        })
    return results


def _compute_metrics(evals: list[dict], dataset: list[TestCase] | None = None) -> dict:
    total = len(evals)
    correct = sum(1 for e in evals if e["correct"])
    ambiguous = sum(1 for e in evals if e["actual"] is None)

    per_tier: dict[str, dict] = {}
    for tier in TIERS:
        t = tier.value
        tp = sum(1 for e in evals if e["resolved"] == t and e["expected"] == t)
        fp = sum(1 for e in evals if e["resolved"] == t and e["expected"] != t)
        fn = sum(1 for e in evals if e["resolved"] != t and e["expected"] == t)
        support = sum(1 for e in evals if e["expected"] == t)
        precision = tp / (tp + fp) if tp + fp > 0 else 0.0
        recall = tp / (tp + fn) if tp + fn > 0 else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if precision + recall > 0 else 0.0
        per_tier[t] = {"precision": precision, "recall": recall, "f1": f1, "support": support}

    weighted_f1 = sum(per_tier[t.value]["f1"] * per_tier[t.value]["support"] / total for t in TIERS)

    per_lang: dict[str, dict] = {}
    for e in evals:
        lang = e["lang"]
        entry = per_lang.setdefault(lang, {"total": 0, "correct": 0})
        entry["total"] += 1
        if e["correct"]:
            entry["correct"] += 1
    for v in per_lang.values():
        v["accuracy"] = v["correct"] / v["total"]

    per_cat: dict[str, dict] = {}
    for i, e in enumerate(evals):
        cat = e["category"]
        src = dataset or DATASET
        entry = per_cat.setdefault(cat, {"total": 0, "correct": 0, "expected_tier": src[i].expected_tier if i < len(src) else e["expected"]})
        entry["total"] += 1
        if e["correct"]:
            entry["correct"] += 1
    for v in per_cat.values():
        v["accuracy"] = v["correct"] / v["total"]

    config_hash = hashlib.md5(json.dumps(ScoringConfig().__dict__, default=str).encode()).hexdigest()[:8]

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config_hash": config_hash,
        "dataset": {"total": total, "langs": sorted(set(e["lang"] for e in evals))},
        "summary": {
            "accuracy": correct / total,
            "weighted_f1": weighted_f1,
            "correct": correct,
            "total": total,
            "ambiguous": ambiguous,
        },
        "per_tier": per_tier,
        "per_lang": per_lang,
        "per_category": per_cat,
    }


def _pct(n: float) -> str:
    return f"{n * 100:.1f}%"


def _delta(curr: float, base: float) -> str:
    diff = curr - base
    sign = "+" if diff >= 0 else ""
    return f"{sign}{diff * 100:.1f}pp"


def _print_summary(r: dict, baseline: dict | None = None) -> None:
    b = baseline["summary"] if baseline else None

    print()
    print("╔═══════════════════════════════════════╗")
    print("║   UncommonRoute Benchmark             ║")
    print("╚═══════════════════════════════════════╝")
    print()
    print(f"  数据集: {r['dataset']['total']} 条 | 语言: {', '.join(r['dataset']['langs'])} | config: {r['config_hash']}")
    print()

    acc_d = f" ({_delta(r['summary']['accuracy'], b['accuracy'])})" if b else ""
    f1_d = f" ({_delta(r['summary']['weighted_f1'], b['weighted_f1'])})" if b else ""
    print(f"  准确率:    {_pct(r['summary']['accuracy'])}{acc_d}    ({r['summary']['correct']}/{r['summary']['total']})")
    print(f"  加权 F1:   {_pct(r['summary']['weighted_f1'])}{f1_d}")
    print(f"  模糊分类:  {r['summary']['ambiguous']}")
    print()

    print("  ┌───────────┬───────────┬────────┬────────┐")
    print("  │   Tier    │ Precision │ Recall │   F1   │")
    print("  ├───────────┼───────────┼────────┼────────┤")
    for tier in TIERS:
        t = tier.value
        m = r["per_tier"][t]
        p = _pct(m["precision"]).rjust(6)
        rc = _pct(m["recall"]).rjust(5)
        f = _pct(m["f1"]).rjust(5)
        suffix = ""
        if baseline and t in baseline["per_tier"]:
            suffix = f" {_delta(m['f1'], baseline['per_tier'][t]['f1'])}"
        print(f"  │ {t:<9} │ {p}    │ {rc}  │ {f}  │{suffix}")
    print("  └───────────┴───────────┴────────┴────────┘")

    failed = [(cat, v) for cat, v in sorted(r["per_category"].items()) if v["accuracy"] < 1.0]
    if failed:
        failed.sort(key=lambda x: x[1]["accuracy"])
        print()
        print("  未通过的类别:")
        for cat, v in failed:
            bc = baseline["per_category"].get(cat) if baseline else None
            d = f" ({_delta(v['accuracy'], bc['accuracy'])})" if bc else ""
            print(f"    ✗ {cat:<20} {v['correct']}/{v['total']} {_pct(v['accuracy'])}{d}  [{v['expected_tier']}]")

    print()


def _load_jsonl_as_testcases(path: Path) -> list[TestCase]:
    cases = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            cases.append(TestCase(
                prompt=d["prompt"],
                expected_tier=d["expected_tier"],
                category=d["category"],
                lang=d["lang"],
                system_prompt=d.get("system_prompt"),
            ))
    return cases


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    args = sys.argv[1:]
    is_baseline = "--baseline" in args
    compare_path = None
    data_path = None
    for i, a in enumerate(args):
        if a == "--compare" and i + 1 < len(args):
            compare_path = args[i + 1]
        elif a == "--data" and i + 1 < len(args):
            data_path = Path(args[i + 1])

    dataset = _load_jsonl_as_testcases(data_path) if data_path else DATASET

    config = ScoringConfig()
    evals = _evaluate(dataset, config)
    result = _compute_metrics(evals)

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

    (RESULTS_DIR / "latest.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"  结果已保存: {result_path}")
    print()

    if result["summary"]["accuracy"] < 0.7:
        sys.exit(1)


if __name__ == "__main__":
    main()
