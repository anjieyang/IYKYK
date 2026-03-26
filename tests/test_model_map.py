from __future__ import annotations

from uncommon_route.model_map import DiscoveredModel, ModelMapper, infer_capabilities
from uncommon_route.router.types import ModelPricing


def test_routing_models_prefer_internal_aliases_for_direct_provider_ids() -> None:
    mapper = ModelMapper("https://api.openai.com/v1")
    zero = ModelPricing(0.0, 0.0)
    mapper._discovered = True
    mapper._upstream_models = {"gpt-4o-mini", "gpt-4o"}
    mapper._pool = {
        "gpt-4o-mini": DiscoveredModel(
            id="gpt-4o-mini",
            provider="openai",
            owned_by="openai",
            pricing=zero,
            capabilities=infer_capabilities("gpt-4o-mini", zero, has_explicit_pricing=False),
            pricing_explicit=False,
        ),
        "gpt-4o": DiscoveredModel(
            id="gpt-4o",
            provider="openai",
            owned_by="openai",
            pricing=zero,
            capabilities=infer_capabilities("gpt-4o", zero, has_explicit_pricing=False),
            pricing_explicit=False,
        ),
    }
    mapper._map = {
        "openai/gpt-4o-mini": "gpt-4o-mini",
        "openai/gpt-4o": "gpt-4o",
    }

    assert set(mapper.routing_models) == {"openai/gpt-4o-mini", "openai/gpt-4o"}
    assert "gpt-4o-mini" not in mapper.routing_models


def test_dynamic_pricing_skips_unpriced_discovery_entries() -> None:
    mapper = ModelMapper("https://api.openai.com/v1")
    zero = ModelPricing(0.0, 0.0)
    mapper._discovered = True
    mapper._upstream_models = {"gpt-4o-mini"}
    mapper._pool = {
        "gpt-4o-mini": DiscoveredModel(
            id="gpt-4o-mini",
            provider="openai",
            owned_by="openai",
            pricing=zero,
            capabilities=infer_capabilities("gpt-4o-mini", zero, has_explicit_pricing=False),
            pricing_explicit=False,
        ),
    }
    mapper._map = {
        "openai/gpt-4o-mini": "gpt-4o-mini",
    }

    assert mapper.dynamic_pricing == {}
