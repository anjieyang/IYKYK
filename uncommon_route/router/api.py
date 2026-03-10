"""Public API — the route() entry point."""

from __future__ import annotations

from uncommon_route.router.types import (
    RequestRequirements,
    RoutingConfig,
    RoutingDecision,
    RoutingProfile,
    Tier,
    TierConfig,
)
from uncommon_route.router.classifier import classify
from uncommon_route.router.selector import select_model
from uncommon_route.router.structural import estimate_tokens
from uncommon_route.router.config import (
    DEFAULT_CONFIG,
    get_bandit_config,
    get_selection_weights,
    get_tier_configs,
)


def route(
    prompt: str,
    system_prompt: str | None = None,
    max_output_tokens: int = 4096,
    config: RoutingConfig | None = None,
    routing_profile: RoutingProfile | str = RoutingProfile.AUTO,
    request_requirements: RequestRequirements | None = None,
    user_keyed_models: set[str] | None = None,
    model_experience: object | None = None,
    tier_cap: Tier | None = None,
    tier_floor: Tier | None = None,
) -> RoutingDecision:
    """Route a prompt to the best model.

    This is the main entry point. <1ms, pure local, no external calls.

    Args:
        user_keyed_models: Model IDs backed by user-provided API keys.
            When set, models the user already pays for are prioritized.
    """
    cfg = config or DEFAULT_CONFIG
    requirements = request_requirements or RequestRequirements()
    profile = routing_profile if isinstance(routing_profile, RoutingProfile) else RoutingProfile(routing_profile)

    # Token estimate from user prompt only — system prompts from agentic
    # frameworks are overhead, not task complexity.
    estimated_tokens = estimate_tokens(prompt)

    result = classify(prompt, system_prompt, cfg.scoring)

    tier = result.tier if result.tier is not None else cfg.ambiguous_default_tier

    # Structured-output floor: only check the user prompt, not the system
    # prompt.  Agentic frameworks (Claude Code, etc.) always mention "json",
    # "schema", etc. in their system prompt regardless of the actual task.
    if prompt and any(kw in prompt.lower() for kw in ("json", "structured", "schema")):
        tier_rank = {Tier.SIMPLE: 0, Tier.MEDIUM: 1, Tier.COMPLEX: 2, Tier.REASONING: 3}
        min_tier = cfg.structured_output_min_tier
        if tier_rank[tier] < tier_rank[min_tier]:
            tier = min_tier

    tier_rank = {Tier.SIMPLE: 0, Tier.MEDIUM: 1, Tier.COMPLEX: 2, Tier.REASONING: 3}
    if tier_floor is not None and tier_rank[tier] < tier_rank[tier_floor]:
        tier = tier_floor
    if tier_cap is not None and tier_rank[tier] > tier_rank[tier_cap]:
        tier = tier_cap

    reasoning = f"score={result.score:.3f} | {', '.join(result.signals)}"
    use_agentic_tiers = profile is RoutingProfile.AGENTIC or (
        profile is RoutingProfile.AUTO and requirements.is_agentic
    )

    return select_model(
        tier=tier,
        profile=profile,
        confidence=result.confidence,
        method="cascade",
        reasoning=reasoning,
        tier_configs=get_tier_configs(cfg, profile, agentic=use_agentic_tiers),
        estimated_input_tokens=estimated_tokens,
        max_output_tokens=max_output_tokens,
        prompt=prompt,
        model_capabilities=cfg.model_capabilities,
        request_requirements=requirements,
        agentic_score=result.agentic_score,
        user_keyed_models=user_keyed_models,
        selection_weights=get_selection_weights(cfg, profile, agentic=use_agentic_tiers),
        bandit_config=get_bandit_config(cfg, profile, agentic=use_agentic_tiers),
        model_experience=model_experience,
    )
