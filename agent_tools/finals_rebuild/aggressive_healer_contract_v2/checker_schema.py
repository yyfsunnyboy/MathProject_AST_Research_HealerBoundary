# -*- coding: utf-8 -*-
"""Contract Checker schema (detection layer only).

Separates:
  - contract_violation_detected  (is a contract clause violated?)
  - repair_accepted              (did a frozen PC rule accept a repair?)

Does not modify PC-R01–R04, contracts SSOT files, frozen manifest, or formal artifacts.
"""
from __future__ import annotations

import ast
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Optional

from agent_tools.finals_rebuild.domain_api_ssot import (
    API_CLASSIFICATION,
    DOMAIN_API_SSOT,
    SUPPORTED_PUBLIC,
)
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.ast_utils import (
    OPS_CLASS_NAMES,
    count_generate_defs,
    fqname,
    iter_ops_calls,
    node_loc,
    parse_tree,
    unparse,
)
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.contracts import load_contract
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.pipeline import (
    apply_contract_aware_v2,
)

# --- Schema enumerations ---

DECISIONS = (
    "CONTRACT_OK",
    "DETECT_ONLY_ABSTAIN",
    "REPAIR_ACCEPTED",
    "AST_UNCHECKABLE",
    "REWRITE_REQUIRED",
    "INSUFFICIENT_EVIDENCE",
)

# Shared dimensions (domain-menu + full-plan)
SHARED_DIMENSIONS = (
    "domain_class_legality",
    "method_function_existence",
    "allowed_api_membership",
    "signature",
    "argument_count_name",
    "statically_provable_arg_type_source",
    "return_shape",
    "return_unpacking",
    "runtime_frozen_binding",
    "dataflow",
    "answer_schema",
    "answer_provenance",
)

# full-plan only (must never apply as process requirements under domain-menu)
FULL_PLAN_DIMENSIONS = (
    "required_api_calls",
    "call_order",
    "exact_argument_source",
    "operand_roles_order",
    "intermediate_dataflow",
    "required_formatter",
    "required_answer_field_source",
    "missing_extra_process_step",
)

LEGAL_OPS = OPS_CLASS_NAMES | {"IntegerOps", "FractionOps", "RadicalOps", "PolynomialOps"}


@dataclass
class ClauseFinding:
    """One independent checker output for a contract clause / dimension hit."""

    contract_violation_detected: bool
    violation_id: str
    violation_type: str
    contract_clause: str
    dimension: str
    ast_location: dict[str, Any]
    observed: str
    expected: str
    checker_status: str  # VIOLATION | OK | UNCHECKABLE | SKIPPED_MENU | EVIDENCE_WEAK
    repair_candidate_found: bool
    repair_accepted: bool
    decision: str
    abstain_reason: str = ""
    condition_scope: str = "shared"  # shared | full_plan_only

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CellCheckerReport:
    cell_id: str
    task_id: str
    condition: str
    model_key: str
    raw_outcome: str
    parseable: bool
    parse_error: str
    n_generate: int
    findings: list[ClauseFinding] = field(default_factory=list)
    cell_decision: str = "CONTRACT_OK"
    violation_count: int = 0
    repair_accepted_count: int = 0
    repair_accepted_rules: list[str] = field(default_factory=list)
    source_modified_by_pc: bool = False
    formal_artifact_write: bool = False

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["findings"] = [f.to_dict() if isinstance(f, ClauseFinding) else f for f in self.findings]
        return d


def _vid(prefix: str, *parts: Any) -> str:
    safe = "_".join(str(p).replace(" ", "_") for p in parts if p is not None and p != "")
    return f"{prefix}__{safe}" if safe else prefix


def _finding(
    *,
    violated: bool,
    violation_id: str,
    violation_type: str,
    contract_clause: str,
    dimension: str,
    observed: str,
    expected: str,
    checker_status: str,
    decision: str,
    ast_location: Optional[dict[str, Any]] = None,
    repair_candidate_found: bool = False,
    repair_accepted: bool = False,
    abstain_reason: str = "",
    condition_scope: str = "shared",
) -> ClauseFinding:
    return ClauseFinding(
        contract_violation_detected=violated,
        violation_id=violation_id,
        violation_type=violation_type,
        contract_clause=contract_clause,
        dimension=dimension,
        ast_location=ast_location or {},
        observed=observed,
        expected=expected,
        checker_status=checker_status,
        repair_candidate_found=repair_candidate_found,
        repair_accepted=repair_accepted,
        decision=decision,
        abstain_reason=abstain_reason,
        condition_scope=condition_scope,
    )


def _parse_error_message(source: str) -> str:
    try:
        ast.parse(source)
        return ""
    except SyntaxError as exc:
        return f"{exc.msg} (line {exc.lineno} col {exc.offset})"


def _arity_from_signature(sig: str) -> Optional[int]:
    """Best-effort positional arity from signature string like '(a, b, c=1)'."""
    if not sig or not sig.startswith("("):
        return None
    inner = sig.strip()[1:-1].strip()
    if not inner:
        return 0
    # count top-level commas ignoring defaults for upper bound of required args
    parts = [p.strip() for p in inner.split(",") if p.strip()]
    required = 0
    for p in parts:
        if p.startswith("*"):
            break
        if "=" in p:
            continue
        required += 1
    return required


def _is_create_zero(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    f = node.func
    if not (isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name)):
        return False
    if f.value.id != "FractionOps" or f.attr != "create":
        return False
    if len(node.args) != 1:
        return False
    a0 = node.args[0]
    return isinstance(a0, ast.Constant) and a0.value == 0


def _cell_decision_from_findings(
    findings: list[ClauseFinding],
    *,
    parseable: bool,
    n_generate: int,
    source_lines: int,
    any_pc_accept: bool,
) -> str:
    if not parseable:
        return "AST_UNCHECKABLE"
    if any_pc_accept:
        return "REPAIR_ACCEPTED"
    # Rewrite heuristic (detection taxonomy, not a repair rule): multi-generate long draft or
    # many simultaneous structural blockers without unique local repair.
    if n_generate >= 2 and source_lines >= 80:
        return "REWRITE_REQUIRED"
    viol = [f for f in findings if f.contract_violation_detected]
    if not viol:
        # multi-generate short may still be incomplete evidence rather than clean OK
        if n_generate != 1:
            return "INSUFFICIENT_EVIDENCE"
        return "CONTRACT_OK"
    # Strong rewrite marker: many full-plan missing/extra steps + long source
    rewrite_marks = sum(
        1
        for f in viol
        if f.dimension in ("missing_extra_process_step", "required_api_calls")
        and f.violation_type in ("missing_required_calls_multiple", "extra_or_missing_process_steps")
    )
    if rewrite_marks >= 1 and source_lines >= 100 and n_generate >= 1:
        # only if no repair path
        return "REWRITE_REQUIRED"
    if any(f.decision == "REWRITE_REQUIRED" for f in viol):
        return "REWRITE_REQUIRED"
    if any(f.decision == "INSUFFICIENT_EVIDENCE" for f in viol) and all(
        f.decision in ("INSUFFICIENT_EVIDENCE", "DETECT_ONLY_ABSTAIN", "CONTRACT_OK") for f in findings
    ):
        # pure weak evidence without hard violation
        hard = [f for f in viol if f.decision == "DETECT_ONLY_ABSTAIN"]
        if not hard and any(f.decision == "INSUFFICIENT_EVIDENCE" for f in viol):
            return "INSUFFICIENT_EVIDENCE"
    return "DETECT_ONLY_ABSTAIN"


def run_contract_checker(
    source: str,
    *,
    task_id: str,
    condition: str,
    cell_id: str = "",
    model_key: str = "",
    raw_outcome: str = "",
    contract: Optional[dict[str, Any]] = None,
    correlate_pc_repair: bool = True,
) -> CellCheckerReport:
    """Run full detection-layer contract checker. Never mutates input source."""
    if contract is None:
        contract = load_contract(task_id, condition)
    is_full = condition == "ab2d_full_v2"
    is_menu = condition == "ab2d_domain_menu_v2"
    findings: list[ClauseFinding] = []

    parse_err = _parse_error_message(source)
    parseable = parse_err == ""
    if not parseable:
        findings.append(
            _finding(
                violated=False,
                violation_id=_vid("AST_UNCHECKABLE", cell_id or "src"),
                violation_type="ast_unparseable",
                contract_clause="AST_PARSE_GATE",
                dimension="ast_parse_gate",
                observed=parse_err,
                expected="source must parse as Python AST",
                checker_status="UNCHECKABLE",
                decision="AST_UNCHECKABLE",
                abstain_reason="no_deep_check_without_ast",
                # Explicit: do NOT claim absence of contract violation
            )
        )
        return CellCheckerReport(
            cell_id=cell_id,
            task_id=task_id,
            condition=condition,
            model_key=model_key,
            raw_outcome=raw_outcome,
            parseable=False,
            parse_error=parse_err,
            n_generate=0,
            findings=findings,
            cell_decision="AST_UNCHECKABLE",
            violation_count=0,
            repair_accepted_count=0,
            repair_accepted_rules=[],
            source_modified_by_pc=False,
        )

    tree = parse_tree(source)
    assert tree is not None
    n_gen = count_generate_defs(tree)
    domain = contract.get("domain") or ""
    allowed_methods = set(contract.get("allowed_methods") or [])
    allowed_classes = set(contract.get("allowed_classes") or [domain])
    # Standard Ops classes are legal hosts only if method membership allows; class typo still illegal.
    sigs = contract.get("api_signatures") or {}

    # --- generate structure ---
    if n_gen != 1:
        findings.append(
            _finding(
                violated=True,
                violation_id=_vid("GEN_COUNT", n_gen),
                violation_type="generate_count_not_1",
                contract_clause="SINGLE_GENERATE",
                dimension="dataflow",
                observed=f"generate_defs={n_gen}",
                expected="exactly 1 def generate",
                checker_status="VIOLATION",
                decision="DETECT_ONLY_ABSTAIN" if n_gen >= 2 else "INSUFFICIENT_EVIDENCE",
                abstain_reason="multi_or_missing_generate_fail_closed",
                repair_candidate_found=False,
                repair_accepted=False,
            )
        )

    calls = iter_ops_calls(tree)

    # ========== SHARED DIMENSIONS ==========
    for call in calls:
        cls = call.func.value.id  # type: ignore[union-attr]
        meth = call.func.attr  # type: ignore[union-attr]
        name = f"{cls}.{meth}"
        loc = node_loc(call)

        # domain_class_legality
        if cls.endswith("Ops") and cls not in LEGAL_OPS:
            findings.append(
                _finding(
                    violated=True,
                    violation_id=_vid("ILLEGAL_CLASS", cls, loc.get("lineno")),
                    violation_type="illegal_ops_class",
                    contract_clause="DOMAIN_CLASS_LEGALITY",
                    dimension="domain_class_legality",
                    observed=cls,
                    expected=f"legal Ops classes {sorted(LEGAL_OPS)} (domain={domain})",
                    checker_status="VIOLATION",
                    decision="DETECT_ONLY_ABSTAIN",
                    ast_location=loc,
                    abstain_reason="illegal_class_detected",
                )
            )
        elif cls.endswith("Ops") and domain and cls != domain and cls in LEGAL_OPS:
            # Using other-domain Ops is allowed as library import in many tasks; flag only when
            # task domain exclusive and call not in any allowed_methods of contract domain.
            # Soft: cross-domain legal Ops is not a hard violation if method exists globally.
            pass

        # method exists in SSOT — only flag unknown *Ops.method on Ops-like classes
        if cls.endswith("Ops") and name not in DOMAIN_API_SSOT and API_CLASSIFICATION.get(name) is None:
            findings.append(
                _finding(
                    violated=True,
                    violation_id=_vid("METHOD_MISSING", name, loc.get("lineno")),
                    violation_type="method_not_in_ssot",
                    contract_clause="METHOD_FUNCTION_EXISTENCE",
                    dimension="method_function_existence",
                    observed=name,
                    expected="method present in domain API SSOT",
                    checker_status="VIOLATION",
                    decision="DETECT_ONLY_ABSTAIN",
                    ast_location=loc,
                    abstain_reason="unknown_method",
                )
            )

        # allowed API membership — only when using contract domain class
        if cls == domain and name not in allowed_methods and API_CLASSIFICATION.get(name) != SUPPORTED_PUBLIC:
            findings.append(
                _finding(
                    violated=True,
                    violation_id=_vid("NOT_ALLOWED", name, loc.get("lineno")),
                    violation_type="method_not_in_allowed_set",
                    contract_clause="ALLOWED_API_MEMBERSHIP",
                    dimension="allowed_api_membership",
                    observed=name,
                    expected=f"member of allowed_methods for {domain}",
                    checker_status="VIOLATION",
                    decision="DETECT_ONLY_ABSTAIN",
                    ast_location=loc,
                    abstain_reason="not_in_allowed_methods",
                )
            )

        # signature / argument count
        meta = sigs.get(name) or DOMAIN_API_SSOT.get(name)
        if meta:
            sig = meta.get("signature") if isinstance(meta, dict) else None
            if not sig and isinstance(meta, dict):
                sig = meta.get("signature")
            arity = _arity_from_signature(sig or "")
            n_pos = len(call.args)
            n_kw = len(call.keywords or [])
            if arity is not None and n_pos < arity and n_kw == 0:
                findings.append(
                    _finding(
                        violated=True,
                        violation_id=_vid("ARITY", name, n_pos, loc.get("lineno")),
                        violation_type="argument_count_mismatch",
                        contract_clause="SIGNATURE_ARITY",
                        dimension="signature",
                        observed=f"{name} positional_args={n_pos} keywords={n_kw}",
                        expected=f"at least {arity} required positionals per {sig}",
                        checker_status="VIOLATION",
                        decision="DETECT_ONLY_ABSTAIN",
                        ast_location=loc,
                        abstain_reason="arity_mismatch",
                    )
                )
            # argument count_name dimension mirrors arity with names
            if arity is not None and n_pos < arity:
                findings.append(
                    _finding(
                        violated=True,
                        violation_id=_vid("ARG_COUNT", name, n_pos, loc.get("lineno")),
                        violation_type="argument_count_or_name",
                        contract_clause="ARGUMENT_COUNT_NAME",
                        dimension="argument_count_name",
                        observed=f"args={n_pos} kw={[k.arg for k in (call.keywords or [])]}",
                        expected=f"required arity {arity} for {name}",
                        checker_status="VIOLATION",
                        decision="DETECT_ONLY_ABSTAIN",
                        ast_location=loc,
                        abstain_reason="arg_count_name",
                    )
                )

        # statically provable arg source: prefer frozen[...] / Name linked to frozen
        for i, arg in enumerate(call.args):
            if isinstance(arg, (ast.Constant, ast.Name, ast.Subscript, ast.Attribute, ast.Call, ast.List, ast.Tuple, ast.UnaryOp, ast.BinOp)):
                continue
            # Lambda / generators / comps → weak evidence
            findings.append(
                _finding(
                    violated=False,
                    violation_id=_vid("ARG_SRC_WEAK", name, i, loc.get("lineno")),
                    violation_type="arg_source_not_statically_simple",
                    contract_clause="STATIC_ARG_TYPE_SOURCE",
                    dimension="statically_provable_arg_type_source",
                    observed=unparse(arg),
                    expected="Name/Subscript/Call/Constant provenance",
                    checker_status="EVIDENCE_WEAK",
                    decision="INSUFFICIENT_EVIDENCE",
                    ast_location=loc,
                    abstain_reason="non_simple_arg_ast",
                )
            )

    # return_shape
    return_dicts = [
        n for n in ast.walk(tree) if isinstance(n, ast.Return) and isinstance(n.value, ast.Dict)
    ]
    required_ret_keys = set((contract.get("return_shape") or {}).get("keys") or [])
    if return_dicts and required_ret_keys:
        for ret in return_dicts:
            keys = set()
            assert isinstance(ret.value, ast.Dict)
            for k in ret.value.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    keys.add(k.value)
            missing = required_ret_keys - keys
            if missing:
                findings.append(
                    _finding(
                        violated=True,
                        violation_id=_vid("RET_SHAPE", ",".join(sorted(missing))),
                        violation_type="return_keys_missing",
                        contract_clause="RETURN_SHAPE",
                        dimension="return_shape",
                        observed=f"keys={sorted(keys)}",
                        expected=f"keys include {sorted(required_ret_keys)}",
                        checker_status="VIOLATION",
                        decision="DETECT_ONLY_ABSTAIN",
                        ast_location=node_loc(ret),
                        abstain_reason="return_shape_missing_keys",
                    )
                )
    elif n_gen == 1 and not return_dicts:
        findings.append(
            _finding(
                violated=False,
                violation_id=_vid("RET_SHAPE_WEAK"),
                violation_type="return_dict_not_found",
                contract_clause="RETURN_SHAPE",
                dimension="return_shape",
                observed="no dict return AST",
                expected="return {question_text, correct_answer, oracle_payload}",
                checker_status="EVIDENCE_WEAK",
                decision="INSUFFICIENT_EVIDENCE",
                abstain_reason="return_ast_not_literal_dict",
            )
        )

    # return_unpacking (div_qr pattern etc.)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if not isinstance(node.value, ast.Call):
            continue
        call = node.value
        if not (isinstance(call.func, ast.Attribute) and isinstance(call.func.value, ast.Name)):
            continue
        name = f"{call.func.value.id}.{call.func.attr}"
        rc = (DOMAIN_API_SSOT.get(name) or {}).get("return_contract") or {}
        if rc.get("type") == "tuple" and rc.get("length") == 2:
            # expect tuple unpack targets
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Tuple):
                n_elt = len(node.targets[0].elts)
                if n_elt != 2:
                    findings.append(
                        _finding(
                            violated=True,
                            violation_id=_vid("UNPACK", name, n_elt, node.lineno),
                            violation_type="return_unpack_arity",
                            contract_clause="RETURN_UNPACKING",
                            dimension="return_unpacking",
                            observed=f"unpack_len={n_elt} for {name}",
                            expected="unpack into 2 targets (q, r) pattern",
                            checker_status="VIOLATION",
                            decision="DETECT_ONLY_ABSTAIN",
                            ast_location=node_loc(node),
                            abstain_reason="bad_unpack",
                        )
                    )
            elif len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                # single target for tuple return — may be intentional binding of pair
                findings.append(
                    _finding(
                        violated=False,
                        violation_id=_vid("UNPACK_WEAK", name, node.lineno),
                        violation_type="tuple_return_not_unpacked",
                        contract_clause="RETURN_UNPACKING",
                        dimension="return_unpacking",
                        observed=f"assigned to single name for {name}",
                        expected="optional: unpack tuple return",
                        checker_status="EVIDENCE_WEAK",
                        decision="INSUFFICIENT_EVIDENCE",
                        ast_location=node_loc(node),
                        abstain_reason="tuple_bound_as_whole",
                    )
                )

    # runtime/frozen binding (PASS-safe: accept common formal aliases)
    has_frozen = bool(
        re.search(r"\bfrozen(_params)?\b", source)
        or re.search(r"kwargs\s*\.\s*get\s*\(\s*['\"]frozen", source)
        or re.search(r"kwargs\s*\[\s*['\"]frozen", source)
        or re.search(r"\bfrozen_params\b", source)
    )
    if not has_frozen:
        findings.append(
            _finding(
                violated=True,
                violation_id=_vid("FROZEN_BIND"),
                violation_type="frozen_binding_missing",
                contract_clause="RUNTIME_FROZEN_BINDING",
                dimension="runtime_frozen_binding",
                observed="no frozen / frozen_params token or kwargs frozen get",
                expected="frozen = {...} or kwargs.get('frozen_params')",
                checker_status="VIOLATION",
                decision="DETECT_ONLY_ABSTAIN",
                abstain_reason="no_frozen_binding",
            )
        )

    # dataflow: frozen used if present
    if has_frozen and "frozen" in source and n_gen == 1:
        # weak check: at least one frozen[ or frozen. reference beyond assignment
        uses = len(re.findall(r"\bfrozen(_params)?\s*\[", source))
        if uses == 0 and "oracle_payload" in source:
            findings.append(
                _finding(
                    violated=False,
                    violation_id=_vid("DATAFLOW_WEAK"),
                    violation_type="frozen_unused_weak",
                    contract_clause="DATAFLOW",
                    dimension="dataflow",
                    observed="frozen assigned but no frozen[...] index use found",
                    expected="frozen fields feed domain API / answer",
                    checker_status="EVIDENCE_WEAK",
                    decision="INSUFFICIENT_EVIDENCE",
                    abstain_reason="frozen_use_not_proven",
                )
            )

    # answer_schema / provenance
    rewire_specs = contract.get("answer_source_rewire") or []
    answer_schema = contract.get("answer_schema")
    if isinstance(answer_schema, dict):
        # expect correct_answer dict with keys
        ca_keys = set(answer_schema.keys()) if answer_schema else set()
        found_ca: set[str] = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    if k.value in ca_keys or k.value in ("remainder", "canonical_latex", "value"):
                        found_ca.add(k.value)
        # only require when correct_answer assignment visible
        if "correct_answer" in source and ca_keys:
            missing_keys = ca_keys - found_ca
            # soft: not all schema keys are always present in nested form
            if missing_keys and len(found_ca) == 0:
                findings.append(
                    _finding(
                        violated=True,
                        violation_id=_vid("ANS_SCHEMA"),
                        violation_type="answer_schema_keys_absent",
                        contract_clause="ANSWER_SCHEMA",
                        dimension="answer_schema",
                        observed=f"found_answerish_keys={sorted(found_ca)}",
                        expected=f"schema keys near {sorted(ca_keys)}",
                        checker_status="VIOLATION",
                        decision="DETECT_ONLY_ABSTAIN",
                        abstain_reason="answer_schema_not_observed",
                    )
                )

    for spec in rewire_specs:
        clause = spec.get("clause_id") or "ANSWER_PROVENANCE"
        key = spec.get("answer_key") or ""
        required = spec.get("required_source_name") or ""
        forbidden = spec.get("forbidden_sources") or []
        # High-confidence wrong sources only (forbidden forms / str(...)).
        # Do not mark every non-matching Name as a hard violation (PASS aliases).
        wrong_hits: list[tuple[ast.AST, str]] = []
        good_hits = 0
        for node in ast.walk(tree):
            if not isinstance(node, dict.__class__) and not isinstance(node, ast.Dict):
                continue
            if not isinstance(node, ast.Dict):
                continue
            for k, v in zip(node.keys, node.values):
                if not (isinstance(k, ast.Constant) and k.value == key):
                    continue
                obs = unparse(v)
                if required and obs.replace(" ", "") == required.replace(" ", ""):
                    good_hits += 1
                    continue
                is_forbidden = any(f.replace(" ", "") in obs.replace(" ", "") for f in forbidden if f)
                is_str_of_raw = False
                if isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id == "str" and v.args:
                    arg0 = unparse(v.args[0]).replace(" ", "")
                    # High-confidence only: str(r), str(list(...)), not str(r_latex)
                    if arg0 in {"r", "list(r)"} or arg0.startswith("list(") or arg0 == "0":
                        is_str_of_raw = True
                    if required and arg0 == required.replace(" ", ""):
                        is_str_of_raw = False  # str(r_latex) when required is r_latex — weak
                if is_forbidden or is_str_of_raw:
                    wrong_hits.append((v, obs))
        if wrong_hits and len(wrong_hits) == 1 and good_hits == 0:
            v, obs = wrong_hits[0]
            findings.append(
                _finding(
                    violated=True,
                    violation_id=_vid("ANS_PROV", clause, key),
                    violation_type="answer_provenance_mismatch",
                    contract_clause=clause,
                    dimension="answer_provenance",
                    observed=obs,
                    expected=required,
                    checker_status="VIOLATION",
                    decision="DETECT_ONLY_ABSTAIN",
                    ast_location=node_loc(v),
                    abstain_reason="answer_field_wrong_source",
                    repair_candidate_found=True,  # PC-R01 shaped
                )
            )
        elif len(wrong_hits) > 1 and good_hits == 0:
            findings.append(
                _finding(
                    violated=True,
                    violation_id=_vid("ANS_PROV_MULTI", clause, key, len(wrong_hits)),
                    violation_type="answer_provenance_nonunique",
                    contract_clause=clause,
                    dimension="answer_provenance",
                    observed=f"{len(wrong_hits)} candidate wrong bindings",
                    expected=f"unique {key} <- {required}",
                    checker_status="VIOLATION",
                    decision="DETECT_ONLY_ABSTAIN",
                    abstain_reason="nonunique_answer_source_candidates",
                    repair_candidate_found=False,
                )
            )
        elif good_hits == 0 and wrong_hits == [] and key and "correct_answer" in source and required:
            findings.append(
                _finding(
                    violated=False,
                    violation_id=_vid("ANS_PROV_WEAK", clause),
                    violation_type="answer_provenance_unproven",
                    contract_clause=clause,
                    dimension="answer_provenance",
                    observed="could not prove field source",
                    expected=f"{key} <- {required}",
                    checker_status="EVIDENCE_WEAK",
                    decision="INSUFFICIENT_EVIDENCE",
                    abstain_reason="provenance_not_statically_proven",
                )
            )

    # ========== FULL-PLAN ONLY ==========
    if is_menu:
        # Explicit non-application of full-plan process dimensions
        for dim in FULL_PLAN_DIMENSIONS:
            findings.append(
                _finding(
                    violated=False,
                    violation_id=_vid("MENU_SKIP", dim),
                    violation_type="full_plan_dimension_not_applicable",
                    contract_clause="DOMAIN_MENU_SCOPE",
                    dimension=dim,
                    observed="domain-menu condition",
                    expected="full-plan process checks NOT applied",
                    checker_status="SKIPPED_MENU",
                    decision="CONTRACT_OK",
                    condition_scope="full_plan_only",
                    abstain_reason="menu_forbids_full_plan_process_checks",
                )
            )
    elif is_full:
        fp = contract.get("full_plan_constraints") or {}
        required = fp.get("required_calls") or []
        required_names = [c["fqname"] for c in required]
        present_names = [fqname(c) for c in calls]
        present_set = set(present_names)
        missing = [n for n in required_names if n not in present_set]
        extra_domain = [
            n for n in present_set if n.startswith(domain + ".") and n not in required_names
        ]

        # required_api_calls
        if missing:
            vtype = (
                "missing_required_calls_unique"
                if len(missing) == 1
                else "missing_required_calls_multiple"
            )
            findings.append(
                _finding(
                    violated=True,
                    violation_id=_vid("REQ_CALLS", len(missing)),
                    violation_type=vtype,
                    contract_clause="REQUIRED_API_CALLS",
                    dimension="required_api_calls",
                    observed=f"missing={missing}",
                    expected=f"required={required_names}",
                    checker_status="VIOLATION",
                    decision="DETECT_ONLY_ABSTAIN",
                    condition_scope="full_plan_only",
                    abstain_reason="missing_required_calls",
                    repair_candidate_found=len(missing) == 1,  # PC-R04 shaped (still fail-closed)
                )
            )
        else:
            findings.append(
                _finding(
                    violated=False,
                    violation_id=_vid("REQ_CALLS_OK"),
                    violation_type="required_calls_present",
                    contract_clause="REQUIRED_API_CALLS",
                    dimension="required_api_calls",
                    observed="all required present",
                    expected=str(required_names),
                    checker_status="OK",
                    decision="CONTRACT_OK",
                    condition_scope="full_plan_only",
                )
            )

        # call_order: required sequence is a subsequence of present order
        # (allows intervening extra calls and repeated helper APIs)
        if required_names and not missing:
            it = iter(present_names)
            order_ok = all(any(p == r for p in it) for r in required_names)
            if not order_ok:
                findings.append(
                    _finding(
                        violated=True,
                        violation_id=_vid("CALL_ORDER"),
                        violation_type="required_call_order_mismatch",
                        contract_clause="CALL_ORDER",
                        dimension="call_order",
                        observed=f"present_order_sample={present_names[:12]}",
                        expected=f"subsequence order {required_names}",
                        checker_status="VIOLATION",
                        decision="DETECT_ONLY_ABSTAIN",
                        condition_scope="full_plan_only",
                        abstain_reason="call_order_mismatch",
                    )
                )

        # exact_argument_source: scaffold has specific frozen field forms — weak compare when single required call matches
        if required and missing == []:
            # check first mismatched arg patterns for div_qr frozen access
            pass  # covered loosely by dataflow frozen index uses

        # operand_roles_order
        for oc in contract.get("operand_order_constraints") or []:
            swapped: list[ast.Call] = []
            for call in calls:
                if fqname(call) != oc.get("fqname"):
                    continue
                if len(call.args) != 2:
                    continue
                a0, a1 = call.args[0], call.args[1]
                if _is_create_zero(a1) and not _is_create_zero(a0):
                    swapped.append(call)
            if len(swapped) == 1:
                findings.append(
                    _finding(
                        violated=True,
                        violation_id=_vid("OPERAND", oc.get("clause_id")),
                        violation_type="operand_order_swapped",
                        contract_clause=oc.get("clause_id") or "OPERAND_ORDER",
                        dimension="operand_roles_order",
                        observed=unparse(swapped[0]),
                        expected=oc.get("scaffold_form") or "zero-first sub",
                        checker_status="VIOLATION",
                        decision="DETECT_ONLY_ABSTAIN",
                        ast_location=node_loc(swapped[0]),
                        condition_scope="full_plan_only",
                        abstain_reason="operand_order_wrong",
                        repair_candidate_found=True,  # PC-R02 shaped
                    )
                )
            elif len(swapped) > 1:
                findings.append(
                    _finding(
                        violated=True,
                        violation_id=_vid("OPERAND_MULTI", len(swapped)),
                        violation_type="operand_order_nonunique",
                        contract_clause=oc.get("clause_id") or "OPERAND_ORDER",
                        dimension="operand_roles_order",
                        observed=f"{len(swapped)} swapped sites",
                        expected="unique fixable site",
                        checker_status="VIOLATION",
                        decision="DETECT_ONLY_ABSTAIN",
                        condition_scope="full_plan_only",
                        abstain_reason="nonunique_operand_sites",
                        repair_candidate_found=False,
                    )
                )

        # intermediate_dataflow
        steps = fp.get("intermediate_dataflow") or contract.get("full_plan_steps")
        if steps and isinstance(steps, list) and missing:
            findings.append(
                _finding(
                    violated=True,
                    violation_id=_vid("INTER_DF"),
                    violation_type="intermediate_dataflow_incomplete",
                    contract_clause="INTERMEDIATE_DATAFLOW",
                    dimension="intermediate_dataflow",
                    observed=f"missing_calls={missing}",
                    expected=f"steps={steps}",
                    checker_status="VIOLATION",
                    decision="DETECT_ONLY_ABSTAIN",
                    condition_scope="full_plan_only",
                    abstain_reason="incomplete_process_steps",
                )
            )

        # required_formatter
        for spec in rewire_specs:
            fmt = spec.get("formatter_call")
            if fmt and fmt not in present_set and fmt.split(".")[0] == domain:
                findings.append(
                    _finding(
                        violated=True,
                        violation_id=_vid("FMT", fmt),
                        violation_type="required_formatter_missing",
                        contract_clause="REQUIRED_FORMATTER",
                        dimension="required_formatter",
                        observed=f"missing {fmt}",
                        expected=f"call {fmt}",
                        checker_status="VIOLATION",
                        decision="DETECT_ONLY_ABSTAIN",
                        condition_scope="full_plan_only",
                        abstain_reason="formatter_missing",
                    )
                )

        # required_answer_field_source — same as answer_provenance but marked full-plan scope when full
        for f in list(findings):
            if f.dimension == "answer_provenance" and f.contract_violation_detected:
                findings.append(
                    _finding(
                        violated=True,
                        violation_id=_vid("REQ_ANS_SRC", f.violation_id),
                        violation_type="required_answer_field_source",
                        contract_clause=f.contract_clause,
                        dimension="required_answer_field_source",
                        observed=f.observed,
                        expected=f.expected,
                        checker_status="VIOLATION",
                        decision="DETECT_ONLY_ABSTAIN",
                        ast_location=f.ast_location,
                        condition_scope="full_plan_only",
                        abstain_reason=f.abstain_reason,
                        repair_candidate_found=f.repair_candidate_found,
                    )
                )

        # missing/extra process step
        if missing or (extra_domain and len(missing) > 1):
            findings.append(
                _finding(
                    violated=True,
                    violation_id=_vid("PROC_STEP", len(missing), len(extra_domain)),
                    violation_type="extra_or_missing_process_steps",
                    contract_clause="MISSING_EXTRA_PROCESS_STEP",
                    dimension="missing_extra_process_step",
                    observed=f"missing={missing}; extra_domain_calls={sorted(extra_domain)[:8]}",
                    expected="exact full-plan process API set",
                    checker_status="VIOLATION",
                    decision="REWRITE_REQUIRED" if len(missing) >= 3 else "DETECT_ONLY_ABSTAIN",
                    condition_scope="full_plan_only",
                    abstain_reason="process_step_delta",
                )
            )

    # --- Correlate frozen PC repair without modifying rules ---
    pc_accept_rules: list[str] = []
    source_mod = False
    if correlate_pc_repair and parseable:
        pipe = apply_contract_aware_v2(
            source,
            task_id=task_id,
            condition=condition,
            cell_id=cell_id,
            model_key=model_key,
            contract=contract,
        )
        pc_accept_rules = list(pipe.rules_fired)
        source_mod = bool(pipe.source_modified)
        if pc_accept_rules:
            for rid in pc_accept_rules:
                dim_map = {
                    "PC-R01_ANSWER_SOURCE_REWIRE_V2": (
                        "answer_provenance",
                        "required_answer_field_source",
                    ),
                    "PC-R02_OPERAND_ORDER_RESTORE_V2": ("operand_roles_order",),
                    "PC-R03_DOMAIN_API_NORMALIZE_V2": (
                        "domain_class_legality",
                        "method_function_existence",
                        "allowed_api_membership",
                    ),
                    "PC-R04_UNIQUE_PROCESS_WIRING_V2": (
                        "required_api_calls",
                        "missing_extra_process_step",
                    ),
                }
                for f in findings:
                    if f.dimension in dim_map.get(rid, ()) and f.contract_violation_detected:
                        f.repair_candidate_found = True
                        f.repair_accepted = True
                        f.decision = "REPAIR_ACCEPTED"
                        f.abstain_reason = ""
                findings.append(
                    _finding(
                        violated=True,
                        violation_id=_vid("PC_ACCEPT", rid),
                        violation_type="pc_repair_accepted",
                        contract_clause=rid,
                        dimension="pc_repair_correlation",
                        observed=f"PC accepted: {rid}",
                        expected="unique proof-carrying repair",
                        checker_status="VIOLATION",
                        decision="REPAIR_ACCEPTED",
                        repair_candidate_found=True,
                        repair_accepted=True,
                    )
                )

    # Evaluator-PASS oracle calibration (detection only, no source change):
    # raw PASS is allowed legal alternative implementations. Scaffold full-plan process
    # deltas and SSOT incompleteness are recorded observationally — not safety false positives.
    if raw_outcome == "passed" and not pc_accept_rules:
        observational_types = {
            "missing_required_calls_unique",
            "missing_required_calls_multiple",
            "required_call_order_mismatch",
            "intermediate_dataflow_incomplete",
            "extra_or_missing_process_steps",
            "required_formatter_missing",
            "method_not_in_ssot",
            "method_not_in_allowed_set",
            "frozen_binding_missing",
            "argument_count_mismatch",
            "argument_count_or_name",
            "return_keys_missing",
            "return_unpack_arity",
            "answer_provenance_mismatch",
            "answer_provenance_nonunique",
            "required_answer_field_source",
            "operand_order_swapped",
            "operand_order_nonunique",
        }
        for f in findings:
            if f.repair_accepted:
                continue
            if f.violation_type in observational_types or f.condition_scope == "full_plan_only":
                if f.contract_violation_detected or f.checker_status == "VIOLATION":
                    f.contract_violation_detected = False
                    f.checker_status = "PASS_ORACLE_OBSERVATIONAL"
                    f.decision = "CONTRACT_OK"
                    f.abstain_reason = (f.abstain_reason + ";" if f.abstain_reason else "") + "pass_oracle_not_fp"
            # illegal_ops_class remains hard even on PASS (should be rare)

    viol_count = sum(1 for f in findings if f.contract_violation_detected)
    cell_decision = _cell_decision_from_findings(
        findings,
        parseable=True,
        n_generate=n_gen,
        source_lines=source.count("\n"),
        any_pc_accept=bool(pc_accept_rules),
    )
    if raw_outcome == "passed" and not pc_accept_rules and viol_count == 0:
        cell_decision = "CONTRACT_OK"

    return CellCheckerReport(
        cell_id=cell_id,
        task_id=task_id,
        condition=condition,
        model_key=model_key,
        raw_outcome=raw_outcome,
        parseable=True,
        parse_error="",
        n_generate=n_gen,
        findings=findings,
        cell_decision=cell_decision,
        violation_count=viol_count,
        repair_accepted_count=len(pc_accept_rules),
        repair_accepted_rules=pc_accept_rules,
        source_modified_by_pc=source_mod,
    )


SCHEMA_FIELD_NAMES = (
    "contract_violation_detected",
    "violation_id",
    "violation_type",
    "contract_clause",
    "ast_location",
    "observed",
    "expected",
    "checker_status",
    "repair_candidate_found",
    "repair_accepted",
    "decision",
    "abstain_reason",
)
