# -*- coding: utf-8 -*-
"""Types for Contract-Aware Aggressive Healer v2 certificates and rule outcomes."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Optional

RISK_TIER = "ContractAware_v2"
HEALER_FAMILY = "aggressive_healer_contract_v2"


@dataclass
class PatchCertificate:
    """Machine-computed patch certificate (all fields produced by code, never hand-filled)."""

    rule_id: str
    decision: str  # ACCEPT | ABSTAIN
    contract_id: str
    contract_sha256: str
    contract_clause: str
    cell_id: str
    task_id: str
    condition: str
    model_key: str
    ast_location: dict[str, Any]
    before_snippet: str
    after_snippet: str
    before_source_sha256: str
    after_source_sha256: str
    candidate_count: int
    preconditions: list[str]
    postconditions: list[str]
    changed_ast_nodes: list[str]
    unrelated_ast_unchanged: bool
    expected_answer_not_read: bool
    evaluator_result_not_read: bool
    candidate_trial_count: int
    abstention_reason: str = ""
    extras: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RuleOutcome:
    rule_id: str
    applied: bool
    abstained: bool
    source_out: str
    certificate: Optional[PatchCertificate]
    trigger_evidence: str = ""
    abstention_reason: str = ""

    def to_audit_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "applied": self.applied,
            "abstained": self.abstained,
            "trigger_evidence": self.trigger_evidence,
            "abstention_reason": self.abstention_reason,
            "certificate": None if self.certificate is None else self.certificate.to_dict(),
        }


@dataclass
class PipelineOutcome:
    cell_id: str
    task_id: str
    condition: str
    model_key: str
    pre_source_sha256: str
    post_source_sha256: str
    source_modified: bool
    rules_fired: list[str]
    rule_logs: list[dict[str, Any]]
    certificates: list[dict[str, Any]]
    abstentions: list[dict[str, Any]]
    proposed_repair_count: int
    formal_artifact_write: bool = False
    source_out: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        # Keep source out of bulk audits when serializing huge payloads is undesirable;
        # callers that need the healed source read source_out directly.
        return d
