# Math16 C4→C5 Tier D D3+D1 Supplemental Closure v1

> **status:** `read_only_supplemental_closure`
> **verdict:** `LOGGING_ONLY_DIFFERENCE` + `ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API` + `FIXED_ORDER_D3_THEN_D1`
> **parent_replay:** `docs/experiments/reports/math16_c4_c5_tier_d_d3_d1_development_replay_v1.md`
> **parent_manifest:** `docs/experiments/manifests/math16_c4_c5_tier_d_d3_d1_development_replay_v1.json`
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`
> **method:** 唯讀靜態稽核（AST binding／call-site／SHA 追溯）；不修改規則、不重跑 replay、不執行 candidate／evaluator、不呼叫模型

---

## 1. Scope

本補充閉合三項 Development 敘事風險：

1. census D1 eligible=4 vs replay D1 triggered=5
2. `ce112_q04` 兩格 verified rescue 的 shadow class 實際呼叫／綁定狀態
3. 重疊格 `ce111_q02…seed_2026072002` 的固定執行順序語意

輸入錨點一律為既有 C4 final post-source 與既有 replay pre／post artifacts；**不**改 replay 統計數字。

---

## 2. D1 trigger-count closure

### 2.1 額外 1 格 identity

| Field | Value |
|---|---|
| Extra cell_id | `qwen3_5_4b__ce111_q10_ordered_quadratic_roots_radical__ab2d__seed_2026072002` |
| Why in replay pool | census **D3 ELIGIBLE**（`parseable_trailing_non_def_residue`） |
| Census D1 status | **`AMBIGUOUS_ABSTAIN`**（`multiple_ops_shadows`）— **非** ELIGIBLE |
| Replay D1 | `triggered=True`, `modified=False`, `abstained=True`, reason=`multiple_ops_shadows` |
| Formal post-source modified by D1? | **否** |

其餘 4 格 census D1 ELIGIBLE 均 `triggered=True` 且 `modified=True`。因此：

\[
\text{D1 triggered}=5 = 4\ (\text{census eligible modified}) + 1\ (\text{non-eligible abstain-trigger in union pool})
\]

### 2.2 C4 → D3 post → D1 靜態比較

| Stage | Source SHA-256 (prefix) | Ops shadows (AST) | D1 `apply_once` |
|---|---|---|---|
| C4 input | `665533e4…afc4` | `RadicalOps` ClassDef L6；`FractionOps` ClassDef L33（**2**） | trigger+abstain；`multiple_ops_shadows`；**未修改** |
| After D3 only | `4030119d…`（trailing L120–135 comment-out） | **相同 2 個 ClassDef／相同 lineno** | 同樣 trigger+abstain；**未修改** |

結論：

- D3 **有**改 AST（trailing residue quarantine），但**未**改變 Ops shadow 集合。
- D1 在純 C4 input 上即會觸發後 abstain；**不是** D3 把該格從「未檢查／非候選」變成「可觸發」。
- 任何路徑下該格 D1 **皆未修改** source。

### 2.3 判定

| Candidate code | Result |
|---|---|
| `ORDER_DEPENDENT_CANDIDATE_EXPANSION` | **駁回**（shadow 不變；C4 上 D1 行為已相同） |
| `CENSUS_CLASSIFICATION_BUG` | **駁回**（census 正確標 `AMBIGUOUS_ABSTAIN`） |
| `LOGGING_ONLY_DIFFERENCE` | **成立**（eligible 計數 ≠ pipeline-realized trigger 計數） |

### 2.4 Census 報告建議（分帳，不改本輪數字）

後續 Tier D 應**分開**報告：

1. **pre-pipeline static supply**＝對 C4 final source 的靜態 eligibility（本輪 D1=4）
2. **pipeline-realized trigger supply**＝固定順序 runner 實際 `triggered`（可含他規則帶入池後的 abstain-trigger；本輪 D1=5）

不得把二者混成單一「eligible／triggered」而無註解。本輪 5 vs 4 **不是 bug**。

---

## 3. Rescue shadow-binding closure

對象（皆 D1-only、verified rescue）：

1. `qwen3_5_4b__ce112_q04_radical_simplification__ab2d__seed_2026071301`
2. `qwen3_5_4b__ce112_q04_radical_simplification__ab2d__seed_2026072002`

### 3.1 seed 2026071301

| Evidence | Detail |
|---|---|
| Pre SHA | `c0c22edcc52f416e962cf6c307cdeba895d25e6f572112c0b33a6a36c86e95f8` |
| Post SHA | `7feb0d2d618d40b1863c4e84d471bf792199e5ca608a952e8abd861a1c1013f2` |
| Shadow 定義 | `ClassDef RadicalOps` L6–39（C4／pre source） |
| `generate` 內 call sites（移除前） | `RadicalOps.simplify_term` L51；`RadicalOps.format_term` L54 |
| Lexical resolution（移除前） | 兩 call 皆綁定至上述 **本地 ClassDef**（非 unresolved） |
| 執行路徑是否使用 shadow | **是**（call 位於 `generate` body） |
| 移除後 | 無本地 `RadicalOps` binding；同名 call 改為 **unresolved → runtime 注入 Ops** |
| 分類 | **`ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API`** |

### 3.2 seed 2026072002

| Evidence | Detail |
|---|---|
| Pre SHA | `b9b53d13d27f4800900e3f43c7765f668fdaa3e4233c0bc0fe01d0127defaee7` |
| Post SHA | `b033b87a052cef51f5d4f0ebbb3ab94cb2f33b8319fa20bf6847fd8fd8c384d3` |
| Shadow 定義 | `ClassDef RadicalOps` L6–47 |
| `generate` 內 call sites（移除前） | `RadicalOps.simplify_term` L58；`RadicalOps.format_term` L60 |
| Lexical resolution（移除前） | 皆綁定本地 ClassDef |
| 執行路徑是否使用 shadow | **是** |
| 移除後 | 無本地 binding → runtime 注入 |
| 分類 | **`ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API`** |

### 3.3 排除項

- **不是** `DEAD_SHADOW_REMOVAL`（shadow 非未被 call 的死定義）。
- **不是** `MIXED_OR_UNRESOLVED`（兩格證據一致、可解析）。

### 3.4 正式措辭（強制）

禁止（除非該 cell 已證明屬 `DEAD_SHADOW_REMOVAL`）：移除死代碼；清除未使用 class；刪除無關定義。

統一使用：

> 以 frozen scaffold 注入的正式 Ops implementation，取代模型自訂的 active shadow implementation。

`verified rescue = 2` **仍可保留**（觀測 FAIL→PASS 不變；僅機制敘事鎖定為 active replacement，不得寫成 dead-code removal）。

---

## 4. Overlap order closure

Cell：`qwen3_5_4b__ce111_q02_polynomial_division_remainder__ab2d__seed_2026072002`

| Check | Evidence |
|---|---|
| 固定順序 | `RULE_ORDER = (D3, D1)`；pipeline 原始碼無 evaluator／PASS／answer 分支 |
| 非動態競選 | `selected_rule` 由 `rules_fired` 序列字串化（`D3+D1`），非 ranking 勝出 |
| D3 edit | residue comment-out L127–144；pre `a6500a06…d360` → mid `f22c2d70…f938` |
| D1 edit | remove `ClassDef PolynomialOps` L18–49；mid `f22c2d70…f938` → post `5f9713c3…6a14` |
| 累積 | 同格兩條不同規則皆 `applied`；各 `edit_count=1` |
| 每規則最多一次 | 第二次全 pipeline 零 diff（既有 replay 已記錄） |
| Final post SHA | `5f9713c34759d08e9c5e1690cb4d20af423763e626cfdeb24cc04a2cb8616a14`（與 replay 一致） |

**判定：** `FIXED_ORDER_D3_THEN_D1`（固定序列累積，不是候選競選）。

---

## 5. Interpretation impact

| Question | Answer |
|---|---|
| D1 5 triggered vs 4 eligible 是否 bug？ | **否** — `LOGGING_ONLY_DIFFERENCE` |
| census 與 pipeline trigger 是否順序依賴？ | **本差異不依賴順序**；D3 未擴張該格 D1 候選。仍建議分帳 static supply vs pipeline-realized triggers |
| 兩格 rescue 機制？ | **`ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API`** |
| D3→D1 是否固定？ | **是** |
| verified rescue 2 是否保留？ | **是**（改敘事，不改計數） |

不影響既有 aggregate：modified=7、rescue=2、regression=0、degraded=0。

---

## 6. Final wording for report／Q&A

**建議正式段落（可直接引用）：**

> Tier D Development（D3→D1）在 C4 still-FAIL 的 D3／D1 union 池上觀察到 **verified rescue = 2**，且無 parse／execution regression。兩格 rescue 皆來自 D1，binding class 為 **`ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API`**：以 frozen scaffold 注入的正式 Ops implementation，取代模型自訂的 active shadow implementation（AST 證明 `generate` 內 `RadicalOps.*` 原綁本地 ClassDef）。**不得**稱為死代碼清除。D1 triggered=5 對 census eligible=4 的差額來自 1 格 D3-eligible／D1-`AMBIGUOUS_ABSTAIN` 細胞在固定 pipeline 中觸發後 abstain 且未修改，屬 **logging／計數定義差異**，不是 census 錯標，也不是 D3 造成的候選擴張。重疊格依固定順序 D3→D1 各最多修改一次，`selected=D3+D1` 表示序列累積而非競賽選元。

**Q&A 短答：**

- Q: 5 vs 4 是 bug 嗎？ → A: 不是；分帳看 static eligibility 與 pipeline triggers。
- Q: rescue 是刪死代碼嗎？ → A: 不是；屬 `ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API`——以 frozen scaffold 注入的正式 Ops implementation，取代模型自訂的 active shadow implementation。
- Q: 順序會依結果變嗎？ → A: 不會；凍結為 D3→D1。

---

## Declarations

- 未修改規則實作
- 未重跑 Development replay／未改 replay 統計
- 未執行 candidate／evaluator（本輪）
- 未呼叫模型
- 未 commit／未 push
