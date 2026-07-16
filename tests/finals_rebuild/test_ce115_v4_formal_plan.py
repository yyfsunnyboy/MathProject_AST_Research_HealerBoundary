"""Targeted integrity checks for CE115 v4 formal 18-cell plan."""
from scripts.ce115_v4_formal_cohort import formal_plan, EXPECTED_DIGESTS


def test_formal_plan_is_eighteen_unique_from_v3_geometry():
    p = formal_plan()
    assert p["planned_cells"] == 18
    assert len(p["cells"]) == 18
    ids = [c["cell_id"] for c in p["cells"]]
    assert len(set(ids)) == 18
    assert all("ab2d_assembly_v4" in i for i in ids)
    assert all(c["max_model_calls"] == 1 for c in p["cells"])
    assert all(c["retry"] == c["replay"] == c["repair"] == c["healer"] == 0 for c in p["cells"])
    assert p["resume"] is False
    models = {c["model"] for c in p["cells"]}
    assert models == {"qwen3.5:4b", "qwen3.5:9b"}
    assert all(c["digest_prefix"] == EXPECTED_DIGESTS[c["model"]] for c in p["cells"])
    # Stable order: sequence 1..18
    assert [c["sequence"] for c in p["cells"]] == list(range(1, 19))
    # Hash stable across calls
    assert formal_plan()["hash"] == p["hash"]


def test_formal_plan_preserves_v3_task_seed_model_order():
    import json
    from pathlib import Path

    src = json.loads(
        Path("docs/experiments/manifests/ce115_ab2d_corrected_formal_rerun_manifest.json").read_text(
            encoding="utf8"
        )
    )
    p = formal_plan()
    for a, b in zip(src["cells"], p["cells"]):
        assert a["model"] == b["model"]
        assert a["task"] == b["task"]
        assert a["seed"] == b["seed"]
        assert a["cell_id"].replace("ab2d_assembly_v3", "ab2d_assembly_v4") == b["cell_id"]
