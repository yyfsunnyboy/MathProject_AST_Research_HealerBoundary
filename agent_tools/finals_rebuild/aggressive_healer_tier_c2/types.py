"""Result types for Tier C2 narrow signature-form repair."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Optional

RISK_TIER = "Tier C"
CURRENT_TIER = "Tier C2"
LAYER_ROLE = "contract_aware_repair_candidate"


@dataclass
class RuleResult:
    rule_id: str
    risk_tier: str = RISK_TIER
    current_tier: str = CURRENT_TIER
    layer_role: str = LAYER_ROLE
    repair_subtype: str = "default_optional_pure_form_cleanup"
    ssot_entry_id: str = ""
    sequence_index: int = 1
    triggered: bool = False
    applied: bool = False
    abstained: bool = False
    trigger_evidence: str = ""
    abstention_reason: str = ""
    pre_source_sha: str = ""
    post_source_sha: str = ""
    edit_count: int = 0
    edit_scope: str = ""
    ast_node_location: Any = None
    pre_parseable: Optional[bool] = None
    post_parseable: Optional[bool] = None
    pre_executable: Optional[bool] = None
    post_executable: Optional[bool] = None
    pre_pass_fail: Optional[str] = None
    post_pass_fail: Optional[str] = None
    outcome_taxonomy: str = "noop"
    extras: dict[str, Any] = field(default_factory=dict)
    source_out: str = ""

    def to_audit_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d.pop("source_out", None)
        return d


@dataclass
class PipelineResult:
    pre_source: str
    post_source: str
    pre_source_sha: str
    post_source_sha: str
    rule_logs: list[dict[str, Any]]
    rules_fired: list[str]
    mutation_count: int
    pipeline_idempotent: bool
    outcome_taxonomy: str
    abstention_reason: str = ""
    rolled_back: bool = False
    risk_tier: str = RISK_TIER
    current_tier: str = CURRENT_TIER
    layer_role: str = LAYER_ROLE

    def to_audit_dict(self) -> dict[str, Any]:
        return {
            "pre_source_sha": self.pre_source_sha,
            "post_source_sha": self.post_source_sha,
            "rule_logs": self.rule_logs,
            "rules_fired": self.rules_fired,
            "mutation_count": self.mutation_count,
            "pipeline_idempotent": self.pipeline_idempotent,
            "outcome_taxonomy": self.outcome_taxonomy,
            "abstention_reason": self.abstention_reason,
            "rolled_back": self.rolled_back,
            "risk_tier": self.risk_tier,
            "current_tier": self.current_tier,
            "layer_role": self.layer_role,
        }
