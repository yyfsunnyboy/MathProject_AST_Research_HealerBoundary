# -*- coding: utf-8 -*-
"""Qwen4B cell-wise deterministic fixpoint replay runner (v1).

Implements the frozen protocol:
``docs/experiments/design/math16_qwen4b_cellwise_fixpoint_replay_protocol_v1.md``

This module provides:
- Round 1 residual population lock (232 FAIL active / 88 PASS excluded)
- cell journal + aggregate summary schemas
- termination / SHA-history judgment
- one-cycle stack application A→B→C1→C2→D3→D1→D5→D2
- resume / duplicate / determinism guards
- zero-execution preflight

Formal 232-cell replay is gated behind ``allow_formal_execution=True`` and is
not invoked by the default preflight CLI.
"""
from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Optional

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.aggressive_healer_tier_a import (  # noqa: E402
    RULE_ORDER as TIER_B_RULE_ORDER,
    run_tier_a_pipeline,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_c2 import (  # noqa: E402
    RULE_ID as TIER_C2_RULE_ID,
    run_tier_c2_default_optional_cleanup,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d import (  # noqa: E402
    RULE_ID_D1,
    RULE_ID_D2,
    RULE_ID_D3,
    RULE_ID_D5,
    run_tier_d_d2_pipeline,
    run_tier_d_d5_pipeline,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d import (  # noqa: E402
    rule_d1_ops_shadow_removal as d1_mod,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d import (  # noqa: E402
    rule_d2_duplicate_definition_selection as d2_mod,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d import (  # noqa: E402
    rule_d3_syntax_residue_quarantine as d3_mod,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d import (  # noqa: E402
    rule_d5_ranked_domain_method_binding as d5_mod,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_d.ranking import (  # noqa: E402
    MIN_MARGIN,
    MIN_SCORE,
)
from agent_tools.finals_rebuild.ce115_research_healer_runner import (  # noqa: E402
    RULE_ALLOWLIST,
    MathHealerRunner,
)
from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id  # noqa: E402
from scripts.preflight_math16_method2_all_cell import decide_eligibility  # noqa: E402
from scripts.run_math16_c2_c3_tier_c1_qwen9b_v1 import (  # noqa: E402
    adjudicate_c1,
    apply_c1_rename,
)
from scripts.run_math16_c3_c4_tier_c2_qwen9b_v1 import adjudicate_c2  # noqa: E402

PROTOCOL_MANIFEST = (
    ROOT
    / "docs/experiments/manifests/math16_qwen4b_cellwise_fixpoint_replay_protocol_v1.json"
)
ROUND1_SUMMARY = (
    ROOT / "docs/experiments/manifests/math16_three_model_round1_summary_v1.json"
)
C5A_CLOSURE = (
    ROOT / "docs/experiments/manifests/math16_c5a_final_source_closure_v1.json"
)
D5_REPLAY = (
    ROOT / "docs/experiments/manifests/math16_c5a_tier_d_d5_development_replay_v1.json"
)
D2_REPLAY = (
    ROOT / "docs/experiments/manifests/math16_c5a_tier_d_d2_development_replay_v1.json"
)
CONTRACT_MATRIX = (
    ROOT / "docs/experiments/manifests/math16_ab2d_task_contract_matrix_v1.json"
)
RESULTS_ROOT = (
    ROOT / "docs/experiments/results/math16_qwen4b_cellwise_fixpoint_replay_v1"
)
CELL_JOURNAL_NAME = "cell_cycle_journal.jsonl"
CELL_FINAL_JOURNAL_NAME = "cell_final_journal.jsonl"
SUMMARY_NAME = "summary.json"
RUN_LOCK_NAME = "formal_run.lock"

MAX_ROUND = 8
EXPECTED_TOTAL = 320
EXPECTED_PASS = 88
EXPECTED_FAIL = 232
MODEL_GROUP = "qwen4b"
FIXED_SEQUENCE = "A→B→C1→C2→D3→D1→D5→D2"
LAYER_ORDER = (
    "tier_a",
    "tier_b",
    "tier_c1",
    "tier_c2",
    "tier_d3",
    "tier_d1",
    "tier_d5",
    "tier_d2",
)
TERMINATION_ENUM = (
    "ITERATIVE_RESCUE",
    "ZERO_CHANGE_CONVERGENCE",
    "CYCLE_DETECTED",
    "MAX_ROUND_NON_CONVERGENT",
)
TIER_B_EXPECTED_ORDER = (
    "core.normalize_fullwidth_python_punctuation",
    "TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1",
    "TIER_A_EMPTY_SUITE_INSERT_PASS_V1",
    "TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1",
)
RULE_ID_C1 = "TIER_B_EXPLICIT_DOMAIN_METHOD_BINDING_REPAIR_V1"

CELL_JOURNAL_REQUIRED_FIELDS = (
    "cell_id",
    "cycle_index",
    "round_start_sha",
    "per_rule_pre_sha",
    "per_rule_post_sha",
    "rule_id",
    "eligible",
    "modified",
    "abstained",
    "round_end_sha",
    "source_changed",
    "full_sha_history",
    "newly_eligible",
    "enabling_prior_rule",
    "iterative_partial_repair",
    "rescue_cycle",
    "rescue_rule_id",
    "convergence_cycle_count",
    "termination_reason",
    "regression",
    "cycle_detected",
    "max_round_reached",
)

CELL_FINAL_REQUIRED_FIELDS = (
    "cell_id",
    "round1_final_sha",
    "final_sha",
    "cycles_completed",
    "termination_reason",
    "rescue_cycle",
    "rescue_rule_id",
    "full_sha_history",
    "cycle_detected",
    "max_round_reached",
    "regression",
)

AGGREGATE_SUMMARY_REQUIRED_FIELDS = (
    "protocol_id",
    "model_group",
    "n_active_cells",
    "n_excluded_pass_cells",
    "max_round",
    "fixed_sequence",
    "termination_counts",
    "iterative_rescue_n",
    "zero_change_n",
    "cycle_detected_n",
    "max_round_n",
    "model_calls",
    "formal_replay_executed",
    "deterministic_second_cycle_probe",
)


class FixpointProtocolError(RuntimeError):
    """Raised when frozen protocol invariants are violated."""


class FormalExecutionBlocked(RuntimeError):
    """Raised when formal 232-cell replay is requested without authorization."""


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


@dataclass
class Round1Cell:
    cell_id: str
    task_id: str
    condition: str
    seed: int
    model: str
    model_group: str
    round1_outcome: str  # PASS | FAIL
    round1_final_source_path: str
    round1_final_source_sha256: str
    source_origin: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "cell_id": self.cell_id,
            "task_id": self.task_id,
            "condition": self.condition,
            "seed": self.seed,
            "model": self.model,
            "model_group": self.model_group,
            "round1_outcome": self.round1_outcome,
            "round1_final_source_path": self.round1_final_source_path,
            "round1_final_source_sha256": self.round1_final_source_sha256,
            "source_origin": self.source_origin,
        }


@dataclass
class Population:
    active_fail: list[Round1Cell]
    excluded_pass: list[Round1Cell]

    @property
    def active_ids(self) -> set[str]:
        return {c.cell_id for c in self.active_fail}

    @property
    def excluded_ids(self) -> set[str]:
        return {c.cell_id for c in self.excluded_pass}


@dataclass
class RuleStep:
    layer: str
    rule_id: Optional[str]
    pre_sha: str
    post_sha: str
    eligible: bool
    modified: bool
    abstained: bool
    newly_eligible: bool = False
    enabling_prior_rule: Optional[str] = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "layer": self.layer,
            "rule_id": self.rule_id,
            "pre_sha": self.pre_sha,
            "post_sha": self.post_sha,
            "eligible": self.eligible,
            "modified": self.modified,
            "abstained": self.abstained,
            "newly_eligible": self.newly_eligible,
            "enabling_prior_rule": self.enabling_prior_rule,
        }


@dataclass
class CycleResult:
    cell_id: str
    cycle_index: int
    round_start_source: str
    round_end_source: str
    round_start_sha: str
    round_end_sha: str
    source_changed: bool
    rule_trace: list[RuleStep] = field(default_factory=list)
    final_status: Optional[str] = None  # PASS|FAIL observational
    decision: dict[str, Any] = field(default_factory=dict)

    def journal_row(self) -> dict[str, Any]:
        """Flatten protocol-required fields for one cycle row."""
        decision = self.decision
        newly = [
            s.rule_id
            for s in self.rule_trace
            if s.newly_eligible and s.rule_id is not None
        ]
        enabling = [
            {
                "rule_id": s.rule_id,
                "enabling_prior_rule": s.enabling_prior_rule,
            }
            for s in self.rule_trace
            if s.newly_eligible and s.enabling_prior_rule
        ]
        row = {
            "cell_id": self.cell_id,
            "cycle_index": self.cycle_index,
            "round_start_sha": self.round_start_sha,
            "per_rule_pre_sha": [s.pre_sha for s in self.rule_trace],
            "per_rule_post_sha": [s.post_sha for s in self.rule_trace],
            "rule_id": [s.rule_id for s in self.rule_trace],
            "eligible": [s.eligible for s in self.rule_trace],
            "modified": [s.modified for s in self.rule_trace],
            "abstained": [s.abstained for s in self.rule_trace],
            "rule_trace": [s.as_dict() for s in self.rule_trace],
            "round_end_sha": self.round_end_sha,
            "source_changed": self.source_changed,
            "full_sha_history": list(decision.get("full_sha_history") or []),
            "newly_eligible": newly,
            "enabling_prior_rule": enabling,
            "iterative_partial_repair": bool(
                self.source_changed and self.final_status != "PASS"
            ),
            "rescue_cycle": decision.get("rescue_cycle"),
            "rescue_rule_id": decision.get("rescue_rule_id"),
            "convergence_cycle_count": decision.get("convergence_cycle_count"),
            "termination_reason": decision.get("termination_reason"),
            "regression": False,
            "cycle_detected": bool(decision.get("cycle_detected")),
            "max_round_reached": bool(decision.get("max_round_reached")),
            "final_status": self.final_status,
            "continue": bool(decision.get("continue")),
        }
        missing = [k for k in CELL_JOURNAL_REQUIRED_FIELDS if k not in row]
        if missing:
            raise FixpointProtocolError(f"journal row missing fields: {missing}")
        return row


_CONTRACTS: Optional[dict[tuple[str, str], dict[str, Any]]] = None


def contracts_by_key() -> dict[tuple[str, str], dict[str, Any]]:
    global _CONTRACTS
    if _CONTRACTS is None:
        matrix = load_json(CONTRACT_MATRIX)
        _CONTRACTS = {
            (c["task_id"], c["condition_code"]): c for c in matrix["contracts"]
        }
    return _CONTRACTS


def attribute_rescue_rule_id(rule_trace: Iterable[Mapping[str, Any] | RuleStep]) -> Optional[str]:
    last: Optional[str] = None
    for step in rule_trace:
        if isinstance(step, RuleStep):
            pre, post, modified, rule_id = (
                step.pre_sha,
                step.post_sha,
                step.modified,
                step.rule_id,
            )
        else:
            pre = step["pre_sha"]
            post = step["post_sha"]
            modified = bool(step.get("modified"))
            rule_id = step.get("rule_id")
        if modified and post != pre and rule_id:
            last = str(rule_id)
    return last


def judge_after_cycle(
    *,
    final_status: str,
    round_start_sha: str,
    round_end_sha: str,
    full_sha_history: list[str],
    cycle_index: int,
    max_round: int = MAX_ROUND,
    rule_trace: list[Any] | None = None,
) -> dict[str, Any]:
    """Frozen termination order after one complete cell-wise cycle."""
    if not full_sha_history:
        raise FixpointProtocolError("full_sha_history must start from Round 1 final SHA")

    source_changed = round_end_sha != round_start_sha
    history = list(full_sha_history)

    if final_status == "PASS":
        return {
            "termination_reason": "ITERATIVE_RESCUE",
            "rescue_cycle": cycle_index,
            "rescue_rule_id": attribute_rescue_rule_id(rule_trace or []),
            "source_changed": source_changed,
            "cycle_detected": False,
            "max_round_reached": False,
            "convergence_cycle_count": cycle_index,
            "full_sha_history": history,
            "continue": False,
        }
    if final_status != "FAIL":
        raise FixpointProtocolError(f"unsupported final_status: {final_status}")

    if not source_changed:
        return {
            "termination_reason": "ZERO_CHANGE_CONVERGENCE",
            "rescue_cycle": None,
            "rescue_rule_id": None,
            "source_changed": False,
            "cycle_detected": False,
            "max_round_reached": False,
            "convergence_cycle_count": cycle_index,
            "full_sha_history": history,
            "continue": False,
        }

    if round_end_sha in history:
        return {
            "termination_reason": "CYCLE_DETECTED",
            "rescue_cycle": None,
            "rescue_rule_id": None,
            "source_changed": True,
            "cycle_detected": True,
            "max_round_reached": False,
            "convergence_cycle_count": cycle_index,
            "full_sha_history": history,
            "continue": False,
        }

    history.append(round_end_sha)
    if cycle_index >= max_round:
        return {
            "termination_reason": "MAX_ROUND_NON_CONVERGENT",
            "rescue_cycle": None,
            "rescue_rule_id": None,
            "source_changed": True,
            "cycle_detected": False,
            "max_round_reached": True,
            "convergence_cycle_count": cycle_index,
            "full_sha_history": history,
            "continue": False,
        }

    return {
        "termination_reason": None,
        "rescue_cycle": None,
        "rescue_rule_id": None,
        "source_changed": True,
        "cycle_detected": False,
        "max_round_reached": False,
        "convergence_cycle_count": cycle_index,
        "full_sha_history": history,
        "continue": True,
        "advance_policy": "SAME_CELL_ONLY",
    }


def _override_map() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for label, path in (("d5_post", D5_REPLAY), ("d2_post", D2_REPLAY)):
        cell = load_json(path)["cell"]
        out[cell["cell_id"]] = {
            "path": cell["post_source_path"],
            "sha256": cell["post_source_sha256"],
            "origin": label,
        }
    return out


def load_round1_population(*, root: Path = ROOT) -> Population:
    """Load sealed Round 1 4B population; lock 232 FAIL / 88 PASS."""
    summary = load_json(root / ROUND1_SUMMARY.relative_to(ROOT))
    c5a = load_json(root / C5A_CLOSURE.relative_to(ROOT))
    q4 = summary["models"]["qwen4b"]
    if q4["final_pass"] != EXPECTED_PASS or q4["final_fail"] != EXPECTED_FAIL:
        raise FixpointProtocolError(
            f"Round1 summary mismatch: pass={q4['final_pass']} fail={q4['final_fail']}"
        )
    val = c5a["validation"]
    if val["pass_n"] != EXPECTED_PASS or val["fail_n"] != EXPECTED_FAIL:
        raise FixpointProtocolError(
            f"C5a closure mismatch: pass={val['pass_n']} fail={val['fail_n']}"
        )
    if val["n_cells"] != EXPECTED_TOTAL:
        raise FixpointProtocolError(f"C5a n_cells={val['n_cells']} != 320")

    overrides = _override_map()
    active: list[Round1Cell] = []
    excluded: list[Round1Cell] = []
    for raw in c5a["cells"]:
        if raw.get("model_group") != MODEL_GROUP:
            raise FixpointProtocolError(f"non-4B cell in C5a: {raw.get('cell_id')}")
        outcome = raw["c5a_outcome"]
        cid = raw["cell_id"]
        if cid in overrides and outcome == "FAIL":
            ov = overrides[cid]
            path = ov["path"]
            sha = ov["sha256"]
            origin = ov["origin"]
        else:
            path = raw["c5a_final_source_path"]
            sha = raw["c5a_final_source_sha256"]
            origin = raw.get("source_origin") or "C5A_FINAL"
        cell = Round1Cell(
            cell_id=cid,
            task_id=raw["task_id"],
            condition=raw["condition"],
            seed=int(raw["seed"]),
            model=raw["model"],
            model_group=raw["model_group"],
            round1_outcome="PASS" if outcome == "PASS" else "FAIL",
            round1_final_source_path=path,
            round1_final_source_sha256=sha,
            source_origin=origin,
        )
        if cell.round1_outcome == "PASS":
            excluded.append(cell)
        else:
            active.append(cell)

    if len(active) != EXPECTED_FAIL or len(excluded) != EXPECTED_PASS:
        raise FixpointProtocolError(
            f"population lock failed: active={len(active)} excluded={len(excluded)}"
        )
    if population_ids_overlap(active, excluded):
        raise FixpointProtocolError("PASS/FAIL id overlap")
    return Population(active_fail=active, excluded_pass=excluded)


def population_ids_overlap(
    active: list[Round1Cell], excluded: list[Round1Cell]
) -> bool:
    return bool({c.cell_id for c in active} & {c.cell_id for c in excluded})


def read_round1_final_source(cell: Round1Cell, *, root: Path = ROOT) -> str:
    path = root / cell.round1_final_source_path
    if not path.is_file():
        raise FixpointProtocolError(f"missing Round1 final source: {path}")
    text = path.read_text(encoding="utf-8")
    digest = sha256_text(text)
    if digest != cell.round1_final_source_sha256:
        raise FixpointProtocolError(
            f"SHA drift for {cell.cell_id}: {digest} != {cell.round1_final_source_sha256}"
        )
    return text


def assert_pass_cells_excluded(
    population: Population, scanned_ids: Iterable[str]
) -> None:
    scanned = set(scanned_ids)
    leaked = scanned & population.excluded_ids
    if leaked:
        raise FixpointProtocolError(
            f"PASS cells must never be scanned: {sorted(leaked)[:5]}"
        )


# ---------------------------------------------------------------------------
# Layer healers (frozen APIs; no rule/threshold/order changes)
# ---------------------------------------------------------------------------


def _static_status(step: Any) -> str:
    if step.applied:
        return "ELIGIBLE"
    if step.triggered and step.abstained:
        return "AMBIGUOUS_ABSTAIN"
    return "INELIGIBLE"


def _step(
    *,
    layer: str,
    rule_id: Optional[str],
    pre: str,
    post: str,
    eligible: bool,
    modified: bool,
    abstained: bool,
    last_modifying_rule: Optional[str],
    eligible_on_round_start: bool,
) -> RuleStep:
    newly = bool(eligible and not eligible_on_round_start)
    return RuleStep(
        layer=layer,
        rule_id=rule_id,
        pre_sha=sha256_text(pre),
        post_sha=sha256_text(post),
        eligible=eligible,
        modified=modified,
        abstained=abstained,
        newly_eligible=newly,
        enabling_prior_rule=last_modifying_rule if newly else None,
    )


def heal_tier_a_trace(
    *, cell: Mapping[str, Any], pre_source: str, round_start_source: str, last_mod: Optional[str]
) -> tuple[str, list[RuleStep], Optional[str]]:
    runner = MathHealerRunner(max_passes=3)
    tasks = tasks_by_id()
    frozen = frozen_for_prompt(tasks[cell["task_id"]])["oracle_payload"]
    context = {"frozen": frozen}
    elig_start = decide_eligibility(round_start_source or None, context)["eligible"]
    eligibility = decide_eligibility(pre_source or None, context)
    steps: list[RuleStep] = []
    if not eligibility["eligible"]:
        steps.append(
            _step(
                layer="tier_a",
                rule_id=None,
                pre=pre_source,
                post=pre_source,
                eligible=False,
                modified=False,
                abstained=True,
                last_modifying_rule=last_mod,
                eligible_on_round_start=elig_start,
            )
        )
        return pre_source, steps, last_mod

    result = runner.run(pre_source, context=context)
    post = result.output_source
    current = pre_source
    local_last = last_mod
    changed_any = False
    for prov in result.provenance:
        rid = getattr(prov, "selected_rule_id", None)
        changed = bool(getattr(prov, "changed", False))
        if not rid:
            continue
        # Provenance lacks intermediate source; attribute whole-tier delta to last changed rule.
        if changed:
            changed_any = True
            steps.append(
                _step(
                    layer="tier_a",
                    rule_id=rid,
                    pre=current,
                    post=post if changed else current,
                    eligible=True,
                    modified=True,
                    abstained=False,
                    last_modifying_rule=local_last,
                    eligible_on_round_start=elig_start,
                )
            )
            current = post
            local_last = rid
    if not changed_any:
        steps.append(
            _step(
                layer="tier_a",
                rule_id=eligibility.get("rule_id"),
                pre=pre_source,
                post=pre_source,
                eligible=True,
                modified=False,
                abstained=True,
                last_modifying_rule=last_mod,
                eligible_on_round_start=elig_start,
            )
        )
        return pre_source, steps, last_mod
    # Collapse multi-provenance intermediates to final post once.
    if len(steps) > 1:
        first_pre = pre_source
        collapsed = [
            _step(
                layer="tier_a",
                rule_id=local_last,
                pre=first_pre,
                post=post,
                eligible=True,
                modified=post != pre_source,
                abstained=post == pre_source,
                last_modifying_rule=last_mod,
                eligible_on_round_start=elig_start,
            )
        ]
        steps = collapsed
        local_last = local_last if post != pre_source else last_mod
    return post, steps, local_last if post != pre_source else last_mod


def heal_tier_b_trace(
    *, pre_source: str, round_start_source: str, last_mod: Optional[str]
) -> tuple[str, list[RuleStep], Optional[str]]:
    start_pipe = run_tier_a_pipeline(round_start_source)
    start_fired = set(start_pipe.rules_fired or [])
    pipe = run_tier_a_pipeline(pre_source)
    steps: list[RuleStep] = []
    current = pre_source
    local_last = last_mod
    # Expand frozen Tier B rule order using rule_logs when present.
    logs = list(pipe.rule_logs or [])
    if logs:
        for log in logs:
            rid = log.get("rule_id")
            pre_sha = log.get("pre_source_sha") or sha256_text(current)
            post_sha = log.get("post_source_sha") or pre_sha
            applied = bool(log.get("applied"))
            # Reconstruct local text only via cumulative mutation when applied.
            post_text = current
            if applied and post_sha != pre_sha:
                # Use pipeline final if this is the last applied; otherwise keep marker via sha pair.
                post_text = pipe.post_source if rid in (pipe.rules_fired or []) else current
                # Prefer exact: if only one mutation, post is pipe.post_source.
                if pipe.mutation_count == 1 and applied:
                    post_text = pipe.post_source
            step = RuleStep(
                layer="tier_b",
                rule_id=rid,
                pre_sha=pre_sha,
                post_sha=post_sha if applied else pre_sha,
                eligible=bool(log.get("triggered") or applied),
                modified=applied and post_sha != pre_sha,
                abstained=not (applied and post_sha != pre_sha),
                newly_eligible=bool((log.get("triggered") or applied) and rid not in start_fired),
                enabling_prior_rule=local_last
                if (log.get("triggered") or applied) and rid not in start_fired
                else None,
            )
            steps.append(step)
            if step.modified:
                current = pipe.post_source
                local_last = rid
        return pipe.post_source, steps, local_last if pipe.post_source != pre_source else last_mod

    modified = pipe.post_source != pre_source
    steps.append(
        _step(
            layer="tier_b",
            rule_id=(pipe.rules_fired or [None])[0] if pipe.rules_fired else None,
            pre=pre_source,
            post=pipe.post_source,
            eligible=modified or bool(pipe.rules_fired),
            modified=modified,
            abstained=not modified,
            last_modifying_rule=last_mod,
            eligible_on_round_start=bool(start_fired),
        )
    )
    return (
        pipe.post_source,
        steps,
        (pipe.rules_fired[-1] if modified and pipe.rules_fired else last_mod),
    )


def heal_tier_c1_trace(
    *, cell: Mapping[str, Any], pre_source: str, round_start_source: str, last_mod: Optional[str]
) -> tuple[str, list[RuleStep], Optional[str]]:
    contracts = contracts_by_key()
    start_adj = adjudicate_c1(
        source=round_start_source,
        task_id=cell["task_id"],
        condition=cell["condition"],
        contracts_by_key=contracts,
    )
    adj = adjudicate_c1(
        source=pre_source,
        task_id=cell["task_id"],
        condition=cell["condition"],
        contracts_by_key=contracts,
    )
    if adj["status"] != "C1_ELIGIBLE":
        step = _step(
            layer="tier_c1",
            rule_id=RULE_ID_C1,
            pre=pre_source,
            post=pre_source,
            eligible=False,
            modified=False,
            abstained=True,
            last_modifying_rule=last_mod,
            eligible_on_round_start=start_adj["status"] == "C1_ELIGIBLE",
        )
        return pre_source, [step], last_mod
    post = apply_c1_rename(pre_source, adj)
    modified = post != pre_source
    step = _step(
        layer="tier_c1",
        rule_id=RULE_ID_C1,
        pre=pre_source,
        post=post if modified else pre_source,
        eligible=modified,
        modified=modified,
        abstained=not modified,
        last_modifying_rule=last_mod,
        eligible_on_round_start=start_adj["status"] == "C1_ELIGIBLE",
    )
    return (post if modified else pre_source), [step], (RULE_ID_C1 if modified else last_mod)


def heal_tier_c2_trace(
    *, cell: Mapping[str, Any], pre_source: str, round_start_source: str, last_mod: Optional[str]
) -> tuple[str, list[RuleStep], Optional[str]]:
    contracts = contracts_by_key()
    start_adj = adjudicate_c2(
        source=round_start_source,
        task_id=cell["task_id"],
        condition=cell["condition"],
        contracts_by_key=contracts,
    )
    adj = adjudicate_c2(
        source=pre_source,
        task_id=cell["task_id"],
        condition=cell["condition"],
        contracts_by_key=contracts,
    )
    if adj["status"] != "C2_ELIGIBLE":
        step = _step(
            layer="tier_c2",
            rule_id=TIER_C2_RULE_ID,
            pre=pre_source,
            post=pre_source,
            eligible=False,
            modified=False,
            abstained=True,
            last_modifying_rule=last_mod,
            eligible_on_round_start=start_adj["status"] == "C2_ELIGIBLE",
        )
        return pre_source, [step], last_mod
    pipe = run_tier_c2_default_optional_cleanup(pre_source)
    ok = (
        pipe.mutation_count == 1
        and not pipe.rolled_back
        and pipe.post_source != pre_source
    )
    if not ok:
        step = _step(
            layer="tier_c2",
            rule_id=TIER_C2_RULE_ID,
            pre=pre_source,
            post=pre_source,
            eligible=False,
            modified=False,
            abstained=True,
            last_modifying_rule=last_mod,
            eligible_on_round_start=start_adj["status"] == "C2_ELIGIBLE",
        )
        return pre_source, [step], last_mod
    step = _step(
        layer="tier_c2",
        rule_id=TIER_C2_RULE_ID,
        pre=pre_source,
        post=pipe.post_source,
        eligible=True,
        modified=True,
        abstained=False,
        last_modifying_rule=last_mod,
        eligible_on_round_start=start_adj["status"] == "C2_ELIGIBLE",
    )
    return pipe.post_source, [step], TIER_C2_RULE_ID


def _heal_single_d_trace(
    *,
    layer: str,
    rule_id: str,
    pre_source: str,
    step_obj: Any,
    last_mod: Optional[str],
    eligible_on_round_start: bool,
    pipeline_post: Optional[str] = None,
) -> tuple[str, list[RuleStep], Optional[str]]:
    status = _static_status(step_obj)
    post = pre_source
    if pipeline_post is not None:
        post = pipeline_post
    elif step_obj.applied and step_obj.source_out:
        post = step_obj.source_out
    modified = post != pre_source and bool(step_obj.applied or (pipeline_post and pipeline_post != pre_source))
    if pipeline_post is not None:
        modified = pipeline_post != pre_source
        post = pipeline_post if modified else pre_source
    step = _step(
        layer=layer,
        rule_id=rule_id,
        pre=pre_source,
        post=post,
        eligible=modified or status == "ELIGIBLE",
        modified=modified,
        abstained=not modified,
        last_modifying_rule=last_mod,
        eligible_on_round_start=eligible_on_round_start,
    )
    return post, [step], (rule_id if modified else last_mod)


def heal_d3_trace(
    *, pre_source: str, round_start_source: str, last_mod: Optional[str]
) -> tuple[str, list[RuleStep], Optional[str]]:
    start = d3_mod.apply_once(round_start_source)
    step = d3_mod.apply_once(pre_source)
    return _heal_single_d_trace(
        layer="tier_d3",
        rule_id=RULE_ID_D3,
        pre_source=pre_source,
        step_obj=step,
        last_mod=last_mod,
        eligible_on_round_start=_static_status(start) == "ELIGIBLE",
    )


def heal_d1_trace(
    *, pre_source: str, round_start_source: str, last_mod: Optional[str]
) -> tuple[str, list[RuleStep], Optional[str]]:
    start = d1_mod.apply_once(round_start_source)
    step = d1_mod.apply_once(pre_source)
    return _heal_single_d_trace(
        layer="tier_d1",
        rule_id=RULE_ID_D1,
        pre_source=pre_source,
        step_obj=step,
        last_mod=last_mod,
        eligible_on_round_start=_static_status(start) == "ELIGIBLE",
    )


def heal_d5_trace(
    *, cell: Mapping[str, Any], pre_source: str, round_start_source: str, last_mod: Optional[str]
) -> tuple[str, list[RuleStep], Optional[str]]:
    start = d5_mod.apply_once(
        round_start_source, task_id=cell["task_id"], condition=cell["condition"]
    )
    step = d5_mod.apply_once(
        pre_source, task_id=cell["task_id"], condition=cell["condition"]
    )
    pipe = run_tier_d_d5_pipeline(
        pre_source, task_id=cell["task_id"], condition=cell["condition"]
    )
    post = pre_source if pipe.rolled_back else pipe.post_source
    return _heal_single_d_trace(
        layer="tier_d5",
        rule_id=RULE_ID_D5,
        pre_source=pre_source,
        step_obj=step,
        last_mod=last_mod,
        eligible_on_round_start=_static_status(start) == "ELIGIBLE",
        pipeline_post=post,
    )


def heal_d2_trace(
    *, pre_source: str, round_start_source: str, last_mod: Optional[str]
) -> tuple[str, list[RuleStep], Optional[str]]:
    start = d2_mod.apply_once(round_start_source)
    step = d2_mod.apply_once(pre_source)
    pipe = run_tier_d_d2_pipeline(pre_source)
    post = pre_source if pipe.rolled_back else pipe.post_source
    return _heal_single_d_trace(
        layer="tier_d2",
        rule_id=RULE_ID_D2,
        pre_source=pre_source,
        step_obj=step,
        last_mod=last_mod,
        eligible_on_round_start=_static_status(start) == "ELIGIBLE",
        pipeline_post=post,
    )


def apply_stack_once(
    *,
    cell: Mapping[str, Any],
    source: str,
    cycle_index: int,
) -> CycleResult:
    """Apply full frozen stack once. Does not read evaluator outcomes for mutation."""
    round_start = source
    current = source
    trace: list[RuleStep] = []
    last_mod: Optional[str] = None

    current, steps, last_mod = heal_tier_a_trace(
        cell=cell, pre_source=current, round_start_source=round_start, last_mod=last_mod
    )
    trace.extend(steps)
    current, steps, last_mod = heal_tier_b_trace(
        pre_source=current, round_start_source=round_start, last_mod=last_mod
    )
    trace.extend(steps)
    current, steps, last_mod = heal_tier_c1_trace(
        cell=cell, pre_source=current, round_start_source=round_start, last_mod=last_mod
    )
    trace.extend(steps)
    current, steps, last_mod = heal_tier_c2_trace(
        cell=cell, pre_source=current, round_start_source=round_start, last_mod=last_mod
    )
    trace.extend(steps)
    current, steps, last_mod = heal_d3_trace(
        pre_source=current, round_start_source=round_start, last_mod=last_mod
    )
    trace.extend(steps)
    current, steps, last_mod = heal_d1_trace(
        pre_source=current, round_start_source=round_start, last_mod=last_mod
    )
    trace.extend(steps)
    current, steps, last_mod = heal_d5_trace(
        cell=cell, pre_source=current, round_start_source=round_start, last_mod=last_mod
    )
    trace.extend(steps)
    current, steps, last_mod = heal_d2_trace(
        pre_source=current, round_start_source=round_start, last_mod=last_mod
    )
    trace.extend(steps)

    start_sha = sha256_text(round_start)
    end_sha = sha256_text(current)
    return CycleResult(
        cell_id=str(cell["cell_id"]),
        cycle_index=cycle_index,
        round_start_source=round_start,
        round_end_source=current,
        round_start_sha=start_sha,
        round_end_sha=end_sha,
        source_changed=end_sha != start_sha,
        rule_trace=trace,
        final_status=None,
        decision={},
    )


def finalize_cycle_observation(
    cycle: CycleResult,
    *,
    final_status: str,
    full_sha_history: list[str],
    max_round: int = MAX_ROUND,
) -> CycleResult:
    """Attach observational PASS/FAIL termination; never rollback source."""
    if final_status not in {"PASS", "FAIL"}:
        raise FixpointProtocolError(f"bad final_status: {final_status}")
    decision = judge_after_cycle(
        final_status=final_status,
        round_start_sha=cycle.round_start_sha,
        round_end_sha=cycle.round_end_sha,
        full_sha_history=full_sha_history,
        cycle_index=cycle.cycle_index,
        max_round=max_round,
        rule_trace=cycle.rule_trace,
    )
    cycle.final_status = final_status
    cycle.decision = decision
    return cycle


def apply_one_cycle(
    *,
    cell: Mapping[str, Any],
    source: str,
    cycle_index: int,
    full_sha_history: list[str],
    final_status: str,
    max_round: int = MAX_ROUND,
) -> CycleResult:
    """Apply stack once, then classify termination from observational status."""
    cycle = apply_stack_once(cell=cell, source=source, cycle_index=cycle_index)
    return finalize_cycle_observation(
        cycle,
        final_status=final_status,
        full_sha_history=full_sha_history,
        max_round=max_round,
    )


def apply_one_cycle_with_stub_stack(
    *,
    cell_id: str,
    source: str,
    cycle_index: int,
    full_sha_history: list[str],
    final_status: str,
    mutate: Callable[[str], str],
    rule_id: str = "STUB_RULE",
    max_round: int = MAX_ROUND,
) -> CycleResult:
    """Synthetic stack for focused termination tests (no frozen healer calls)."""
    round_start = source
    post = mutate(source)
    step = RuleStep(
        layer="stub",
        rule_id=rule_id,
        pre_sha=sha256_text(round_start),
        post_sha=sha256_text(post),
        eligible=post != round_start,
        modified=post != round_start,
        abstained=post == round_start,
    )
    decision = judge_after_cycle(
        final_status=final_status,
        round_start_sha=step.pre_sha,
        round_end_sha=step.post_sha,
        full_sha_history=full_sha_history,
        cycle_index=cycle_index,
        max_round=max_round,
        rule_trace=[step],
    )
    return CycleResult(
        cell_id=cell_id,
        cycle_index=cycle_index,
        round_start_source=round_start,
        round_end_source=post,
        round_start_sha=step.pre_sha,
        round_end_sha=step.post_sha,
        source_changed=post != round_start,
        rule_trace=[step],
        final_status=final_status,
        decision=decision,
    )


# ---------------------------------------------------------------------------
# Guards
# ---------------------------------------------------------------------------


def check_freeze_invariants() -> dict[str, Any]:
    protocol = load_json(PROTOCOL_MANIFEST)
    errors: list[str] = []
    if protocol["execution_model"]["max_round"] != MAX_ROUND:
        errors.append("max_round mismatch")
    if protocol["fixed_sequence"] != FIXED_SEQUENCE:
        errors.append("fixed_sequence mismatch")
    if protocol["layer_order"] != list(LAYER_ORDER):
        errors.append("layer_order mismatch")
    if list(TIER_B_RULE_ORDER) != list(TIER_B_EXPECTED_ORDER):
        errors.append("tier_b rule order drift")
    if MIN_SCORE != 8 or MIN_MARGIN != 2:
        errors.append("d5 threshold drift")
    if not RULE_ALLOWLIST:
        errors.append("tier_a allowlist empty")
    if protocol["population"]["fixpoint_active_n"] != EXPECTED_FAIL:
        errors.append("protocol active_n drift")
    if protocol["population"]["permanently_excluded_pass_n"] != EXPECTED_PASS:
        errors.append("protocol excluded_n drift")
    return {"ok": not errors, "errors": errors}


def check_resume_and_duplicate_guards(
    *, results_root: Path = RESULTS_ROOT, allow_resume: bool = False
) -> dict[str, Any]:
    """Refuse accidental overwrite / duplicate formal outputs unless resume opted in."""
    journal = results_root / CELL_JOURNAL_NAME
    final_journal = results_root / CELL_FINAL_JOURNAL_NAME
    summary = results_root / SUMMARY_NAME
    lock = results_root / RUN_LOCK_NAME
    existing = [p.name for p in (journal, final_journal, summary, lock) if p.exists()]
    if existing and not allow_resume:
        return {
            "ok": False,
            "errors": [
                "formal outputs already present; refuse duplicate run without allow_resume",
                f"existing={existing}",
            ],
            "existing": existing,
        }
    if allow_resume and lock.exists():
        return {
            "ok": False,
            "errors": ["formal_run.lock present; incomplete prior run — manual triage required"],
            "existing": existing,
        }
    return {"ok": True, "errors": [], "existing": existing}


def empty_aggregate_summary(*, formal_replay_executed: bool = False) -> dict[str, Any]:
    summary = {
        "protocol_id": "math16_qwen4b_cellwise_fixpoint_replay_protocol_v1",
        "model_group": MODEL_GROUP,
        "n_active_cells": EXPECTED_FAIL,
        "n_excluded_pass_cells": EXPECTED_PASS,
        "max_round": MAX_ROUND,
        "fixed_sequence": FIXED_SEQUENCE,
        "termination_counts": {k: 0 for k in TERMINATION_ENUM},
        "iterative_rescue_n": 0,
        "zero_change_n": 0,
        "cycle_detected_n": 0,
        "max_round_n": 0,
        "model_calls": 0,
        "formal_replay_executed": formal_replay_executed,
        "deterministic_second_cycle_probe": None,
    }
    missing = [k for k in AGGREGATE_SUMMARY_REQUIRED_FIELDS if k not in summary]
    if missing:
        raise FixpointProtocolError(f"summary missing: {missing}")
    return summary


def build_aggregate_summary(final_rows: list[Mapping[str, Any]]) -> dict[str, Any]:
    summary = empty_aggregate_summary(formal_replay_executed=True)
    counts = {k: 0 for k in TERMINATION_ENUM}
    for row in final_rows:
        reason = row.get("termination_reason")
        if reason not in counts:
            raise FixpointProtocolError(f"unknown termination: {reason}")
        counts[reason] += 1
    summary["termination_counts"] = counts
    summary["iterative_rescue_n"] = counts["ITERATIVE_RESCUE"]
    summary["zero_change_n"] = counts["ZERO_CHANGE_CONVERGENCE"]
    summary["cycle_detected_n"] = counts["CYCLE_DETECTED"]
    summary["max_round_n"] = counts["MAX_ROUND_NON_CONVERGENT"]
    if len(final_rows) != EXPECTED_FAIL:
        raise FixpointProtocolError(
            f"final rows {len(final_rows)} != active {EXPECTED_FAIL}"
        )
    return summary


# ---------------------------------------------------------------------------
# Preflight (zero-execution) and gated formal runner
# ---------------------------------------------------------------------------


def run_preflight(*, root: Path = ROOT, results_root: Path = RESULTS_ROOT) -> dict[str, Any]:
    """Zero-execution preflight: no healer application, no model, no formal replay."""
    errors: list[str] = []
    freeze = check_freeze_invariants()
    if not freeze["ok"]:
        errors.extend(freeze["errors"])

    population = load_round1_population(root=root)
    assert_pass_cells_excluded(population, population.active_ids)

    sha_mismatches = 0
    missing_sources = 0
    for cell in population.active_fail:
        path = root / cell.round1_final_source_path
        if not path.is_file():
            missing_sources += 1
            continue
        # Round 1 closures pin UTF-8 text digests (read_text), not raw CRLF bytes.
        digest = sha256_text(path.read_text(encoding="utf-8"))
        if digest != cell.round1_final_source_sha256:
            sha_mismatches += 1

    guards = check_resume_and_duplicate_guards(results_root=results_root, allow_resume=False)

    # Confirm D5/D2 overrides are in the active set and not among PASS exclusions.
    overrides = _override_map()
    for cid in overrides:
        if cid not in population.active_ids:
            errors.append(f"override cell not active: {cid}")
        if cid in population.excluded_ids:
            errors.append(f"override cell incorrectly excluded: {cid}")

    if missing_sources:
        errors.append(f"missing_sources={missing_sources}")
    if sha_mismatches:
        errors.append(f"sha_mismatches={sha_mismatches}")
    if not guards["ok"]:
        # Existing formal outputs are a soft note for preflight readiness, not a hard
        # block on protocol validity — surface separately.
        pass

    report = {
        "status": "PREFLIGHT_PASSED" if not errors else "PREFLIGHT_FAILED",
        "ok": not errors,
        "errors": errors,
        "model_calls": 0,
        "formal_replay_executed": False,
        "healer_cycles_executed": 0,
        "population": {
            "total": EXPECTED_TOTAL,
            "active_fail_n": len(population.active_fail),
            "excluded_pass_n": len(population.excluded_pass),
            "active_fail_locked": len(population.active_fail) == EXPECTED_FAIL,
            "excluded_pass_locked": len(population.excluded_pass) == EXPECTED_PASS,
            "disjoint": not population_ids_overlap(
                population.active_fail, population.excluded_pass
            ),
        },
        "sources": {
            "checked": len(population.active_fail),
            "missing": missing_sources,
            "sha_mismatches": sha_mismatches,
            "override_cells": sorted(overrides),
        },
        "freeze_checks": freeze,
        "resume_duplicate_guards": guards,
        "fixed_sequence": FIXED_SEQUENCE,
        "max_round": MAX_ROUND,
        "termination_enum": list(TERMINATION_ENUM),
        "journal_required_fields": list(CELL_JOURNAL_REQUIRED_FIELDS),
        "summary_required_fields": list(AGGREGATE_SUMMARY_REQUIRED_FIELDS),
        "results_root_reserved": str(results_root.relative_to(root)),
        "declarations": [
            "zero_execution_preflight",
            "no_formal_232_replay",
            "no_model_calls",
            "pass_88_never_scanned",
            "residual_fail_232_only",
        ],
    }
    return report


def run_formal_fixpoint_replay(
    *,
    allow_formal_execution: bool = False,
    evaluate_final_status: Optional[Callable[[str, Mapping[str, Any]], str]] = None,
    root: Path = ROOT,
    results_root: Path = RESULTS_ROOT,
) -> dict[str, Any]:
    """Formal 232-cell replay.

    Blocked unless ``allow_formal_execution=True``. Evaluator callback is
    observational only (PASS/FAIL classification) and must not mutate source.
    """
    if not allow_formal_execution:
        raise FormalExecutionBlocked(
            "formal 232-cell fixpoint replay is blocked this round "
            "(set allow_formal_execution=True only in an authorized execution round)"
        )
    if evaluate_final_status is None:
        raise FixpointProtocolError(
            "formal replay requires an observational evaluate_final_status callback"
        )

    pre = run_preflight(root=root, results_root=results_root)
    if not pre["ok"]:
        raise FixpointProtocolError(f"preflight failed: {pre['errors']}")
    guards = check_resume_and_duplicate_guards(results_root=results_root, allow_resume=False)
    if not guards["ok"]:
        raise FixpointProtocolError(f"duplicate/resume guard failed: {guards['errors']}")

    population = load_round1_population(root=root)
    results_root.mkdir(parents=True, exist_ok=True)
    lock = results_root / RUN_LOCK_NAME
    lock.write_text("running\n", encoding="utf-8")

    cycle_rows: list[dict[str, Any]] = []
    final_rows: list[dict[str, Any]] = []
    try:
        for cell in population.active_fail:
            assert_pass_cells_excluded(population, [cell.cell_id])
            source = read_round1_final_source(cell, root=root)
            history = [cell.round1_final_source_sha256]
            meta = cell.as_dict()
            termination = None
            rescue_cycle = None
            rescue_rule_id = None
            cycles_completed = 0
            for cycle_index in range(1, MAX_ROUND + 1):
                # Stack mutation is evaluator-blind. Observational PASS/FAIL is
                # applied only after the stack output is fixed (no rollback).
                cycle = apply_stack_once(
                    cell=meta, source=source, cycle_index=cycle_index
                )
                obs = evaluate_final_status(cycle.round_end_source, meta)
                if obs not in {"PASS", "FAIL"}:
                    raise FixpointProtocolError(f"bad observational status: {obs}")
                cycle = finalize_cycle_observation(
                    cycle,
                    final_status=obs,
                    full_sha_history=history,
                    max_round=MAX_ROUND,
                )
                decision = cycle.decision
                row = cycle.journal_row()
                cycle_rows.append(row)
                source = cycle.round_end_source
                history = list(decision["full_sha_history"])
                cycles_completed = cycle_index
                if not decision["continue"]:
                    termination = decision["termination_reason"]
                    rescue_cycle = decision["rescue_cycle"]
                    rescue_rule_id = decision["rescue_rule_id"]
                    break
            if termination is None:
                raise FixpointProtocolError(f"cell did not terminate: {cell.cell_id}")
            final_rows.append(
                {
                    "cell_id": cell.cell_id,
                    "round1_final_sha": cell.round1_final_source_sha256,
                    "final_sha": sha256_text(source),
                    "cycles_completed": cycles_completed,
                    "termination_reason": termination,
                    "rescue_cycle": rescue_cycle,
                    "rescue_rule_id": rescue_rule_id,
                    "full_sha_history": history,
                    "cycle_detected": termination == "CYCLE_DETECTED",
                    "max_round_reached": termination == "MAX_ROUND_NON_CONVERGENT",
                    "regression": False,
                }
            )
            for key in CELL_FINAL_REQUIRED_FIELDS:
                if key not in final_rows[-1]:
                    raise FixpointProtocolError(f"final journal missing {key}")

        summary = build_aggregate_summary(final_rows)
        (results_root / CELL_JOURNAL_NAME).write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in cycle_rows),
            encoding="utf-8",
            newline="\n",
        )
        (results_root / CELL_FINAL_JOURNAL_NAME).write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in final_rows),
            encoding="utf-8",
            newline="\n",
        )
        write_json(results_root / SUMMARY_NAME, summary)
    finally:
        if lock.exists():
            lock.unlink()

    return {
        "ok": True,
        "n_cells": len(final_rows),
        "summary": summary,
        "model_calls": 0,
    }
