"""Build Math16 Gemini Phase 2 five-seed interim report (programmatic; no hand tables)."""
from __future__ import annotations

import hashlib
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RESULTS = ROOT / "docs/experiments/results"
REPORT_MD = ROOT / "docs/experiments/reports/math16_gemini_five_seed_interim_report.md"
REPORT_DATA = ROOT / "docs/experiments/reports/math16_gemini_five_seed_interim_report_data.json"
PREDICTIONS = ROOT / "docs/experiments/predictions/math16_gemini_multiseed_predictions.json"
AB3 = RESULTS / "math16_gemini_multiseed_ab3_phase2" / "ab3_report_data.json"
SEED1_RUN = "gemini35flash_math16_latex_v1_ab123_run_001"
NEW_RUN = "gemini35flash_math16_ab123_run_003_multiseed"
LAYERS = ("L0", "L1", "L2", "L3", "L4", "L5")
SEEDS = (2026071301, 2026072001, 2026072002, 2026072003, 2026072004)
NEW_SEEDS = (2026072001, 2026072002, 2026072003, 2026072004)
CONDITIONS = ("ab1", "ab2g", "ab2d")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def mean_sample_sd(values: list[float]) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    if len(values) == 1:
        return values[0], 0.0
    return statistics.mean(values), statistics.stdev(values)


def outcome_bucket(artifact: dict[str, Any]) -> str:
    if artifact.get("evaluator_status") == "PASSED":
        return "PASS"
    layer = (artifact.get("failure_layer") or {}).get("primary_layer")
    status = artifact.get("evaluator_status") or ""
    empty_hash = hashlib.sha256(b"").hexdigest()
    extracted_hash = (artifact.get("hashes") or {}).get("extracted_candidate")
    if extracted_hash == empty_hash or status in {
        "EMPTY_RESPONSE",
        "EXTRACTION_FAILURE",
        "MISSING_ENTRY_POINT",
        "CATASTROPHIC_TRUNCATION",
    }:
        return "no-program-structure"
    if layer == "L5" or status == "ANSWER_INCORRECT":
        return "semantic"
    if layer == "L4" or status in {"EXECUTION_FAILURE", "RUNTIME_FAILURE"}:
        return "runtime"
    return "structural/syntax"


def load_seed_cells(seed: int) -> list[dict[str, Any]]:
    if seed == 2026071301:
        root = RESULTS / SEED1_RUN / "cells"
    else:
        root = RESULTS / NEW_RUN / f"seed_{seed}" / "cells"
    arts = [load_json(p) for p in sorted(root.glob("*/artifact.json"))]
    if len(arts) != 48:
        raise RuntimeError(f"Gemini seed {seed}: expected 48 got {len(arts)}")
    return arts


def layer_counts(cells: list[dict[str, Any]]) -> dict[str, int]:
    c: Counter[str] = Counter()
    for a in cells:
        if a.get("evaluator_status") == "PASSED":
            continue
        layer = (a.get("failure_layer") or {}).get("primary_layer") or "UNKNOWN"
        c[layer] += 1
    return {k: int(c.get(k, 0)) for k in LAYERS}


def band_status(actual: float, lo: float, hi: float) -> str:
    if actual < lo:
        return "below band"
    if actual > hi:
        return "above band"
    return "within band"


def verify_seed1() -> dict[str, Any]:
    snap = load_json(RESULTS / "_phase1_immutability" / "gemini_run_001_pre_phase2_fingerprint.json")
    root = RESULTS / SEED1_RUN
    arts = sorted((root / "cells").glob("*/artifact.json"))
    raws = sorted((root / "cells").glob("*/raw_response.txt"))
    ha = hashlib.sha256(b"".join(p.read_bytes() for p in arts)).hexdigest()
    hr = hashlib.sha256(b"".join(p.read_bytes() for p in raws)).hexdigest()
    return {
        "artifact_unchanged": ha == snap["artifact_concat_sha256"],
        "raw_unchanged": hr == snap["raw_concat_sha256"],
        "artifact_concat_sha256": ha,
        "raw_concat_sha256": hr,
        "count": len(arts),
    }


def verify_h0_new_vs_pre_ab3() -> dict[str, Any]:
    pre_path = RESULTS / "_phase1_immutability" / "gemini_h0_new_192_pre_ab3_fingerprint.json"
    arts: list[Path] = []
    for seed in NEW_SEEDS:
        root = RESULTS / NEW_RUN / f"seed_{seed}" / "cells"
        arts.extend(sorted(root.glob("*/artifact.json")))
    h = hashlib.sha256(b"".join(p.read_bytes() for p in arts)).hexdigest()
    if not pre_path.exists():
        return {
            "count": len(arts),
            "current_sha256": h,
            "unchanged": False,
            "note": "pre_ab3 fingerprint missing",
        }
    pre = load_json(pre_path)
    return {
        "count": len(arts),
        "pre_ab3_sha256": pre["concat_sha256"],
        "current_sha256": h,
        "unchanged": h == pre["concat_sha256"] and len(arts) == 192,
    }


def collect_transient_resumes() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for seed in NEW_SEEDS:
        summary_path = RESULTS / NEW_RUN / f"seed_{seed}" / "run_summary.json"
        if not summary_path.exists():
            continue
        summary = load_json(summary_path)
        for item in summary.get("transient_resumes") or []:
            out.append({"seed": seed, **item} if isinstance(item, dict) else {"seed": seed, "raw": item})
    return out


def build() -> dict[str, Any]:
    data: dict[str, Any] = {
        "title": "Gemini Phase 2 five-seed interim report",
        "generated_by": "scripts/build_math16_gemini_five_seed_interim_report.py",
        "inputs": {
            "h0_seed1": f"docs/experiments/results/{SEED1_RUN}/cells/*/artifact.json",
            "h0_new_seeds": f"docs/experiments/results/{NEW_RUN}/seed_*/cells/*/artifact.json",
            "ab3": "docs/experiments/results/math16_gemini_multiseed_ab3_phase2/ab3_report_data.json",
            "predictions": "docs/experiments/predictions/math16_gemini_multiseed_predictions.json",
            "taxonomy_mapping": "docs/experiments/manifests/math16_outcome_taxonomy_mapping.json",
        },
        "sd_definition": "sample_standard_deviation_n_minus_1",
        "replication_label": "repeated generations under fixed nominal seeds",
        "seed1_immutability": verify_seed1(),
        "h0_new_immutability": verify_h0_new_vs_pre_ab3(),
        "transient_resumes": collect_transient_resumes(),
    }

    per_seed = {}
    pass_rates = []
    all_cells: list[dict[str, Any]] = []
    for seed in SEEDS:
        cells = load_seed_cells(seed)
        all_cells.extend(cells)
        pass_n = sum(1 for a in cells if a.get("evaluator_status") == "PASSED")
        fail_n = 48 - pass_n
        layers = layer_counts(cells)
        assert pass_n + fail_n == 48
        assert sum(layers.values()) == fail_n
        props = {k: (layers[k] / fail_n if fail_n else 0.0) for k in LAYERS}
        per_seed[str(seed)] = {
            "PASS": pass_n,
            "FAIL": fail_n,
            "row_sum": pass_n + fail_n,
            "pass_rate": pass_n / 48,
            "failure_layer_counts": layers,
            "failure_layer_proportions_among_fail": props,
        }
        pass_rates.append(pass_n / 48)
    assert len(all_cells) == 240
    pooled_pass = sum(1 for a in all_cells if a.get("evaluator_status") == "PASSED")
    mean_r, sd_r = mean_sample_sd(pass_rates)

    groups = defaultdict(list)
    for a in all_cells:
        groups[(a["task_id"], a["condition"])].append(a)
    assert len(groups) == 48
    stability = {"stable_pass": 0, "stable_fail": 0, "unstable": 0, "groups": {}}
    for (tid, cond), items in sorted(groups.items()):
        assert len(items) == 5
        passes = [1 if x.get("evaluator_status") == "PASSED" else 0 for x in items]
        freq = sum(passes)
        buckets = [outcome_bucket(x) for x in items]
        fail_layers = [
            (x.get("failure_layer") or {}).get("primary_layer")
            for x in items
            if x.get("evaluator_status") != "PASSED"
        ]
        if freq == 5:
            label = "stable_pass"
            stability["stable_pass"] += 1
        elif freq == 0:
            label = "stable_fail"
            stability["stable_fail"] += 1
        else:
            label = "unstable"
            stability["unstable"] += 1
        stability["groups"][f"{tid}__{cond}"] = {
            "task_id": tid,
            "condition": cond,
            "pass_frequency": f"{freq}/5",
            "pass_count": freq,
            "stability": label,
            "outcome_consistency": len(set(buckets)) == 1,
            "layer_diversity": len(set(fail_layers)) if fail_layers else 0,
            "failure_layer_consistency": len(set(fail_layers)) <= 1,
            "outcome_buckets": dict(Counter(buckets)),
        }
    assert stability["stable_pass"] + stability["stable_fail"] + stability["unstable"] == 48

    cond_stats = {}
    for cond in CONDITIONS:
        subset = [a for a in all_cells if a["condition"] == cond]
        assert len(subset) == 80
        by_seed_pass = []
        for seed in SEEDS:
            sc = [a for a in subset if int(a.get("seed") or seed) == seed]
            if len(sc) != 16:
                # Seed-1 artifacts may store seed differently; filter by path-derived seed via cell_id
                sc = [a for a in subset if f"__seed_{seed}" in a.get("cell_id", "") or a.get("seed") == seed]
            assert len(sc) == 16, f"{cond} seed {seed}: {len(sc)}"
            by_seed_pass.append(sum(1 for a in sc if a.get("evaluator_status") == "PASSED") / 16)
        p = sum(1 for a in subset if a.get("evaluator_status") == "PASSED")
        m, s = mean_sample_sd(by_seed_pass)
        layers = layer_counts(subset)
        fail_n = 80 - p
        cond_stats[cond] = {
            "pooled_pass_fraction": f"{p}/80",
            "pooled_pass_rate": p / 80,
            "seed_level_mean": m,
            "seed_level_sample_sd": s,
            "failure_layer_counts": layers,
            "failure_layer_proportions_among_fail": {
                k: (layers[k] / fail_n if fail_n else 0.0) for k in LAYERS
            },
            "PASS": p,
            "FAIL": fail_n,
            "denominator": 80,
        }

    data["model"] = {
        "model_id": "gemini-3.5-flash",
        "per_seed": per_seed,
        "pooled_pass_fraction": f"{pooled_pass}/240",
        "pooled_pass_count": pooled_pass,
        "pooled_pass_rate": pooled_pass / 240,
        "seed_level_mean": mean_r,
        "seed_level_sample_sd": sd_r,
        "task_condition_stability": stability,
        "condition_comparison": cond_stats,
    }

    ab3 = load_json(AB3)
    summary = ab3["summary"]
    results = ab3["results"]
    assert len(results) == 192
    by_outcome = Counter(r["actual"] for r in results)
    assert sum(by_outcome.values()) == 192
    h0_pass = sum(1 for r in results if r["h0_status"] == "PASSED")
    h0_fail = 192 - h0_pass
    trigger_n = int(summary.get("trigger_count", 0))
    rescue_n = int(summary.get("rescue_to_pass", 0))
    exposure_n = int(summary.get("layer_exposure", 0))
    abstain_n = int(summary.get("guarded_abstain", 0))
    regression_n = int(summary.get("regression", 0))
    excluded_n = int(summary.get("excluded_no_program_structure", 0))
    eval_fail_n = int(summary.get("evaluator_failure", 0))
    no_trigger_n = int(summary.get("no_trigger", 0))
    identity_n = int(summary.get("identity_reuse", 0))
    outcome_sum = (
        no_trigger_n
        + abstain_n
        + exposure_n
        + rescue_n
        + regression_n
        + excluded_n
        + eval_fail_n
        + identity_n
    )
    assert outcome_sum == 192
    assert h0_pass == identity_n
    assert h0_fail == 192 - identity_n

    data["ab3_new_seeds"] = {
        "label": "frozen-rule generalization across unseen generation seeds on the same fixed task set",
        "cells": 192,
        "H0_PASS": h0_pass,
        "H0_FAIL": h0_fail,
        "evaluable_FAIL": h0_fail - excluded_n,
        "no_trigger": no_trigger_n,
        "guarded_abstain": abstain_n,
        "trigger": trigger_n,
        "layer_exposure": exposure_n,
        "rescue_to_pass": rescue_n,
        "regression": regression_n,
        "excluded": excluded_n,
        "evaluator_failure": eval_fail_n,
        "identity_reuse": identity_n,
        "trigger_over_192": trigger_n / 192,
        "trigger_over_H0_FAIL": (trigger_n / h0_fail) if h0_fail else None,
        "exposure_over_trigger": (exposure_n / trigger_n) if trigger_n else None,
        "rescue_over_192": rescue_n / 192,
        "rescue_over_H0_FAIL": (rescue_n / h0_fail) if h0_fail else None,
        "rescue_over_trigger": (rescue_n / trigger_n) if trigger_n else None,
        "regression_over_H0_PASS": (regression_n / h0_pass) if h0_pass else None,
        "by_outcome": dict(by_outcome),
        "outcome_sum": outcome_sum,
    }

    preds = load_json(PREDICTIONS)
    new_cells: list[dict[str, Any]] = []
    for seed in NEW_SEEDS:
        new_cells.extend(load_seed_cells(seed))
    assert len(new_cells) == 192
    pass_n = sum(1 for a in new_cells if a.get("evaluator_status") == "PASSED")
    pass_rate = 100.0 * pass_n / 192
    band = preds["model"]["h0_pass_rate"]["predicted_pass_rate_pct_band"]
    fail_n = 192 - pass_n
    layer_c = layer_counts(new_cells)
    layer_cmp = {}
    for L, info in preds["model"]["failure_layer_share_among_fail"]["layers"].items():
        share = 100.0 * layer_c.get(L, 0) / fail_n if fail_n else 0.0
        layer_cmp[L] = {
            "actual_share_pct": share,
            "actual_count": layer_c.get(L, 0),
            "fail_denominator": fail_n,
            "band": info["predicted_share_pct_band"],
            "status": band_status(
                share, info["predicted_share_pct_band"]["min"], info["predicted_share_pct_band"]["max"]
            ),
        }
    ab3_pred = preds["model"]["ab3_frozen_rule_generalization_on_192"]
    data["prediction_vs_actual"] = {
        "h0_pass_rate_pct": {
            "actual": pass_rate,
            "actual_fraction": f"{pass_n}/192",
            "band": band,
            "status": band_status(pass_rate, band["min"], band["max"]),
        },
        "failure_layers": layer_cmp,
        "trigger_count": {
            "actual": trigger_n,
            "band": ab3_pred["trigger_count"]["predicted_count_band"],
            "status": band_status(
                trigger_n,
                ab3_pred["trigger_count"]["predicted_count_band"]["min"],
                ab3_pred["trigger_count"]["predicted_count_band"]["max"],
            ),
        },
        "layer_exposure": {
            "actual": exposure_n,
            "band": ab3_pred["layer_exposure"]["predicted_count_band"],
            "status": band_status(
                exposure_n,
                ab3_pred["layer_exposure"]["predicted_count_band"]["min"],
                ab3_pred["layer_exposure"]["predicted_count_band"]["max"],
            ),
        },
        "rescue_to_pass": {
            "actual": rescue_n,
            "band": ab3_pred["rescue_to_pass"]["predicted_count_band"],
            "status": band_status(
                rescue_n,
                ab3_pred["rescue_to_pass"]["predicted_count_band"]["min"],
                ab3_pred["rescue_to_pass"]["predicted_count_band"]["max"],
            ),
        },
        "regression": {
            "actual": regression_n,
            "band": {"min": 0, "max": 0},
            "status": "within band" if regression_n == 0 else "above band",
        },
    }

    # Model metadata sample from first new-seed artifact
    sample = new_cells[0]
    data["provider_metadata_sample"] = {
        "requested_model": sample.get("requested_model") or sample.get("model"),
        "runtime_version": (sample.get("provider_metadata") or {}).get("runtime_version"),
        "sdk": (sample.get("provider_metadata") or {}).get("sdk"),
        "temperature": sample.get("temperature"),
        "max_output_tokens": sample.get("max_output_tokens"),
        "seed_support_note": data["replication_label"],
    }

    data["assertions"] = {
        "cells_per_seed_48": all(v["row_sum"] == 48 for v in per_seed.values()),
        "gemini_total_240": len(all_cells) == 240,
        "new_seeds_total_192": len(new_cells) == 192,
        "ab3_outcome_sum_192": outcome_sum == 192,
        "ab3_identity_equals_h0_pass": h0_pass == identity_n,
        "seed1_byte_level_unchanged": data["seed1_immutability"]["artifact_unchanged"]
        and data["seed1_immutability"]["raw_unchanged"],
        "h0_new_192_unchanged_vs_pre_ab3": data["h0_new_immutability"]["unchanged"],
        "sample_sd_used": True,
        "regression_zero": regression_n == 0,
    }
    for k, v in data["assertions"].items():
        if not v:
            raise RuntimeError(f"assertion failed: {k}")
    return data


def _fmt_props(props: dict[str, float]) -> str:
    return ", ".join(f"{k}:{props[k]:.4f}" for k in LAYERS if props.get(k, 0) > 0) or "—"


def render_md(data: dict[str, Any]) -> str:
    md = data["model"]
    lines: list[str] = []
    lines.append("# Gemini Phase 2 five-seed interim report")
    lines.append("")
    lines.append(
        "This document is the **Gemini five-seed formal interim report**. "
        "It is not yet the final three-model 720-cell report."
    )
    lines.append("")
    lines.append(
        f"Generated programmatically by `{data['generated_by']}` "
        f"(sample SD = n−1). Not hand-copied."
    )
    lines.append("")
    lines.append("## Inputs")
    lines.append("")
    for key, val in data["inputs"].items():
        lines.append(f"- {key}: `{val}`")
    lines.append("")

    lines.append("## A. Per seed H0")
    lines.append("")
    lines.append(
        "| seed | PASS/48 | FAIL/48 | row sum | L0 | L1 | L2 | L3 | L4 | L5 | "
        "L0 prop | L1 prop | L2 prop | L3 prop | L4 prop | L5 prop |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for seed, row in md["per_seed"].items():
        c = row["failure_layer_counts"]
        p = row["failure_layer_proportions_among_fail"]
        lines.append(
            f"| {seed} | {row['PASS']}/48 | {row['FAIL']}/48 | {row['row_sum']} | "
            f"{c['L0']} | {c['L1']} | {c['L2']} | {c['L3']} | {c['L4']} | {c['L5']} | "
            f"{p['L0']:.4f} | {p['L1']:.4f} | {p['L2']:.4f} | {p['L3']:.4f} | {p['L4']:.4f} | {p['L5']:.4f} |"
        )
    lines.append("")
    lines.append("Proportions are among FAIL cells in that seed. Each row sum PASS+FAIL = 48.")
    lines.append("")

    lines.append("## B. Five-seed pooled and seed-level statistics")
    lines.append("")
    lines.append(
        f"- pooled count/proportion (denominator 240): "
        f"**{md['pooled_pass_fraction']}** = {md['pooled_pass_rate']:.6f}"
    )
    lines.append(
        f"- seed-level mean ± sample SD (n−1) of five seed PASS rates: "
        f"**{md['seed_level_mean']:.6f} ± {md['seed_level_sample_sd']:.6f}**"
    )
    lines.append("- pooled proportion and mean ± SD are reported separately (not interchangeable).")
    lines.append("")

    st = md["task_condition_stability"]
    lines.append("## C. Task–condition stability (48 groups × 5 seeds)")
    lines.append("")
    lines.append(
        f"- summary: stable_pass={st['stable_pass']}; "
        f"stable_fail={st['stable_fail']}; unstable={st['unstable']}"
    )
    lines.append("")
    lines.append(
        "| task_id | condition | pass_frequency | stability | outcome_consistency | "
        "layer_diversity | failure_layer_consistency | outcome_buckets |"
    )
    lines.append("|---|---|---:|---|---:|---:|---:|---|")
    for _key, g in st["groups"].items():
        buckets = ", ".join(f"{k}:{v}" for k, v in sorted(g["outcome_buckets"].items()))
        lines.append(
            f"| {g['task_id']} | {g['condition']} | {g['pass_frequency']} | {g['stability']} | "
            f"{g['outcome_consistency']} | {g['layer_diversity']} | "
            f"{g['failure_layer_consistency']} | {buckets} |"
        )
    lines.append("")

    lines.append("## D. Prompt-condition comparison")
    lines.append("")
    lines.append(
        "| condition | pooled PASS | pooled rate | seed mean | seed sample SD | "
        "FAIL | L0 | L1 | L2 | L3 | L4 | L5 |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for cond, cs in md["condition_comparison"].items():
        c = cs["failure_layer_counts"]
        lines.append(
            f"| {cond} | {cs['pooled_pass_fraction']} | {cs['pooled_pass_rate']:.4f} | "
            f"{cs['seed_level_mean']:.4f} | {cs['seed_level_sample_sd']:.4f} | "
            f"{cs['FAIL']}/80 | {c['L0']} | {c['L1']} | {c['L2']} | {c['L3']} | {c['L4']} | {c['L5']} |"
        )
    lines.append("")
    for cond, cs in md["condition_comparison"].items():
        lines.append(f"- `{cond}` FAIL-layer props: {_fmt_props(cs['failure_layer_proportions_among_fail'])}")
    lines.append("")

    ab = data["ab3_new_seeds"]
    lines.append("## E. Frozen Healer seed-generalization (4 new seeds only)")
    lines.append("")
    lines.append(f"Label: `{ab['label']}`")
    lines.append("")
    lines.append("This is **not** cross-task held-out generalization.")
    lines.append("")
    lines.append("| metric | value |")
    lines.append("|---|---:|")
    for key in (
        "cells",
        "H0_PASS",
        "H0_FAIL",
        "evaluable_FAIL",
        "no_trigger",
        "guarded_abstain",
        "trigger",
        "layer_exposure",
        "rescue_to_pass",
        "regression",
        "excluded",
        "evaluator_failure",
        "identity_reuse",
        "outcome_sum",
    ):
        lines.append(f"| {key} | {ab[key]} |")
    lines.append(f"| trigger / 192 | {ab['trigger_over_192']:.6f} |")
    lines.append(f"| trigger / H0 FAIL | {ab['trigger_over_H0_FAIL']} |")
    lines.append(f"| exposure / trigger | {ab['exposure_over_trigger']} |")
    lines.append(f"| rescue / 192 | {ab['rescue_over_192']:.6f} |")
    lines.append(f"| rescue / H0 FAIL | {ab['rescue_over_H0_FAIL']} |")
    lines.append(f"| rescue / trigger | {ab['rescue_over_trigger']} |")
    lines.append(f"| regression / H0 PASS | {ab['regression_over_H0_PASS']} |")
    lines.append("")

    lines.append("## F. Prediction vs actual (192 new cells)")
    lines.append("")
    lines.append("Bands are pre-registered tolerance bands, not confidence intervals.")
    lines.append("")
    lines.append("| metric | prediction band | actual | status |")
    lines.append("|---|---|---|---|")
    pva = data["prediction_vs_actual"]
    pr = pva["h0_pass_rate_pct"]
    lines.append(
        f"| H0 PASS rate % | [{pr['band']['min']}, {pr['band']['max']}] | "
        f"{pr['actual']:.6f} ({pr['actual_fraction']}) | {pr['status']} |"
    )
    for L, info in pva["failure_layers"].items():
        lines.append(
            f"| FAIL-share {L} % | [{info['band']['min']}, {info['band']['max']}] | "
            f"{info['actual_share_pct']:.6f} ({info['actual_count']}/{info['fail_denominator']}) | "
            f"{info['status']} |"
        )
    for key in ("trigger_count", "layer_exposure", "rescue_to_pass", "regression"):
        info = pva[key]
        lines.append(
            f"| {key} | [{info['band']['min']}, {info['band']['max']}] | "
            f"{info['actual']} | {info['status']} |"
        )
    lines.append("")

    lines.append("## G. Limits and provider notes")
    lines.append("")
    lines.append(
        f"- Gemini nominal seed does **not** guarantee reproducible generations; "
        f"formal label: `{data['replication_label']}`."
    )
    lines.append(
        f"- Provider metadata sample: `{json.dumps(data['provider_metadata_sample'], ensure_ascii=False)}`."
    )
    lines.append("- Sample SD uses n−1, matching the Qwen five-seed report.")
    lines.append(
        f"- Transient API resumes: {len(data['transient_resumes'])}; "
        f"cell IDs: {[x.get('cell_id') for x in data['transient_resumes']]}."
    )
    lines.append("- No new Healer rules were developed.")
    lines.append("- H0 artifacts are immutable; H1 lives outside H0 directories.")
    lines.append("- This is not yet the final three-model report.")
    lines.append("")

    lines.append("## Assertions")
    lines.append("")
    for k, v in data["assertions"].items():
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    data = build()
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_DATA.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    REPORT_MD.write_text(render_md(data), encoding="utf-8")
    print(
        json.dumps(
            {
                "report": str(REPORT_MD),
                "assertions": data["assertions"],
                "ab3": {
                    "PASS": data["ab3_new_seeds"]["H0_PASS"],
                    "FAIL": data["ab3_new_seeds"]["H0_FAIL"],
                    "trigger": data["ab3_new_seeds"]["trigger"],
                    "exposure": data["ab3_new_seeds"]["layer_exposure"],
                    "rescue": data["ab3_new_seeds"]["rescue_to_pass"],
                    "regression": data["ab3_new_seeds"]["regression"],
                },
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
