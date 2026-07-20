"""Build Math16 Qwen Phase 1 five-seed interim report (programmatic; no hand tables)."""
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
REPORT_MD = ROOT / "docs/experiments/reports/math16_qwen_five_seed_interim_report.md"
REPORT_DATA = ROOT / "docs/experiments/reports/math16_qwen_five_seed_interim_report_data.json"
PREDICTIONS = ROOT / "docs/experiments/predictions/math16_qwen_multiseed_predictions.json"
AB3 = RESULTS / "math16_qwen_multiseed_ab3_phase1" / "ab3_report_data.json"
LAYERS = ("L0", "L1", "L2", "L3", "L4", "L5")

MODELS = {
    "qwen35_4b": {"tag": "qwen3.5:4b", "seed1": "qwen35_4b_math16_ab123_run_002"},
    "qwen35_9b": {"tag": "qwen3.5:9b", "seed1": "qwen35_9b_math16_ab123_run_002"},
}
SEEDS = (2026071301, 2026072001, 2026072002, 2026072003, 2026072004)
NEW_SEEDS = (2026072001, 2026072002, 2026072003, 2026072004)
CONDITIONS = ("ab1", "ab2g", "ab2d")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def mean_sample_sd(values: list[float]) -> tuple[float, float]:
    """Mean and sample SD (n-1)."""
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


def load_seed_cells(model: str, seed: int) -> list[dict[str, Any]]:
    if seed == 2026071301:
        root = RESULTS / MODELS[model]["seed1"] / "cells"
    else:
        root = RESULTS / f"{model}_math16_ab123_run_003_multiseed" / f"seed_{seed}" / "cells"
    arts = [load_json(p) for p in sorted(root.glob("*/artifact.json"))]
    if len(arts) != 48:
        raise RuntimeError(f"{model} seed {seed}: expected 48 got {len(arts)}")
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


def verify_run002() -> dict[str, Any]:
    snap = load_json(RESULTS / "_phase1_immutability" / "run_002_pre_generation_fingerprint.json")
    out = {}
    for run, expected in snap.items():
        root = RESULTS / run
        arts = sorted((root / "cells").glob("*/artifact.json"))
        raws = sorted((root / "cells").glob("*/raw_response.txt"))
        ha = hashlib.sha256(b"".join(p.read_bytes() for p in arts)).hexdigest()
        hr = hashlib.sha256(b"".join(p.read_bytes() for p in raws)).hexdigest()
        out[run] = {
            "artifact_unchanged": ha == expected["artifact_concat_sha256"],
            "raw_unchanged": hr == expected["raw_concat_sha256"],
            "artifact_concat_sha256": ha,
            "raw_concat_sha256": hr,
        }
    return out


def verify_h0_new_vs_pre_ab3() -> dict[str, Any]:
    pre = load_json(RESULTS / "_phase1_immutability" / "h0_new_384_pre_ab3_fingerprint.json")
    arts: list[Path] = []
    for model in MODELS:
        for seed in NEW_SEEDS:
            root = RESULTS / f"{model}_math16_ab123_run_003_multiseed" / f"seed_{seed}" / "cells"
            arts.extend(sorted(root.glob("*/artifact.json")))
    h = hashlib.sha256(b"".join(p.read_bytes() for p in arts)).hexdigest()
    return {
        "count": len(arts),
        "pre_ab3_sha256": pre["concat_sha256"],
        "current_sha256": h,
        "unchanged": h == pre["concat_sha256"] and len(arts) == 384,
    }


def build() -> dict[str, Any]:
    data: dict[str, Any] = {
        "title": "Qwen Phase 1 interim report",
        "generated_by": "scripts/build_math16_qwen_five_seed_interim_report.py",
        "inputs": {
            "h0_seed1": [
                "docs/experiments/results/qwen35_4b_math16_ab123_run_002/cells/*/artifact.json",
                "docs/experiments/results/qwen35_9b_math16_ab123_run_002/cells/*/artifact.json",
            ],
            "h0_new_seeds": [
                "docs/experiments/results/qwen35_4b_math16_ab123_run_003_multiseed/seed_*/cells/*/artifact.json",
                "docs/experiments/results/qwen35_9b_math16_ab123_run_003_multiseed/seed_*/cells/*/artifact.json",
            ],
            "ab3": "docs/experiments/results/math16_qwen_multiseed_ab3_phase1/ab3_report_data.json",
            "predictions": "docs/experiments/predictions/math16_qwen_multiseed_predictions.json",
        },
        "sd_definition": "sample_standard_deviation_n_minus_1",
        "models": {},
        "assertions": {},
        "prediction_vs_actual": {},
        "ab3_new_seeds": {},
        "run_002_immutability": verify_run002(),
        "h0_new_immutability": verify_h0_new_vs_pre_ab3(),
    }

    total_cells = 0
    for model in MODELS:
        per_seed = {}
        pass_rates = []
        all_cells: list[dict[str, Any]] = []
        for seed in SEEDS:
            cells = load_seed_cells(model, seed)
            all_cells.extend(cells)
            pass_n = sum(1 for a in cells if a.get("evaluator_status") == "PASSED")
            fail_n = 48 - pass_n
            layers = layer_counts(cells)
            layer_sum = sum(layers.values())
            assert pass_n + fail_n == 48
            assert layer_sum == fail_n
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
        total_cells += len(all_cells)
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
                "failure_layers_across_seeds": [x if x is not None else "PASS" for x in [
                    (x.get("failure_layer") or {}).get("primary_layer")
                    if x.get("evaluator_status") != "PASSED"
                    else None
                    for x in items
                ]],
            }
        assert stability["stable_pass"] + stability["stable_fail"] + stability["unstable"] == 48

        cond_stats = {}
        for cond in CONDITIONS:
            subset = [a for a in all_cells if a["condition"] == cond]
            assert len(subset) == 80
            by_seed_pass = []
            for seed in SEEDS:
                sc = [a for a in subset if a["seed"] == seed]
                assert len(sc) == 16
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

        data["models"][model] = {
            "model_tag": MODELS[model]["tag"],
            "per_seed": per_seed,
            "pooled_pass_fraction": f"{pooled_pass}/240",
            "pooled_pass_count": pooled_pass,
            "pooled_pass_rate": pooled_pass / 240,
            "seed_level_mean": mean_r,
            "seed_level_sample_sd": sd_r,
            "task_condition_stability": stability,
            "condition_comparison": cond_stats,
        }

    assert total_cells == 480

    ab3 = load_json(AB3)
    summary = ab3["summary"]
    results = ab3["results"]
    assert len(results) == 384
    by_outcome = Counter(r["actual"] for r in results)
    assert sum(by_outcome.values()) == 384
    h0_pass = sum(1 for r in results if r["h0_status"] == "PASSED")
    h0_fail = 384 - h0_pass
    trigger_n = int(summary.get("trigger_count", 0))
    rescue_n = int(summary.get("rescue_to_pass", 0))
    exposure_n = int(summary.get("layer_exposure", 0))
    abstain_n = int(summary.get("guarded_abstain", 0))
    regression_n = int(summary.get("regression", 0))
    excluded_n = int(summary.get("excluded_no_program_structure", 0))
    eval_fail_n = int(summary.get("evaluator_failure", 0))
    no_trigger_n = int(summary.get("no_trigger", 0))
    identity_n = int(summary.get("identity_reuse", 0))
    # Closure over reported Ab3 outcomes (identity_reuse is PASS negative-control label)
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
    assert outcome_sum == 384
    assert h0_pass == identity_n == 51
    assert h0_fail == 333
    assert trigger_n == 8
    assert exposure_n == 8
    assert rescue_n == 0
    assert regression_n == 0

    data["ab3_new_seeds"] = {
        "label": "frozen-rule generalization across unseen generation seeds on the same fixed task set",
        "cells": 384,
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
        "trigger_over_384": trigger_n / 384,
        "trigger_over_H0_FAIL": trigger_n / h0_fail,
        "exposure_over_trigger": (exposure_n / trigger_n) if trigger_n else None,
        "rescue_over_384": rescue_n / 384,
        "rescue_over_H0_FAIL": rescue_n / h0_fail,
        "rescue_over_trigger": (rescue_n / trigger_n) if trigger_n else None,
        "regression_over_H0_PASS": regression_n / h0_pass,
        "by_outcome": dict(by_outcome),
        "by_model": summary.get("by_model"),
        "outcome_sum": outcome_sum,
    }

    preds = load_json(PREDICTIONS)
    pva = {}
    for model_key in ("qwen35_4b", "qwen35_9b"):
        new_cells: list[dict[str, Any]] = []
        for seed in NEW_SEEDS:
            new_cells.extend(load_seed_cells(model_key, seed))
        assert len(new_cells) == 192
        pass_n = sum(1 for a in new_cells if a.get("evaluator_status") == "PASSED")
        pass_rate = 100.0 * pass_n / 192
        band = preds["models"][model_key]["h0_pass_rate"]["predicted_pass_rate_pct_band"]
        fail_n = 192 - pass_n
        layer_c = layer_counts(new_cells)
        layer_cmp = {}
        for L, info in preds["models"][model_key]["failure_layer_share_among_fail"]["layers"].items():
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
        ab3_m = summary["by_model"][model_key]
        trig = ab3_m.get("trigger", 0)
        exp = ab3_m.get("layer_exposure", 0)
        resc = ab3_m.get("rescue_to_pass", 0)
        reg = ab3_m.get("regression", 0)
        pva[model_key] = {
            "h0_pass_rate_pct": {
                "actual": pass_rate,
                "actual_fraction": f"{pass_n}/192",
                "band": band,
                "status": band_status(pass_rate, band["min"], band["max"]),
            },
            "failure_layers": layer_cmp,
            "trigger_count": {
                "actual": trig,
                "band": {"min": 0, "max": 8},
                "status": band_status(trig, 0, 8),
            },
            "layer_exposure": {
                "actual": exp,
                "band": {"min": 0, "max": 8},
                "status": band_status(exp, 0, 8),
            },
            "rescue_to_pass": {
                "actual": resc,
                "band": {"min": 0, "max": 2},
                "status": band_status(resc, 0, 2),
            },
            "regression": {
                "actual": reg,
                "band": {"min": 0, "max": 0},
                "status": "within band" if reg == 0 else "above band",
            },
        }
    data["prediction_vs_actual"] = pva

    data["assertions"] = {
        "cells_per_model_seed_48": True,
        "cells_per_model_240": True,
        "qwen_total_480": total_cells == 480,
        "new_seeds_total_384": True,
        "new_seeds_PASS_51": h0_pass == 51,
        "new_seeds_FAIL_333": h0_fail == 333,
        "ab3_trigger_8": trigger_n == 8,
        "ab3_layer_exposure_8": exposure_n == 8,
        "ab3_rescue_0": rescue_n == 0,
        "ab3_regression_0": regression_n == 0,
        "ab3_outcome_sum_384": outcome_sum == 384,
        "run_002_byte_level_unchanged": all(
            v["artifact_unchanged"] and v["raw_unchanged"] for v in data["run_002_immutability"].values()
        ),
        "h0_new_384_unchanged_vs_pre_ab3": data["h0_new_immutability"]["unchanged"],
        "sample_sd_used": True,
    }
    for k, v in data["assertions"].items():
        if not v:
            raise RuntimeError(f"assertion failed: {k}")
    return data


def _fmt_props(props: dict[str, float]) -> str:
    return ", ".join(f"{k}:{props[k]:.4f}" for k in LAYERS if props.get(k, 0) > 0) or "—"


def render_md(data: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Qwen Phase 1 interim report")
    lines.append("")
    lines.append(
        "This document is a **Qwen Phase 1 interim report**. "
        "Gemini Phase 2 is not completed. No full three-model conclusions are drawn. "
        "New seeds are not used for rule development."
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
        if isinstance(val, list):
            for item in val:
                lines.append(f"- {key}: `{item}`")
        else:
            lines.append(f"- {key}: `{val}`")
    lines.append("")

    for model, md in data["models"].items():
        lines.append(f"## Model `{md['model_tag']}` (`{model}`)")
        lines.append("")
        lines.append("### A. Per seed")
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

        lines.append("### B. Five-seed pooled and seed-level statistics")
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
        lines.append("### C. Task–condition stability (48 groups × 5 seeds)")
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

        lines.append("### D. Prompt-condition comparison")
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
        lines.append("Failure-layer proportions among FAIL for each condition:")
        lines.append("")
        for cond, cs in md["condition_comparison"].items():
            lines.append(f"- `{cond}`: {_fmt_props(cs['failure_layer_proportions_among_fail'])}")
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
    lines.append(f"| cells | {ab['cells']} |")
    lines.append(f"| H0 PASS | {ab['H0_PASS']} |")
    lines.append(f"| H0 FAIL | {ab['H0_FAIL']} |")
    lines.append(f"| evaluable FAIL | {ab['evaluable_FAIL']} |")
    lines.append(f"| no_trigger | {ab['no_trigger']} |")
    lines.append(f"| guarded_abstain | {ab['guarded_abstain']} |")
    lines.append(f"| trigger | {ab['trigger']} |")
    lines.append(f"| layer_exposure | {ab['layer_exposure']} |")
    lines.append(f"| rescue_to_pass | {ab['rescue_to_pass']} |")
    lines.append(f"| regression | {ab['regression']} |")
    lines.append(f"| excluded | {ab['excluded']} |")
    lines.append(f"| evaluator_failure | {ab['evaluator_failure']} |")
    lines.append(f"| identity_reuse (PASS negative control) | {ab['identity_reuse']} |")
    lines.append(f"| outcome sum | {ab['outcome_sum']} |")
    lines.append(f"| trigger / 384 | {ab['trigger_over_384']:.6f} |")
    lines.append(f"| trigger / H0 FAIL | {ab['trigger_over_H0_FAIL']:.6f} |")
    lines.append(f"| exposure / trigger | {ab['exposure_over_trigger']} |")
    lines.append(f"| rescue / 384 | {ab['rescue_over_384']:.6f} |")
    lines.append(f"| rescue / H0 FAIL | {ab['rescue_over_H0_FAIL']:.6f} |")
    lines.append(f"| rescue / trigger | {ab['rescue_over_trigger']} |")
    lines.append(f"| regression / H0 PASS | {ab['regression_over_H0_PASS']:.6f} |")
    lines.append("")

    lines.append("## F. Prediction vs actual (192 new cells / model)")
    lines.append("")
    lines.append("Bands are pre-registered tolerance bands, not confidence intervals.")
    lines.append("")
    for model, pva in data["prediction_vs_actual"].items():
        lines.append(f"### `{model}`")
        lines.append("")
        lines.append("| metric | prediction band | actual | status |")
        lines.append("|---|---|---|---|")
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

    lines.append("## G. Protocol and limits")
    lines.append("")
    lines.append("- Gemini Phase 2 is not completed.")
    lines.append("- This document is a Qwen Phase 1 interim report.")
    lines.append(
        "- Workflow-order deviation: H0 scoring was completed synchronously during generation "
        "(same frozen evaluator / classify path as Seed-1 live runner); no separate re-score pass was required."
    )
    lines.append(
        "- Additive runners (`scripts/run_math16_qwen_multiseed_h0.py`, "
        "`scripts/run_math16_ab3_multiseed_phase1.py`, "
        "`scripts/build_math16_qwen_five_seed_interim_report.py`) did not modify frozen Prompt, "
        "evaluator, answer contract, Healer rules, allowlist, priorities, or max_passes."
    )
    lines.append("- run_002 and this round's 384 H0 artifacts are byte-level immutable (verified).")
    lines.append("- New seeds were not used for rule development.")
    lines.append("- No full three-model conclusions are drawn.")
    lines.append("")

    lines.append("## Assertions")
    lines.append("")
    for k, v in data["assertions"].items():
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append("## Immutability evidence")
    lines.append("")
    lines.append("```json")
    lines.append(
        json.dumps(
            {
                "run_002_immutability": data["run_002_immutability"],
                "h0_new_immutability": data["h0_new_immutability"],
            },
            indent=2,
        )
    )
    lines.append("```")
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
