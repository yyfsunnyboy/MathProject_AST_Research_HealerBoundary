# CE115 Q9 — Gemini-only L5 mechanism forensic (frozen)

Status: offline forensic only. `real_model_calls = 0`. No prompt / evaluator / oracle / Healer changes. No commit/push.

Evidence policy: visible `raw_response.txt`, `extracted_candidate.py`, and evaluator records only. No hidden chain-of-thought.

Machine-readable ledger: `ce115_q09_gemini_l5_mechanism_ledger.json`.

## Oracle target

`(leading·x − subtracted)·(x + shared_shift) = 0`
→ roots `{subtracted/leading, −shared_shift}`, ordered `a>b`, then `value = a + 2b`.

## A. Observable generation path for `[12, 7]`

Observed on formal pilot Ab1/Ab2d and all three sign-pairing `xp7_2xm10` cells.

Visible code (example Ab1):

```text
# Equation: leading_factor * (x - shared_shift)^2 - subtracted_factor * (x - shared_shift) = 0
r1 = shared_shift                              # → 7
r2 = shared_shift + subtracted_factor/leading   # → 7 + 10/2 = 12
order a>b → [12, 7]
value = 12 + 2*7 = 26
```

That equation is algebraically solved correctly for itself, but it is **not** the oracle identity `(2x−10)(x+7)=0` (roots `[5,−7]`).

Earliest observable error: **equation reconstruction** → primary `EQUATION_RECONSTRUCTION_WRONG`
Secondary label: `SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE`.

Note: `actual_question_text` showing `2(x-7)^2 − 10(x-7)=0` is the model’s own `question_text`, consistent with the same wrong template — not an external gold stem.

## B. Primary mechanism distribution (15 Gemini cells)

| Primary L5 | n | Where |
|---|---|---|
| `EQUATION_RECONSTRUCTION_WRONG` | 8 | xp7_2xm10×3; xm7_2xm10 ab1; xp7_2xp10 ab1/ab2g; pilot ab1/ab2d |
| `PARAMETER_ARITHMETIC_TEMPLATE` | 4 | xm7_2xm10 ab2g/ab2d; xm7_2xp10 ab1; pilot ab2g |
| `FACTOR_CONSTANT_COPIED_AS_ROOT` | 2 | xm7_2xp10 ab2g/ab2d |
| `LINEAR_COEFFICIENT_IGNORED` | 1 | xp7_2xp10 ab2d |
| `NOT_VERIFIED` | 0 | — |

## C. Cross-condition / cross-instance stability

Stable mechanisms (same generation path, not merely same final numbers):

1. **SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE** — Ab1+Ab2g+Ab2d on `xp7_2xm10`; also formal pilot Ab1/Ab2d; also `xp7_2xp10` Ab1/Ab2g (output `[7,2]` with `subtracted=-10`); also `xm7_2xm10` Ab1 (`[-2,-7]`).
2. **SHIFT_PM_SUBTRACTED** — `xm7_2xm10` Ab2g+Ab2d → `[3,-17]`.
3. **PARAMS_COPIED_AS_ROOTS** — `xm7_2xp10` Ab2g+Ab2d → `[-7,-10]`.

## D. Secondary taxonomy (safe reporting layer)

New secondary labels under existing primary candidates (analysis-only; **not** Healer rules):

| Secondary | Primary | Formula |
|---|---|---|
| `SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE` | `EQUATION_RECONSTRUCTION_WRONG` | `{s, s+D/L}` via `L(x−s)^2 − D(x−s)=0` |
| `SHIFT_PM_SUBTRACTED` | `PARAMETER_ARITHMETIC_TEMPLATE` | `{s+D, s−D}` |
| `PARAMS_COPIED_AS_ROOTS` | `FACTOR_CONSTANT_COPIED_AS_ROOT` | `{s, D}` |
| `SHIFT_AND_SHIFT_MINUS_SUB` | `PARAMETER_ARITHMETIC_TEMPLATE` | `{s, s−D}` |
| `SHIFT_AND_SHIFT_PLUS_SUB_NO_DIV` | `LINEAR_COEFFICIENT_IGNORED` | `{s, s+D}` |
| `SHIFT_PM_SUB_OVER_LEADING` | `PARAMETER_ARITHMETIC_TEMPLATE` | `{s±D/L}` (pilot Ab2g → `[12,2]`) |

Same final answer ≠ same mechanism only when checked against code. Here, repeated finals **do** share mechanisms when they repeat.

## E. NOT_VERIFIED

None in this Gemini cohort — every cell has an explicit root assignment in extracted code.

## F. Report-safe conclusions

1. Gemini q09 failures are **generator reconstruction / parameter-template errors**, not ordering or final-combination errors on correct roots.
2. `[12,7]` is a fully observable, cross-condition **SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE** path; it is not unexplained fabrication.
3. Sign-pairing did **not** surface a clean `ROOT_SIGN_NOT_NEGATED`-only syndrome as the earliest step; sign issues appear as consequences of wrong factor form.
4. Ab2d DOMAIN (`FractionOps`) does not block the dominant wrong template on `xp7_2xm10`.
5. Safe next research focus: force / check reconstruction of `(leading·x − subtracted)·(x + shift)` before inventing root arithmetic — not a new Healer rule in this round.

## G. Commit status

Uncommitted / unpushed. Offline forensic artifacts only.
