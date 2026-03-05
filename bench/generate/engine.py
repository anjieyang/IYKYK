"""Main generation engine. Combines templates + slots to produce datasets.

Usage:
    python -m bench.generate.engine --count 2000 --seed 42
    python -m bench.generate.engine --count 10000 --seed 42 --out bench/data/10k.jsonl
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

from bench.generate.templates import (
    SIMPLE_GENERATORS, MEDIUM_GENERATORS, COMPLEX_GENERATORS, REASONING_GENERATORS,
    GeneratedCase,
)
from bench.generate.slots import HUMAN_LANGS

# Tier distribution targets (approximate real-world distribution)
TIER_WEIGHTS = {
    "SIMPLE": 0.25,
    "MEDIUM": 0.35,
    "COMPLEX": 0.25,
    "REASONING": 0.15,
}

TIER_GENERATORS = {
    "SIMPLE": SIMPLE_GENERATORS,
    "MEDIUM": MEDIUM_GENERATORS,
    "COMPLEX": COMPLEX_GENERATORS,
    "REASONING": REASONING_GENERATORS,
}

# Language distribution (weighted toward English but covering all)
LANG_WEIGHTS = {
    "en": 0.35, "zh": 0.12, "ru": 0.08, "es": 0.08,
    "de": 0.07, "fr": 0.07, "pt": 0.06, "ja": 0.07,
    "ko": 0.05, "ar": 0.05,
}


def generate_dataset(count: int, seed: int = 42) -> list[GeneratedCase]:
    """Generate `count` labeled prompt cases."""
    rng = random.Random(seed)
    langs = list(LANG_WEIGHTS.keys())
    lang_probs = list(LANG_WEIGHTS.values())
    tiers = list(TIER_WEIGHTS.keys())
    tier_probs = list(TIER_WEIGHTS.values())

    cases: list[GeneratedCase] = []
    seen_prompts: set[str] = set()

    attempts = 0
    max_attempts = count * 3

    while len(cases) < count and attempts < max_attempts:
        attempts += 1

        tier = rng.choices(tiers, weights=tier_probs, k=1)[0]
        lang = rng.choices(langs, weights=lang_probs, k=1)[0]
        generators = TIER_GENERATORS[tier]
        gen_func = rng.choice(generators)

        try:
            # Some generators accept lang, some don't
            import inspect
            sig = inspect.signature(gen_func)
            if "lang" in sig.parameters:
                case = gen_func(rng, lang=lang)
            else:
                case = gen_func(rng)
        except (KeyError, IndexError, ValueError):
            continue

        # Deduplicate
        if case.prompt in seen_prompts:
            continue
        seen_prompts.add(case.prompt)
        cases.append(case)

    return cases


def export_jsonl(cases: list[GeneratedCase], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for c in cases:
            json.dump({
                "prompt": c.prompt,
                "expected_tier": c.expected_tier,
                "category": c.category,
                "lang": c.lang,
            }, f, ensure_ascii=False)
            f.write("\n")


def load_jsonl(path: Path) -> list[dict]:
    cases = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def main() -> None:
    args = sys.argv[1:]
    count = 2000
    seed = 42
    out_path = None

    i = 0
    while i < len(args):
        if args[i] == "--count" and i + 1 < len(args):
            count = int(args[i + 1])
            i += 2
        elif args[i] == "--seed" and i + 1 < len(args):
            seed = int(args[i + 1])
            i += 2
        elif args[i] == "--out" and i + 1 < len(args):
            out_path = Path(args[i + 1])
            i += 2
        else:
            i += 1

    print(f"Generating {count} cases (seed={seed})...")
    cases = generate_dataset(count, seed)

    # Stats
    from collections import Counter
    tier_counts = Counter(c.expected_tier for c in cases)
    lang_counts = Counter(c.lang for c in cases)
    cat_counts = Counter(c.category for c in cases)

    print(f"Generated: {len(cases)}")
    print(f"Tiers: {dict(tier_counts)}")
    print(f"Languages: {dict(lang_counts)}")
    print(f"Categories: {len(cat_counts)} — {dict(cat_counts)}")

    if out_path is None:
        out_path = Path(__file__).parent.parent / "data" / f"{len(cases)}.jsonl"

    export_jsonl(cases, out_path)
    print(f"Saved to: {out_path}")


if __name__ == "__main__":
    main()
