"""Default routing configuration."""

from uncommon_route.router.types import (
    ModelPricing,
    RoutingConfig,
    ScoringConfig,
    Tier,
    TierConfig,
)

DEFAULT_MODEL_PRICING: dict[str, ModelPricing] = {
    "nvidia/gpt-oss-120b": ModelPricing(0.0, 0.0),
    "google/gemini-2.5-flash-lite": ModelPricing(0.10, 0.40),
    "deepseek/deepseek-chat": ModelPricing(0.28, 0.42),
    "deepseek/deepseek-reasoner": ModelPricing(0.28, 0.42),
    "moonshot/kimi-k2.5": ModelPricing(0.60, 3.00),
    "minimax/minimax-m2.5": ModelPricing(0.30, 1.20),
    "xai/grok-4-1-fast-reasoning": ModelPricing(0.20, 0.50),
    "xai/grok-4-1-fast-non-reasoning": ModelPricing(0.20, 1.50),
    "xai/grok-4-0709": ModelPricing(0.20, 1.50),
    "xai/grok-code-fast-1": ModelPricing(0.20, 1.50),
    "google/gemini-2.5-flash": ModelPricing(0.30, 2.50),
    "google/gemini-2.5-pro": ModelPricing(1.25, 10.00),
    "google/gemini-3-pro-preview": ModelPricing(2.00, 12.00),
    "google/gemini-3.1-pro": ModelPricing(2.00, 12.00),
    "openai/gpt-4o-mini": ModelPricing(0.15, 0.60),
    "openai/gpt-4o": ModelPricing(2.50, 10.00),
    "openai/gpt-5.2": ModelPricing(1.75, 14.00),
    "openai/gpt-5.2-codex": ModelPricing(1.75, 14.00),
    "openai/o1-mini": ModelPricing(1.10, 4.40),
    "openai/o3": ModelPricing(2.00, 8.00),
    "openai/o4-mini": ModelPricing(1.10, 4.40),
    "anthropic/claude-haiku-4.5": ModelPricing(1.00, 5.00),
    "anthropic/claude-sonnet-4.6": ModelPricing(3.00, 15.00),
    "anthropic/claude-opus-4.6": ModelPricing(5.00, 25.00),
}

BASELINE_MODEL = "anthropic/claude-opus-4.6"

DEFAULT_CONFIG = RoutingConfig(
    version="3.0",
    scoring=ScoringConfig(),
    tiers={
        Tier.SIMPLE: TierConfig(
            primary="moonshot/kimi-k2.5",
            fallback=["google/gemini-2.5-flash-lite", "nvidia/gpt-oss-120b", "deepseek/deepseek-chat"],
        ),
        Tier.MEDIUM: TierConfig(
            primary="moonshot/kimi-k2.5",
            fallback=["deepseek/deepseek-chat", "google/gemini-2.5-flash-lite", "xai/grok-4-1-fast-non-reasoning"],
        ),
        Tier.COMPLEX: TierConfig(
            primary="google/gemini-3.1-pro",
            fallback=[
                "google/gemini-2.5-flash-lite", "google/gemini-3-pro-preview", "google/gemini-2.5-pro",
                "deepseek/deepseek-chat", "xai/grok-4-0709", "openai/gpt-5.2", "anthropic/claude-sonnet-4.6",
            ],
        ),
        Tier.REASONING: TierConfig(
            primary="xai/grok-4-1-fast-reasoning",
            fallback=["deepseek/deepseek-reasoner", "openai/o4-mini", "openai/o3"],
        ),
    },
)
