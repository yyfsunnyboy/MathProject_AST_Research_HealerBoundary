#!/usr/bin/env python3
"""Build the read-only 479-cell Historical Round 1 final-overlay audit.

Inputs are the already-built unified ledger and the sealed corrected-overlay
manifest.  No journals, manifests, overlays, or ledger inputs are changed.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
LEDGER = REPO / "docs/experiments/results/math16_three_model_historical_round1_unified_cell_ledger_v1/unified_cell_ledger.jsonl"
OVERLAY = REPO / "docs/experiments/manifests/math16_aggressive_round1_corrected_overlay_v1.json"
OUTDIR = REPO / "docs/experiments/results/math16_historical_round1_final_overlay_audit_v1"
AUDIT = OUTDIR / "final_overlay_audit.jsonl"
SUMMARY = OUTDIR / "validation_summary.json"
MANIFEST = OUTDIR / "sha256_manifest.json"


def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def text_sha256(path: Path) -> str:
    # Matches the repository's text-UTF-8 SHA convention for source artifacts.
    return hashlib.sha256(path.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail_if(condition: bool, message: str) -> None:
    if condition:
        raise RuntimeError(message)


def read_jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def source_check(repo: Path, path_value, sha_value):
    if not path_value or not sha_value:
        return False, False, None
    path = repo / path_value
    exists = path.is_file()
    actual = text_sha256(path) if exists else None
    return exists, actual == sha_value, actual


def main() -> None:
    ledger_rows = read_jsonl(LEDGER)
    overlay = json.loads(OVERLAY.read_text(encoding="utf-8"))
    anomaly = overlay["anomalous_cell"]
    sealed_audit = overlay["three_model_final_pass_sealed_source_consistency_v1"]

    fail_if(len(ledger_rows) != 960, f"ledger row count is {len(ledger_rows)}, not 960")
    fail_if(any(row["account_namespace"] != "historical_round1" for row in ledger_rows), "non-historical ledger row")
    fail_if(any("safety" in canon(row).lower() or "fixpoint" in canon(row).lower() for row in ledger_rows), "safety/fixpoint reference in ledger")

    selected = [row for row in ledger_rows if row["final_frozen_status"] == "PASS"]
    fail_if(len(selected) != 479, f"frozen PASS selection is {len(selected)}, not 479")
    target_id = anomaly["cell_id"]
    target_rows = [row for row in selected if row["raw_cell_id"] == target_id]
    fail_if(len(target_rows) != 1, f"overlay target selection count is {len(target_rows)}, not 1")
    target = target_rows[0]
    fail_if(target["final_frozen_source_path"] != anomaly["c5a_final_source_path"], "overlay before path does not match ledger frozen source")
    fail_if(target["final_frozen_source_sha256"] != anomaly["c5a_final_source_sha256_text_utf8"], "overlay before SHA does not match ledger frozen source")

    rows = []
    frozen_copy_mismatch = 0
    source_path_missing = 0
    source_sha_mismatch = 0
    overlay_before_after_sha_mismatch = 0
    for source in sorted(selected, key=lambda row: row["raw_cell_id"]):
        matched = source["raw_cell_id"] == target_id
        # The overlay is a one-cell correction.  It records the only changed
        # cell explicitly; every non-target's corrected result is its retained
        # frozen result.  This is an explicit target-scope application, not a
        # NULL-filling COALESCE of the ledger's sparse corrected columns.
        if matched:
            corrected_status = source["final_corrected_status"]
            corrected_path = source["final_corrected_source_path"]
            corrected_sha = source["final_corrected_source_sha256"]
            corrected_source_provenance = source["final_corrected_source_provenance"]
            corrected_status_provenance = source["final_corrected_status_provenance"]
            corrected_retention = "OVERLAY_TARGET"
        else:
            corrected_status = source["final_frozen_status"]
            corrected_path = source["final_frozen_source_path"]
            corrected_sha = source["final_frozen_source_sha256"]
            corrected_source_provenance = source["final_frozen_source_provenance"]
            corrected_status_provenance = "OVERLAY"
            corrected_retention = "OVERLAY_NON_TARGET_FROZEN_RETAINED"
        frozen_exists, frozen_ok, frozen_actual = source_check(REPO, source["final_frozen_source_path"], source["final_frozen_source_sha256"])
        corrected_exists, corrected_ok, corrected_actual = source_check(REPO, corrected_path, corrected_sha)
        source_path_missing += int(not frozen_exists) + int(not corrected_exists)
        source_sha_mismatch += int(not frozen_ok) + int(not corrected_ok)
        source_changed = (source["final_frozen_source_path"], source["final_frozen_source_sha256"]) != (corrected_path, corrected_sha)
        status_changed = source["final_frozen_status"] != corrected_status

        before_match = None
        after_match = None
        if matched:
            before_match = (source["final_frozen_source_path"] == anomaly["c5a_final_source_path"] and source["final_frozen_source_sha256"] == anomaly["c5a_final_source_sha256_text_utf8"])
            # Corrected outcome revalidates exactly the sealed C5a source; the
            # promotion mismatch is a source-label lineage defect, not new bytes.
            after_match = (corrected_path == anomaly["c5a_final_source_path"] and corrected_sha == anomaly["c5a_final_source_sha256_text_utf8"])
            overlay_before_after_sha_mismatch += int(not before_match) + int(not after_match)

        verdict = "PASS"
        if not (frozen_exists and frozen_ok and corrected_exists and corrected_ok):
            verdict = "FAIL_SOURCE_VERIFICATION"
        elif matched and not (before_match and after_match and status_changed and source["final_frozen_status"] == "PASS" and corrected_status == "FAIL"):
            verdict = "FAIL_OVERLAY_CHAIN"
        elif not matched and (status_changed or source_changed or source["formal_final_status"] != source["final_frozen_status"]):
            verdict = "FAIL_NON_TARGET_CHANGED"

        audit_row = {
            "schema_version": "math16_historical_round1_final_overlay_audit_v1",
            "account_namespace": "historical_round1",
            "model_group": source["model_group"],
            "raw_cell_id": source["raw_cell_id"],
            "canonical_identity": source["canonical_identity"],
            "frozen_final_status": source["final_frozen_status"],
            "frozen_final_source_path": source["final_frozen_source_path"],
            "frozen_final_source_sha256": source["final_frozen_source_sha256"],
            "frozen_final_source_provenance": source["final_frozen_source_provenance"],
            "frozen_final_status_provenance": source["final_frozen_status_provenance"],
            "frozen_final_evidence_refs": source["evidence_refs"],
            "overlay_matched": matched,
            "overlay_id": overlay["overlay_id"] if matched else None,
            "overlay_evidence_ref": "docs/experiments/manifests/math16_aggressive_round1_corrected_overlay_v1.json#anomalous_cell" if matched else None,
            "overlay_target_identity": target["canonical_identity"] if matched else None,
            "overlay_before_source_path": anomaly["c5a_final_source_path"] if matched else None,
            "overlay_before_source_sha256": anomaly["c5a_final_source_sha256_text_utf8"] if matched else None,
            "overlay_after_source_path": anomaly["c5a_final_source_path"] if matched else None,
            "overlay_after_source_sha256": anomaly["c5a_final_source_sha256_text_utf8"] if matched else None,
            "overlay_before_sha_matches_ledger": before_match,
            "overlay_after_sha_matches_ledger": after_match,
            "corrected_final_status": corrected_status,
            "corrected_final_source_path": corrected_path,
            "corrected_final_source_sha256": corrected_sha,
            "corrected_final_source_provenance": corrected_source_provenance,
            "corrected_final_status_provenance": corrected_status_provenance,
            "corrected_final_derivation": corrected_retention,
            "corrected_final_evidence_refs": source["evidence_refs"],
            "formal_final_account": source["formal_final_account"],
            "formal_final_status": source["formal_final_status"],
            "status_changed": status_changed,
            "source_changed": source_changed,
            "path_exists": frozen_exists and corrected_exists,
            "sha_verified": frozen_ok and corrected_ok,
            "frozen_fields_match_unified_ledger": True,
            "audit_verdict": verdict,
            "frozen_source_actual_sha256": frozen_actual,
            "corrected_source_actual_sha256": corrected_actual,
        }
        # Guard against accidental output transformation of frozen evidence.
        frozen_copy_mismatch += int(any(audit_row[key] != source[source_key] for key, source_key in (
            ("frozen_final_status", "final_frozen_status"),
            ("frozen_final_source_path", "final_frozen_source_path"),
            ("frozen_final_source_sha256", "final_frozen_source_sha256"),
            ("frozen_final_source_provenance", "final_frozen_source_provenance"),
            ("frozen_final_status_provenance", "final_frozen_status_provenance"),
        )))
        rows.append(audit_row)

    raw_counts = Counter(row["raw_cell_id"] for row in rows)
    identity_counts = Counter((row["model_group"], row["canonical_identity"]) for row in rows)
    frozen_by_model = Counter(row["model_group"] for row in rows)
    corrected_formal_by_model = Counter(row["model_group"] for row in rows if row["corrected_final_status"] == "PASS")
    transitions = Counter((row["frozen_final_status"], row["corrected_final_status"]) for row in rows)
    overlay_rows = [row for row in rows if row["overlay_matched"]]
    non_targets = [row for row in rows if not row["overlay_matched"]]
    missing = len(set(row["raw_cell_id"] for row in selected) - set(raw_counts))
    unmatched = len(set(raw_counts) - set(row["raw_cell_id"] for row in selected))
    duplicate = sum(count - 1 for count in raw_counts.values() if count > 1)
    identity_duplicate = sum(count - 1 for count in identity_counts.values() if count > 1)
    non_target_changed = sum(bool(row["status_changed"]) for row in non_targets)
    frozen_source_overwritten = frozen_copy_mismatch
    audit_verdict_failures = sum(row["audit_verdict"] != "PASS" for row in rows)
    formal_pass_total = sum(row["formal_final_status"] == "PASS" for row in rows)
    safety_fixpoint_rows = sum(row["account_namespace"] != "historical_round1" for row in rows)

    checks = {
        "audit_rows_479": len(rows) == 479,
        "unique_raw_identity_479": len(raw_counts) == 479,
        "frozen_by_model_88_102_289": dict(frozen_by_model) == {"qwen4b": 88, "qwen9b": 102, "gemini": 289},
        "duplicate_zero": duplicate == 0 and identity_duplicate == 0,
        "missing_zero": missing == 0,
        "unmatched_zero": unmatched == 0,
        "overlay_target_count_1": len(overlay_rows) == 1,
        "status_changed_count_1": sum(bool(row["status_changed"]) for row in rows) == 1,
        "pass_to_fail_count_1": transitions[("PASS", "FAIL")] == 1,
        "fail_to_pass_count_0": transitions[("FAIL", "PASS")] == 0,
        "non_target_478_unchanged": len(non_targets) == 478 and non_target_changed == 0,
        "corrected_formal_pass_478": formal_pass_total == 478,
        "corrected_formal_by_model_87_102_289": dict(corrected_formal_by_model) == {"qwen4b": 87, "qwen9b": 102, "gemini": 289},
        "frozen_fields_not_overwritten": frozen_source_overwritten == 0,
        "source_path_missing_zero": source_path_missing == 0,
        "source_sha_mismatch_zero": source_sha_mismatch == 0,
        "overlay_before_after_sha_identity_mismatch_zero": overlay_before_after_sha_mismatch == 0,
        "safety_fixpoint_rows_zero": safety_fixpoint_rows == 0,
        "all_audit_rows_pass": audit_verdict_failures == 0,
        "overlay_manifest_summary_agrees": sealed_audit["n_total"] == 479 and sealed_audit["pass_to_fail"] == 1 and sealed_audit["sealed_consistent_three_model_final_pass_n"] == 478 and sealed_audit["unique_mismatch_cell_id"] == target_id,
    }
    fail_if(not all(checks.values()), "audit invariants failed: " + ", ".join(key for key, value in checks.items() if not value))

    OUTDIR.mkdir(parents=True, exist_ok=True)
    AUDIT.write_text("".join(canon(row) + "\n" for row in rows), encoding="utf-8", newline="\n")
    summary = {
        "schema_version": "math16_historical_round1_final_overlay_audit_v1",
        "account_namespace": "historical_round1",
        "input": {"unified_ledger": str(LEDGER.relative_to(REPO)).replace("\\", "/"), "corrected_overlay": str(OVERLAY.relative_to(REPO)).replace("\\", "/")},
        "counts": {"audit_rows": len(rows), "unique_raw_identity": len(raw_counts), "duplicate": duplicate, "canonical_identity_duplicate": identity_duplicate, "missing": missing, "unmatched": unmatched, "frozen_final_pass_by_model": dict(sorted(frozen_by_model.items())), "corrected_formal_final_pass_by_model": dict(sorted(corrected_formal_by_model.items())), "corrected_formal_final_pass_total": formal_pass_total, "overlay_target_count": len(overlay_rows), "status_changed_count": sum(bool(row["status_changed"]) for row in rows), "pass_to_fail": transitions[("PASS", "FAIL")], "fail_to_pass": transitions[("FAIL", "PASS")], "non_target_count": len(non_targets), "non_target_status_changed": non_target_changed, "source_path_missing": source_path_missing, "source_sha_mismatch": source_sha_mismatch, "overlay_before_after_sha_identity_mismatch": overlay_before_after_sha_mismatch, "frozen_source_fields_overwritten": frozen_source_overwritten, "safety_benchmark_or_fixpoint_rows": safety_fixpoint_rows, "audit_verdict_failures": audit_verdict_failures},
        "unique_changed_cell": {"raw_cell_id": target_id, "canonical_identity": target["canonical_identity"], "frozen_status": target["final_frozen_status"], "corrected_status": target["final_corrected_status"], "frozen_source_path": target["final_frozen_source_path"], "frozen_source_sha256": target["final_frozen_source_sha256"], "overlay_evidence_ref": "docs/experiments/manifests/math16_aggressive_round1_corrected_overlay_v1.json#anomalous_cell", "lineage_exception_id": target["lineage_exception_id"]},
        "checks": checks,
        "verdict": "PASS",
    }
    SUMMARY.write_text(canon(summary) + "\n", encoding="utf-8", newline="\n")
    manifest = {"schema_version": "math16_historical_round1_final_overlay_audit_v1", "files": {str(path.relative_to(REPO)).replace("\\", "/"): file_sha256(path) for path in (Path(__file__), AUDIT, SUMMARY)}}
    MANIFEST.write_text(canon(manifest) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
