# Math16-LaTeX-v1 pre-live freeze closeout

- Pool: `Math16-LaTeX-v1`
- Base HEAD at freeze: `6107ac7a3cc46d7d41d6e373ef191ac278f2fe98`
- Gemini live run: **not executed** in this closeout
- Purpose: freeze pool/contracts/oracles/prompts/preflight before 48-cell Gemini run

## Known baseline failure (not introduced by Math16)

| Item | Detail |
|------|--------|
| Test | `tests/finals_rebuild/test_math_task_oracles.py::test_manifest_is_twelve_immutable_oracle_tasks` |
| Status at clean HEAD `6107ac7…` | Already failing |
| Cause | Fixture `math_generation_tasks_ce115_pilot.jsonl` has **31** rows; test still asserts `len(tasks) == 12` |
| Math16 impact | **None** — Math16 did not modify that fixture or that test |
| Policy | Do **not** relax or patch this legacy test as part of Math16 freeze; track separately |

## No-model gates for this freeze

- `pytest tests/finals_rebuild/test_math16_latex_v1.py` → 14 passed
- `python scripts/preflight_math16_latex_v1.py` → passed
- JSON parse of Math16 manifests / preflight artifact → passed
- `git diff --check` → passed

## Frozen hashes

| Key | SHA256 |
|-----|--------|
| pool_identity_hash | `2ff41465d818d7e3d9b990a27ad2a1535e72c271bb04b2a37abe29cec1824636` |
| final_manifest_hash | `a4fc49b035cb6fed2d7a6946e241dc3ef36ed66f1a9fc09b3ecee5714a28a591` |
| task_freeze_hash | `349dfb2f786a4aa029453d844cac7eca07deb24a777ba1be4ef70f7002882e14` |
| manifest_file_sha256 | `8f2d6b4a9bc55e2ba8d5c00b372b8421ba89463b9a0802865ff791ffce1c3b9e` |

Prompt lineage: `ce115_clean_incremental_ablation_v1`  
48 prompt hashes: `docs/experiments/results/math16_latex_v1_freeze_closeout_report.json`  
Preflight artifact: `docs/experiments/results/math16_latex_v1_preflight.json`
