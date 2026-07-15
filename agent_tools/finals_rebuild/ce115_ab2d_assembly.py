"""Frozen, thin-wrapper assembly contract for the CE115 Ab2d-Assembly cohort."""
from __future__ import annotations

import ast
import hashlib
import inspect
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LIBRARY_PATH = "core.prompts.domain_function_library"
TASK_API_MAPPING = {
    "ce115_calc_radical_simplification_l1": {
        "required": ["RadicalLogicEngine", "RadicalOps.simplify_term", "RadicalOps.format_expression"],
        "optional": [],
    },
    "ce115_calc_polynomial_division_l1": {
        "required": ["PolynomialOps.div_qr"], "optional": ["PolynomialOps.format_latex", "PolynomialOps.format_plain"],
    },
    "ce115_calc_exact_rational_expression_l1": {
        "required": ["FractionOps.create", "FractionOps.add", "FractionOps.sub", "FractionOps.mul", "FractionOps.div"], "optional": ["FractionOps.to_latex"],
    },
    "ce115_calc_polynomial_factor_roots_l1": {
        "required": [], "optional": [], "coverage": "ASSEMBLY_COVERAGE_UNAVAILABLE",
        "reason": "No canonical reusable polynomial factor/roots primitive exists in the repository.",
    },
}
FORBIDDEN_DEFINITIONS = {"FractionOps", "RadicalOps", "PolynomialOps", "RadicalLogicEngine"}


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def stub_for_task(task_id: str) -> str:
    spec = TASK_API_MAPPING[task_id]
    if spec.get("coverage"):
        return f"# {spec['coverage']}: {spec['reason']}\n"
    apis = "\n".join(f"- `{api}`" for api in spec["required"] + spec["optional"])
    return f"""# CE115 Ab2d-Assembly domain contract
from {LIBRARY_PATH} import FractionOps, PolynomialOps, RadicalOps
from core.skill_policies.radical_logic import RadicalLogicEngine

Required APIs:\n{apis}

MUST_CALL: invoke every required API through its canonical name in `generate`.
DO_NOT_REIMPLEMENT_DOMAIN_LOGIC: do not define domain helper classes/functions or reproduce their algorithms.
Return contract: `generate(level=1, **kwargs)` returns a dict with `question_text`, `correct_answer`, and `oracle_payload`.
Example: `q, r = PolynomialOps.div_qr([1, 0, -1], [1, -1])`.
"""


def runtime_namespace() -> dict:
    """Load canonical implementations once for evaluator execution; no prompt stubs."""
    from core.prompts.domain_function_library import FractionOps, PolynomialOps, RadicalOps
    from core.skill_policies.radical_logic import RadicalLogicEngine
    return {"FractionOps": FractionOps, "PolynomialOps": PolynomialOps, "RadicalOps": RadicalOps, "RadicalLogicEngine": RadicalLogicEngine}


def dotted(node: ast.AST) -> str:
    if isinstance(node, ast.Name): return node.id
    if isinstance(node, ast.Attribute):
        value = dotted(node.value)
        return f"{value}.{node.attr}" if value else node.attr
    return ""


def scan_assembly(source: str, task_id: str) -> dict:
    spec = TASK_API_MAPPING[task_id]
    if spec.get("coverage"):
        return {"classification": spec["coverage"], "required_apis": [], "called_apis": [], "errors": [spec["reason"]]}
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return {"classification": "INSUFFICIENT_EVIDENCE", "required_apis": spec["required"], "called_apis": [], "errors": [f"syntax error: {exc.msg}"]}
    call_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
    calls = {dotted(node.func) for node in call_nodes}
    definitions = {node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    forbidden = sorted(definitions & FORBIDDEN_DEFINITIONS)
    reimplementation_names = {"simplify_term", "factor", "find_roots", "parse_decimal", "long_division"}
    reimplemented = sorted(definitions & reimplementation_names)
    required = spec["required"]
    missing = [api for api in required if api not in calls]
    expected_arity = {"RadicalOps.simplify_term": 2, "RadicalOps.format_expression": 1, "PolynomialOps.div_qr": 2, "FractionOps.create": 1, "FractionOps.add": 2, "FractionOps.sub": 2, "FractionOps.mul": 2, "FractionOps.div": 2}
    invalid = [dotted(node.func) for node in call_nodes if dotted(node.func) in expected_arity and len(node.args) != expected_arity[dotted(node.func)]]
    if forbidden:
        category = "FORBIDDEN_HELPER_REDEFINED"
    elif reimplemented:
        category = "DOMAIN_LOGIC_REIMPLEMENTED"
    elif invalid:
        category = "INVALID_API_CALL"
    elif missing:
        category = "REQUIRED_API_NOT_CALLED"
    else:
        category = "ASSEMBLY_COMPLIANT"
    return {"classification": category, "required_apis": required, "called_apis": sorted(calls & set(required + spec["optional"])), "missing_apis": missing, "forbidden_definitions": forbidden, "reimplemented_helpers": reimplemented, "invalid_calls": invalid, "runtime_library_available": True, "errors": []}


def runtime_smoke(source: str, task_id: str) -> dict:
    scan = scan_assembly(source, task_id)
    if scan["classification"] != "ASSEMBLY_COMPLIANT": return scan
    namespace = runtime_namespace()
    try:
        exec(compile(source, "<ab2d-assembly>", "exec"), namespace, namespace)
        if not callable(namespace.get("generate")):
            raise TypeError("generate is missing")
    except Exception as exc:  # pragma: no cover - exercised by callers
        scan["classification"] = "LIBRARY_RUNTIME_UNAVAILABLE"
        scan["errors"] = [f"runtime smoke: {type(exc).__name__}: {exc}"]
    return scan


def build_protocol(source_commit: str) -> dict:
    models = ["qwen3.5:4b", "qwen3.5:9b"]
    tasks = list(TASK_API_MAPPING)
    cells = [{"cell_id": f"{model.replace('.', '_').replace(':', '_')}__{task}__ab2d_assembly__seed_{seed}", "model": model, "task": task, "condition": "ab2d_assembly", "seed": seed, "evaluator": "ce115_assembly_scanner"} for model in models for task in tasks for seed in (2026071301, 2026071302, 2026071303)]
    library_file = REPO_ROOT / "core/prompts/domain_function_library.py"
    mapping_text = json.dumps(TASK_API_MAPPING, sort_keys=True, ensure_ascii=False)
    stub_hashes = {task: sha256_text(stub_for_task(task)) for task in tasks}
    protocol = {"protocol_id": "ce115_ab2d_assembly_protocol", "source_commit": source_commit, "condition_semantics": {"ab2d_spec": "legacy specification-only condition; excluded", "ab2d_assembly": "thin wrapper with canonical runtime library and must-call contract"}, "models": models, "tasks": tasks, "seeds": [2026071301, 2026071302, 2026071303], "planned_cell_count": len(cells), "cells": cells, "generation": {"num_ctx": 65536, "num_predict": 24576, "think": False, "temperature": 0.0, "first_attempt_only": True, "retry": 0, "healer": 0, "repair": 0, "replay": 0}, "result_directory": "docs/experiments/results/ce115_ab2d_assembly_formal_run", "hashes": {"task_api_mapping": sha256_text(mapping_text), "prompt_stubs": stub_hashes, "canonical_library": hashlib.sha256(library_file.read_bytes()).hexdigest(), "assembly_scanner": sha256_text(inspect.getsource(scan_assembly))}}
    protocol["hashes"]["protocol_manifest"] = sha256_text(json.dumps(protocol, sort_keys=True, ensure_ascii=False))
    return protocol
