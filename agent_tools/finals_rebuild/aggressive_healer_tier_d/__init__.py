"""Tier D — Risk-accepting repair (Development slices: D3/D1 + D5 + D2).

current_tier: Tier D
layer_role: failure_gated_risk_accepting_repair

Specification:
``docs/experiments/design/math16_tier_d_risk_accepting_repair_spec_v1.md``

Implemented:
- TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1 (D3)
- TIER_D_OPS_SHADOW_REMOVAL_V1 (D1)
- TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1 (D5)
- TIER_D_DUPLICATE_DEFINITION_SELECTION_V1 (D2)

D4/D6 remain out of scope. After D5/D2 Development: TIER_D_4B_EXPLORATION_CLOSED.
"""

from __future__ import annotations

from agent_tools.finals_rebuild.aggressive_healer_tier_d import rule_d1_ops_shadow_removal as d1
from agent_tools.finals_rebuild.aggressive_healer_tier_d import rule_d2_duplicate_definition_selection as d2
from agent_tools.finals_rebuild.aggressive_healer_tier_d import rule_d3_syntax_residue_quarantine as d3
from agent_tools.finals_rebuild.aggressive_healer_tier_d import rule_d5_ranked_domain_method_binding as d5
from agent_tools.finals_rebuild.aggressive_healer_tier_d.pipeline import (
    RULE_ORDER,
    run_tier_d_d2_pipeline,
    run_tier_d_d3_d1_pipeline,
    run_tier_d_d5_pipeline,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d.types import (
    CURRENT_TIER,
    LAYER_ROLE,
    RISK_TIER,
    PipelineResult,
    RuleResult,
)

RULE_ID_D3 = d3.RULE_ID
RULE_ID_D1 = d1.RULE_ID
RULE_ID_D5 = d5.RULE_ID
RULE_ID_D2 = d2.RULE_ID

__all__ = [
    "RULE_ID_D3",
    "RULE_ID_D1",
    "RULE_ID_D5",
    "RULE_ID_D2",
    "RULE_ORDER",
    "RISK_TIER",
    "CURRENT_TIER",
    "LAYER_ROLE",
    "RuleResult",
    "PipelineResult",
    "d3",
    "d1",
    "d5",
    "d2",
    "run_tier_d_d3_d1_pipeline",
    "run_tier_d_d5_pipeline",
    "run_tier_d_d2_pipeline",
]
