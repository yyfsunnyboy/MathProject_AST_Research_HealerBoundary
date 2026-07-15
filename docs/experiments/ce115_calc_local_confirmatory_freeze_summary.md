# CE115 Qwen3.5 Local Confirmatory — Observed Results Freeze

## Freeze identity

| Field | Value |
|-------|-------|
| Starting HEAD (pre-freeze) | `a4b9ee490d2bba4a3405aacea70a7036fa2a94a9` |
| Cohort | `qwen3.5:4b` + `qwen3.5:9b` |
| Ollama | `0.32.0` |
| Results dir | `docs/experiments/results/ce115_calc_local_confirmatory/` |
| Manifest hash | `d8f6c5fc91ec66e581aa27194cfb83e3ff825b1d08117bfaee2116eabd1d5a7d` |
| Artifact content hash (72-cell set) | `c6e47dddb0c3e01846a8043a4604bb7eb9000622aaa34aee7f894aacbf788468` |
| Evidence dataset hash | `6d9fb828a7b804dee8d5070f3982266bb24dc15cdf6791aa5a9c30a420e6dfcc` |
| Evidence build hash | `7b905f4ec6120382e9e1d2fdc88326f0605a390576298e8244cffd0cf1bb147d` |

## Geometry

| Metric | Value |
|--------|-------|
| planned / executed | 72 / 72 |
| unique cell_id | 72 |
| duplicates / missing / unexpected | 0 / 0 / 0 |
| qwen3.5:4b / qwen3.5:9b | 36 / 36 |
| per task | 18 |
| per condition (ab1 / ab2g / ab2d) | 24 / 24 / 24 |
| per seed (2026071301/02/03) | 24 / 24 / 24 |

## Model digests

| Model | Digest prefix |
|-------|---------------|
| `qwen3.5:4b` | `2a654d98e6fb` |
| `qwen3.5:9b` | `6488c96fa5fa` |

## Call counts (observed freeze)

| Counter | Value |
|---------|------:|
| model calls | 72 |
| healer | 0 |
| retry | 0 |
| external API | 0 |

## Schema / G6 notes (observed, immutable)

- Formal executed JSONL **does not persist** model-returned `correct_answer` / `oracle_expected` answer text fields; report Answer G6a/G6b remain `NOT_OBSERVED` by design.
- Unique Question G6b FAIL cell_id (genuine renderer residual LaTeX):
  `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071303`

## Smoke continuity

One prior smoke cell is included unchanged in the 72-cell set:

`qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071301`

content SHA-256: `137f05c3ddf21af06c71e1cea0431b106bcdaf82b844f2a2c328b9d0afb44e4d`

## Live runner

Reusable entrypoint (transport injected; resume-safe):

`scripts/run_ce115_calc_local_confirmatory_live.py`
