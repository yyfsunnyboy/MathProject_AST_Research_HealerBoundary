# Math16 Combined Amendment — Batch 4 (One-Pager only) Report v1

Report date: 2026-07-29  
Batch: **4（縮減版）— One-Pager presentation generator + regen**  
Result: **PASS**

## 0. Scope

| In scope | Out of scope（本輪零修改／零生成） |
|---|---|
| `scripts/build_math16_pilot02_one_pager_v23.py` | Poster generator／PNG／PDF |
| One-Pager PNG／PDF／manifest／build report／compacts | `poster_and_oral_figure_order` |
| Read-only：`presentation_claims_v1.json`、canonical Fig1–5 PNG | PPT／簡報／口頭報告資產 |
| | Final Report／Integrated／Method1–2／handoff／Jury Q&A |
| | Canonical Fig1–6 內容、frozen builder／claims／results／tests |
| | 決賽 package copy-forward、Correction Note links |

## 1. Generator changes

File: `scripts/build_math16_pilot02_one_pager_v23.py`

- 只讀 `presentation_claims_v1.json`（不讀寫 `frozen_numeric_claims.json`／`results/**`）
- 模型序固定 **Gemini → 9B → 4B**；顏色身份固定（Gemini `#4285F4`、9B `#D97706`、4B `#0F9D58`）
- Headline：**Baseline 79／Final 85／Verified rescue=6**；Primary 84 僅 demotion 註記
- 右欄改為 **Fig1 → Fig2 → Fig5 → Fig3**（左欄 Fig4）
- Fig2：byte-copy canonical `figure_02_prompt_conditions.png`（**不** re-rasterize）；caption 標示 `80/80*`
- 星號註記（底部）：  
  `* Gemini 3.5 Flash 的 Ab2d+spec 採 Post-hoc spec-v2，結果為 80/80；原 Primary spec-v1 為 63/80。`
- Protected SHA 加入 Fig2 canonical PNG

## 2. Outputs

| File | SHA-256 | Size / pages |
|---|---|---|
| `docs/experiments/presentation/math16_pilot02_one_pager_v23/math16_pilot02_one_pager_v23.png` | `7eee10d8b53f911cafa1a68e5333840568ff6e89afd9ca91c2591566bdc941c4` | **3619×2541** |
| `docs/experiments/presentation/math16_pilot02_one_pager_v23/math16_pilot02_one_pager_v23.pdf` | `ed4194b31676837b5211ef0d754b8b88db26cdd083716d666c6d7e200fbfa1bc` | **1 page**；≈868.71×609.84 pt（A4 landscape） |
| `one_pager_v23_manifest.json` | regenerated | presentation-layer |
| `one_pager_v23_build_report.md` | regenerated | presentation-layer |
| `one_pager_v23_element_bboxes.json` | regenerated | 18 elements；153/153 pairs no collision |

### Compact assets

| Asset | Role | SHA-256 |
|---|---|---|
| `assets/fig1_compact_v23.png` | matplotlib compact from claims | (build-time) |
| `assets/fig2_compact_v23.png` | **byte-copy** of canonical Fig2 | `8b72c42e4e8590a0fd67388a3b1c30317d174521fc9469beff1d6fae25ddae5f` |
| `assets/fig3_compact_table_v23.png` | matplotlib compact from claims | (build-time) |
| `assets/fig4_compact_v23.png` | matplotlib compact from claims | (build-time) |
| `assets/fig5_compact_v23.png` | matplotlib compact from claims | (build-time) |

## 3. Canonical Figure SHA used（read-only；本輪零變動）

| Figure | File | SHA-256 |
|---|---|---|
| Fig1 PNG | `figure_01_baseline_overall.png` | `c5e091eedd82c4a39c78b596b970cd538d6503022546315b7832f3df4ba8d684` |
| Fig2 PNG | `figure_02_prompt_conditions.png` | `8b72c42e4e8590a0fd67388a3b1c30317d174521fc9469beff1d6fae25ddae5f` |
| Fig3 PNG | `figure_03_family_breakdown.png` | `2d225e069a62529d3657aec629a0b90df10ba63df9f68c927e81ab35e5b729c2` |
| Fig4 PNG | `figure_04_tier1_paired_analysis.png` | `0daa7d332941709708f021b6f20bbb2d180f41a7ab7a36cc4f4c1572a7ac6da9` |
| Fig5 PNG | `figure_05_healer_eligibility_boundary.png` | `05b81728393037f0657a42af34de883bbc860e44eccdfbfbf40553e86e6f1849` |
| Fig6 PNG | `figure_06_healer_concept_zones.png` | `3b358862434ea81b74841def4ca81a6168b8e1ff36ab2b44f3868d4db891c71c`（未嵌入 One-Pager；未修改） |

Pre/post SHA snapshot：`core_zero = True`。

## 4. Model-order & core-number audit

| Check | Result |
|---|---|
| Cards left→right | Gemini 289 → 9B 101 → 4B Final 85（rescue=6） |
| Header / captions | Gemini→9B→4B／G→9B→4B |
| Fig1 bars | Gemini／9B／4B（79/320 baseline） |
| Fig2 | Gemini Ab2d+spec = **80/80***；星號註記含 Post-hoc spec-v2 與 Primary 63/80 |
| Baseline→Final | **79 → 85**；Verified rescue=**6** |
| Fig4 matrix | 52／27／49／192；p=0.015440 |
| Primary 84 | 僅「不作主表」註記；不在成果主表 |

## 5. Visual check

Opened：One-Pager PNG + PDF（1 page）。

| Item | Result |
|---|---|
| 模型序處處 G→9B→4B | PASS |
| 數值與模型身份／顏色一致 | PASS |
| 無欄名移動但數值未移動 | PASS |
| 無重疊／截斷／跑版（bbox 153/153） | PASS |
| 星號註記清楚 | PASS |
| Fig2 80/80* 呈現 | PASS |
| 79→85、rescue=6 一致 | PASS |

## 6. Residual audit（generator + manifest + build report + PDF text）

| Pattern | Current-facing blocked hits |
|---|---|
| `78/320` | **0** |
| `84/320` | **0** |
| `242`（作為 BOTH FAIL／舊總數） | **0** |
| `Gemini→4B→9B` | **0** |
| 三模型排列 4B 在 9B 前 | **0** |
| Primary 84 主表 | **0**（僅允許 demotion 註記；5 處 allowed） |

**Blocked residual count = 0。**

## 7. Poster／PPT 零變動確認

本輪執行前後對下列路徑做 SHA 快照比對：`poster_zero = True`。

- `scripts/build_math16_pilot02_poster_v11.py`
- `docs/experiments/presentation/math16_pilot02_poster_v11/math16_pilot02_poster_v11.{png,pdf}`
- `poster_v11_manifest.json`／`poster_v11_build_report.md`

PPT／簡報／口頭報告資產：本輪未開啟、未修改、未生成。  
（工作區若仍見 Poster 相對 git HEAD 的既有 `M`，屬先前對話殘留，非本輪產出。）

## 8. Forbidden paths

| Path class | 本輪變動 |
|---|---|
| Canonical Fig1–6 SVG／PNG | **0** |
| frozen claims／results／tests／journals | **0** |
| Final Report／Integrated／Method／Jury／handoff | **0** |
| 決賽 package | **0** |

## 9. Verdict

**Batch 4（One-Pager only）：PASS**  
可進入後續 Batch 5（copy-forward）時再處理決賽 package；本輪未執行 Batch 5–7。
