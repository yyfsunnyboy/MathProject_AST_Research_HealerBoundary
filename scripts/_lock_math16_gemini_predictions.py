"""One-shot helper to lock Gemini Phase 2 predictions (not part of frozen protocol)."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def clip(lo: float, hi: float) -> tuple[float, float]:
    return max(0.0, lo), min(100.0, hi)


def layer_band(count: int, fail_n: int, delta: float = 15.0) -> dict:
    share = (count / fail_n) * 100 if fail_n else 0.0
    lo, hi = clip(share - delta, share + delta)
    return {
        "seed1_count": count,
        "seed1_fail_denominator": fail_n,
        "seed1_share_pct": share,
        "tolerance_pp": delta,
        "predicted_share_pct_band": {"min": lo, "max": hi},
        "band_kind": "pre-registered tolerance bands, not confidence intervals",
    }


def main() -> None:
    pass_n, fail_n, total = 40, 8, 48
    pass_rate = pass_n / total * 100
    lo, hi = clip(pass_rate - 10, pass_rate + 10)
    n = 192
    cmin = int(math.ceil(lo / 100 * n - 1e-12))
    cmax = int(math.floor(hi / 100 * n + 1e-12))
    layers = {"L0": 0, "L1": 1, "L2": 0, "L3": 1, "L4": 1, "L5": 5}

    doc = {
        "prediction_id": "math16_gemini_multiseed_predictions_v1",
        "protocol_id": "MATH16-R06-FIXED",
        "phase": 2,
        "title": "Math16 Gemini Phase 2 multiseed prediction lock",
        "locked_before_generation": True,
        "band_kind_global": "pre-registered tolerance bands, not confidence intervals",
        "scope": {
            "model": "gemini-3.5-flash",
            "new_cells": 192,
            "formula": "1 model × 16 tasks × 3 conditions × 4 new seeds = 192",
            "new_seeds": [2026072001, 2026072002, 2026072003, 2026072004],
            "seed1_reused_not_regenerated": 2026071301,
            "seed1_directory": "docs/experiments/results/gemini35flash_math16_latex_v1_ab123_run_001",
            "generation_label": "repeated generations under fixed nominal seeds",
        },
        "baseline_sources": {
            "h0_pass_fail": "docs/experiments/results/gemini35flash_math16_latex_v1_ab123_run_001/evaluation_revision_003/cell_outcomes.json",
            "ab3": "docs/experiments/results/math16_ab3_full_report_data.json",
            "note": "PASS/FAIL from confirmatory revision_003. Failure layers mapped from revised_evaluator_status. No new-seed artifacts consulted.",
        },
        "tolerance_rules": {
            "h0_pass_rate_pp": 10,
            "failure_layer_share_among_fail_pp": 15,
            "proportion_clip": [0, 100],
            "trigger_count_on_192": [0, 4],
            "layer_exposure_on_192": [0, 4],
            "rescue_to_pass_on_192": [0, 2],
            "regression_on_192": 0,
            "band_kind": "pre-registered tolerance bands, not confidence intervals",
        },
        "model": {
            "model_tag": "gemini-3.5-flash",
            "seed1_run_id": "gemini35flash_math16_latex_v1_ab123_run_001",
            "new_cells_in_scope": 192,
            "h0_pass_rate": {
                "seed1_pass_numerator": pass_n,
                "seed1_pass_denominator": total,
                "seed1_pass_rate_pct": pass_rate,
                "seed1_fail_numerator": fail_n,
                "seed1_fail_denominator": total,
                "tolerance_pp": 10.0,
                "predicted_pass_rate_pct_band": {"min": lo, "max": hi},
                "implied_pass_count_band_on_192": {
                    "min_inclusive": cmin,
                    "max_inclusive": cmax,
                    "denominator": 192,
                    "exact_min_real": lo / 100 * 192,
                    "exact_max_real": hi / 100 * 192,
                    "derivation": "Counts c where 100*c/192 is inside the pass-rate band after clip.",
                },
                "band_kind": "pre-registered tolerance bands, not confidence intervals",
                "derivation": (
                    f"Seed1 confirmatory PASS {pass_n}/{total} = {pass_rate}%; "
                    "band = clip([rate-10, rate+10], 0..100)."
                ),
            },
            "failure_layer_share_among_fail": {
                "seed1_fail_denominator": fail_n,
                "tolerance_pp": 15.0,
                "band_kind": "pre-registered tolerance bands, not confidence intervals",
                "derivation": (
                    "Layer from revised_evaluator_status: PARSE_MINOR→L1, "
                    "LATEX_MISMATCH→L3, EXECUTION_FAILURE→L4, ANSWER_INCORRECT→L5."
                ),
                "layers": {k: layer_band(layers[k], fail_n) for k in ["L0", "L1", "L2", "L3", "L4", "L5"]},
            },
            "ab3_frozen_rule_generalization_on_192": {
                "band_kind": "pre-registered tolerance bands, not confidence intervals",
                "seed1_reference": {
                    "cells": 48,
                    "trigger_count": 0,
                    "layer_exposure": 0,
                    "rescue_to_pass": 0,
                    "regression": 0,
                    "source": "docs/experiments/results/math16_ab3_full_report_data.json",
                },
                "trigger_count": {
                    "numerator_min": 0,
                    "numerator_max": 4,
                    "denominator": 192,
                    "predicted_count_band": {"min": 0, "max": 4},
                    "derivation": "Protocol fixed band 0–4 / 192.",
                },
                "layer_exposure": {
                    "numerator_min": 0,
                    "numerator_max": 4,
                    "denominator": 192,
                    "predicted_count_band": {"min": 0, "max": 4},
                    "derivation": "Protocol fixed band 0–4 / 192.",
                },
                "rescue_to_pass": {
                    "numerator_min": 0,
                    "numerator_max": 2,
                    "denominator": 192,
                    "predicted_count_band": {"min": 0, "max": 2},
                    "derivation": "Protocol fixed band 0–2 / 192.",
                },
                "regression": {
                    "numerator_min": 0,
                    "numerator_max": 0,
                    "denominator": 192,
                    "predicted_count": 0,
                    "derivation": "Protocol requires regression = 0 / 192.",
                },
            },
        },
    }

    canon = json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    sha = hashlib.sha256(canon.encode("utf-8")).hexdigest()
    doc["canonical_sha256"] = sha
    doc["canonical_sha256_basis"] = {
        "algorithm": "SHA-256",
        "encoding": "utf-8",
        "serialization": "json.dumps(obj_without_hash_fields, sort_keys=True, separators=(',', ':'), ensure_ascii=False)",
        "excludes_fields": ["canonical_sha256", "canonical_sha256_basis"],
        "band_kind_reminder": "pre-registered tolerance bands, not confidence intervals",
    }
    out = ROOT / "docs/experiments/predictions/math16_gemini_multiseed_predictions.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    loaded = json.loads(out.read_text(encoding="utf-8"))
    basis = {k: v for k, v in loaded.items() if k not in ("canonical_sha256", "canonical_sha256_basis")}
    rehash = hashlib.sha256(
        json.dumps(basis, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    print(json.dumps({"sha": sha, "ok": rehash == sha, "pass_band": [lo, hi], "counts": [cmin, cmax]}, indent=2))


if __name__ == "__main__":
    main()
