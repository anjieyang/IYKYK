"""Train / Dev / Test splitter with hold-out language support.

Usage:
    python -m bench.split bench/data/2000.jsonl --holdout-langs ja,ko,ar
"""

from __future__ import annotations

import json
import random
import sys
from collections import defaultdict
from pathlib import Path


def stratified_split(
    cases: list[dict],
    train_ratio: float = 0.70,
    dev_ratio: float = 0.15,
    seed: int = 42,
    holdout_langs: set[str] | None = None,
) -> dict[str, list[dict]]:
    """Stratified split by (tier, lang) ensuring balanced distribution.

    Hold-out languages go entirely to the test set.
    """
    rng = random.Random(seed)
    holdout_langs = holdout_langs or set()

    holdout = [c for c in cases if c["lang"] in holdout_langs]
    main = [c for c in cases if c["lang"] not in holdout_langs]

    # Group by (tier, lang) for stratified split
    groups: dict[str, list[dict]] = defaultdict(list)
    for c in main:
        key = f"{c['expected_tier']}_{c['lang']}"
        groups[key].append(c)

    train: list[dict] = []
    dev: list[dict] = []
    test: list[dict] = []

    for key, items in groups.items():
        rng.shuffle(items)
        n = len(items)
        n_train = max(1, int(n * train_ratio))
        n_dev = max(0, int(n * dev_ratio))

        train.extend(items[:n_train])
        dev.extend(items[n_train : n_train + n_dev])
        test.extend(items[n_train + n_dev :])

    # Hold-out languages go to test
    test.extend(holdout)

    rng.shuffle(train)
    rng.shuffle(dev)
    rng.shuffle(test)

    return {"train": train, "dev": dev, "test": test}


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m bench.split <data.jsonl> [--holdout-langs ja,ko,ar]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    holdout_langs: set[str] = set()

    for i, arg in enumerate(sys.argv):
        if arg == "--holdout-langs" and i + 1 < len(sys.argv):
            holdout_langs = set(sys.argv[i + 1].split(","))

    cases = []
    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                cases.append(json.loads(line))

    print(f"Input: {len(cases)} cases")
    if holdout_langs:
        print(f"Hold-out languages: {holdout_langs}")

    splits = stratified_split(cases, holdout_langs=holdout_langs)

    out_dir = input_path.parent
    for name, data in splits.items():
        out_path = out_dir / f"{name}.jsonl"
        with out_path.open("w", encoding="utf-8") as f:
            for c in data:
                json.dump(c, f, ensure_ascii=False)
                f.write("\n")
        # Stats
        from collections import Counter

        tiers = Counter(c["expected_tier"] for c in data)
        langs = Counter(c["lang"] for c in data)
        print(f"  {name}: {len(data)} cases | tiers={dict(tiers)} | langs={len(langs)}")

    print("Done.")


if __name__ == "__main__":
    main()
