# G4 forensic: 113-10 Ab2d after kwargs-bag inline

## A. Mechanism

1. Prior experimental rule inlined empty `kwargs.get('frozen', {})` → frozen literal.
2. Candidate runs Domain API chain and builds a factors dict.
3. Return wraps answer as `json.dumps(correct_answer)` → **str**.
4. Oracle `exam_factorization_common_binomial` requires `dict` with `factors` list.
5. Field compare (report-only):
   - expected: `{"factors": [{"x_coefficient": 5, "constant": -2}, {"x_coefficient": -15, "constant": 8}]}`
   - predicted (parsed): `{"factors": [{"x_coefficient": -5, "constant": 2}, {"x_coefficient": 15, "constant": -8}]}`
   - algebraically equivalent under overall sign flip; oracle accepts when typed as dict.
6. G4 fails solely because submitted type is str.

## B. Nature

**a_format_wrapping** — 格式/包裝層錯誤：值（經 json.loads + 符號翻轉等價）通過 oracle，但 correct_answer 以 json.dumps 字串回傳導致 oracle 拒收

## C/D. Follow-on

See `summary.json` / `RULE_CARD.md` for unwrap experimental rule + regression.
