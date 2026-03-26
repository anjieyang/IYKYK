"""Side-channel semantic compression contracts."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol

from uncommon_route.router.structural import estimate_tokens


@dataclass(frozen=True, slots=True)
class QualityFallbackPolicy:
    min_chars: int = 48
    min_alpha_chars: int = 24
    min_source_ratio: float = 0.01
    max_source_ratio: float = 0.75
    min_query_overlap_terms: int = 0
    reject_markers: tuple[str, ...] = (
        "cannot summarize",
        "can't summarize",
        "insufficient information",
        "no relevant information",
    )

    @classmethod
    def from_dict(
        cls,
        data: Mapping[str, Any] | None,
        *,
        base: QualityFallbackPolicy | None = None,
    ) -> QualityFallbackPolicy:
        base = base or cls()
        if not data:
            return base
        policy = cls(
            min_chars=int(data.get("min_chars", base.min_chars)),
            min_alpha_chars=int(data.get("min_alpha_chars", base.min_alpha_chars)),
            min_source_ratio=float(data.get("min_source_ratio", base.min_source_ratio)),
            max_source_ratio=float(data.get("max_source_ratio", base.max_source_ratio)),
            min_query_overlap_terms=int(
                data.get("min_query_overlap_terms", base.min_query_overlap_terms),
            ),
            reject_markers=tuple(data.get("reject_markers", base.reject_markers)),
        )
        if policy.min_chars < 0 or policy.min_alpha_chars < 0:
            raise ValueError("quality thresholds must be non-negative")
        if policy.min_source_ratio < 0 or policy.max_source_ratio <= 0:
            raise ValueError("quality source ratios must be positive")
        if policy.max_source_ratio < policy.min_source_ratio:
            raise ValueError("quality max_source_ratio must be >= min_source_ratio")
        if policy.min_query_overlap_terms < 0:
            raise ValueError("quality min_query_overlap_terms must be non-negative")
        return policy

    def to_dict(self) -> dict[str, Any]:
        return {
            "min_chars": self.min_chars,
            "min_alpha_chars": self.min_alpha_chars,
            "min_source_ratio": self.min_source_ratio,
            "max_source_ratio": self.max_source_ratio,
            "min_query_overlap_terms": self.min_query_overlap_terms,
            "reject_markers": list(self.reject_markers),
        }


@dataclass(frozen=True, slots=True)
class SideChannelTaskConfig:
    primary: str
    fallback: tuple[str, ...] = ()
    max_tokens: int = 256
    quality: QualityFallbackPolicy = field(default_factory=QualityFallbackPolicy)

    def candidates(self) -> list[str]:
        return [self.primary, *self.fallback]

    @classmethod
    def from_dict(
        cls,
        data: Mapping[str, Any] | None,
        *,
        base: SideChannelTaskConfig,
    ) -> SideChannelTaskConfig:
        if not data:
            return base
        primary = str(data.get("primary", base.primary)).strip()
        if not primary:
            raise ValueError("side-channel primary model cannot be empty")
        fallback = tuple(str(model).strip() for model in data.get("fallback", base.fallback) if str(model).strip())
        task = cls(
            primary=primary,
            fallback=fallback,
            max_tokens=int(data.get("max_tokens", base.max_tokens)),
            quality=QualityFallbackPolicy.from_dict(
                data.get("quality"),
                base=base.quality,
            ),
        )
        if task.max_tokens <= 0:
            raise ValueError("side-channel max_tokens must be > 0")
        return task

    def to_dict(self) -> dict[str, Any]:
        return {
            "primary": self.primary,
            "fallback": list(self.fallback),
            "max_tokens": self.max_tokens,
            "quality": self.quality.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class SideChannelConfig:
    tool_summary: SideChannelTaskConfig
    checkpoint: SideChannelTaskConfig
    rehydrate: SideChannelTaskConfig

    @classmethod
    def from_dict(
        cls,
        data: Mapping[str, Any] | None,
        *,
        base: SideChannelConfig | None = None,
    ) -> SideChannelConfig:
        base = base or DEFAULT_SIDECHANNEL_CONFIG
        if not data:
            return base
        return cls(
            tool_summary=SideChannelTaskConfig.from_dict(
                data.get("tool_summary"),
                base=base.tool_summary,
            ),
            checkpoint=SideChannelTaskConfig.from_dict(
                data.get("checkpoint"),
                base=base.checkpoint,
            ),
            rehydrate=SideChannelTaskConfig.from_dict(
                data.get("rehydrate"),
                base=base.rehydrate,
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool_summary": self.tool_summary.to_dict(),
            "checkpoint": self.checkpoint.to_dict(),
            "rehydrate": self.rehydrate.to_dict(),
        }


DEFAULT_SIDECHANNEL_CONFIG = SideChannelConfig(
    tool_summary=SideChannelTaskConfig(
        primary="deepseek/deepseek-chat",
        fallback=("google/gemini-2.5-flash-lite", "moonshot/kimi-k2.5"),
        max_tokens=260,
        quality=QualityFallbackPolicy(
            min_chars=64,
            min_alpha_chars=32,
            min_source_ratio=0.01,
            max_source_ratio=0.35,
            min_query_overlap_terms=1,
        ),
    ),
    checkpoint=SideChannelTaskConfig(
        primary="deepseek/deepseek-chat",
        fallback=("google/gemini-2.5-flash", "anthropic/claude-haiku-4.5"),
        max_tokens=340,
        quality=QualityFallbackPolicy(
            min_chars=96,
            min_alpha_chars=48,
            min_source_ratio=0.01,
            max_source_ratio=0.25,
            min_query_overlap_terms=1,
        ),
    ),
    rehydrate=SideChannelTaskConfig(
        primary="google/gemini-2.5-flash-lite",
        fallback=("deepseek/deepseek-chat", "moonshot/kimi-k2.5"),
        max_tokens=220,
        quality=QualityFallbackPolicy(
            min_chars=40,
            min_alpha_chars=20,
            min_source_ratio=0.005,
            max_source_ratio=0.20,
            min_query_overlap_terms=1,
        ),
    ),
)


@dataclass(frozen=True, slots=True)
class SemanticCallResult:
    text: str
    model: str
    estimated_cost: float = 0.0
    actual_cost: float | None = None
    quality_score: float = 1.0
    attempts: int = 1
    quality_fallbacks: int = 0


class SemanticCompressor(Protocol):
    async def summarize_tool_result(
        self,
        content: str,
        *,
        tool_name: str,
        latest_user_prompt: str,
        request: object,
    ) -> SemanticCallResult | None: ...

    async def summarize_history(
        self,
        transcript: str,
        *,
        latest_user_prompt: str,
        session_id: str,
        request: object,
    ) -> SemanticCallResult | None: ...

    async def rehydrate_artifact(
        self,
        query: str,
        *,
        artifact_id: str,
        content: str,
        summary: str,
        request: object,
    ) -> SemanticCallResult | None: ...


def score_semantic_quality(
    text: str,
    *,
    source_text: str,
    query_text: str = "",
    policy: QualityFallbackPolicy | None = None,
) -> tuple[bool, float, str]:
    policy = policy or QualityFallbackPolicy()
    candidate = text.strip()
    if not candidate:
        return False, 0.0, "empty"

    lowered = candidate.lower()
    for marker in policy.reject_markers:
        if marker in lowered:
            return False, 0.0, f"reject_marker:{marker}"

    alpha_chars = sum(1 for ch in candidate if ch.isalpha())
    if len(candidate) < policy.min_chars:
        return False, 0.15, "too_short"
    if alpha_chars < policy.min_alpha_chars:
        return False, 0.2, "too_sparse"

    source_tokens = max(1, estimate_tokens(source_text))
    candidate_tokens = estimate_tokens(candidate)
    ratio = candidate_tokens / source_tokens
    if ratio < policy.min_source_ratio:
        return False, min(0.3, ratio / max(policy.min_source_ratio, 1e-6)), "ratio_too_small"
    if ratio > policy.max_source_ratio:
        return False, max(0.1, 1.0 - ratio), "ratio_too_large"

    overlap_required = policy.min_query_overlap_terms
    overlap = _query_overlap_terms(candidate, query_text)
    if overlap_required > 0 and overlap < overlap_required:
        return False, 0.35, "low_query_overlap"

    ratio_score = min(1.0, ratio / max(policy.min_source_ratio, 1e-6))
    overlap_score = 1.0 if overlap_required == 0 else min(1.0, overlap / overlap_required)
    quality = min(1.0, 0.5 + min(ratio_score, 1.0) * 0.25 + overlap_score * 0.25)
    return True, quality, "ok"


def _query_overlap_terms(candidate: str, query_text: str) -> int:
    if not query_text.strip():
        return 0
    query_terms = {
        term
        for term in re.findall(r"[a-zA-Z_][a-zA-Z0-9_/-]{2,}", query_text.lower())
        if term not in {"the", "and", "for", "with", "that", "this", "from", "into"}
    }
    if not query_terms:
        return 0
    candidate_terms = set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_/-]{2,}", candidate.lower()))
    return len(query_terms & candidate_terms)
