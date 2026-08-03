# -*- coding: utf-8 -*-
"""32 task×condition contract SSOT for Contract-Aware Aggressive Healer v2."""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any

from agent_tools.finals_rebuild.artifacts import sha256_json, sha256_text
from agent_tools.finals_rebuild.domain_api_ssot import (
    API_CLASSIFICATION,
    DOMAIN_API_SSOT,
    SUPPORTED_PUBLIC,
)
from agent_tools.finals_rebuild.math16_ab2d_v2_scaffolds import TASK_SCAFFOLDS_V2
from agent_tools.finals_rebuild.math_answer_contracts import CONTRACTS

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_DIR = ROOT / "artifacts/math16_contract_aware_aggressive_healer_v2/contracts"

CONDITIONS = ("ab2d_domain_menu_v2", "ab2d_full_v2")


def _allowed_methods(domain: str) -> list[str]:
    return sorted(
        name
        for name, cls in API_CLASSIFICATION.items()
        if cls == SUPPORTED_PUBLIC and name.startswith(domain + ".")
    )


def _signatures(methods: list[str]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for m in methods:
        if m in DOMAIN_API_SSOT:
            out[m] = {
                "signature": DOMAIN_API_SSOT[m]["signature"],
                "returns": DOMAIN_API_SSOT[m]["returns_model_facing"],
                "return_contract": DOMAIN_API_SSOT[m]["return_contract"],
            }
    return out


def _parse_required_calls(full_plan_body: str, domain: str) -> list[dict[str, Any]]:
    """Extract Ops calls from scaffold body in document order (relative ordering)."""
    # Scaffold body is indented as function body — wrap for parse.
    wrapped = "def generate(level=1, **kwargs):\n" + full_plan_body
    if not full_plan_body.endswith("\n"):
        wrapped += "\n"
    # May need frozen dummy for completeness if body references only.
    try:
        tree = ast.parse(wrapped)
    except SyntaxError:
        # Fallback: regex extract Class.method(
        found = re.findall(r"([A-Za-z]+Ops)\.([A-Za-z_]+)\s*\(", full_plan_body)
        return [
            {
                "order": i,
                "class": c,
                "method": m,
                "fqname": f"{c}.{m}",
                "args_unparsed": [],
                "arg_roles": [],
            }
            for i, (c, m) in enumerate(found)
        ]
    calls: list[dict[str, Any]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name)):
            continue
        if not func.value.id.endswith("Ops"):
            continue
        args = []
        for a in node.args:
            try:
                args.append(ast.unparse(a))
            except Exception:
                args.append(type(a).__name__)
        calls.append(
            {
                "order": len(calls),
                "class": func.value.id,
                "method": func.attr,
                "fqname": f"{func.value.id}.{func.attr}",
                "args_unparsed": args,
                "lineno": getattr(node, "lineno", None),
            }
        )
    return calls


def _answer_provenance(full_plan_body: str, answer_schema: Any) -> dict[str, Any]:
    """Static provenance: which answer keys map to which RHS names if visible in scaffold."""
    prov: dict[str, Any] = {"schema": answer_schema, "field_sources": {}}
    if answer_schema == "int":
        m = re.search(r"correct_answer\s*=\s*(.+)", full_plan_body)
        if m:
            prov["field_sources"]["correct_answer"] = m.group(1).strip()
        return prov
    # dict fields: "key": expr
    for m in re.finditer(r'["\']([A-Za-z_]+)["\']\s*:\s*([^\n,]+)', full_plan_body):
        key, expr = m.group(1), m.group(2).strip()
        if key in ("question_text", "oracle_payload"):
            continue
        if isinstance(answer_schema, dict) and (
            key in answer_schema or key in ("remainder", "canonical_latex", "value", "coefficient", "radicand")
        ):
            prov["field_sources"][key] = expr.rstrip(",")
    return prov


def _operand_order_constraints(task_id: str) -> list[dict[str, Any]]:
    """Explicit operand roles for selected full-plan patterns used by PC-R02."""
    constraints: list[dict[str, Any]] = []
    if task_id == "ce115_calc_exact_rational_expression_l1":
        constraints.append(
            {
                "clause_id": "SIGN_NEGATE_SUB_ZERO_FIRST",
                "fqname": "FractionOps.sub",
                "when": "p[\"sign\"] == -1 inside signed product",
                "arg0_role": "zero_value",  # FractionOps.create(0)
                "arg1_role": "term",
                "scaffold_form": "FractionOps.sub(FractionOps.create(0), term)",
                "forbidden_forms": ["FractionOps.sub(term, FractionOps.create(0))"],
            }
        )
    return constraints


def build_contract(task_id: str, condition: str) -> dict[str, Any]:
    if task_id not in TASK_SCAFFOLDS_V2:
        raise KeyError(task_id)
    if condition not in CONDITIONS:
        raise ValueError(condition)
    sc = TASK_SCAFFOLDS_V2[task_id]
    domain = sc["domain"]
    methods = _allowed_methods(domain)
    oracle_type = sc["oracle_type"]
    answer_contract_text = CONTRACTS.get(oracle_type, "")
    required_calls = _parse_required_calls(sc["full_plan_body"], domain)
    answer_prov = _answer_provenance(sc["full_plan_body"], sc["answer_schema"])
    is_full = condition == "ab2d_full_v2"
    payload: dict[str, Any] = {
        "contract_id": f"{task_id}__{condition}",
        "task_id": task_id,
        "condition": condition,
        "domain": domain,
        "allowed_classes": [domain],
        "allowed_methods": methods,
        "api_signatures": _signatures(methods),
        "frozen_fields": sorted(sc["frozen_literal"].keys())
        if isinstance(sc["frozen_literal"], dict)
        else [],
        "frozen_literal_shape": sc["frozen_literal"],
        "return_shape": {
            "keys": ["question_text", "correct_answer", "oracle_payload"],
            "oracle_payload": "must equal frozen_params object",
        },
        "answer_schema": sc["answer_schema"],
        "answer_provenance": answer_prov,
        "oracle_type": oracle_type,
        "answer_contract_source": "agent_tools/finals_rebuild/math_answer_contracts.py",
        "answer_contract_excerpt_sha256": sha256_text(answer_contract_text),
        "scaffold_ssot": "agent_tools/finals_rebuild/math16_ab2d_v2_scaffolds.py::TASK_SCAFFOLDS_V2",
        "full_plan_steps": sc.get("full_plan_steps") if is_full else None,
        "checks": {
            "api_legality": True,
            "signature": True,
            "binding": True,
            "dataflow": True,
            "answer_provenance": True,
            "enforce_unique_api_flow": False,
        },
        "full_plan_constraints": None,
        "operand_order_constraints": _operand_order_constraints(task_id) if is_full else [],
    }
    if is_full:
        payload["checks"]["enforce_unique_api_flow"] = False  # not forced repair except PC-R04 uniqueness
        payload["full_plan_constraints"] = {
            "required_calls": required_calls,
            "call_order": [c["fqname"] for c in required_calls],
            "exact_argument_source": "from_scaffold_full_plan_body",
            "return_unpacking": _detect_unpacking(sc["full_plan_body"]),
            "intermediate_dataflow": sc.get("full_plan_steps"),
            "answer_field_provenance": answer_prov["field_sources"],
        }
        # Answer rewire targets for PC-R01 when scaffold maps fields to formatter vars
        payload["answer_source_rewire"] = _answer_source_rewire_spec(task_id, sc)
    else:
        # domain-menu: still expose rewire when schema+formatter is contract-unique for this task
        payload["answer_source_rewire"] = _answer_source_rewire_spec(task_id, sc)
        payload["checks"]["enforce_unique_api_flow"] = False

    payload["contract_sha256"] = sha256_json(payload)
    # Recompute sha excluding nested contract_sha256
    payload_no_sha = {k: v for k, v in payload.items() if k != "contract_sha256"}
    payload["contract_sha256"] = sha256_json(payload_no_sha)
    return payload


def _detect_unpacking(body: str) -> list[str]:
    return re.findall(r"([A-Za-z_,\s]+)\s*=\s*[A-Za-z]+Ops\.[A-Za-z_]+\s*\(", body)


def _answer_source_rewire_spec(task_id: str, sc: dict[str, Any]) -> list[dict[str, Any]]:
    """Declare unique correct answer field sources from contract scaffold."""
    specs: list[dict[str, Any]] = []
    if task_id == "ce111_q02_polynomial_division_remainder":
        specs.append(
            {
                "clause_id": "REMAINDER_FROM_FORMAT_LATEX",
                "answer_key": "remainder",
                "required_source_name": "r_latex",
                "formatter_call": "PolynomialOps.format_latex",
                "formatter_input_name": "r",
                "also_keys": ["canonical_latex"],
                "forbidden_sources": [
                    "str(r)",
                    "str(list)",
                    "str(0)",
                    "str(PolynomialOps.normalize",
                ],
            }
        )
    if task_id in (
        "ce115_calc_radical_simplification_l1",
        "ce112_q04_radical_simplification",
    ):
        specs.append(
            {
                "clause_id": "CANONICAL_LATEX_FROM_FORMAT_TERM",
                "answer_key": "canonical_latex",
                "required_source_name": "canonical_latex",
                "formatter_call": "RadicalOps.format_term",
                "also_keys": [],
                "forbidden_sources": [],
            }
        )
    return specs


def build_all_contracts(*, write: bool = True) -> dict[str, Any]:
    contracts: dict[str, dict[str, Any]] = {}
    for task_id in TASK_SCAFFOLDS_V2:
        for cond in CONDITIONS:
            c = build_contract(task_id, cond)
            contracts[c["contract_id"]] = c
    index = {
        "n_contracts": len(contracts),
        "conditions": list(CONDITIONS),
        "task_ids": list(TASK_SCAFFOLDS_V2.keys()),
        "contract_ids": sorted(contracts.keys()),
        "contract_sha256_by_id": {k: v["contract_sha256"] for k, v in contracts.items()},
    }
    index["index_sha256"] = sha256_json(
        {k: v for k, v in index.items() if k != "index_sha256"}
    )
    if write:
        CONTRACT_DIR.mkdir(parents=True, exist_ok=True)
        for cid, c in contracts.items():
            path = CONTRACT_DIR / f"{cid}.json"
            path.write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (CONTRACT_DIR / "index.json").write_text(
            json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return {"index": index, "contracts": contracts}


def load_contract(task_id: str, condition: str) -> dict[str, Any]:
    path = CONTRACT_DIR / f"{task_id}__{condition}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return build_contract(task_id, condition)


def load_all_contracts() -> dict[str, dict[str, Any]]:
    if not CONTRACT_DIR.exists() or not list(CONTRACT_DIR.glob("*__*.json")):
        return build_all_contracts(write=True)["contracts"]
    out = {}
    for p in CONTRACT_DIR.glob("*__*.json"):
        c = json.loads(p.read_text(encoding="utf-8"))
        out[c["contract_id"]] = c
    return out
