"""Core type definitions for UncommonRoute."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


class Tier(str, Enum):
    SIMPLE = "SIMPLE"
    MEDIUM = "MEDIUM"
    COMPLEX = "COMPLEX"
    REASONING = "REASONING"



@dataclass(frozen=True, slots=True)
class DimensionScore:
    name: str
    score: float  # [-1, 1]
    signal: str | None = None


@dataclass(frozen=True, slots=True)
class ScoringResult:
    score: float
    tier: Tier | None  # None = ambiguous
    confidence: float  # [0, 1]
    signals: list[str]
    dimensions: list[DimensionScore] = field(default_factory=list)
    agentic_score: float = 0.0


@dataclass(frozen=True, slots=True)
class RoutingDecision:
    model: str
    tier: Tier
    confidence: float
    method: Literal["rules", "cascade"]
    reasoning: str
    cost_estimate: float
    baseline_cost: float
    savings: float  # 0-1
    agentic_score: float = 0.0
    suggested_output_budget: int = 4096
    fallback_chain: list[FallbackOption] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class FallbackOption:
    """One option in the cost-aware fallback chain."""
    model: str
    cost_estimate: float
    suggested_output_budget: int


@dataclass(frozen=True, slots=True)
class TierConfig:
    primary: str
    fallback: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class ModelPricing:
    input_price: float  # per 1M tokens
    output_price: float  # per 1M tokens


@dataclass
class StructuralWeights:
    """Weights for language-agnostic structural features."""
    normalized_length: float = 0.05
    enumeration_density: float = 0.10
    sentence_count: float = 0.08
    code_markers: float = 0.07
    math_symbols: float = 0.06
    nesting_depth: float = 0.03
    vocabulary_diversity: float = 0.03
    avg_word_length: float = 0.03
    alphabetic_ratio: float = 0.03
    functional_intent: float = 0.06
    unique_concept_density: float = 0.07
    requirement_phrases: float = 0.06


@dataclass
class KeywordWeights:
    """Weights for keyword-based features (language-specific, secondary)."""
    code_presence: float = 0.06
    reasoning_markers: float = 0.06
    technical_terms: float = 0.04
    creative_markers: float = 0.02
    simple_indicators: float = 0.02
    imperative_verbs: float = 0.02
    constraint_count: float = 0.02
    output_format: float = 0.02
    domain_specificity: float = 0.01
    agentic_task: float = 0.02
    analytical_verbs: float = 0.04
    multi_step_patterns: float = 0.04


@dataclass
class TierBoundaries:
    simple_medium: float = -0.02
    medium_complex: float = 0.15
    complex_reasoning: float = 0.25


@dataclass
class ScoringConfig:
    structural_weights: StructuralWeights = field(default_factory=StructuralWeights)
    keyword_weights: KeywordWeights = field(default_factory=KeywordWeights)
    tier_boundaries: TierBoundaries = field(default_factory=TierBoundaries)
    confidence_steepness: float = 18.0
    confidence_threshold: float = 0.55


@dataclass
class RoutingConfig:
    version: str = "3.0"
    scoring: ScoringConfig = field(default_factory=ScoringConfig)
    tiers: dict[Tier, TierConfig] = field(default_factory=dict)
    max_tokens_force_complex: int = 100_000
    structured_output_min_tier: Tier = Tier.MEDIUM
    ambiguous_default_tier: Tier = Tier.MEDIUM
