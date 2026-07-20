# Evidence gap: Qwen Math16 prose predictions

Audit date: 2026-07-20 (Asia/Taipei)

The prose-qualification predictions artifact previously identified by the
SHA-256 prefix `ffe24652` is not present in reachable Git history.

The audit used both path history and reachable-object enumeration:

- `git log --all --full-history --name-status --pretty=... -- "*predictions*"`
- `git rev-list --objects --all`, filtered case-insensitively for paths containing
  `predictions`
- exact SHA-256 calculation over every matching Git blob via `git cat-file blob`

Reachable prediction blobs found:

| Commit | Path | Git blob SHA-256 |
|---|---|---|
| `6cacaf52d6a718909bafe816b13a110058d739e2` | `docs/experiments/predictions/qwen_math16_predictions.md` | `393252c7c3dd74e189dea8c7bcdcd8fb61c371b35217899ec386003b5755cd2b` |
| `36126ce4ef6eaf4e79185650552e61e65b896c87` | `docs/experiments/results/qwen_math16_run_002_delimiter_extended_predictions.json` | `6ff74bff1bfe23d147de7bde6eca3e450d198a1d688c94370223648692af5e6f` |
| `16cf3466b71ccf2f728202ea0e7386534e981b2d` | `docs/experiments/results/qwen_math16_run_002_healer_predictions.json` | `783a96e405d2d890e634a1513a186cb3b7c61ddd498255f81b0b5b36d694eba1` |

No matching blob has a SHA-256 beginning with `ffe24652`. Consequently, the
original prose predictions artifact cannot be restored from reachable Git
history. This note records the missing link without reconstructing or
back-dating evidence.
