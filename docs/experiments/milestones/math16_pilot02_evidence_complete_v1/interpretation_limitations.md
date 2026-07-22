# Math16 Pilot-02 方法學與推論限制清冊 (Interpretation Limitations v1)

```text
INTERPRETATION_LIMITATIONS_V1_FROZEN
TEN_MANDATORY_METHODOLOGY_LIMITATIONS
BOUNDED_SCIENTIFIC_CLAIMS_ONLY
```

本清冊收錄「Ivan旺宏科學展」HealerBoundary 研究線在 Math16 Pilot-02 階段凍結之 10 項關鍵方法學限制。任何基於本實驗成果之報告書、展板、口頭簡報與學術論文，均不得超出以下邊界宣稱：

---

## 10 項強制方法學限制 (Ten Mandatory Methodology Limitations)

1. **Overall 統計顯著性與外推不確定性 (Cell-level vs Task-level)**：
   - 細胞層級 Exact McNemar 檢定顯示 9B-only PASS (49格) 顯著多於 4B-only PASS (26格)，$p = 0.010582$。
   - 然考慮 16 個 Task 聚類效應之 Task-clustered Bootstrap 95% CI 跨 0 (`[-0.94%, +14.38%]`)，顯示將結論外推至未知全新數學題型時仍具抽樣不確定性。不得宣稱「9B 在所有未見題型上均保證優於 4B」。

2. **四大數學家族分層屬探索性分析 (Exploratory Subgroup Analysis)**：
   - Integer, Polynomial, Radical, Fraction 四大家族分層並未在事前預註冊 Protocol 中作 alpha 族群矯正 (Family-wise Error Rate control)，屬 Post-hoc 事後探索性分析，其 $p$-values 僅供假說生成參考。

3. **Fraction 家族差距不可解讀為純數學能力差異 (Fraction Gap Interpretation)**：
   - Qwen 9B 在 Fraction 家族淨勝 4B 達 14 格 ($p = 0.012541$)。機制拆解顯示 21 格 9B-only PASS 主要源於 4B 的語法格式標點缺失 (SyntaxError, Pydantic JSON/LaTeX parsing error)，而非純分數運算數學推理能力差異。

4. **Polynomial 9B 偏低為局部格式共現 (Polynomial Anomaly Localized Co-occurrence)**：
   - Qwen 9B 在 Polynomial 家族表現低下 (9/80 vs 4B 的 16/80) 集中於 `ce115` 多項式除法單一題型與特定 LaTeX 組裝衝突。此屬特定欄位格式敏感性，未建立因果關係，不可外推為 9B 全域能力失控或數學能力下降。

5. **Qwen 4B `Ab2d+api` 77.8% 語法錯誤侷限於診斷樣本 (4B Ab2d Anomaly Sample Bound)**：
   - 4B 在 `Ab2d+api` 條件下通過數異常下降至 8/80，其 77.8% (21/27) SyntaxError 診斷結論僅適用於已剖析之 27 格失敗診斷樣本，不可外推為全域所有 72 格失敗之比例。

6. **Gemini 作為 Tier 2 描述性參照 (Gemini as Tier 2 Reference Only)**：
   - Gemini 3.5 Flash (289/320, 90.31%) 僅作 Tier 2 強模型描述性基準參照。因 API 部署條件、基礎架構與模型訓練資料均不相同，嚴禁宣稱「證明大模型規模因果壓倒性勝出」。

7. **Prompt 提示版本異質性 (Prompt Version Discrepancy)**：
   - Gemini 正式生成採用 `Ab2d+spec-v1` (63/80)；Qwen 4B 與 9B 採用 `Ab2d+spec-v2` (36/80 與 40/80)。兩者不得假裝為完全相同版本之提示條件。

8. **`Regression = 0` 僅屬實證觀察 (Observed Zero Regression Only)**：
   - `Observed Regression = 0` 僅代表在本次 320 個匹配測試單元與凍結修復規則下「觀察到零倒退」，不可宣稱「Deterministic AST Healer 保證在任意未受限情境下 100% 絕不倒退」。

9. **`Eligible = 0` 不代表模型無失敗 (Eligibility Zero Scope)**：
   - Gemini (31 FAIL) 與 Qwen 9B (219 FAIL) 之 `Eligible = 0` 僅代表殘餘失敗未命中事前凍結之修復規則，系統依 Protocol 主動選擇 Abstain，不代表模型生成無任何錯誤。

10. **全域邊界與範疇受限 (Global Protocol Bound)**：
    - 本研究所有數字、結論與邊界，僅嚴格適用於本次測試之 16 道數學題型、3 個模型、4 種 Prompt 條件、5 個隨機種子、量化設定與凍結 Healer 規則。
