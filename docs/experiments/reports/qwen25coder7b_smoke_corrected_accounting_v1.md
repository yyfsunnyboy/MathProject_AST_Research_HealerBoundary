# Qwen2.5-Coder:7B Math16 Four-Condition Smoke — Corrected Accounting v1

- **狀態**：唯讀稽核產物。不覆寫、不修改 `docs/experiments/results/qwen25coder7b_math16_four_condition_smoke_20260725_001/` 下任何既有 artifact、summary或報告。
- **依據**：`docs/experiments/reports/smoke_pipeline_known_issues_v1.md` 所記載的 K1／K2／K3 缺陷定義。
- **範圍**：僅本run（16 cell），不外推至其他run或其他模型。

---

## 逐格修正表（16/16）

| # | task | condition | original outcome | corrected validity | corrected descriptive outcome | K1/K2/K3觸發 | 納入有效分母 | 為有效模型FAIL | direct evidence path |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ce115_calc_polynomial_division_l1 | ab1 | runtime_failure | VALID_MODEL_OUTCOME | 真實runtime_failure（模型candidate執行期例外，於oracle階段之前發生，與K1/K2/K3無關） | 無 | 是 | 是 | `.../qwen25coder7b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301/artifact.json` |
| 2 | ce115_calc_polynomial_division_l1 | ab2g | runtime_failure | VALID_MODEL_OUTCOME | 同上 | 無 | 是 | 是 | `.../qwen25coder7b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071301/artifact.json` |
| 3 | ce115_calc_polynomial_division_l1 | ab2d | passed | VALID_MODEL_OUTCOME | 真實PASS | 無 | 是 | 否（PASS） | `.../qwen25coder7b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301/artifact.json` |
| 4 | ce115_calc_polynomial_division_l1 | ab2d_spec_v2 | passed | VALID_MODEL_OUTCOME | 真實PASS | 無 | 是 | 否（PASS） | `.../qwen25coder7b__ce115_calc_polynomial_division_l1__ab2d_spec_v2__seed_2026071301/artifact.json` |
| 5 | ce111_q03_prime_factor_selection | ab1 | schema_failure | VALID_MODEL_OUTCOME | 真實schema_failure：candidate執行時`n`被迴圈就地修改（`n //= candidate`），回傳`oracle_payload={"candidates":[...],"n":1}`≠frozen`{"n":156}`，evaluator正確攔截 | 無 | 是 | 是 | `.../qwen25coder7b__ce111_q03_prime_factor_selection__ab1__seed_2026071301/{artifact.json,extracted_candidate.py}` |
| 6 | ce111_q03_prime_factor_selection | ab2g | intrinsic_safety | **INVALID_CONTRACT** | oracle_payload恆為`{"candidates":[11,12,13,14],"n":156}`，缺`selected`/`value`/`a`+`b`；`evaluate_integer_exact()`無條件回傳`error="integer_exact payload incomplete"`，與提交答案內容無關（見candidate提交13，本身正確） | **K1** | **否** | **否**（不得算模型PASS或FAIL） | `.../qwen25coder7b__ce111_q03_prime_factor_selection__ab2g__seed_2026071301/{artifact.json,extracted_candidate.py}` |
| 7 | ce111_q03_prime_factor_selection | ab2d | intrinsic_safety | **INVALID_CONTRACT** | 同上機制；candidate提交`correct_answer=2`（`len(prime_factors)`，本身即為錯誤答案），但oracle仍因缺鍵而恆定回錯誤，與此答案對錯無關 | **K1** | **否** | **否** | `.../qwen25coder7b__ce111_q03_prime_factor_selection__ab2d__seed_2026071301/{artifact.json,extracted_candidate.py}` |
| 8 | ce111_q03_prime_factor_selection | ab2d_spec_v2 | intrinsic_safety | **INVALID_CONTRACT** | 同上機制；candidate提交`correct_answer=13`（客觀正確），仍被判錯——最強反證 | **K1** | **否** | **否** | `.../qwen25coder7b__ce111_q03_prime_factor_selection__ab2d_spec_v2__seed_2026071301/{artifact.json,extracted_candidate.py}` |
| 9 | ce111_q05_exact_fraction_expression | ab1 | intrinsic_safety | **有效模型FAIL（label錯誤）** | payload完整（`{"expression":"9/22 + 11/18 - (23/22 - 7/18)"}` == frozen），oracle正確算出期望值4/11，candidate提交40/99，`Fraction(40,99)≠Fraction(4,11)`，`evaluate_exact_fraction_canonical()`回傳`error="fraction_mismatch"`（非執行錯誤），被`classify_response`誤映射為`intrinsic_safety` | **K2** | **是** | **是** | `.../qwen25coder7b__ce111_q05_exact_fraction_expression__ab1__seed_2026071301/{artifact.json,extracted_candidate.py}` |
| 10 | ce111_q05_exact_fraction_expression | ab2g | passed | VALID_MODEL_OUTCOME | 真實PASS | 無 | 是 | 否（PASS） | `.../qwen25coder7b__ce111_q05_exact_fraction_expression__ab2g__seed_2026071301/artifact.json` |
| 11 | ce111_q05_exact_fraction_expression | ab2d | runtime_failure | VALID_MODEL_OUTCOME | 真實runtime_failure，於oracle階段之前發生 | 無 | 是 | 是 | `.../qwen25coder7b__ce111_q05_exact_fraction_expression__ab2d__seed_2026071301/artifact.json` |
| 12 | ce111_q05_exact_fraction_expression | ab2d_spec_v2 | passed | VALID_MODEL_OUTCOME | 真實PASS | 無 | 是 | 否（PASS） | `.../qwen25coder7b__ce111_q05_exact_fraction_expression__ab2d_spec_v2__seed_2026071301/artifact.json` |
| 13 | ce115_calc_radical_simplification_l1 | ab1 | intrinsic_safety | **有效模型FAIL（label錯誤）** | payload完整（`{"radicand":27}`==frozen），oracle正確算出期望`{coefficient:3,radicand:3}`，candidate提交`{coefficient:3,radicand:27}`（未化簡），`structural_ok=False`→`error="structural_mismatch"`，被誤映射為`intrinsic_safety` | **K2** | **是** | **是** | `.../qwen25coder7b__ce115_calc_radical_simplification_l1__ab1__seed_2026071301/{artifact.json,extracted_candidate.py}` |
| 14 | ce115_calc_radical_simplification_l1 | ab2g | intrinsic_safety | **有效模型FAIL（label錯誤）** | 同上機制，candidate同樣提交`{coefficient:3,radicand:27}` | **K2** | **是** | **是** | `.../qwen25coder7b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301/{artifact.json,extracted_candidate.py}` |
| 15 | ce115_calc_radical_simplification_l1 | ab2d | passed | VALID_MODEL_OUTCOME | 真實PASS | 無 | 是 | 否（PASS） | `.../qwen25coder7b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301/artifact.json` |
| 16 | ce115_calc_radical_simplification_l1 | ab2d_spec_v2 | answer_incorrect | VALID_MODEL_OUTCOME | 真實answer_incorrect：`evaluation_details_keys`不含`oracle_error`，走的是乾淨比對路徑（error=None），非K2誤標 | 無 | 是 | 是 | `.../qwen25coder7b__ce115_calc_radical_simplification_l1__ab2d_spec_v2__seed_2026071301/artifact.json` |

（路徑前綴皆為 `docs/experiments/results/qwen25coder7b_math16_four_condition_smoke_20260725_001/`）

verified 16/16（每格皆對照summary.json outcome、artifact.json、extracted_candidate.py，K1/K2觸發格另交叉核對math16_oracles.py之oracle函數原始碼）。第1/2/11格（runtime_failure）之確切exception子類型本輪未重新逐字核對detail文字（僅outcome label與階段順序已確認在oracle之前發生），不影響其VALID_MODEL_OUTCOME／有效FAIL之分類。

---

## 統計口徑（confirmed）

| 項目 | 數值 | 說明 |
|---|---|---|
| total cells | 16 | run manifest原生cell數 |
| INVALID_CONTRACT（K1，排除） | 3 | #6,7,8 |
| valid evaluated cells | **13** | 16 − 3(K1) |
| PASS | **5** | #3,4,10,12,15 |
| valid FAIL | **8** | 13 − 5；= K2的3格(#9,13,14) + 其他有效FAIL的5格(#1,2,5,11,16) |
| valid-cell PASS rate | **5/13 ≈ 38.5%** | 排除K1後，母體=13的真實模型能力比較口徑 |
| historical raw PASS rate | **5/16 = 31.25%** | 僅描述原始run的原生分母，**不得**用於任何模型間公平能力比較（因分母混入3格根本無法判分的INVALID_CONTRACT） |
| Healer eligibility母體 | **8個有效FAIL**（不是11個） | K1的3格因oracle無法判分，天生不具備「可修復後重判」的前提，必須排除；K2的3格是真實答錯，屬合法Healer eligibility審查對象 |

**K2的3格（#9,13,14）明確處置**：計入13格有效分母、計入8格有效FAIL、計入後續Healer eligibility審查母體。
**K1的3格（#6,7,8）明確處置**：排除於PASS rate分母、排除於Healer eligibility母體、不算模型PASS也不算模型FAIL。

本輪**不**執行8格Healer eligibility的實際規則判定（哪幾格屬於哪個修復規則、是否可修復），該項留待下一輪。

---

## 5/13 與 5/16 的用途差異

- **5/13**（valid-cell PASS rate）：分母已扣除3格INVALID_CONTRACT（oracle物理上無法判分的cell），代表「在oracle contract有效的前提下，模型的真實PASS比例」，是唯一可用於後續與其他模型/其他run做能力比較的口徑。
- **5/16**（historical raw PASS rate）：分母是原始summary.json的原生cell數，未扣除任何contract缺陷，**只能用於描述「這個run原始記錄長什麼樣子」這一歷史事實**，因為其中3格根本不是模型能力的展現（oracle無論答案對錯都會回錯誤），把它們留在分母裡會系統性低估模型真實能力，**不得**拿5/16去跟其他模型的PASS rate做公平比較。

---

## K1排除的3格

1. `ce111_q03_prime_factor_selection / ab2g`
2. `ce111_q03_prime_factor_selection / ab2d`
3. `ce111_q03_prime_factor_selection / ab2d_spec_v2`

（皆為INVALID_CONTRACT，排除於PASS rate分母與Healer eligibility母體，不算模型PASS或FAIL）

## K2仍納入有效FAIL的3格

1. `ce111_q05_exact_fraction_expression / ab1`（真實答錯：40/99 vs 正解4/11）
2. `ce115_calc_radical_simplification_l1 / ab1`（真實答錯：radicand=27未化簡，正解radicand=3）
3. `ce115_calc_radical_simplification_l1 / ab2g`（同上機制）

（皆為有效模型FAIL，只是outcome label被錯誤映射為`intrinsic_safety`；納入13格有效分母、8格有效FAIL、Healer eligibility母體）

---

## 被撤回或降級的舊7B結論

| 舊結論 | 處置 | 理由 |
|---|---|---|
| `Rule coverage 9%` | **撤回** | 此比例的分母/分子基礎未排除K1的3格INVALID_CONTRACT cell，計算基礎已知有誤，不可沿用 |
| `1/11 eligible` | **撤回或改列為未驗證** | 「11」這個分母混用了K1(3格，不該進入FAIL母體)與K2(3格，本應計入有效FAIL)，且本輪未重新做eligibility判定，故該數字目前既非13、也非8，狀態應為未驗證 |
| `6格intrinsic_safety可能為安全過濾／evaluator false positive` | **撤回** | 逐格核對後，6格中3格(#6,7,8)確認為K1(合約缺鍵，非安全過濾)，另3格(#9,13,14)確認為K2(oracle正確判斷答錯，只是label映射錯誤，同樣非安全過濾)。「可能為安全過濾」的表述本身已被直接證據排除；正確定性是「evaluator label defect」，且該defect本身分屬兩種不同機制(K1/K2)，不可合併成單一"6格"陳述 |
| `5/16 PASS` 作為公平模型比較口徑 | **撤回** | 分母未排除K1的3格，屬於受汙染的原始記錄口徑，僅能描述本run歷史事實，不得用於跨模型比較 |
| corrected有效PASS rate | **確認為 `5/13`** | 見上表 |
| Healer eligibility母體 | **確認為8個有效FAIL，不是11個** | 11 = 13(有效分母) − 5(PASS) + 3(誤把K1也算進FAIL母體)，此前的11混入了3格根本不該進入FAIL母體的INVALID_CONTRACT cell |

---

## 起始／結束Git狀態

- 起始：`main` @ `c5bddac8`，origin/main同步，2個既存modified正式檔案未變動，untracked清單與任務起始時一致。
- 結束：與起始相同，僅新增本文件與同輪的K1/K2/K3文件，2個既存modified正式檔案未被觸碰，未stage、未commit、未push。
