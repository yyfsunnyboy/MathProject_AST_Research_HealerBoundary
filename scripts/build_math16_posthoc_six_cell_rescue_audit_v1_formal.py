"""
build_math16_posthoc_six_cell_rescue_audit_v1_formal.py
========================================================
Formal Builder for Math16 Post-hoc Six-Cell Rescue Mechanism Audit.

Generates:
  artifacts/math16_posthoc_six_cell_rescue_audit_v1/formal/
    - six_cell_audit_records.jsonl
    - six_cell_audit_table.csv
    - condition_family_crosstab.csv
    - condition_failure_layer_crosstab.csv
    - condition_rule_crosstab.csv
    - condition_primary_posthoc_crosstab.csv
    - condition_denominator_table.csv
    - repair_signature_catalog.json
    - audit_evidence_index.json

Strictly Read-Only with zero model calls, zero Healer executions, and zero rescoring.
"""

import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
OUTPUT_DIR = REPO_ROOT / "artifacts/math16_posthoc_six_cell_rescue_audit_v1/formal"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def build_formal_artifacts():
    print("Building formal audit artifacts...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 6 cells data definitions
    cells = [
        {
            "cell_id": "qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072004",
            "model": "qwen3_5_4b",
            "task_id": "ce112_q04_radical_simplification",
            "family": "radical",
            "condition": "Ab2g",
            "seed": "2026072004",
            "primary_is_rescued": True,
            "posthoc_is_rescued": True,
            "is_incremental_posthoc_pass": False,
            "baseline_outcome": "FAILED",
            "surface_failure_layer": "L2",
            "root_mechanism_layer": "L2_CONTRACT_SCHEMA_ENTRYPOINT",
            "surface_failure": "schema_failure",
            "root_mechanism": "Model wrapped output payload in a single-key JSON dictionary object instead of raw expression format.",
            "rule_id": "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
            "precondition_evidence": "Frozen precondition symptom matched: L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP (single-key dictionary wrapping output)",
            "before_snippet_hash": "c8e83cecbd57121723a290f1a91c9a32a75ab3ecd2d593b2279f70bffe141ae7",
            "after_snippet_hash": "2e77e663c63a9660ceb9a6b6fa3cc417dcb6ab43609e090b242cb32fa73eca8c",
            "unified_diff": "UNRESOLVED_SOURCE_NOT_COMMITTED",
            "source_span": "UNRESOLVED_SHA_ONLY",
            "changed_line_count": -1,
            "changed_ast_node_count": -1,
            "changed_ast_node_types": [],
            "tree_depth_range": "UNRESOLVED",
            "control_flow_changed": "UNRESOLVED",
            "literals_changed": "UNRESOLVED",
            "function_signature_changed": "UNRESOLVED",
            "semantic_operator_changed": "UNRESOLVED",
            "primary_disposition": "MODIFIED_RESCUED",
            "posthoc_disposition": "MODIFIED_RESCUED",
            "final_pass_fail": "PASS",
            "oracle_answer_used": False,
            "unique": "TRUE",
            "local": "TRUE",
            "offline_verifiable": "TRUE",
            "repair_signature_match": "AMBIGUOUS_SIGNATURE_MATCH",
            "evidence_citation": "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/healer_results.jsonl",
            "analyst_notes": "Identical behavior in Primary and Post-hoc. L2 payload wrap safely stripped to yield PASS."
        },
        {
            "cell_id": "qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2d_spec_v2__seed_2026072002",
            "model": "qwen3_5_4b",
            "task_id": "ce113_q01_negative_fraction_subtraction",
            "family": "fraction",
            "condition": "Ab2d+spec",
            "seed": "2026072002",
            "primary_is_rescued": True,
            "posthoc_is_rescued": True,
            "is_incremental_posthoc_pass": False,
            "baseline_outcome": "FAILED",
            "surface_failure_layer": "L2",
            "root_mechanism_layer": "L2_CONTRACT_SCHEMA_ENTRYPOINT",
            "surface_failure": "schema_failure",
            "root_mechanism": "Model wrapped output payload in a single-key JSON dictionary object instead of raw expression format.",
            "rule_id": "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
            "precondition_evidence": "Frozen precondition symptom matched: L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP (single-key dictionary wrapping output)",
            "before_snippet_hash": "61c5bbe666505b451b43d5c8cf341dcd1fe6d08781be401035c5c30e6da55714",
            "after_snippet_hash": "5c0096122f64bcc5a63e9f767029c35f9aa9ebf402f9346e4608727a2a9116fc",
            "unified_diff": "UNRESOLVED_SOURCE_NOT_COMMITTED",
            "source_span": "UNRESOLVED_SHA_ONLY",
            "changed_line_count": -1,
            "changed_ast_node_count": -1,
            "changed_ast_node_types": [],
            "tree_depth_range": "UNRESOLVED",
            "control_flow_changed": "UNRESOLVED",
            "literals_changed": "UNRESOLVED",
            "function_signature_changed": "UNRESOLVED",
            "semantic_operator_changed": "UNRESOLVED",
            "primary_disposition": "MODIFIED_RESCUED",
            "posthoc_disposition": "MODIFIED_RESCUED",
            "final_pass_fail": "PASS",
            "oracle_answer_used": False,
            "unique": "TRUE",
            "local": "TRUE",
            "offline_verifiable": "TRUE",
            "repair_signature_match": "AMBIGUOUS_SIGNATURE_MATCH",
            "evidence_citation": "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/healer_results.jsonl",
            "analyst_notes": "Identical behavior in Primary and Post-hoc. Fraction family L2 wrap safely unnested."
        },
        {
            "cell_id": "qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2g__seed_2026072003",
            "model": "qwen3_5_4b",
            "task_id": "ce113_q01_negative_fraction_subtraction",
            "family": "fraction",
            "condition": "Ab2g",
            "seed": "2026072003",
            "primary_is_rescued": True,
            "posthoc_is_rescued": True,
            "is_incremental_posthoc_pass": False,
            "baseline_outcome": "FAILED",
            "surface_failure_layer": "L2",
            "root_mechanism_layer": "L2_CONTRACT_SCHEMA_ENTRYPOINT",
            "surface_failure": "schema_failure",
            "root_mechanism": "Model wrapped output payload in a single-key JSON dictionary object instead of raw expression format.",
            "rule_id": "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
            "precondition_evidence": "Frozen precondition symptom matched: L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP (single-key dictionary wrapping output)",
            "before_snippet_hash": "8699b3c183676d9e7b28d43998acb688d45ab70864ee1f88fb49d710caa1e020",
            "after_snippet_hash": "f5d064162554e6256e5ee44ad4f0810b1ba0990a51f18e3eb7374e280320db05",
            "unified_diff": "UNRESOLVED_SOURCE_NOT_COMMITTED",
            "source_span": "UNRESOLVED_SHA_ONLY",
            "changed_line_count": -1,
            "changed_ast_node_count": -1,
            "changed_ast_node_types": [],
            "tree_depth_range": "UNRESOLVED",
            "control_flow_changed": "UNRESOLVED",
            "literals_changed": "UNRESOLVED",
            "function_signature_changed": "UNRESOLVED",
            "semantic_operator_changed": "UNRESOLVED",
            "primary_disposition": "MODIFIED_RESCUED",
            "posthoc_disposition": "MODIFIED_RESCUED",
            "final_pass_fail": "PASS",
            "oracle_answer_used": False,
            "unique": "TRUE",
            "local": "TRUE",
            "offline_verifiable": "TRUE",
            "repair_signature_match": "AMBIGUOUS_SIGNATURE_MATCH",
            "evidence_citation": "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/healer_results.jsonl",
            "analyst_notes": "Identical behavior in Primary and Post-hoc. Fraction family under Ab2g safely rescued."
        },
        {
            "cell_id": "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301",
            "model": "qwen3_5_4b",
            "task_id": "ce115_calc_radical_simplification_l1",
            "family": "radical",
            "condition": "Ab2d+api",
            "seed": "2026071301",
            "primary_is_rescued": False,
            "posthoc_is_rescued": True,
            "is_incremental_posthoc_pass": True,
            "baseline_outcome": "FAILED",
            "surface_failure_layer": "L2",
            "root_mechanism_layer": "L2_CONTRACT_SCHEMA_ENTRYPOINT",
            "surface_failure": "schema_failure",
            "root_mechanism": "Model wrapped output payload in a single-key JSON dictionary object instead of raw expression format.",
            "rule_id": "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
            "precondition_evidence": "Frozen precondition symptom matched: L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP (single-key dictionary wrapping output)",
            "before_snippet_hash": "c74c03157866c1b595bf9dfdaffcdb351de06215e6dd08aa465bf14f2ae95c1d",
            "after_snippet_hash": "ac6299da36256125e27fc76c71bb76ff1ef1b31939f71e72fc22df1f4b092aaf",
            "unified_diff": "UNRESOLVED_SOURCE_NOT_COMMITTED",
            "source_span": "UNRESOLVED_SHA_ONLY",
            "changed_line_count": -1,
            "changed_ast_node_count": -1,
            "changed_ast_node_types": [],
            "tree_depth_range": "UNRESOLVED",
            "control_flow_changed": "UNRESOLVED",
            "literals_changed": "UNRESOLVED",
            "function_signature_changed": "UNRESOLVED",
            "semantic_operator_changed": "UNRESOLVED",
            "primary_disposition": "NO_OP",
            "posthoc_disposition": "MODIFIED_RESCUED",
            "final_pass_fail": "PASS",
            "oracle_answer_used": False,
            "unique": "TRUE",
            "local": "TRUE",
            "offline_verifiable": "TRUE",
            "repair_signature_match": "AMBIGUOUS_SIGNATURE_MATCH",
            "evidence_citation": "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/healer_results.jsonl",
            "analyst_notes": "INCREMENTAL POST-HOC PASS (+1 cell). Primary run had false-loop rollback triggered (Primary disposition NO_OP). Post-hoc corrected-chain removed false-loop rollback, retaining L2 wrap transformation to achieve formal PASS."
        },
        {
            "cell_id": "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026072002",
            "model": "qwen3_5_4b",
            "task_id": "ce115_calc_radical_simplification_l1",
            "family": "radical",
            "condition": "Ab2d+api",
            "seed": "2026072002",
            "primary_is_rescued": True,
            "posthoc_is_rescued": True,
            "is_incremental_posthoc_pass": False,
            "baseline_outcome": "FAILED",
            "surface_failure_layer": "L2",
            "root_mechanism_layer": "L2_CONTRACT_SCHEMA_ENTRYPOINT",
            "surface_failure": "schema_failure",
            "root_mechanism": "Model wrapped output payload in a single-key JSON dictionary object instead of raw expression format.",
            "rule_id": "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
            "precondition_evidence": "Frozen precondition symptom matched: L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP (single-key dictionary wrapping output)",
            "before_snippet_hash": "d9af6acf3f2f1a9fbe9e608dc1895e06bf5879f8a1fbb98c4a0e62fd686e4858",
            "after_snippet_hash": "0ddd4fb757580b67e7f6e9ba0c57a665a96f20e0a445ca54d97f2fe567610a25",
            "unified_diff": "UNRESOLVED_SOURCE_NOT_COMMITTED",
            "source_span": "UNRESOLVED_SHA_ONLY",
            "changed_line_count": -1,
            "changed_ast_node_count": -1,
            "changed_ast_node_types": [],
            "tree_depth_range": "UNRESOLVED",
            "control_flow_changed": "UNRESOLVED",
            "literals_changed": "UNRESOLVED",
            "function_signature_changed": "UNRESOLVED",
            "semantic_operator_changed": "UNRESOLVED",
            "primary_disposition": "MODIFIED_RESCUED",
            "posthoc_disposition": "MODIFIED_RESCUED",
            "final_pass_fail": "PASS",
            "oracle_answer_used": False,
            "unique": "TRUE",
            "local": "TRUE",
            "offline_verifiable": "TRUE",
            "repair_signature_match": "AMBIGUOUS_SIGNATURE_MATCH",
            "evidence_citation": "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/healer_results.jsonl",
            "analyst_notes": "Identical behavior in Primary and Post-hoc. Radical family under Ab2d+api safely rescued."
        },
        {
            "cell_id": "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d_spec_v2__seed_2026071301",
            "model": "qwen3_5_4b",
            "task_id": "ce115_calc_radical_simplification_l1",
            "family": "radical",
            "condition": "Ab2d+spec",
            "seed": "2026071301",
            "primary_is_rescued": True,
            "posthoc_is_rescued": True,
            "is_incremental_posthoc_pass": False,
            "baseline_outcome": "FAILED",
            "surface_failure_layer": "L2",
            "root_mechanism_layer": "L2_CONTRACT_SCHEMA_ENTRYPOINT",
            "surface_failure": "schema_failure",
            "root_mechanism": "Model wrapped output payload in a single-key JSON dictionary object instead of raw expression format.",
            "rule_id": "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
            "precondition_evidence": "Frozen precondition symptom matched: L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP (single-key dictionary wrapping output)",
            "before_snippet_hash": "b2006e371ba0db41cb0bf5639a8bc10001f58b25a58ed3186028ea9e727e1a9d",
            "after_snippet_hash": "a03ab5c3aa293ec62608839352f34456f0252a5d8752f31674ea58a39a2d33f2",
            "unified_diff": "UNRESOLVED_SOURCE_NOT_COMMITTED",
            "source_span": "UNRESOLVED_SHA_ONLY",
            "changed_line_count": -1,
            "changed_ast_node_count": -1,
            "changed_ast_node_types": [],
            "tree_depth_range": "UNRESOLVED",
            "control_flow_changed": "UNRESOLVED",
            "literals_changed": "UNRESOLVED",
            "function_signature_changed": "UNRESOLVED",
            "semantic_operator_changed": "UNRESOLVED",
            "primary_disposition": "MODIFIED_RESCUED",
            "posthoc_disposition": "MODIFIED_RESCUED",
            "final_pass_fail": "PASS",
            "oracle_answer_used": False,
            "unique": "TRUE",
            "local": "TRUE",
            "offline_verifiable": "TRUE",
            "repair_signature_match": "AMBIGUOUS_SIGNATURE_MATCH",
            "evidence_citation": "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/healer_results.jsonl",
            "analyst_notes": "Identical behavior in Primary and Post-hoc. Radical family under Ab2d+spec safely rescued."
        }
    ]

    # 1. six_cell_audit_records.jsonl
    with open(OUTPUT_DIR / "six_cell_audit_records.jsonl", "w", encoding="utf-8") as f:
        for c in cells:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    # 2. six_cell_audit_table.csv
    csv_fields = [
        "cell_id", "model", "task_id", "family", "condition", "seed",
        "primary_disposition", "posthoc_disposition", "final_pass_fail",
        "surface_failure_layer", "root_mechanism_layer", "rule_id",
        "oracle_answer_used", "unique", "local", "offline_verifiable",
        "repair_signature_match", "before_snippet_hash", "after_snippet_hash"
    ]
    with open(OUTPUT_DIR / "six_cell_audit_table.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction="ignore")
        writer.writeheader()
        for c in cells:
            writer.writerow(c)

    # 3. condition_family_crosstab.csv
    # Fixed layout: Condition | Radical | Fraction | Integer | Polynomial | Total
    cf_data = [
        {"Condition": "Ab1", "Radical": 0, "Fraction": 0, "Integer": 0, "Polynomial": 0, "Total": 0},
        {"Condition": "Ab2g", "Radical": 1, "Fraction": 1, "Integer": 0, "Polynomial": 0, "Total": 2},
        {"Condition": "Ab2d+api", "Radical": 2, "Fraction": 0, "Integer": 0, "Polynomial": 0, "Total": 2},
        {"Condition": "Ab2d+spec", "Radical": 1, "Fraction": 1, "Integer": 0, "Polynomial": 0, "Total": 2},
    ]
    with open(OUTPUT_DIR / "condition_family_crosstab.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Condition", "Radical", "Fraction", "Integer", "Polynomial", "Total"])
        writer.writeheader()
        writer.writerows(cf_data)

    # 4. condition_failure_layer_crosstab.csv
    cfl_data = [
        {"Condition": "Ab1", "L1_PARSE_SYNTAX": 0, "L2_CONTRACT_SCHEMA_ENTRYPOINT": 0, "L3_DOMAIN_API": 0, "L4_RUNTIME_EXECUTION": 0, "L5_SEMANTIC_ANSWER": 0, "UNRESOLVED": 0, "Total": 0},
        {"Condition": "Ab2g", "L1_PARSE_SYNTAX": 0, "L2_CONTRACT_SCHEMA_ENTRYPOINT": 2, "L3_DOMAIN_API": 0, "L4_RUNTIME_EXECUTION": 0, "L5_SEMANTIC_ANSWER": 0, "UNRESOLVED": 0, "Total": 2},
        {"Condition": "Ab2d+api", "L1_PARSE_SYNTAX": 0, "L2_CONTRACT_SCHEMA_ENTRYPOINT": 2, "L3_DOMAIN_API": 0, "L4_RUNTIME_EXECUTION": 0, "L5_SEMANTIC_ANSWER": 0, "UNRESOLVED": 0, "Total": 2},
        {"Condition": "Ab2d+spec", "L1_PARSE_SYNTAX": 0, "L2_CONTRACT_SCHEMA_ENTRYPOINT": 2, "L3_DOMAIN_API": 0, "L4_RUNTIME_EXECUTION": 0, "L5_SEMANTIC_ANSWER": 0, "UNRESOLVED": 0, "Total": 2},
    ]
    with open(OUTPUT_DIR / "condition_failure_layer_crosstab.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Condition", "L1_PARSE_SYNTAX", "L2_CONTRACT_SCHEMA_ENTRYPOINT", "L3_DOMAIN_API", "L4_RUNTIME_EXECUTION", "L5_SEMANTIC_ANSWER", "UNRESOLVED", "Total"])
        writer.writeheader()
        writer.writerows(cfl_data)

    # 5. condition_rule_crosstab.csv
    cr_data = [
        {"Condition": "Ab1", "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP": 0, "Total": 0},
        {"Condition": "Ab2g", "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP": 2, "Total": 2},
        {"Condition": "Ab2d+api", "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP": 2, "Total": 2},
        {"Condition": "Ab2d+spec", "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP": 2, "Total": 2},
    ]
    with open(OUTPUT_DIR / "condition_rule_crosstab.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Condition", "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP", "Total"])
        writer.writeheader()
        writer.writerows(cr_data)

    # 6. condition_primary_posthoc_crosstab.csv
    cpp_data = [
        {"Condition": "Ab1", "Primary rescued": 0, "Incremental Post-hoc PASS": 0, "Post-hoc rescued total": 0},
        {"Condition": "Ab2g", "Primary rescued": 2, "Incremental Post-hoc PASS": 0, "Post-hoc rescued total": 2},
        {"Condition": "Ab2d+api", "Primary rescued": 1, "Incremental Post-hoc PASS": 1, "Post-hoc rescued total": 2},
        {"Condition": "Ab2d+spec", "Primary rescued": 2, "Incremental Post-hoc PASS": 0, "Post-hoc rescued total": 2},
    ]
    with open(OUTPUT_DIR / "condition_primary_posthoc_crosstab.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Condition", "Primary rescued", "Incremental Post-hoc PASS", "Post-hoc rescued total"])
        writer.writeheader()
        writer.writerows(cpp_data)

    # 7. condition_denominator_table.csv
    # 320-cell Qwen4B results per condition:
    # Ab1: total 80, baseline_pass 15, baseline_fail 65, eligible 1, primary_rescued 0, posthoc_rescued 0, rescued/FAIL 0/65 (0.0%), rescued/eligible 0/1 (0.0%)
    # Ab2g: total 80, baseline_pass 19, baseline_fail 61, eligible 3, primary_rescued 2, posthoc_rescued 2, rescued/FAIL 2/61 (3.28%), rescued/eligible 2/3 (66.67%)
    # Ab2d+api: total 80, baseline_pass 8, baseline_fail 72, eligible 3, primary_rescued 1, posthoc_rescued 2, rescued/FAIL 2/72 (2.78%), rescued/eligible 2/3 (66.67%)
    # Ab2d+spec: total 80, baseline_pass 36, baseline_fail 44, eligible 3, primary_rescued 2, posthoc_rescued 2, rescued/FAIL 2/44 (4.55%), rescued/eligible 2/3 (66.67%)
    cd_data = [
        {"Condition": "Ab1", "Total Cells": 80, "Baseline PASS": 15, "Baseline FAIL": 65, "Eligible": 1, "Primary Rescued": 0, "Post-hoc Rescued": 0, "Rescued/FAIL Rate": "0.00% (0/65)", "Rescued/Eligible Rate": "0.00% (0/1)"},
        {"Condition": "Ab2g", "Total Cells": 80, "Baseline PASS": 19, "Baseline FAIL": 61, "Eligible": 3, "Primary Rescued": 2, "Post-hoc Rescued": 2, "Rescued/FAIL Rate": "3.28% (2/61)", "Rescued/Eligible Rate": "66.67% (2/3)"},
        {"Condition": "Ab2d+api", "Total Cells": 80, "Baseline PASS": 8, "Baseline FAIL": 72, "Eligible": 3, "Primary Rescued": 1, "Post-hoc Rescued": 2, "Rescued/FAIL Rate": "2.78% (2/72)", "Rescued/Eligible Rate": "66.67% (2/3)"},
        {"Condition": "Ab2d+spec", "Total Cells": 80, "Baseline PASS": 36, "Baseline FAIL": 44, "Eligible": 3, "Primary Rescued": 2, "Post-hoc Rescued": 2, "Rescued/FAIL Rate": "4.55% (2/44)", "Rescued/Eligible Rate": "66.67% (2/3)"},
        {"Condition": "Total (Qwen4B)", "Total Cells": 320, "Baseline PASS": 78, "Baseline FAIL": 242, "Eligible": 10, "Primary Rescued": 5, "Post-hoc Rescued": 6, "Rescued/FAIL Rate": "2.48% (6/242)", "Rescued/Eligible Rate": "60.00% (6/10)"},
    ]
    with open(OUTPUT_DIR / "condition_denominator_table.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Condition", "Total Cells", "Baseline PASS", "Baseline FAIL", "Eligible", "Primary Rescued", "Post-hoc Rescued", "Rescued/FAIL Rate", "Rescued/Eligible Rate"])
        writer.writeheader()
        writer.writerows(cd_data)

    # 8. repair_signature_catalog.json
    repair_catalog = {
        "catalog_id": "math16_posthoc_repair_signature_catalog_v1",
        "preregistered_rule": "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
        "description": "Strips single-key JSON wrapper dict surrounding expression output, extracting raw expression string.",
        "precondition": "Output parses as JSON object with exactly one key containing expression payload string.",
        "transformation": "Extract string payload from the single dictionary key.",
        "safety_properties": {
            "deterministic": True,
            "oracle_answer_used": False,
            "unique_solution": True,
            "local_edit": True,
            "offline_verifiable": True
        },
        "rescued_cells": [c["cell_id"] for c in cells]
    }
    with open(OUTPUT_DIR / "repair_signature_catalog.json", "w", encoding="utf-8") as f:
        json.dump(repair_catalog, f, indent=2, ensure_ascii=False)

    # 9. audit_evidence_index.json
    evidence_index = {
        "index_id": "math16_posthoc_six_cell_audit_evidence_index_v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "taxonomy_json": "docs/experiments/manifests/math16_posthoc_shared_taxonomy_v1.json",
            "spec_md": "docs/experiments/design/math16_posthoc_six_cell_rescue_audit_v1_spec.md",
            "manifest_json": "docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_manifest.json",
            "comparison_json": "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/primary_vs_corrected_chain_comparison.json",
            "primary_records": "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligible_execution_records.jsonl",
            "healer_results_jsonl": "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/healer_results.jsonl"
        },
        "cell_count": len(cells),
        "primary_rescued": 5,
        "posthoc_rescued": 6,
        "incremental_posthoc": 1
    }
    with open(OUTPUT_DIR / "audit_evidence_index.json", "w", encoding="utf-8") as f:
        json.dump(evidence_index, f, indent=2, ensure_ascii=False)

    print(f"All 9 formal artifacts successfully written to: {OUTPUT_DIR}")

if __name__ == "__main__":
    build_formal_artifacts()
