"""Build Math16 Qwen Phase 1 five-seed interim report (programmatic; no hand tables)."""
from __future__ import annotations

import hashlib
import json
import math
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

MODELS = {
    "qwen35_4b": {"tag": "qwen3.5:4b", "seed1": "qwen35_4b_math16_ab123_run_002"},
    "qwen35_9b": {"tag": "qwen3.5:9b", "seed1": "qwen35_9b_math16_ab123_run_002"},
}
SEEDS = (2026071301, 2026072001, 2026072002, 2026072003, 2026072004)
NEW_SEEDS = (2026072001, 2026072002, 2026072003, 2026072004)
CONDITIONS = ("ab1", "ab2g", "ab2d")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def mean_sd(values: list[float]) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    if len(values) == 1:
        return values[0], 0.0
    return statistics.mean(values), statistics.pstdev(values)


def outcome_bucket(artifact: dict[str, Any]) -> str:
    if artifact.get("evaluator_status") == "PASSED":
        return "PASS"
    layer = (artifact.get("failure_layer") or {}).get("primary_layer")
    status = artifact.get("evaluator_status") or ""
    if layer == "L5" or status == "ANSWER_INCORRECT":
        return "semantic"
    if layer in {"L1", "L2", "L3"} or status in {
        "PARSE_MINOR",
        "EXTRACTION_FAILURE",
        "MISSING_ENTRY_POINT",
        "CATASTROPHIC_TRUNCATION",
        "EMPTY_RESPONSE",
        "SCHEMA_FAILURE",
        "STRUCTURAL_MISMATCH",
        "LATEX_MISMATCH",
    }:
        return "structural/syntax"
    if layer == "L4" or status in {"EXECUTION_FAILURE", "RUNTIME_FAILURE"}:
        return "runtime"
    if not (artifact.get("hashes") or {}).get("extracted_candidate") and not (
        Path("x")  # placeholder
    ):
        pass
    code_empty = False
    # Infer no-program from empty extracted hash of empty string
    if (artifact.get("hashes") or {}).get("extracted_candidate") == hashlib.sha256(b"").hexdigest():
        code_empty = True
    if code_empty or status in {"EMPTY_RESPONSE", "EXTRACTION_FAILURE", "MISSING_ENTRY_POINT"}:
        return "no-program-structure"
    return "structural/syntax"


def load_seed_cells(model: str, seed: int) -> list[dict[str, Any]]:
    if seed == 2026071301:
        root = RESULTS / MODELS[model]["seed1"] / "cells"
    else:
        root = RESULTS / f"{model}_math16_ab123_run_003_multiseed" / f"seed_{seed}" / "cells"
    arts = []
    for p in sorted(root.glob("*/artifact.json")):
        arts.append(load_json(p))
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
    return dict(c)


def band_status(actual: float, lo: float, hi: float) -> str:
    if actual < lo:
        return "below band"
    if actual > hi:
        return "above band"
    return "within band"


def verify_run002() -> dict[str, Any]:
    snap = load_json(
        RESULTS / "_phase1_immutability" / "run_002_pre_generation_fingerprint.json"
    )
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
        }
    return out


def build() -> dict[str, Any]:
    data: dict[str, Any] = {
        "title": "Qwen Phase 1 interim report",
        "models": {},
        "assertions": {},
        "prediction_vs_actual": {},
        "ab3_new_seeds": {},
        "run_002_immutability": verify_run002(),
    }

    total_cells = 0
    for model in MODELS:
        per_seed = {}
        pass_rates = []
        all_cells = []
        for seed in SEEDS:
            cells = load_seed_cells(model, seed)
            all_cells.extend(cells)
            pass_n = sum(1 for a in cells if a.get("evaluator_status") == "PASSED")
            fail_n = 48 - pass_n
            layers = layer_counts(cells)
            fail = fail_n if fail_n else 1
            per_seed[str(seed)] = {
                "PASS": pass_n,
                "FAIL": fail_n,
                "pass_rate": pass_n / 48,
                "failure_layer_counts": layers,
                "failure_layer_proportions": {k: v / fail_n for k, v in layers.items()}
                if fail_n
                else {},
            }
            pass_rates.append(pass_n / 48)
            assert len(cells) == 48
        total_cells += len(all_cells)
        pooled_pass = sum(1 for a in all_cells if a.get("evaluator_status") == "PASSED")
        mean_r, sd_r = mean_sd(pass_rates)

        # task-condition groups
        groups = defaultdict(list)
        for a in all_cells:
            key = (a["task_id"], a["condition"])
            groups[key].append(a)
        assert len(groups) == 48
        stability = {
            "stable_pass": 0,
            "stable_fail": 0,
            "unstable": 0,
            "groups": {},
        }
        for (tid, cond), items in sorted(groups.items()):
            assert len(items) == 5
            passes = [1 if x.get("evaluator_status") == "PASSED" else 0 for x in items]
            freq = sum(passes)
            buckets = [outcome_bucket(x) for x in items]
            layers = [
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
            outcome_consistency = len(set(buckets)) == 1
            layer_diversity = len(set(layers)) if layers else 0
            failure_layer_consistency = len(set(layers)) <= 1
            stability["groups"][f"{tid}__{cond}"] = {
                "pass_frequency": f"{freq}/5",
                "stability": label,
                "outcome_consistency": outcome_consistency,
                "layer_diversity": layer_diversity,
                "failure_layer_consistency": failure_layer_consistency,
                "outcome_buckets": dict(Counter(buckets)),
            }

        # condition comparison
        cond_stats = {}
        for cond in CONDITIONS:
            subset = [a for a in all_cells if a["condition"] == cond]
            # 5 seeds * 16 tasks = 80
            assert len(subset) == 80
            by_seed_pass = []
            for seed in SEEDS:
                sc = [a for a in subset if a["seed"] == seed]
                assert len(sc) == 16
                by_seed_pass.append(sum(1 for a in sc if a.get("evaluator_status") == "PASSED") / 16)
            p = sum(1 for a in subset if a.get("evaluator_status") == "PASSED")
            m, s = mean_sd(by_seed_pass)
            fails = [a for a in subset if a.get("evaluator_status") != "PASSED"]
            cond_stats[cond] = {
                "pooled_pass": f"{p}/80",
                "pooled_pass_rate": p / 80,
                "seed_level_mean": m,
                "seed_level_sd": s,
                "failure_layer_counts": layer_counts(fails) if False else layer_counts(subset),
            }

        data["models"][model] = {
            "model_tag": MODELS[model]["tag"],
            "per_seed": per_seed,
            "pooled_pass": f"{pooled_pass}/240",
            "pooled_pass_rate": pooled_pass / 240,
            "seed_level_mean": mean_r,
            "seed_level_sd": sd_r,
            "task_condition_stability": {
                "stable_pass": stability["stable_pass"],
                "stable_fail": stability["stable_fail"],
                "unstable": stability["unstable"],
                "groups": stability["groups"],
            },
            "condition_comparison": cond_stats,
        }

    assert total_cells == 480

    # Ab3 generalization on 384 new cells
    ab3 = load_json(AB3)
    summary = ab3["summary"]
    results = ab3["results"]
    h0_fail = sum(1 for r in results if r["h0_status"] != "PASSED")
    triggers = [
        r
        for r in results
        if r["actual"] in {"layer_exposure", "rescue_to_pass"}
        or (r["actual"] == "guarded_abstain" and r.get("triggered_rule"))
        or r.get("changed")
    ]
    # Prefer summary fields
    trigger_n = summary.get("trigger_count", len(triggers))
    rescue_n = summary.get("rescue_to_pass", 0)
    exposure_n = summary.get("layer_exposure", 0)
    abstain_n = summary.get("guarded_abstain", 0)
    regression_n = summary.get("regression", 0)
    identity = summary.get("identity_reuse", 0)
    data["ab3_new_seeds"] = {
        "label": "frozen-rule generalization across unseen generation seeds on the same fixed task set",
        "H0_FAIL": h0_fail,
        "evaluable_FAIL": h0_fail - summary.get("excluded_no_program_structure", 0),
        "trigger": trigger_n,
        "guarded_abstention": abstain_n,
        "layer_exposure": exposure_n,
        "rescue_to_pass": rescue_n,
        "regression": regression_n,
        "identity_reuse": identity,
        "trigger_over_384": trigger_n / 384,
        "trigger_over_H0_FAIL": (trigger_n / h0_fail) if h0_fail else None,
        "rescue_over_384": rescue_n / 384,
        "rescue_over_triggered": (rescue_n / trigger_n) if trigger_n else None,
        "regression_over_H0_PASS": (regression_n / identity) if identity else 0,
        "by_outcome": summary.get("by_outcome"),
        "by_model": summary.get("by_model"),
    }

    # Prediction vs actual for NEW 192 per model
    preds = load_json(PREDICTIONS)
    pva = {}
    for model_key, model in [("qwen35_4b", "qwen35_4b"), ("qwen35_9b", "qwen35_9b")]:
        new_cells = []
        for seed in NEW_SEEDS:
            new_cells.extend(load_seed_cells(model, seed))
        assert len(new_cells) == 192
        pass_n = sum(1 for a in new_cells if a.get("evaluator_status") == "PASSED")
        pass_rate = 100.0 * pass_n / 192
        band = preds["models"][model_key]["h0_pass_rate"]["predicted_pass_rate_pct_band"]
        fail_cells = [a for a in new_cells if a.get("evaluator_status") != "PASSED"]
        fail_n = len(fail_cells)
        layer_c = layer_counts(new_cells)
        layer_cmp = {}
        for L, info in preds["models"][model_key]["failure_layer_share_among_fail"]["layers"].items():
            share = 100.0 * layer_c.get(L, 0) / fail_n if fail_n else 0.0
            layer_cmp[L] = {
                "actual_share_pct": share,
                "band": info["predicted_share_pct_band"],
                "status": band_status(
                    share, info["predicted_share_pct_band"]["min"], info["predicted_share_pct_band"]["max"]
                ),
            }
        ab3_m = summary["by_model"][model]
        trig = ab3_m.get("trigger", 0)
        exp = ab3_m.get("layer_exposure", 0)
        resc = ab3_m.get("rescue_to_pass", 0)
        reg = ab3_m.get("regression", 0)
        pva[model_key] = {
            "h0_pass_rate_pct": {
                "actual": pass_rate,
                "band": band,
                "status": band_status(pass_rate, band["min"], band["max"]),
                "actual_fraction": f"{pass_n}/192",
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
                "expected": 0,
                "status": "within band" if reg == 0 else "above band",
            },
        }
    data["prediction_vs_actual"] = pva

    # Assertions
    data["assertions"] = {
        "cells_per_model_seed_48": True,
        "cells_per_model_240": True,
        "qwen_total_480": total_cells == 480,
        "run_002_byte_level_unchanged": all(
            v["artifact_unchanged"] and v["raw_unchanged"] for v in data["run_002_immutability"].values()
        ),
        "ab3_outcome_sum_384": sum(summary["by_outcome"].values()) == 384,
    }
    for k, v in data["assertions"].items():
        if not v:
            raise RuntimeError(f"assertion failed: {k}")

    return data


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
    lines.append("All tables below are generated programmatically.")
    lines.append("")

    for model, md in data["models"].items():
        lines.append(f"## Model `{md['model_tag']}` (`{model}`)")
        lines.append("")
        lines.append("### A. Per seed")
        lines.append("")
        lines.append("| seed | PASS/48 | FAIL/48 | failure-layer counts |")
        lines.append("|---|---:|---:|---|")
        for seed, row in md["per_seed"].items():
            layers = ", ".join(f"{k}:{v}" for k, v in sorted(row["failure_layer_counts"].items()))
            lines.append(f"| {seed} | {row['PASS']}/48 | {row['FAIL']}/48 | {layers or '—'} |")
        lines.append("")
        lines.append("### B. Five-seed pooled")
        lines.append("")
        lines.append(
            f"- pooled PASS: **{md['pooled_pass']}** ({md['pooled_pass_rate']:.4f})"
        )
        lines.append(
            f"- seed-level mean ± SD: **{md['seed_level_mean']:.4f} ± {md['seed_level_sd']:.4f}**"
        )
        lines.append("")
        st = md["task_condition_stability"]
        lines.append("### C. Task–condition stability (48 groups × 5 seeds)")
        lines.append("")
        lines.append(
            f"- stable_pass (5/5): {st['stable_pass']}; stable_fail (0/5): {st['stable_fail']}; unstable (1–4/5): {st['unstable']}"
        )
        lines.append("")
        lines.append("### D. Prompt condition comparison")
        lines.append("")
        lines.append("| condition | pooled PASS | seed mean | seed SD |")
        lines.append("|---|---:|---:|---:|")
        for cond, cs in md["condition_comparison"].items():
            lines.append(
                f"| {cond} | {cs['pooled_pass']} | {cs['seed_level_mean']:.4f} | {cs['seed_level_sd']:.4f} |"
            )
        lines.append("")

    ab = data["ab3_new_seeds"]
    lines.append("## E. Frozen Healer seed-generalization (4 new seeds only)")
    lines.append("")
    lines.append(f"Label: `{ab['label']}`")
    lines.append("")
    lines.append(f"- H0 FAIL: {ab['H0_FAIL']}")
    lines.append(f"- evaluable FAIL: {ab['evaluable_FAIL']}")
    lines.append(f"- trigger: {ab['trigger']}")
    lines.append(f"- guarded abstention: {ab['guarded_abstention']}")
    lines.append(f"- layer exposure: {ab['layer_exposure']}")
    lines.append(f"- rescue_to_pass: {ab['rescue_to_pass']}")
    lines.append(f"- regression: {ab['regression']}")
    lines.append(f"- trigger / 384: {ab['trigger_over_384']}")
    lines.append(f"- trigger / H0 FAIL: {ab['trigger_over_H0_FAIL']}")
    lines.append(f"- rescue / 384: {ab['rescue_over_384']}")
    lines.append(f"- rescue / triggered: {ab['rescue_over_triggered']}")
    lines.append(f"- regression / H0 PASS: {ab['regression_over_H0_PASS']}")
    lines.append("")
    lines.append("This is **not** cross-task held-out generalization.")
    lines.append("")

    lines.append("## F. Prediction vs actual (192 new cells / model)")
    lines.append("")
    for model, pva in data["prediction_vs_actual"].items():
        lines.append(f"### `{model}`")
        pr = pva["h0_pass_rate_pct"]
        lines.append(
            f"- H0 PASS rate: actual {pr['actual']:.4f}% ({pr['actual_fraction']}); "
            f"band [{pr['band']['min']}, {pr['band']['max']}] → **{pr['status']}**"
        )
        for L, info in pva["failure_layers"].items():
            lines.append(
                f"- FAIL-share {L}: {info['actual_share_pct']:.4f}% "
                f"band [{info['band']['min']}, {info['band']['max']}] → **{info['status']}**"
            )
        for key in ("trigger_count", "layer_exposure", "rescue_to_pass", "regression"):
            info = pva[key]
            if "band" in info:
                lines.append(
                    f"- {key}: {info['actual']} band [{info['band']['min']}, {info['band']['max']}] → **{info['status']}**"
                )
            else:
                lines.append(f"- {key}: {info['actual']} expected {info['expected']} → **{info['status']}**")
        lines.append("")

    lines.append("## G. Limits")
    lines.append("")
    lines.append("- Qwen Phase 1 interim report only")
    lines.append("- Gemini Phase 2 not completed")
    lines.append("- No full three-model conclusions")
    lines.append("- New seeds not used for rule development")
    lines.append("")
    lines.append("## Assertions")
    lines.append("")
    for k, v in data["assertions"].items():
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append("## run_002 immutability")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(data["run_002_immutability"], indent=2))
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    data = build()
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_MD.write_text(render_md(data), encoding="utf-8")
    print(json.dumps({"report": str(REPORT_MD), "assertions": data["assertions"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
