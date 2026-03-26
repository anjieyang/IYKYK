"""Template definitions for each tier.

Each template function returns (prompt, tier, category, lang).
Templates are designed so the tier label is deterministic from the structure.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from bench.generate.slots import (
    SIMPLE_CONCEPTS,
    SIMPLE_PEOPLE,
    SIMPLE_FACTS,
    TRANSLATE_PHRASES,
    MEDIUM_CODE_TASKS,
    MEDIUM_EXPLAIN_TOPICS,
    MEDIUM_COMPARE_PAIRS,
    MEDIUM_REWRITE_TASKS,
    MEDIUM_EXTRACT_TASKS,
    COMPLEX_SYSTEMS,
    COMPLEX_REQUIREMENTS,
    COMPLEX_CONSTRAINTS,
    REASONING_THEOREMS,
    REASONING_METHODS,
    PROG_LANGS,
    HUMAN_LANGS,
    QA_PATTERNS,
    TRANSLATE_PATTERNS,
    CODE_PATTERNS,
    EXPLAIN_PATTERNS,
    COMPARE_PATTERNS,
    COMPLEX_PATTERNS,
    REASONING_PATTERNS,
    GREETINGS,
)


@dataclass(frozen=True, slots=True)
class GeneratedCase:
    prompt: str
    expected_tier: str
    category: str
    lang: str


def _pick(lst: list, rng: random.Random) -> str:
    return rng.choice(lst)


def _pick_n(lst: list, n: int, rng: random.Random) -> list:
    return rng.sample(lst, min(n, len(lst)))


# ─── SIMPLE Templates ───


def gen_simple_qa(rng: random.Random, lang: str = "en") -> GeneratedCase:
    patterns = QA_PATTERNS.get(lang, QA_PATTERNS["en"])
    pattern = _pick(patterns, rng)
    concept = _pick(SIMPLE_CONCEPTS, rng)
    person = _pick(SIMPLE_PEOPLE, rng)
    prompt = pattern.format(concept=concept, person=person, fact=concept)
    return GeneratedCase(prompt, "SIMPLE", "factual-qa", lang)


def gen_simple_translate(rng: random.Random, lang: str = "en") -> GeneratedCase:
    patterns = TRANSLATE_PATTERNS.get(lang, TRANSLATE_PATTERNS["en"])
    pattern = _pick(patterns, rng)
    phrase = _pick(TRANSLATE_PHRASES, rng)
    target_lang = _pick(list(HUMAN_LANGS.values()), rng)
    prompt = pattern.format(phrase=phrase, target_lang=target_lang)
    return GeneratedCase(prompt, "SIMPLE", "translation", lang)


def gen_simple_greeting(rng: random.Random, lang: str = "en") -> GeneratedCase:
    greets = GREETINGS.get(lang, GREETINGS["en"])
    prompt = _pick(greets, rng)
    return GeneratedCase(prompt, "SIMPLE", "greeting", lang)


def gen_simple_fact(rng: random.Random) -> GeneratedCase:
    fact, _ = _pick(SIMPLE_FACTS, rng)
    patterns = ["What is {f}?", "Tell me {f}", "Do you know {f}?"]
    prompt = _pick(patterns, rng).format(f=fact)
    return GeneratedCase(prompt, "SIMPLE", "factual-qa", "en")


SIMPLE_GENERATORS = [gen_simple_qa, gen_simple_translate, gen_simple_greeting, gen_simple_fact]


# ─── MEDIUM Templates ───


def gen_medium_code(rng: random.Random, lang: str = "en") -> GeneratedCase:
    patterns = CODE_PATTERNS.get(lang, CODE_PATTERNS["en"])
    pattern = _pick(patterns, rng)
    prog_lang = _pick(PROG_LANGS, rng)
    task = _pick(MEDIUM_CODE_TASKS, rng)
    prompt = pattern.format(lang=prog_lang, task=task)
    return GeneratedCase(prompt, "MEDIUM", "simple-code", lang)


def gen_medium_explain(rng: random.Random, lang: str = "en") -> GeneratedCase:
    patterns = EXPLAIN_PATTERNS.get(lang, EXPLAIN_PATTERNS["en"])
    pattern = _pick(patterns, rng)
    topic = _pick(MEDIUM_EXPLAIN_TOPICS, rng)
    topic_short = topic.split("the difference")[0].strip() if "difference" in topic else topic[:30]
    prompt = pattern.format(topic=topic, topic_short=topic_short)
    return GeneratedCase(prompt, "MEDIUM", "explanation", lang)


def gen_medium_compare(rng: random.Random, lang: str = "en") -> GeneratedCase:
    patterns = COMPARE_PATTERNS.get(lang, COMPARE_PATTERNS["en"])
    pattern = _pick(patterns, rng)
    a, b = _pick(MEDIUM_COMPARE_PAIRS, rng)
    prompt = pattern.format(a=a, b=b)
    return GeneratedCase(prompt, "MEDIUM", "comparison", lang)


def gen_medium_rewrite(rng: random.Random) -> GeneratedCase:
    prompt = _pick(MEDIUM_REWRITE_TASKS, rng)
    return GeneratedCase(prompt, "MEDIUM", "rewrite", "en")


def gen_medium_extract(rng: random.Random) -> GeneratedCase:
    prompt = _pick(MEDIUM_EXTRACT_TASKS, rng)
    return GeneratedCase(prompt, "MEDIUM", "extraction", "en")


MEDIUM_GENERATORS = [gen_medium_code, gen_medium_explain, gen_medium_compare, gen_medium_rewrite, gen_medium_extract]


# ─── COMPLEX Templates ───


def gen_complex_system(rng: random.Random, lang: str = "en") -> GeneratedCase:
    patterns = COMPLEX_PATTERNS.get(lang, COMPLEX_PATTERNS["en"])
    pattern = _pick(patterns, rng)
    system = _pick(COMPLEX_SYSTEMS, rng)
    reqs = _pick_n(COMPLEX_REQUIREMENTS, 5, rng)
    constraint = _pick(COMPLEX_CONSTRAINTS, rng)
    prompt = pattern.format(
        system=system,
        r1=reqs[0],
        r2=reqs[1],
        r3=reqs[2],
        r4=reqs[3],
        r5=reqs[4] if len(reqs) > 4 else reqs[0],
        constraint=constraint,
    )
    return GeneratedCase(prompt, "COMPLEX", "system-design", lang)


COMPLEX_GENERATORS = [gen_complex_system]


# ─── REASONING Templates ───


def gen_reasoning_proof(rng: random.Random, lang: str = "en") -> GeneratedCase:
    patterns = REASONING_PATTERNS.get(lang, REASONING_PATTERNS["en"])
    pattern = _pick(patterns, rng)
    theorem = _pick(REASONING_THEOREMS, rng)
    method = _pick(REASONING_METHODS, rng)
    prompt = pattern.format(theorem=theorem, method=method)
    return GeneratedCase(prompt, "REASONING", "formal-proof", lang)


REASONING_GENERATORS = [gen_reasoning_proof]
