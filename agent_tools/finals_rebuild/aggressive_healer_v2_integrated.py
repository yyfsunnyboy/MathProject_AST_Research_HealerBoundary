# -*- coding: utf-8 -*-
"""Aggressive Healer v2 — integrated stack.

Existing Aggressive Healer (unchanged semantics)
  A → B → C1 → C2 → D3 → D1 → D5 → D2
then Contract-Aware layer (frozen PC-R01–R04; answer/evaluator blind):
  AST parse gate → Contract load → PC-R01…R04 → Certificate verify → Static recheck

Does not modify PC rule modules, contracts, certificate schema, prompts, evaluators,
or formal cell artifacts.

Product safety (v2 integrated batch):
  raw_outcome == passed → identity preserve (do not run A–D or PC mutations).
  Residual FAIL/other → full integrated chain. Rules A–D semantics unchanged when applied.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from agent_tools.finals_rebuild.artifacts import sha256_text
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.ast_utils import is_parseable
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.contracts import load_contract
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.pipeline import (
    apply_contract_aware_v2,
)
from agent_tools.finals_rebuild.math16_qwen4b_cellwise_fixpoint_replay_v1 import (
    FIXED_SEQUENCE,
    MAX_ROUND as BASE_MAX_ROUND,
    apply_stack_once,
)

ROOT = Path(__file__).resolve().parents[2]
FORMAL_V2 = ROOT / "artifacts/math16_ab2d_menu_vs_full_runtime_contract_v2/formal"
ARTIFACT_ROOT = ROOT / "artifacts/math16_contract_aware_aggressive_healer_v2"
EXPECTED_FROZEN_SHA = "4b45ec08784146b567b01ae5f46d561d76cf10209df7b50f5eedd87d396853e5"

# Existing prefix is immutable string equality of FIXED_SEQUENCE.
EXISTING_PREFIX = FIXED_SEQUENCE  # "A→B→C1→C2→D3→D1→D5→D2"
INTEGRATED_SEQUENCE = (
    EXISTING_PREFIX
    + "→AST_PARSE_GATE→API_CONTRACT_CHECKER→PC-R01→PC-R02→PC-R03→PC-R04"
    + "→CERT_VERIFY→STATIC_RECHECK"
)
MAX_ROUND_V2 = BASE_MAX_ROUND  # 8

REQUIRED_CERT_FIELDS = (
    "rule_id",
    "decision",
    "contract_sha256",
    "candidate_count",
    "expected_answer_not_read",
    "evaluator_result_not_read",
    "candidate_trial_count",
    "before_source_sha256",
    "after_source_sha256",
)


@dataclass
class RoundRecord:
    round_index: int
    start_sha: str
    end_sha: str
    source_out: str
    source_changed: bool
    existing_stack_changed: bool
    existing_rules_fired: list[str]
    ast_parseable_at_pc_gate: bool
    pc_skipped: bool
    pc_rules_fired: list[str]
    pc_accept_count: int
    pc_abstain_count: int
    certificates: list[dict[str, Any]]
    abstain_reasons: list[str]
    cert_verify_ok: bool
    cert_verify_errors: list[str]
    static_recheck_ok: bool
    static_recheck_detail: str
    stop_reason: str = ""


@dataclass
class IntegratedCellResult:
    cell_id: str
    task_id: str
    condition: str
    model_key: str
    raw_outcome: str
    initial_sha: str
    final_sha: str
    source_modified: bool
    n_rounds: int
    stop_reason: str
    cycle_detected: bool
    max_round_hit: bool
    rounds: list[dict[str, Any]] = field(default_factory=list)
    total_pc_accepts: int = 0
    total_pc_abstains: int = 0
    pc_rules_fired_union: list[str] = field(default_factory=list)
    certificate_pass: bool = True
    formal_artifact_write: bool = False
    proposed_repair: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def verify_certificate(cert: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    for f in REQUIRED_CERT_FIELDS:
        if f not in cert:
            errs.append(f"missing_field:{f}")
    if cert.get("expected_answer_not_read") is not True:
        errs.append("expected_answer_read")
    if cert.get("evaluator_result_not_read") is not True:
        errs.append("evaluator_result_read")
    if cert.get("decision") == "ACCEPT":
        if cert.get("candidate_trial_count") != 1:
            errs.append("candidate_trial_count_not_1")
        if cert.get("candidate_count") != 1:
            errs.append("candidate_count_not_1")
    return errs


def apply_existing_stack(
    source: str,
    *,
    cell_id: str,
    task_id: str,
    condition: str,
    cycle_index: int = 1,
) -> tuple[str, list[str], bool]:
    """Run frozen A→B→C1→C2→D3→D1→D5→D2 once; semantics from apply_stack_once."""
    cell = {
        "cell_id": cell_id,
        "task_id": task_id,
        # Map V2 condition labels to closest historical keys for C1/C2/D5 matrices.
        # Does not change V2 condition identity stored on the result; only stack lookup.
        "condition": _stack_condition_alias(condition),
    }
    cycle = apply_stack_once(cell=cell, source=source, cycle_index=cycle_index)
    fired: list[str] = []
    for step in cycle.rule_trace:
        if getattr(step, "modified", False) and getattr(step, "rule_id", None):
            fired.append(str(step.rule_id))
    return cycle.round_end_source, fired, cycle.source_changed


def _stack_condition_alias(condition: str) -> str:
    """Historical contract matrix uses ab2d / ab1 / ab2g; V2 menu/full both map to ab2d."""
    if condition in {"ab2d_domain_menu_v2", "ab2d_full_v2", "ab2d_full", "ab2d_domain_menu"}:
        return "ab2d"
    return condition


def apply_pc_layer(
    source: str,
    *,
    task_id: str,
    condition: str,
    cell_id: str,
    model_key: str,
) -> dict[str, Any]:
    """AST gate then PC-R01..R04. Fail-closed if not parseable."""
    if not is_parseable(source):
        return {
            "source_out": source,
            "ast_parseable": False,
            "pc_skipped": True,
            "pc_rules_fired": [],
            "pc_accept_count": 0,
            "pc_abstain_count": 0,
            "certificates": [],
            "abstain_reasons": ["ast_parse_gate_failed"],
            "pipeline": None,
        }
    # Contract checker = load + allowlist presence (fail-closed on missing contract)
    try:
        contract = load_contract(task_id, condition)
    except Exception as exc:
        return {
            "source_out": source,
            "ast_parseable": True,
            "pc_skipped": True,
            "pc_rules_fired": [],
            "pc_accept_count": 0,
            "pc_abstain_count": 0,
            "certificates": [],
            "abstain_reasons": [f"contract_load_failed:{exc}"],
            "pipeline": None,
        }
    if not contract.get("allowed_methods"):
        return {
            "source_out": source,
            "ast_parseable": True,
            "pc_skipped": True,
            "pc_rules_fired": [],
            "pc_accept_count": 0,
            "pc_abstain_count": 0,
            "certificates": [],
            "abstain_reasons": ["contract_checker_empty_allowed_methods"],
            "pipeline": None,
        }

    pipe = apply_contract_aware_v2(
        source,
        task_id=task_id,
        condition=condition,
        cell_id=cell_id,
        model_key=model_key,
        contract=contract,
    )
    reasons = []
    for a in pipe.abstentions:
        if a.get("abstention_reason"):
            reasons.append(f"{a.get('rule_id')}:{a.get('abstention_reason')}")
    return {
        "source_out": pipe.source_out or source,
        "ast_parseable": True,
        "pc_skipped": False,
        "pc_rules_fired": list(pipe.rules_fired),
        "pc_accept_count": pipe.proposed_repair_count,
        "pc_abstain_count": len(pipe.abstentions),
        "certificates": list(pipe.certificates) + list(pipe.abstentions),
        "accept_certificates": list(pipe.certificates),
        "abstain_reasons": reasons,
        "pipeline": pipe,
    }


def static_recheck(
    source: str,
    *,
    task_id: str,
    condition: str,
    cell_id: str,
    model_key: str,
) -> tuple[bool, str]:
    """After PC layer: source must parse; a second pure PC pass must not further modify (idempotent)."""
    if not is_parseable(source):
        return False, "post_pc_not_parseable"
    pipe = apply_contract_aware_v2(
        source,
        task_id=task_id,
        condition=condition,
        cell_id=cell_id,
        model_key=model_key,
    )
    if pipe.source_modified:
        return False, f"pc_not_idempotent_rules={pipe.rules_fired}"
    return True, "idempotent_ok"


def apply_aggressive_healer_v2_once(
    source: str,
    *,
    cell_id: str,
    task_id: str,
    condition: str,
    model_key: str = "",
    cycle_index: int = 1,
) -> RoundRecord:
    """One integrated round: existing stack → PC layer → cert verify → recheck."""
    start_sha = sha256_text(source)
    post_stack, existing_fired, stack_changed = apply_existing_stack(
        source,
        cell_id=cell_id,
        task_id=task_id,
        condition=condition,
        cycle_index=cycle_index,
    )
    pc = apply_pc_layer(
        post_stack,
        task_id=task_id,
        condition=condition,
        cell_id=cell_id,
        model_key=model_key,
    )
    final = pc["source_out"]
    cert_errors: list[str] = []
    for cert in pc.get("accept_certificates") or []:
        cert_errors.extend(verify_certificate(cert))
    cert_ok = len(cert_errors) == 0
    # When PC layer is skipped (unparseable / no contract), certificate + static
    # recheck are N/A success (no ACCEPT path, no post-PC invariant to enforce).
    if pc["pc_skipped"]:
        recheck_ok, recheck_detail = True, "pc_skipped_na"
    else:
        recheck_ok, recheck_detail = static_recheck(
            final,
            task_id=task_id,
            condition=condition,
            cell_id=cell_id,
            model_key=model_key,
        )
    end_sha = sha256_text(final)
    return RoundRecord(
        round_index=cycle_index,
        start_sha=start_sha,
        end_sha=end_sha,
        source_out=final,
        source_changed=end_sha != start_sha,
        existing_stack_changed=stack_changed,
        existing_rules_fired=existing_fired,
        ast_parseable_at_pc_gate=bool(pc["ast_parseable"]),
        pc_skipped=bool(pc["pc_skipped"]),
        pc_rules_fired=list(pc["pc_rules_fired"]),
        pc_accept_count=int(pc["pc_accept_count"]),
        pc_abstain_count=int(pc["pc_abstain_count"]),
        certificates=list(pc.get("accept_certificates") or []),
        abstain_reasons=list(pc.get("abstain_reasons") or []),
        cert_verify_ok=cert_ok,
        cert_verify_errors=cert_errors,
        static_recheck_ok=recheck_ok,
        static_recheck_detail=recheck_detail,
    )


def _pass_identity_result(
    source: str,
    *,
    cell_id: str,
    task_id: str,
    condition: str,
    model_key: str,
    raw_outcome: str,
) -> IntegratedCellResult:
    """Safety: raw PASS never enters A–D or PC mutation."""
    sha = sha256_text(source)
    rec = RoundRecord(
        round_index=0,
        start_sha=sha,
        end_sha=sha,
        source_out=source,
        source_changed=False,
        existing_stack_changed=False,
        existing_rules_fired=[],
        ast_parseable_at_pc_gate=is_parseable(source),
        pc_skipped=True,
        pc_rules_fired=[],
        pc_accept_count=0,
        pc_abstain_count=0,
        certificates=[],
        abstain_reasons=["raw_pass_identity_preserve"],
        cert_verify_ok=True,
        cert_verify_errors=[],
        static_recheck_ok=True,
        static_recheck_detail="pass_identity_na",
        stop_reason="PASS_IDENTITY_PRESERVE",
    )
    return IntegratedCellResult(
        cell_id=cell_id,
        task_id=task_id,
        condition=condition,
        model_key=model_key,
        raw_outcome=raw_outcome,
        initial_sha=sha,
        final_sha=sha,
        source_modified=False,
        n_rounds=0,
        stop_reason="PASS_IDENTITY_PRESERVE",
        cycle_detected=False,
        max_round_hit=False,
        rounds=[asdict(rec)],
        total_pc_accepts=0,
        total_pc_abstains=0,
        pc_rules_fired_union=[],
        certificate_pass=True,
        formal_artifact_write=False,
        proposed_repair=0,
    )


def run_fixpoint_v2(
    source: str,
    *,
    cell_id: str,
    task_id: str,
    condition: str,
    model_key: str = "",
    max_round: int = MAX_ROUND_V2,
    raw_outcome: str = "",
    identity_on_raw_pass: bool = True,
) -> IntegratedCellResult:
    """Evaluator-blind fixpoint: stop on no-change / SHA cycle / max-round."""
    if identity_on_raw_pass and raw_outcome == "passed":
        return _pass_identity_result(
            source,
            cell_id=cell_id,
            task_id=task_id,
            condition=condition,
            model_key=model_key,
            raw_outcome=raw_outcome,
        )

    initial_sha = sha256_text(source)
    sha_history = [initial_sha]
    current = source
    rounds: list[RoundRecord] = []
    stop_reason = "MAX_ROUND_NON_CONVERGENT"
    cycle_detected = False
    max_hit = False
    all_pc_accepts = 0
    all_pc_abstains = 0
    fired_union: list[str] = []
    cert_pass = True

    for r in range(1, max_round + 1):
        rec = apply_aggressive_healer_v2_once(
            current,
            cell_id=cell_id,
            task_id=task_id,
            condition=condition,
            model_key=model_key,
            cycle_index=r,
        )
        rounds.append(rec)
        all_pc_accepts += rec.pc_accept_count
        all_pc_abstains += rec.pc_abstain_count
        for rid in rec.pc_rules_fired:
            if rid not in fired_union:
                fired_union.append(rid)
        if not rec.cert_verify_ok or not rec.static_recheck_ok:
            cert_pass = False

        current = rec.source_out
        end_sha = rec.end_sha

        if not rec.source_changed:
            stop_reason = "FIXPOINT_NO_CHANGE"
            break
        if end_sha in sha_history:
            stop_reason = "SHA_CYCLE"
            cycle_detected = True
            break
        sha_history.append(end_sha)
        if r == max_round:
            stop_reason = "MAX_ROUND_NON_CONVERGENT"
            max_hit = True
    else:
        max_hit = True
        stop_reason = "MAX_ROUND_NON_CONVERGENT"

    return IntegratedCellResult(
        cell_id=cell_id,
        task_id=task_id,
        condition=condition,
        model_key=model_key,
        raw_outcome=raw_outcome,
        initial_sha=initial_sha,
        final_sha=sha256_text(current),
        source_modified=sha256_text(current) != initial_sha,
        n_rounds=len(rounds),
        stop_reason=stop_reason,
        cycle_detected=cycle_detected,
        max_round_hit=max_hit,
        rounds=[asdict(r) for r in rounds],
        total_pc_accepts=all_pc_accepts,
        total_pc_abstains=all_pc_abstains,
        pc_rules_fired_union=fired_union,
        certificate_pass=cert_pass,
        formal_artifact_write=False,
        proposed_repair=all_pc_accepts,
    )


def ensure_existing_prefix_unchanged() -> None:
    if FIXED_SEQUENCE != "A→B→C1→C2→D3→D1→D5→D2":
        raise RuntimeError(f"FIXED_SEQUENCE drifted: {FIXED_SEQUENCE}")
    if not INTEGRATED_SEQUENCE.startswith(EXISTING_PREFIX + "→"):
        raise RuntimeError("INTEGRATED_SEQUENCE must start with existing prefix")


def run_integrated_dry_run_480(*, write: bool = True) -> dict[str, Any]:
    ensure_existing_prefix_unchanged()
    out_root = ARTIFACT_ROOT / "integrated_dry_run"
    if write:
        out_root.mkdir(parents=True, exist_ok=True)

    # Frozen integrity
    frozen_path = ARTIFACT_ROOT / "frozen_manifest/frozen_manifest_v2_0_0.json"
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    frozen_ok = frozen.get("frozen_manifest_sha256") == EXPECTED_FROZEN_SHA

    cells: list[dict[str, Any]] = []
    for p in FORMAL_V2.rglob("artifact.json"):
        art = json.loads(p.read_text(encoding="utf-8"))
        src_p = p.parent / "extracted_source.py"
        if not src_p.exists():
            continue
        cells.append(
            {
                "cell_id": art["cell_id"],
                "task_id": art["task_id"],
                "condition": art["condition"],
                "model_key": art["model_key"],
                "outcome": art.get("outcome"),
                "source": src_p.read_text(encoding="utf-8", errors="replace"),
                "dir": str(p.parent),
            }
        )
    cells.sort(key=lambda x: x["cell_id"])

    results: list[IntegratedCellResult] = []
    known6 = {
        "qwen_4b__ce111_q02_polynomial_division_remainder__ab2d_full_v2__seed_2026071301": "PC-R01_ANSWER_SOURCE_REWIRE_V2",
        "qwen_4b__ce111_q02_polynomial_division_remainder__ab2d_full_v2__seed_2026072001": "PC-R01_ANSWER_SOURCE_REWIRE_V2",
        "qwen_4b__ce112_q04_radical_simplification__ab2d_full_v2__seed_2026072004": "PC-R03_DOMAIN_API_NORMALIZE_V2",
        "qwen_4b__ce115_calc_exact_rational_expression_l1__ab2d_full_v2__seed_2026072003": "PC-R02_OPERAND_ORDER_RESTORE_V2",
        "qwen_4b__ce115_calc_exact_rational_expression_l1__ab2d_full_v2__seed_2026072004": "PC-R02_OPERAND_ORDER_RESTORE_V2",
        "qwen_4b__ce111_q02_polynomial_division_remainder__ab2d_domain_menu_v2__seed_2026072002": "PC-R01_ANSWER_SOURCE_REWIRE_V2",
    }
    known6_match: dict[str, Any] = {}

    for row in cells:
        res = run_fixpoint_v2(
            row["source"],
            cell_id=row["cell_id"],
            task_id=row["task_id"],
            condition=row["condition"],
            model_key=row["model_key"],
            raw_outcome=row["outcome"] or "",
            identity_on_raw_pass=True,
        )
        results.append(res)
        if row["cell_id"] in known6:
            expected = known6[row["cell_id"]]
            got = res.pc_rules_fired_union
            known6_match[row["cell_id"]] = {
                "expected_rule": expected,
                "got_rules": got,
                "accept_count": res.total_pc_accepts,
                "match": expected in got and res.total_pc_accepts >= 1,
            }

    # Aggregates
    n = len(results)
    changed = sum(1 for r in results if r.source_modified)
    unchanged = n - changed
    pass_rows = [r for r in results if r.raw_outcome == "passed"]
    pass_mod = sum(1 for r in pass_rows if r.source_modified)
    pass_pc_accept = sum(1 for r in pass_rows if r.total_pc_accepts > 0)
    pass_proposed = sum(int(r.proposed_repair) for r in pass_rows)
    pass_cert_accept = sum(
        1
        for r in pass_rows
        for rnd in r.rounds
        for c in (rnd.get("certificates") or [])
        if c.get("decision") == "ACCEPT"
    )

    stop_counts: dict[str, int] = {}
    for r in results:
        stop_counts[r.stop_reason] = stop_counts.get(r.stop_reason, 0) + 1
    cycle_n = sum(1 for r in results if r.cycle_detected)
    max_n = sum(1 for r in results if r.max_round_hit)
    cert_fail = sum(1 for r in results if not r.certificate_pass)
    cert_pass_n = n - cert_fail
    total_pc_accepts = sum(r.total_pc_accepts for r in results)
    total_pc_abstains = sum(r.total_pc_abstains for r in results)
    total_rounds = sum(r.n_rounds for r in results)

    rule_trigger: dict[str, int] = {}
    rule_accept: dict[str, int] = {}
    existing_rule_trigger: dict[str, int] = {}
    for r in results:
        for rid in r.pc_rules_fired_union:
            rule_trigger[rid] = rule_trigger.get(rid, 0) + 1
        for rnd in r.rounds:
            for rid in rnd.get("pc_rules_fired") or []:
                rule_accept[rid] = rule_accept.get(rid, 0) + 1
            for rid in rnd.get("existing_rules_fired") or []:
                existing_rule_trigger[rid] = existing_rule_trigger.get(rid, 0) + 1

    by_model: dict[str, dict[str, int]] = {}
    by_cond: dict[str, dict[str, int]] = {}
    by_rule_ledger: dict[str, dict[str, int]] = {}
    for r in results:
        by_model.setdefault(r.model_key, {"changed": 0, "unchanged": 0, "n": 0})
        by_model[r.model_key]["n"] += 1
        by_model[r.model_key]["changed" if r.source_modified else "unchanged"] += 1
        by_cond.setdefault(r.condition, {"changed": 0, "unchanged": 0, "n": 0})
        by_cond[r.condition]["n"] += 1
        by_cond[r.condition]["changed" if r.source_modified else "unchanged"] += 1
        for rid in r.pc_rules_fired_union:
            by_rule_ledger.setdefault(rid, {"cells": 0, "accepts": 0})
            by_rule_ledger[rid]["cells"] += 1
            by_rule_ledger[rid]["accepts"] += r.total_pc_accepts

    known6_ok = all(v.get("match") for v in known6_match.values()) and len(known6_match) == 6
    r01 = sum(1 for v in known6_match.values() if "PC-R01" in v.get("expected_rule", "") and v.get("match"))
    r02 = sum(1 for v in known6_match.values() if "PC-R02" in v.get("expected_rule", "") and v.get("match"))
    r03 = sum(1 for v in known6_match.values() if "PC-R03" in v.get("expected_rule", "") and v.get("match"))
    r04 = sum(1 for v in known6_match.values() if "PC-R04" in v.get("expected_rule", "") and v.get("match"))

    summary = {
        "integrated_sequence": INTEGRATED_SEQUENCE,
        "existing_prefix": EXISTING_PREFIX,
        "existing_prefix_ok": EXISTING_PREFIX == "A→B→C1→C2→D3→D1→D5→D2",
        "frozen_manifest_sha_ok": frozen_ok,
        "frozen_manifest_sha": EXPECTED_FROZEN_SHA,
        "identity_on_raw_pass": True,
        "n_cells": n,
        "changed": changed,
        "unchanged": unchanged,
        "pass_cells": len(pass_rows),
        "pass_source_modification": pass_mod,
        "pass_proposed_repair": pass_proposed,
        "pass_pc_accept": pass_pc_accept,
        "pass_certificate_accept": pass_cert_accept,
        "stop_reason_counts": stop_counts,
        "fixpoint_rounds_total": total_rounds,
        "cycle_n": cycle_n,
        "max_round_n": max_n,
        "certificate_pass": cert_pass_n,
        "certificate_fail": cert_fail,
        "total_pc_accepts": total_pc_accepts,
        "total_pc_abstains": total_pc_abstains,
        "pc_rule_accept_counts": rule_accept,
        "pc_rule_trigger_cell_counts": rule_trigger,
        "existing_rule_trigger_counts": existing_rule_trigger,
        "by_model": by_model,
        "by_condition": by_cond,
        "by_rule": by_rule_ledger,
        "known6_match": known6_match,
        "known6_all_match": known6_ok,
        "known6_pc_counts": {"PC-R01": r01, "PC-R02": r02, "PC-R03": r03, "PC-R04": r04},
        "formal_artifact_write": False,
        "llm_calls": 0,
        "evaluator_calls": 0,
    }

    # Safety gate: 381 raw PASS — zero source mod / proposed repair / certificate ACCEPT
    summary["safety_pass"] = (
        pass_mod == 0
        and pass_proposed == 0
        and pass_pc_accept == 0
        and pass_cert_accept == 0
        and len(pass_rows) == 381
    )
    summary["ready"] = (
        summary["safety_pass"]
        and known6_ok
        and frozen_ok
        and n == 480
        and summary["existing_prefix_ok"]
        and cert_fail == 0
        and r01 == 3
        and r02 == 2
        and r03 == 1
        and r04 == 0
    )

    if write:
        (out_root / "summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        # Lightweight per-cell index (no full sources)
        index = [r.to_dict() for r in results]
        (out_root / "cell_results.json").write_text(
            json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        # known6 detail
        (out_root / "known6.json").write_text(
            json.dumps(known6_match, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    return summary
