"""Tier C2 — Domain Signature Form Repair (narrow: default_optional_pure_form_cleanup).

legacy_rule_id: TIER_B_DOMAIN_SIGNATURE_FORM_REPAIR_V1
current_tier: Tier C2
layer_role: contract_aware_repair_candidate

Specification:
``docs/experiments/design/math16_aggressive_healer_domain_api_binding_spec_v1.md``

This package implements ONLY the ``default_optional_pure_form_cleanup`` subtype.
Other Tier C2 signature-form subtypes and Tier C1 are out of scope.
"""

from __future__ import annotations

from agent_tools.finals_rebuild.aggressive_healer_tier_c2.pipeline import (
    run_tier_c2_default_optional_cleanup,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_c2.rule_default_optional_cleanup import (
    CURRENT_TIER,
    LAYER_ROLE,
    RULE_ID,
    SUBTYPE,
    apply_once,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_c2.types import (
    PipelineResult,
    RuleResult,
)

__all__ = [
    "RULE_ID",
    "CURRENT_TIER",
    "LAYER_ROLE",
    "SUBTYPE",
    "RuleResult",
    "PipelineResult",
    "apply_once",
    "run_tier_c2_default_optional_cleanup",
]
