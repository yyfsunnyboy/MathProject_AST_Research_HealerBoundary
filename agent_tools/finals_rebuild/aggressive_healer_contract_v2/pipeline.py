# -*- coding: utf-8 -*-
"""Contract-Aware Aggressive Healer v2 pipeline (proof-carrying; answer/evaluator blind)."""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

from agent_tools.finals_rebuild.artifacts import sha256_json, sha256_text
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.contracts import (
    load_all_contracts,
    load_contract,
    build_all_contracts,
)
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.rules import (
    pc_r01_answer_source_rewire as r01,
    pc_r02_operand_order as r02,
    pc_r03_domain_api_normalize as r03,
    pc_r04_unique_process_wiring as r04,
)
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.types import PipelineOutcome

ROOT = Path(__file__).resolve().parents[3]
ARTIFACT_ROOT = ROOT / "artifacts/math16_contract_aware_aggressive_healer_v2"
FORMAL_V2 = ROOT / "artifacts/math16_ab2d_menu_vs_full_runtime_contract_v2/formal"

# Fixed freeze-time sequence (do not reorder after freeze without new version)
RULE_ORDER: list[tuple[str, Callable[..., Any]]] = [
    (r01.RULE_ID, r01.apply_once),
    (r02.RULE_ID, r02.apply_once),
    (r03.RULE_ID, r03.apply_once),
    (r04.RULE_ID, r04.apply_once),
]

RULE_MODULES = {
    r01.RULE_ID: r01,
    r02.RULE_ID: r02,
    r03.RULE_ID: r03,
    r04.RULE_ID: r04,
}


def apply_contract_aware_v2(
    source: str,
    *,
    task_id: str,
    condition: str,
    cell_id: str = "",
    model_key: str = "",
    contract: Optional[dict[str, Any]] = None,
) -> PipelineOutcome:
    """Apply PC rules once each in freeze order. Never reads evaluator / expected answers."""
    if contract is None:
        contract = load_contract(task_id, condition)
    pre_sha = sha256_text(source)
    cur = source
    logs: list[dict[str, Any]] = []
    certs: list[dict[str, Any]] = []
    abstentions: list[dict[str, Any]] = []
    fired: list[str] = []
    for rule_id, apply_fn in RULE_ORDER:
        outcome = apply_fn(
            cur,
            contract=contract,
            cell_id=cell_id,
            task_id=task_id,
            condition=condition,
            model_key=model_key,
        )
        logs.append(outcome.to_audit_dict())
        if outcome.certificate is not None:
            cdict = outcome.certificate.to_dict()
            if outcome.applied:
                certs.append(cdict)
                fired.append(rule_id)
                cur = outcome.source_out
            else:
                abstentions.append(cdict)
    post_sha = sha256_text(cur)
    return PipelineOutcome(
        cell_id=cell_id,
        task_id=task_id,
        condition=condition,
        model_key=model_key,
        pre_source_sha256=pre_sha,
        post_source_sha256=post_sha,
        source_modified=pre_sha != post_sha,
        rules_fired=fired,
        rule_logs=logs,
        certificates=certs,
        abstentions=abstentions,
        proposed_repair_count=len(certs),
        formal_artifact_write=False,
        source_out=cur,
    )


def _iter_formal_cells(
    *,
    outcomes_filter: Optional[set[str]] = None,
    conditions: Optional[set[str]] = None,
    models: Optional[set[str]] = None,
) -> list[dict[str, Any]]:
    rows = []
    for p in FORMAL_V2.rglob("artifact.json"):
        art = json.loads(p.read_text(encoding="utf-8"))
        outcome = art.get("outcome")
        if outcomes_filter is not None and outcome not in outcomes_filter:
            continue
        cond = art.get("condition")
        if conditions is not None and cond not in conditions:
            continue
        mk = art.get("model_key")
        if models is not None and mk not in models:
            continue
        d = p.parent
        src_path = d / "extracted_source.py"
        if not src_path.exists():
            continue
        rows.append(
            {
                "cell_id": art["cell_id"],
                "task_id": art["task_id"],
                "condition": cond,
                "model_key": mk,
                "seed": art.get("seed"),
                "outcome": outcome,
                "source": src_path.read_text(encoding="utf-8", errors="replace"),
                "cell_dir": str(d),
            }
        )
    return rows


def run_frozen_validation_bundle(*, write_artifacts: bool = True) -> dict[str, Any]:
    """Build contracts, freeze manifest, development replay, safety, menu validation."""
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    for sub in (
        "contracts",
        "checker_audit",
        "proposed_repairs",
        "certificates",
        "frozen_manifest",
        "summaries",
    ):
        (ARTIFACT_ROOT / sub).mkdir(parents=True, exist_ok=True)

    built = build_all_contracts(write=True)
    contracts = built["contracts"]
    index = built["index"]

    # Head
    try:
        head = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(ROOT), text=True).strip()
        )
    except Exception:
        head = "UNKNOWN"

    # Rule source SHAs
    rule_source_shas = {}
    for rid, mod in RULE_MODULES.items():
        path = Path(mod.__file__).resolve()
        rule_source_shas[rid] = {
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256_text(path.read_text(encoding="utf-8")),
            "version": getattr(mod, "RULE_VERSION", "unknown"),
            "discovery_cells": list(getattr(mod, "DISCOVERY_CELLS", [])),
            "debugging_cells": list(getattr(mod, "DEBUGGING_CELLS", [])),
            "positive_examples": list(getattr(mod, "POSITIVE_EXAMPLES", [])),
            "negative_examples": list(getattr(mod, "NEGATIVE_EXAMPLES", [])),
        }

    cert_schema = {
        "fields": [
            "rule_id",
            "decision",
            "contract_id",
            "contract_sha256",
            "contract_clause",
            "ast_location",
            "before_snippet",
            "after_snippet",
            "before_source_sha256",
            "after_source_sha256",
            "candidate_count",
            "preconditions",
            "postconditions",
            "changed_ast_nodes",
            "unrelated_ast_unchanged",
            "expected_answer_not_read",
            "evaluator_result_not_read",
            "candidate_trial_count",
            "ACCEPT/ABSTAIN",
        ]
    }
    cert_schema_sha = sha256_json(cert_schema)

    # Development cells = 21 full-plan FAIL
    full_fails = _iter_formal_cells(
        outcomes_filter=None,
        conditions={"ab2d_full_v2"},
    )
    full_fails = [r for r in full_fails if r["outcome"] != "passed"]
    assert len(full_fails) == 21, f"expected 21 full fails, got {len(full_fails)}"

    dev_results = []
    rule_accept = {rid: 0 for rid, _ in RULE_ORDER}
    rule_abstain = {rid: 0 for rid, _ in RULE_ORDER}
    for row in full_fails:
        out = apply_contract_aware_v2(
            row["source"],
            task_id=row["task_id"],
            condition=row["condition"],
            cell_id=row["cell_id"],
            model_key=row["model_key"],
        )
        for log in out.rule_logs:
            rid = log["rule_id"]
            if log["applied"]:
                rule_accept[rid] = rule_accept.get(rid, 0) + 1
            else:
                rule_abstain[rid] = rule_abstain.get(rid, 0) + 1
        rec = {
            "cell_id": row["cell_id"],
            "task_id": row["task_id"],
            "model_key": row["model_key"],
            "raw_outcome": row["outcome"],
            "source_modified": out.source_modified,
            "rules_fired": out.rules_fired,
            "proposed_repair_count": out.proposed_repair_count,
            "certificates": out.certificates,
            "abstention_reasons": [
                a.get("abstention_reason") for a in out.abstentions if a.get("abstention_reason")
            ],
        }
        dev_results.append(rec)
        if write_artifacts:
            for cert in out.certificates:
                cid = f"{cert['rule_id']}__{row['cell_id']}"
                (ARTIFACT_ROOT / "certificates" / f"{cid}.json").write_text(
                    json.dumps(cert, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
                )
            if out.source_modified:
                (ARTIFACT_ROOT / "proposed_repairs" / f"{row['cell_id']}.json").write_text(
                    json.dumps(
                        {
                            "cell_id": row["cell_id"],
                            "pre_source_sha256": out.pre_source_sha256,
                            "post_source_sha256": out.post_source_sha256,
                            "rules_fired": out.rules_fired,
                            "post_source": None,  # store sha only in summary; large sources in cert diffs
                            "note": "formal artifacts not overwritten; repair suggestion only",
                        },
                        ensure_ascii=False,
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )
                # Store proposed source text under proposed_repairs as .py for inspection
                post_src = apply_contract_aware_v2(
                    row["source"],
                    task_id=row["task_id"],
                    condition=row["condition"],
                    cell_id=row["cell_id"],
                    model_key=row["model_key"],
                )
                # get actual post via re-apply
                src_out = row["source"]
                for _, apply_fn in RULE_ORDER:
                    o = apply_fn(
                        src_out,
                        contract=load_contract(row["task_id"], row["condition"]),
                        cell_id=row["cell_id"],
                        task_id=row["task_id"],
                        condition=row["condition"],
                        model_key=row["model_key"],
                    )
                    if o.applied:
                        src_out = o.source_out
                (ARTIFACT_ROOT / "proposed_repairs" / f"{row['cell_id']}.py").write_text(
                    src_out, encoding="utf-8"
                )

    # Known rewrite cells should abstain all PC rules (no proposed repair).
    # Use prior census list of 13 REWRITE cells approximating: if not in ACCEPT fired, ok
    # For summary: cells with any ACCEPT
    accept_cells = [r["cell_id"] for r in dev_results if r["proposed_repair_count"] > 0]
    abstain_only_cells = [r["cell_id"] for r in dev_results if r["proposed_repair_count"] == 0]

    # Safety: 381 PASS
    passes = _iter_formal_cells(outcomes_filter={"passed"})
    safety = {
        "n_pass_cells": len(passes),
        "proposed_repair": 0,
        "source_modification": 0,
        "regression": 0,
        "modified_cell_ids": [],
    }
    for row in passes:
        out = apply_contract_aware_v2(
            row["source"],
            task_id=row["task_id"],
            condition=row["condition"],
            cell_id=row["cell_id"],
            model_key=row["model_key"],
        )
        if out.proposed_repair_count or out.source_modified:
            safety["proposed_repair"] += out.proposed_repair_count
            if out.source_modified:
                safety["source_modification"] += 1
                safety["modified_cell_ids"].append(row["cell_id"])
                safety["regression"] += 1  # any PASS mutation is treated as regression risk

    # Menu 78 FAIL
    menu_fails = _iter_formal_cells(
        conditions={"ab2d_domain_menu_v2"},
    )
    menu_fails = [r for r in menu_fails if r["outcome"] != "passed"]
    menu_results = []
    menu_accept = 0
    menu_fullplan_forced = 0
    for row in menu_fails:
        out = apply_contract_aware_v2(
            row["source"],
            task_id=row["task_id"],
            condition=row["condition"],
            cell_id=row["cell_id"],
            model_key=row["model_key"],
        )
        # R02/R04 must not fire on menu
        forced = any(rid in out.rules_fired for rid in (r02.RULE_ID, r04.RULE_ID))
        if forced:
            menu_fullplan_forced += 1
        if out.proposed_repair_count:
            menu_accept += 1
        menu_results.append(
            {
                "cell_id": row["cell_id"],
                "rules_fired": out.rules_fired,
                "proposed_repair_count": out.proposed_repair_count,
                "source_modified": out.source_modified,
            }
        )

    referenced_dev_ids = sorted({c for r in dev_results for c in [r["cell_id"]]})
    for mod in RULE_MODULES.values():
        for lst_name in ("DISCOVERY_CELLS", "DEBUGGING_CELLS", "POSITIVE_EXAMPLES", "NEGATIVE_EXAMPLES"):
            for cid in getattr(mod, lst_name, []):
                if cid not in referenced_dev_ids:
                    referenced_dev_ids.append(cid)
    referenced_dev_ids = sorted(set(referenced_dev_ids))

    freeze_ts = datetime.now(timezone.utc).isoformat()
    frozen = {
        "healer": "contract_aware_aggressive_healer_v2",
        "version": "v2.0.0",
        "freeze_timestamp_utc": freeze_ts,
        "git_HEAD": head,
        "rule_execution_order": [rid for rid, _ in RULE_ORDER],
        "rules": rule_source_shas,
        "contract_index_sha256": index["index_sha256"],
        "contract_sha256_by_id": index["contract_sha256_by_id"],
        "certificate_schema_sha256": cert_schema_sha,
        "certificate_schema": cert_schema,
        "referenced_development_cell_ids": referenced_dev_ids,
        "n_contracts": index["n_contracts"],
        "policy": {
            "answer_blind": True,
            "evaluator_blind": True,
            "no_multi_candidate_trial": True,
            "fail_closed_abstention": True,
            "no_formal_artifact_overwrite": True,
            "post_freeze_rule_edit_forbidden": True,
        },
        "rules_modified_after_freeze": False,
    }
    frozen["frozen_manifest_sha256"] = sha256_json(
        {k: v for k, v in frozen.items() if k != "frozen_manifest_sha256"}
    )

    summary = {
        "contracts_loaded": index["n_contracts"],
        "contract_index_sha256": index["index_sha256"],
        "rule_accept_counts": rule_accept,
        "rule_abstain_counts": rule_abstain,
        "development_replay": {
            "n_cells": len(dev_results),
            "accept_cells": accept_cells,
            "n_accept_cells": len(accept_cells),
            "n_abstain_only_cells": len(abstain_only_cells),
            "results": dev_results,
        },
        "safety_benchmark_381": safety,
        "menu_validation_78": {
            "n_cells": len(menu_fails),
            "n_with_proposed_repair": menu_accept,
            "full_plan_rules_forced_count": menu_fullplan_forced,
            "results": menu_results,
        },
        "frozen_manifest_sha256": frozen["frozen_manifest_sha256"],
        "referenced_development_cell_ids": referenced_dev_ids,
        "rules_modified_after_freeze": False,
    }

    if write_artifacts:
        (ARTIFACT_ROOT / "frozen_manifest" / "frozen_manifest_v2_0_0.json").write_text(
            json.dumps(frozen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (ARTIFACT_ROOT / "summaries" / "dry_run_summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (ARTIFACT_ROOT / "checker_audit" / "development_replay.json").write_text(
            json.dumps(dev_results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (ARTIFACT_ROOT / "checker_audit" / "safety_381.json").write_text(
            json.dumps(safety, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (ARTIFACT_ROOT / "checker_audit" / "menu_78.json").write_text(
            json.dumps(menu_results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    return {"frozen": frozen, "summary": summary, "index": index}
