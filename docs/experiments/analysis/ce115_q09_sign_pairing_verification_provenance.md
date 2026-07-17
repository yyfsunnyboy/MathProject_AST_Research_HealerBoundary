# CE115 Q9 linear-factor sign-pairing verification — provenance

Status: experiment-local (does **not** modify production q09 task / oracle / evaluator / Healer).

Cohort class: **diagnostic** (Evidence Freeze cohort C).
Not a production task expansion. Do **not** include in core Healer success rates.

## Equation identity (shared schema)

Frozen fields (same as formal q09):

`shared_shift`, `leading_factor`, `subtracted_factor`, `root_order=a>b`, `linear_combination={a:1,b:2}`

Reconstruction:

`(leading_factor·x − subtracted_factor)·(x + shared_shift) = 0`

## Four instances

| instance_id | equation | factor1 | factor2 | payload (shift, lead, sub) | roots (a>b) | a+2b |
|---|---|---|---|---|---|---|
| `xp7_2xm10` | `(x+7)(2x-10)=0` | x+c | 2x−c | (7, 2, 10) | [5, −7] | −9 |
| `xm7_2xm10` | `(x-7)(2x-10)=0` | x−c | 2x−c | (−7, 2, 10) | [7, 5] | 17 |
| `xp7_2xp10` | `(x+7)(2x+10)=0` | x+c | 2x+c | (7, 2, −10) | [−5, −7] | −19 |
| `xm7_2xp10` | `(x-7)(2x+10)=0` | x−c | 2x+c | (−7, 2, −10) | [7, −5] | −3 |

Notes:

- `xp7_2xm10` ≡ formal q09 freeze (canonical hashes must match).
- Negative `shared_shift` is **experiment-local** evaluation only; production oracle still requires positive shift and is untouched.

## Prompt composition

Shared lineage `ce115_clean_incremental_ablation_v1`:

- Ab1 = BASE
- Ab2g = BASE + frozen GENERIC (unchanged)
- Ab2d = BASE + GENERIC + frozen DOMAIN (unchanged FractionOps set)

## Seed / policy

seed=`2026071301`, first attempt only, retry=0, healer=0, think=false.
