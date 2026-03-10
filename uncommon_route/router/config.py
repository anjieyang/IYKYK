"""Default routing configuration."""

from uncommon_route.router.types import (
    BanditConfig,
    ModelCapabilities,
    ModelPricing,
    RoutingConfig,
    RoutingProfile,
    ScoringConfig,
    SelectionWeights,
    Tier,
    TierConfig,
)

DEFAULT_MODEL_PRICING: dict[str, ModelPricing] = {
    "nvidia/gpt-oss-120b": ModelPricing(0.0, 0.0),
    "google/gemini-2.5-flash-lite": ModelPricing(0.10, 0.40),
    "deepseek/deepseek-chat": ModelPricing(0.28, 0.42, cached_input_price=0.28, cache_write_price=0.28),
    "deepseek/deepseek-reasoner": ModelPricing(0.28, 0.42, cached_input_price=0.28, cache_write_price=0.28),
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
    "openai/gpt-4o-mini": ModelPricing(0.15, 0.60, cached_input_price=0.075),
    "openai/gpt-4o": ModelPricing(2.50, 10.00, cached_input_price=1.25),
    "openai/gpt-5.2": ModelPricing(1.75, 14.00, cached_input_price=0.875),
    "openai/gpt-5.2-codex": ModelPricing(1.75, 14.00, cached_input_price=0.875),
    "openai/o1-mini": ModelPricing(1.10, 4.40, cached_input_price=0.55),
    "openai/o3": ModelPricing(2.00, 8.00, cached_input_price=1.00),
    "openai/o4-mini": ModelPricing(1.10, 4.40, cached_input_price=0.55),
    "anthropic/claude-haiku-4.5": ModelPricing(1.00, 5.00, cached_input_price=0.10, cache_write_price=1.25),
    "anthropic/claude-sonnet-4.6": ModelPricing(3.00, 15.00, cached_input_price=0.30, cache_write_price=3.75),
    "anthropic/claude-opus-4.6": ModelPricing(5.00, 25.00, cached_input_price=0.50, cache_write_price=6.25),
}

BASELINE_MODEL = "anthropic/claude-opus-4.6"
FREE_MODEL = "nvidia/gpt-oss-120b"

VIRTUAL_MODEL_IDS: dict[RoutingProfile, str] = {
    RoutingProfile.AUTO: "uncommon-route/auto",
    RoutingProfile.FREE: "uncommon-route/free",
    RoutingProfile.ECO: "uncommon-route/eco",
    RoutingProfile.PREMIUM: "uncommon-route/premium",
    RoutingProfile.AGENTIC: "uncommon-route/agentic",
}

VIRTUAL_MODEL_ALIASES: dict[str, RoutingProfile] = {
    profile.value: profile for profile in RoutingProfile
}


def _caps(
    *,
    tool_calling: bool = False,
    vision: bool = False,
    reasoning: bool = False,
    free: bool = False,
    local: bool = False,
    responses: bool = False,
) -> ModelCapabilities:
    return ModelCapabilities(
        tool_calling=tool_calling,
        vision=vision,
        reasoning=reasoning,
        free=free,
        local=local,
        responses=responses,
    )


DEFAULT_MODEL_CAPABILITIES: dict[str, ModelCapabilities] = {
    "nvidia/gpt-oss-120b": _caps(free=True),
    "google/gemini-2.5-flash-lite": _caps(vision=True),
    "deepseek/deepseek-chat": _caps(tool_calling=True),
    "deepseek/deepseek-reasoner": _caps(tool_calling=True, reasoning=True),
    "moonshot/kimi-k2.5": _caps(tool_calling=True, reasoning=True),
    "minimax/minimax-m2.5": _caps(tool_calling=True, reasoning=True),
    "xai/grok-4-1-fast-reasoning": _caps(tool_calling=True, reasoning=True),
    "xai/grok-4-1-fast-non-reasoning": _caps(tool_calling=True),
    "xai/grok-4-0709": _caps(tool_calling=True, reasoning=True),
    "xai/grok-code-fast-1": _caps(tool_calling=True),
    "google/gemini-2.5-flash": _caps(vision=True),
    "google/gemini-2.5-pro": _caps(vision=True, reasoning=True),
    "google/gemini-3-pro-preview": _caps(vision=True, reasoning=True),
    "google/gemini-3.1-pro": _caps(vision=True, reasoning=True),
    "openai/gpt-4o-mini": _caps(tool_calling=True, vision=True),
    "openai/gpt-4o": _caps(tool_calling=True, vision=True),
    "openai/gpt-5.2": _caps(tool_calling=True, vision=True, reasoning=True, responses=True),
    "openai/gpt-5.2-codex": _caps(tool_calling=True, reasoning=True, responses=True),
    "openai/o1-mini": _caps(tool_calling=True, reasoning=True),
    "openai/o3": _caps(tool_calling=True, reasoning=True),
    "openai/o4-mini": _caps(tool_calling=True, reasoning=True),
    "anthropic/claude-haiku-4.5": _caps(tool_calling=True, vision=True),
    "anthropic/claude-sonnet-4.6": _caps(tool_calling=True, vision=True, reasoning=True),
    "anthropic/claude-opus-4.6": _caps(tool_calling=True, vision=True, reasoning=True),
}


def routing_profile_from_model(model_id: str) -> RoutingProfile | None:
    normalized = (model_id or "").strip().lower()
    if normalized in VIRTUAL_MODEL_ALIASES:
        return VIRTUAL_MODEL_ALIASES[normalized]
    for profile, virtual_model in VIRTUAL_MODEL_IDS.items():
        if normalized == virtual_model:
            return profile
    return None


def virtual_model_entries() -> list[dict[str, str]]:
    return [
        {"id": VIRTUAL_MODEL_IDS[RoutingProfile.AUTO], "object": "model", "owned_by": "uncommon-route"},
        {"id": VIRTUAL_MODEL_IDS[RoutingProfile.ECO], "object": "model", "owned_by": "uncommon-route"},
        {"id": VIRTUAL_MODEL_IDS[RoutingProfile.PREMIUM], "object": "model", "owned_by": "uncommon-route"},
        {"id": VIRTUAL_MODEL_IDS[RoutingProfile.FREE], "object": "model", "owned_by": "uncommon-route"},
        {"id": VIRTUAL_MODEL_IDS[RoutingProfile.AGENTIC], "object": "model", "owned_by": "uncommon-route"},
    ]


def get_tier_configs(
    config: RoutingConfig,
    profile: RoutingProfile,
    *,
    agentic: bool = False,
) -> dict[Tier, TierConfig]:
    if agentic and config.agentic_tiers:
        return config.agentic_tiers
    if profile is RoutingProfile.FREE and config.free_tiers:
        return config.free_tiers
    if profile is RoutingProfile.ECO and config.eco_tiers:
        return config.eco_tiers
    if profile is RoutingProfile.PREMIUM and config.premium_tiers:
        return config.premium_tiers
    if profile is RoutingProfile.AGENTIC and config.agentic_tiers:
        return config.agentic_tiers
    return config.tiers


def get_selection_weights(
    config: RoutingConfig,
    profile: RoutingProfile,
    *,
    agentic: bool = False,
) -> SelectionWeights:
    if agentic and config.agentic_selection is not None:
        return config.agentic_selection
    if profile is RoutingProfile.AGENTIC and config.agentic_selection is not None:
        return config.agentic_selection
    return config.selection_profiles.get(profile, config.selection_profiles.get(RoutingProfile.AUTO, SelectionWeights()))


def get_bandit_config(
    config: RoutingConfig,
    profile: RoutingProfile,
    *,
    agentic: bool = False,
) -> BanditConfig:
    if agentic and config.agentic_bandit is not None:
        return config.agentic_bandit
    if profile is RoutingProfile.AGENTIC and config.agentic_bandit is not None:
        return config.agentic_bandit
    return config.bandit_profiles.get(profile, config.bandit_profiles.get(RoutingProfile.AUTO, BanditConfig()))

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
    free_tiers={
        Tier.SIMPLE: TierConfig(
            primary="nvidia/gpt-oss-120b",
            fallback=["google/gemini-2.5-flash-lite", "deepseek/deepseek-chat"],
        ),
        Tier.MEDIUM: TierConfig(
            primary="nvidia/gpt-oss-120b",
            fallback=["deepseek/deepseek-chat", "google/gemini-2.5-flash-lite", "moonshot/kimi-k2.5"],
        ),
        Tier.COMPLEX: TierConfig(
            primary="nvidia/gpt-oss-120b",
            fallback=["google/gemini-2.5-flash-lite", "deepseek/deepseek-chat", "google/gemini-3.1-pro"],
        ),
        Tier.REASONING: TierConfig(
            primary="nvidia/gpt-oss-120b",
            fallback=["deepseek/deepseek-reasoner", "xai/grok-4-1-fast-reasoning"],
        ),
    },
    eco_tiers={
        Tier.SIMPLE: TierConfig(
            primary="nvidia/gpt-oss-120b",
            fallback=["google/gemini-2.5-flash-lite", "deepseek/deepseek-chat"],
        ),
        Tier.MEDIUM: TierConfig(
            primary="google/gemini-2.5-flash-lite",
            fallback=["deepseek/deepseek-chat", "moonshot/kimi-k2.5", "nvidia/gpt-oss-120b"],
        ),
        Tier.COMPLEX: TierConfig(
            primary="google/gemini-2.5-flash-lite",
            fallback=["deepseek/deepseek-chat", "google/gemini-2.5-flash", "google/gemini-3.1-pro"],
        ),
        Tier.REASONING: TierConfig(
            primary="xai/grok-4-1-fast-reasoning",
            fallback=["deepseek/deepseek-reasoner", "openai/o4-mini"],
        ),
    },
    premium_tiers={
        Tier.SIMPLE: TierConfig(
            primary="openai/gpt-4o",
            fallback=["moonshot/kimi-k2.5", "anthropic/claude-haiku-4.5"],
        ),
        Tier.MEDIUM: TierConfig(
            primary="openai/gpt-5.2-codex",
            fallback=["openai/gpt-5.2", "anthropic/claude-sonnet-4.6", "moonshot/kimi-k2.5"],
        ),
        Tier.COMPLEX: TierConfig(
            primary="anthropic/claude-opus-4.6",
            fallback=["anthropic/claude-sonnet-4.6", "openai/gpt-5.2", "google/gemini-3.1-pro"],
        ),
        Tier.REASONING: TierConfig(
            primary="anthropic/claude-sonnet-4.6",
            fallback=["anthropic/claude-opus-4.6", "openai/o3", "xai/grok-4-1-fast-reasoning"],
        ),
    },
    agentic_tiers={
        Tier.SIMPLE: TierConfig(
            primary="moonshot/kimi-k2.5",
            fallback=["anthropic/claude-haiku-4.5", "openai/gpt-4o-mini", "deepseek/deepseek-chat"],
        ),
        Tier.MEDIUM: TierConfig(
            primary="moonshot/kimi-k2.5",
            fallback=["anthropic/claude-haiku-4.5", "deepseek/deepseek-chat", "openai/gpt-4o-mini"],
        ),
        Tier.COMPLEX: TierConfig(
            primary="anthropic/claude-sonnet-4.6",
            fallback=["anthropic/claude-opus-4.6", "openai/gpt-5.2", "google/gemini-3.1-pro"],
        ),
        Tier.REASONING: TierConfig(
            primary="anthropic/claude-sonnet-4.6",
            fallback=["anthropic/claude-opus-4.6", "xai/grok-4-1-fast-reasoning", "deepseek/deepseek-reasoner"],
        ),
    },
    selection_profiles={
        RoutingProfile.AUTO: SelectionWeights(
            editorial=0.40,
            cost=0.12,
            latency=0.08,
            reliability=0.10,
            feedback=0.10,
            cache_affinity=0.11,
            byok=0.08,
            free_bias=0.01,
            local_bias=0.01,
            reasoning_bias=0.03,
        ),
        RoutingProfile.ECO: SelectionWeights(
            editorial=0.18,
            cost=0.33,
            latency=0.10,
            reliability=0.10,
            feedback=0.08,
            cache_affinity=0.13,
            byok=0.08,
            free_bias=0.05,
            local_bias=0.01,
            reasoning_bias=0.00,
        ),
        RoutingProfile.PREMIUM: SelectionWeights(
            editorial=0.51,
            cost=0.04,
            latency=0.07,
            reliability=0.11,
            feedback=0.12,
            cache_affinity=0.09,
            byok=0.05,
            free_bias=0.00,
            local_bias=0.00,
            reasoning_bias=0.05,
        ),
        RoutingProfile.FREE: SelectionWeights(
            editorial=0.12,
            cost=0.24,
            latency=0.10,
            reliability=0.09,
            feedback=0.06,
            cache_affinity=0.06,
            byok=0.02,
            free_bias=0.32,
            local_bias=0.03,
            reasoning_bias=0.00,
        ),
        RoutingProfile.AGENTIC: SelectionWeights(
            editorial=0.30,
            cost=0.06,
            latency=0.10,
            reliability=0.16,
            feedback=0.12,
            cache_affinity=0.20,
            byok=0.05,
            free_bias=0.00,
            local_bias=0.01,
            reasoning_bias=0.08,
        ),
    },
    agentic_selection=SelectionWeights(
        editorial=0.28,
        cost=0.06,
        latency=0.10,
        reliability=0.16,
        feedback=0.12,
        cache_affinity=0.22,
        byok=0.05,
        free_bias=0.00,
        local_bias=0.01,
        reasoning_bias=0.06,
    ),
    bandit_profiles={
        RoutingProfile.AUTO: BanditConfig(
            enabled=True,
            reward_weight=0.10,
            exploration_weight=0.16,
            warmup_pulls=2,
            min_samples_for_guardrail=3,
            min_reliability=0.25,
            max_cost_ratio=2.8,
            enabled_tiers=(Tier.SIMPLE, Tier.MEDIUM, Tier.COMPLEX),
        ),
        RoutingProfile.ECO: BanditConfig(
            enabled=True,
            reward_weight=0.08,
            exploration_weight=0.20,
            warmup_pulls=3,
            min_samples_for_guardrail=3,
            min_reliability=0.30,
            max_cost_ratio=1.8,
            enabled_tiers=(Tier.SIMPLE, Tier.MEDIUM),
        ),
        RoutingProfile.PREMIUM: BanditConfig(
            enabled=True,
            reward_weight=0.06,
            exploration_weight=0.08,
            warmup_pulls=1,
            min_samples_for_guardrail=4,
            min_reliability=0.35,
            max_cost_ratio=1.6,
            enabled_tiers=(Tier.SIMPLE, Tier.MEDIUM),
        ),
        RoutingProfile.FREE: BanditConfig(
            enabled=True,
            reward_weight=0.08,
            exploration_weight=0.10,
            warmup_pulls=2,
            min_samples_for_guardrail=2,
            min_reliability=0.20,
            max_cost_ratio=1.4,
            enabled_tiers=(Tier.SIMPLE, Tier.MEDIUM),
        ),
        RoutingProfile.AGENTIC: BanditConfig(
            enabled=True,
            reward_weight=0.05,
            exploration_weight=0.06,
            warmup_pulls=1,
            min_samples_for_guardrail=4,
            min_reliability=0.45,
            max_cost_ratio=1.5,
            enabled_tiers=(Tier.SIMPLE, Tier.MEDIUM),
        ),
    },
    agentic_bandit=BanditConfig(
        enabled=True,
        reward_weight=0.05,
        exploration_weight=0.06,
        warmup_pulls=1,
        min_samples_for_guardrail=4,
        min_reliability=0.45,
        max_cost_ratio=1.5,
        enabled_tiers=(Tier.SIMPLE, Tier.MEDIUM),
    ),
    model_capabilities=DEFAULT_MODEL_CAPABILITIES,
    free_model=FREE_MODEL,
)
