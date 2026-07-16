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


TOOLBOX_RETURN_STRUCTURES = {
    "PolynomialOps.div_qr": "tuple[list[exact coefficient], list[exact coefficient]] (quotient, remainder)",
    "PolynomialOps.format_latex": "str", "PolynomialOps.format_plain": "str",
    "FractionOps.create": "Fraction", "FractionOps.add": "Fraction", "FractionOps.sub": "Fraction", "FractionOps.mul": "Fraction", "FractionOps.div": "Fraction", "FractionOps.to_latex": "str",
    "RadicalOps.simplify_term": "tuple[exact coefficient, int] (coefficient, radicand)", "RadicalOps.format_expression": "str", "RadicalLogicEngine": "RadicalLogicEngine instance",
}
TOOLBOX_PARAMETER_MEANINGS = {
    "PolynomialOps.div_qr": "dividend_coefficients, divisor_coefficients", "PolynomialOps.format_latex": "polynomial value", "PolynomialOps.format_plain": "polynomial value",
    "FractionOps.create": "value", "FractionOps.add": "left, right", "FractionOps.sub": "left, right", "FractionOps.mul": "left, right", "FractionOps.div": "left, right", "FractionOps.to_latex": "value",
    "RadicalOps.simplify_term": "coefficient, radicand", "RadicalOps.format_expression": "terms", "RadicalLogicEngine": "constructor",
}


def runtime_toolbox_inventory() -> list[dict]:
    """Runtime truth used for both rendered prompts and prompt-contract validation."""
    namespace = runtime_namespace()
    names = ["PolynomialOps.div_qr", "PolynomialOps.format_latex", "PolynomialOps.format_plain", "FractionOps.create", "FractionOps.add", "FractionOps.sub", "FractionOps.mul", "FractionOps.div", "FractionOps.to_latex", "RadicalOps.simplify_term", "RadicalOps.format_expression", "RadicalLogicEngine"]
    inventory=[]
    for name in names:
        obj=namespace[name] if "." not in name else getattr(namespace[name.split(".")[0]], name.split(".")[1])
        inventory.append({"canonical_name":name,"import_path":LIBRARY_PATH if name != "RadicalLogicEngine" else "core.skill_policies.radical_logic","signature":str(inspect.signature(obj)),"parameter_meaning":TOOLBOX_PARAMETER_MEANINGS[name],"return_structure":TOOLBOX_RETURN_STRUCTURES[name]})
    return inventory


def stub_for_task(task_id: str) -> str:
    spec = TASK_API_MAPPING[task_id]
    if spec.get("coverage"):
        return f"# {spec['coverage']}: {spec['reason']}\n"
    lines="\n".join(f"- `{x['canonical_name']}` | import: `{x['import_path']}` | signature: `{x['signature']}` | parameters: {x['parameter_meaning']} | returns: {x['return_structure']}" for x in runtime_toolbox_inventory())
    return f"""# CE115 Ab2d-Assembly domain contract
from {LIBRARY_PATH} import FractionOps, PolynomialOps, RadicalOps
from core.skill_policies.radical_logic import RadicalLogicEngine

Available Domain APIs
The following APIs form the available domain toolbox. Select only APIs relevant to the current task. Do not call irrelevant APIs merely for compliance.
{lines}

Use the domain library for every supported core operation actually required by the task. Do not manually reimplement a supported core algorithm. A domain API call counts as adoption only when its returned value contributes to the final answer. Standard Python may be used for control flow, indexing, unpacking, data movement, and output assembly.

Return contract: `generate(level=1, **kwargs)` returns a dict with `question_text`, `correct_answer`, and `oracle_payload`.
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


def resolve_task_operations(task_id, frozen_payload=None):
    """Resolve operations from frozen task structure, never an answer oracle (v4)."""
    payload = frozen_payload or {}
    common = {"required_operations_source": "frozen_task_structure", "required_operations_resolver_version": "v4.1", "oracle_independent": True}
    if task_id == "ce115_calc_polynomial_division_l1":
        return {**common, "required":["PolynomialOps.div_qr"], "optional":["PolynomialOps.format_latex","PolynomialOps.format_plain"], "acceptable_canonical_paths":[["PolynomialOps.div_qr"]]}
    if task_id == "ce115_calc_exact_rational_expression_l1":
        tokens = payload.get("operations") or payload.get("operation_sequence") or []
        tokens = [str(x).lower().replace("fractionops.", "") for x in tokens]
        if not tokens:
            tokens = ["mul"] + (["add"] if len(payload.get("products", [])) > 1 else [])
        required = ["FractionOps.create"] + [f"FractionOps.{x}" for x in ("add", "sub", "mul", "div") if x in tokens]
        return {**common, "required":required, "optional":["FractionOps.to_latex"], "acceptable_canonical_paths":[required]}
    if task_id == "ce115_calc_radical_simplification_l1":
        return {**common, "required":["RadicalOps.simplify_term"], "optional":["RadicalLogicEngine","RadicalOps.format_expression"], "acceptable_canonical_paths":[["RadicalOps.simplify_term"], ["RadicalLogicEngine"]]}
    raise KeyError(task_id)


def scan_toolbox(source, task_id, frozen_payload=None):
    """v4 AST scanner: a domain call counts only when its result reaches output."""
    policy = resolve_task_operations(task_id, frozen_payload)
    try: tree = ast.parse(source)
    except SyntaxError: return {"classification":"INSUFFICIENT_EVIDENCE", "assembly_classification":"INSUFFICIENT_EVIDENCE", "task_required_operations":policy["required"], "called_apis":[], "called_domain_apis":[], "invalid_calls":[], "missing_operations":policy["required"], "domain_library_adopted":False, "called_but_result_unused":False, "domain_call_result_bindings":[], "domain_result_reaches_final_output":[], "manual_recomputation_after_domain_call":False, "surface_compliance_only":False, **policy}
    known = {"PolynomialOps.div_qr":2, "PolynomialOps.format_latex":1, "PolynomialOps.format_plain":1, "FractionOps.create":1, "FractionOps.add":2, "FractionOps.sub":2, "FractionOps.mul":2, "FractionOps.div":2, "FractionOps.to_latex":1, "RadicalOps.simplify_term":2, "RadicalOps.format_expression":1, "RadicalLogicEngine":None}
    aliases, rows, bindings, returned = {}, [], [], set()
    def dotted(n):
        if isinstance(n, ast.Name): return aliases.get(n.id, n.id)
        if isinstance(n, ast.Attribute):
            base=dotted(n.value); return f"{base}.{n.attr}" if base else n.attr
        return ""
    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names:
                if a.name in ("PolynomialOps", "FractionOps", "RadicalOps", "RadicalLogicEngine"): aliases[a.asname or a.name]=a.name
        if isinstance(n, ast.Assign) and isinstance(n.value, (ast.Name, ast.Attribute)):
            val=dotted(n.value)
            if val in known:
                for t in n.targets:
                    if isinstance(t, ast.Name): aliases[t.id]=val
    dependencies = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign):
            value_names = {x.id for x in ast.walk(n.value) if isinstance(x, ast.Name)}
            for target in n.targets:
                if isinstance(target, ast.Name): dependencies[target.id] = value_names
    for n in ast.walk(tree):
        if isinstance(n, ast.Return):
            returned |= {x.id for x in ast.walk(n.value) if isinstance(x, ast.Name)}
            pending = list(returned)
            while pending:
                name = pending.pop()
                for dependency in dependencies.get(name, set()):
                    if dependency not in returned: returned.add(dependency); pending.append(dependency)
        if isinstance(n, ast.Call):
            api=dotted(n.func)
            if api in known:
                assignment=next((p for p in ast.walk(tree) if isinstance(p, (ast.Assign, ast.AnnAssign)) and p.value is n), None)
                names=[]
                if assignment:
                    target=assignment.targets[0] if isinstance(assignment, ast.Assign) else assignment.target
                    names=[x.id for x in ast.walk(target) if isinstance(x, ast.Name)]
                valid=known[api] is None or len(n.args)==known[api]
                rows.append({"api":api,"valid":valid,"bindings":names})
                bindings.extend({"api":api,"binding":x,"reaches_final_output":x in returned} for x in names)
    called=[x["api"] for x in rows if x["valid"]]; invalid=[x["api"] for x in rows if not x["valid"]]
    reaches={x["api"] for x in rows if x["valid"] and x["bindings"] and all(b in returned for b in x["bindings"])}
    unused=any(x["valid"] and (not x["bindings"] or not any(b in returned for b in x["bindings"])) for x in rows)
    missing=[x for x in policy["required"] if x not in reaches]
    manual=bool(called and missing); category="INVALID_API_CALL" if invalid else "REQUIRED_OPERATION_NOT_COVERED" if missing else "ASSEMBLY_COMPLIANT"
    return {"classification":category,"assembly_classification":category,"called_apis":called,"called_domain_apis":called,"invalid_calls":invalid,"task_required_operations":policy["required"],"optional_apis":policy["optional"],"missing_operations":missing,"domain_library_adopted":not missing and bool(reaches),"called_but_result_unused":unused,"domain_call_result_bindings":bindings,"domain_result_reaches_final_output":sorted(reaches),"manual_recomputation_after_domain_call":manual,"surface_compliance_only":manual, **{k:v for k,v in policy.items() if k not in ("required","optional")}}
