"""Aggressive Healer v1 — Tier A rules and pipeline.

Specification:
``docs/experiments/design/math16_aggressive_healer_tier_a_v1_spec.md``

Exactly four rules; no Tier B.
"""

from __future__ import annotations

from agent_tools.finals_rebuild.aggressive_healer_tier_a.pipeline import (
    RULE_ORDER,
    run_tier_a_pipeline,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_a.types import (
    PipelineResult,
    RuleResult,
)

__all__ = [
    "RULE_ORDER",
    "PipelineResult",
    "RuleResult",
    "run_tier_a_pipeline",
]
