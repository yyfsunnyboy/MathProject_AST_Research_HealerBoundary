# Math16 Pilot-02 正式結果詮釋與分帳

```text
MATH16_PILOT02_FINAL_INTERPRETATION_DOCUMENTED
```

**研究線：** HealerBoundary／MathProject_AST_Research_HealerBoundary
**模型 cohort：** Gemini 3.5 Flash × Math16 × 4 條件 × 5 seeds = **320 cells**
**本文件角色：** 成果報告／口頭簡報用的**結果詮釋 SSOT**（只整理證據，不改 evaluator／prompt／raw／taxonomy／Healer）
**撰寫基準 HEAD（文件凍結時）：** 以 `math16_pilot02_full_evaluation_v4_r001` 與 Ab2d+spec-v2 purity 產物為準

---

## 0. 三層結果分帳（必讀）

| 層級 | 名稱 | 關鍵數字 | 可否作為正式四條件比較 |
| :--- | :--- | :--- | :---: |
| **Layer 1** | 修訂前歷史結果（pre-fix） | Ab2d+spec-v1 = **58/80**；Overall **265/320** | **否**（僅保留為修訂歷程） |
| **Layer 2** | **正式 primary comparison** | Ab1 **72**／Ab2g **76**／Ab2d+api **78**／Ab2d+spec-v1 **63**；Overall **289/320** | **是** |
| **Layer 3** | Post-hoc mechanism validation | Ab2d+spec-v2 **80/80**；hybrid inventory **306/320** | **否**（探索性機制驗證，不取代 primary） |

**硬性規則：**

- `306/320` **不得**寫成正式四條件總分。
- Ab2d+spec-v2 **不是**事前凍結條件；屬事後補齊 API 文件卡的機制驗證。
- **不得**宣稱 Ab2d+spec 普遍優於 Ab2d+api。
- evaluator 修正、prompt／API 文件補全 **都不是** Healer rescue。

---

## 1. 結果修訂時間線

| 順序 | 事件 | 產物／commit 錨點 | 數字變化 | 模型呼叫 |
| ---: | :--- | :--- | :--- | ---: |
| 1 | 全量 320 格 Taxonomy v3 評分 | `math16_pilot02_full_evaluation_v3_r001`（`5961ef52`） | Overall **265/320**；Ab2d+spec **58/80** | 0（評分） |
| 2 | Oracle Schema Audit V1 凍結 | `docs/experiments/audits/math16_pilot02_oracle_schema_audit_v1.md`（`6fadc0a5`） | 確認 **24** 格 schema 假陰性；校正估計 289/320（非正式） | 0 |
| 3 | Evaluator normalize 修正後離線重評 | `math16_pilot02_full_evaluation_v4_r001`（`1abf7964`） | Overall **289/320**；Ab2d+spec-v1 **63/80**；**24 fail→pass**、**0 pass→fail** | **0** |
| 4 | Ab2d+spec-v2：Fraction×3 API signature 補卡 + q08 對照 | `math16_pilot02_ab2d_spec_v2_evaluation_r001`（`74cb3989`） | 受影響 20 格全過；hybrid 至 **78/80**（Fraction +15） | 20（生成） |
| 5 | q02 `format_latex` 殘餘 L3 補丁（2 seeds） | `…_q02_patch_evaluation_r001`（`07425382`） | hybrid **78→80/80**；Overall hybrid **304→306** | 2 |
| 6 | q02 其餘 3 seeds 版本純度補齊 | `…_q02_purity_evaluation_r001`（`4f4126fd`） | q02 v2 **5/5** 同 SHA；hybrid **維持 80/80、306/320** | 3 |

> 步驟 4–6 為 **post-hoc**；正式對外比較仍停在步驟 3 的 v4 primary。

---

## 2. 正式 primary comparison（v4 evaluator × 凍結 v1 prompts／raw）

**定義：** 共同使用修正後 v4 evaluator，但保留原始凍結 prompts 與 raw responses；條件名中的 Ab2d+spec 即 **Ab2d+spec-v1**。

### 2.1 四條件（各 80 格）

| 條件 | Pass | 角色 |
| :--- | ---: | :--- |
| Ab1 | **72/80** | 裸考基線 |
| Ab2g | **76/80** | 一般格式／結構引導 |
| Ab2d+api | **78/80** | Domain API 完整暴露 |
| Ab2d+spec-v1 | **63/80** | Domain scaffold（事前凍結規格） |
| **Overall** | **289/320** | 四條件合計 |

**加總核對：** \(72 + 76 + 78 + 63 = 289\) ✓

### 2.2 四家族（各 80 格）

| Family | Pass |
| :--- | ---: |
| Integer | **80/80** |
| Polynomial | **74/80** |
| Radical | **70/80** |
| Fraction | **65/80** |

**加總核對：** \(80 + 74 + 70 + 65 = 289\) ✓

### 2.3 條件差（paired，僅描述 primary）

| 對照 | 差值 |
| :--- | ---: |
| Ab2g − Ab1 | +4 |
| Ab2d+api − Ab2g | +2 |
| Ab2d+spec-v1 − Ab2g | −13 |
| Ab2d+spec-v1 − Ab2d+api | −15 |
| post-Healer − baseline | **0**（rescued = 0） |

**證據路徑：** `docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/`

---

## 3. Evaluator audit 影響（v3 → v4）

| 項目 | 數值 |
| :--- | :--- |
| v3 Overall | **265/320** |
| Schema 假陰性（Audit V1） | **24** 格 |
| v4 Overall | **289/320** |
| fail→pass | **24** |
| pass→fail | **0** |
| 重評時模型呼叫 | **0** |
| Healer rescued | **0** |

**意義：** 若答案契約只接受單一包裝形式，會把**數學正確**答案誤判為語意／結構錯誤。v4 以 structural semantics 對齊後，正式 primary 才可信。

**GAP_SUSPECTED（5–6 題）：** 已在 v4 對齊；本 cohort **無新增 flip**，不另開模型實驗。

**不可變證據：**

- Audit：`docs/experiments/audits/math16_pilot02_oracle_schema_audit_v1.md`
- Manifest SHA-256（文件 raw bytes）：`53906c5c3c8abb9412352a49c0e79f3ecda7b1f20183d9ec1084da1fe816fa73`

**歷史對照（非 primary）：** 修訂前 Ab2d+spec-v1 = **58/80**（v3），僅作 pre-fix 紀錄。

---

## 4. Ab2d+spec-v1 → v2 機制驗證（post-hoc）

### 4.1 總覽

| 指標 | 數值 | 標籤 |
| :--- | :--- | :--- |
| Ab2d+spec-v1（primary） | **63/80** | formal |
| Ab2d+spec-v2（補齊 API 文件卡後） | **80/80** | **post-hoc／exploratory** |
| 改善 | **+17** | post-hoc |
| 其中 Fraction 三題 signature 缺口 | **+15** | post-hoc |
| 其中 q02 `to_latex`／`format_latex` 文件缺口 | **+2** | post-hoc |
| Ab2d+api（primary） | **78/80** | formal |
| Ab2d+spec-v2 − Ab2d+api | **+2** | post-hoc 觀測；**不得**概括為「spec 優於 api」 |
| Hybrid inventory（v4 其餘條件 + v2 替換 Ab2d+spec） | **306/320** | **post-hoc inventory only** |

**加總核對：**

- \(63 + 17 = 80\) ✓
- \(15 + 2 = 17\) ✓
- \(289 - 63 + 80 = 306\) ✓（或 \(289 + 17 = 306\)）✓

### 4.2 機制拆解

1. **Fraction×3（q05／q12／q113）**
   v1 scaffold 文件缺口導致 `create(n, d)` 等錯誤 arity → L3 Domain-API misuse（各 0/5）。
   補齊 `FractionOps.create(value)` 與 `FractionOps.from_parts(numerator, denominator)` 後各 **5/5**（+15）。

2. **q02（polynomial division remainder）**
   文件寫成不存在的 `to_latex`；真實 API 為 `PolynomialOps.format_latex(...)`。
   兩格 L3 → PASS（+2）；其後三格以同一凍結 prompt 補齊版本純度。

3. **q02 版本純度**
   五個 seeds 皆使用同一 frozen prompt SHA：
   `f9a51940b166e8613557d1490cf1a331467ffd95af8ca96617aeded15c78fb87`
   結果：**5/5 PASS**。

4. **q08**
   同批加 `format_latex` 卡，但為 native-only；v1 已 5/5，v2 仍 5/5（Δ0；對照格）。

### 4.3 證據路徑

- 首批 20 格：`docs/experiments/results/math16_pilot02_ab2d_spec_v2_evaluation_r001/`
- q02 補丁：`…/math16_pilot02_ab2d_spec_v2_q02_patch_evaluation_r001/`
- q02 純度：`…/math16_pilot02_ab2d_spec_v2_q02_purity_evaluation_r001/`

---

## 5. Primary 與 post-hoc 分帳（對外口徑）

| 對外說法 | 正確 | 錯誤 |
| :--- | :--- | :--- |
| 「正式四條件比較」 | 72／76／78／**63**，總分 **289/320** | 用 80 或 306 取代 63／289 |
| 「Ab2d+spec 為何較低」 | 先講 v1 **63/80** 為正式結果；再說明 post-hoc 顯示多為 API 文件缺口 | 直接說 scaffold 策略無效或已達 80 |
| 「補文件後如何」 | 標示 **post-hoc mechanism validation：80/80（+17）** | 寫成事前凍結條件或正式條件 |
| 「是否優於 Ab2d+api」 | 僅可說本驗證中 v2 比 api **多 2 格**（特定缺口修復後） | 宣稱普遍優於 Ab2d+api |
| 「Healer」 | rescued = **0**；文件補全 ≠ Healer | 把 17 格或 24 格算成 Healer 成效 |

---

## 6. 對 Healer 邊界研究的意義

1. **原始 Ab2d+spec-v1 表現較差，不能直接解讀為 domain scaffold 策略較弱。**
   正式 primary 的 63/80 必須與「文件是否完整可執行」分開解讀。

2. **17 格失敗集中於可識別的 API 文件缺口，而非數學能力不足。**
   補齊 Fraction create／from_parts 與 Polynomial format_latex 後，17 格全部修復。

3. **Domain scaffold 的效果高度依賴 API 規格是否完整、精確、可直接執行。**
   規格缺口會系統性製造 L3，掩蓋真正的數學／語意失敗。

4. **Evaluator schema audit 證明：** 答案契約過窄會把正確數學答案誤判為錯誤；修正屬**評分契約**，不是模型變強，也不是 Healer。

5. **本輪 Healer 仍無 rescue。**
   API 文件修補屬 prompt／spec 改善；evaluator 修正屬評分修正——兩者皆不得計入 Healer 成效。

6. **可修復性窗口仍窄：** 本 cohort 失敗以 L3（API／規格）與 L5（真語意）為主；凍結 deterministic Healer 的 eligible／rescued 皆為 0。

---

## 7. 可直接放入成果報告／口頭簡報的精簡結論

> Math16 Pilot-02（Gemini，320 格）在修正 evaluator 假陰性後，正式四條件為 **Ab1 72、Ab2g 76、Ab2d+api 78、Ab2d+spec-v1 63，合計 289/320**；Healer **零救回**。
> Ab2d+spec-v1 偏低主因不是 scaffold「比較弱」，而是規格文件缺口：事後補齊 API 簽名卡的 **post-hoc** 驗證可到 **80/80（+17）**，其中 Fraction 文件缺口 +15、q02 `format_latex` +2。
> 該 **80/80** 與 hybrid inventory **306/320** 僅作機制驗證，**不取代**正式比較。結論：domain scaffold 有效的前提是 API 規格完整可執行；評分契約與提示規格的缺口都會扭曲「可修復性邊界」的判讀。

---

## 8. 引用索引（唯讀）

| 用途 | 路徑 |
| :--- | :--- |
| Primary 報告 | `docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/math16_pilot02_full_v4_report.md` |
| Pre-fix 歷史 | `docs/experiments/results/math16_pilot02_full_evaluation_v3_r001/` |
| Schema Audit V1 | `docs/experiments/audits/math16_pilot02_oracle_schema_audit_v1.md` |
| Ab2d+spec-v2 首批 | `docs/experiments/results/math16_pilot02_ab2d_spec_v2_evaluation_r001/` |
| q02 patch | `docs/experiments/results/math16_pilot02_ab2d_spec_v2_q02_patch_evaluation_r001/` |
| q02 purity | `docs/experiments/results/math16_pilot02_ab2d_spec_v2_q02_purity_evaluation_r001/` |

---

*本文件不修改 Audit V1、v3_r001、v4_r001、v1 prompts、raw responses，亦不呼叫模型。*
