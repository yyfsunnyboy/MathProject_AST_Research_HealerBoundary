# Math16 Aggressive Healer — Current Handoff v1

> **狀態：** 4B cumulative Healer／Tier D Development 探索已封存  
> **標記：** `TIER_D_4B_EXPLORATION_CLOSED`  
> **性質：** Tier D 為 **Development evidence**，**不是** Confirmatory  
> **凍結起點 HEAD（封存前）：** `f0eae63fe8c3760e9912589654657510119175ce`  
> **權威協議：** `docs/experiments/design/math16_cumulative_healer_layering_protocol_v1.md`  
> **Rule→Tier mapping：** `docs/experiments/manifests/math16_healer_rule_id_tier_mapping_v1.json`

---

## 1. 研究主軸（已完成事實）

不同 Prompt 條件產生不同失敗供給；再以**累積層級**（C0→C1→C2→C3/C4→C5a／Tier D slices）探索 Healer 作用邊界。  
規則以 frozen contract／census 為準；**不得**依新模型結果回頭改規則。

---

## 2. 4B 累積結果（唯一 headline）

| 層級 | PASS | Δ verified rescue | 備註 |
|---|---:|---:|---|
| C0 Raw | **79**/320 | — | Baseline |
| C1 Conservative（Tier A 六規則） | **85**/320 | **+6** | Pilot-02 frozen allowlist |
| C2 Tier B（safe structural） | **86**/320（frozen）／**85**/320（corrected） | **+1** frozen／**+0** corrected | Development replay；+1＝幽靈帳（sealed bytes 未晉升） |
| Tier C（C1 spec-only + C2 narrow） | **86**/320（frozen）／**85**/320（corrected） | **+0** | 無 PASS 增益 |
| Tier D D3+D1（C5a） | **88**/320（frozen）／**87**/320（corrected） | **+2** | Development evidence；D1 active-shadow ×2 |
| Tier D D5 | 88／87 | **0** | `NO_DEVELOPMENT_GAIN` |
| Tier D D2 | 88／87 | **0** | `BLOCKER_REMOVAL_ONLY`；execution gain **1** |

- **最終 4B（analysis overlay）：** **87/320**（frozen archive **88/320** 永久保留）
- **總 verified rescue（overlay）：** **+8**（6+0+0+2）；frozen 帳面曾記 +9（含 C2 幽靈 +1）
- **Regression：** **無**
- **`TIER_D_4B_EXPLORATION_CLOSED`：** 是（停止新增 D4／D6／其他 Tier D 規則探索）
- **Correction Note（2026-07-30）：** `docs/決賽文件/實驗結果文件/Math16/10_math16_aggressive_round1_source_label_promotion_mismatch_correction_note_v1.md`

### D1 正式措辭（兩格 rescue）

兩格皆 `ce112_q04_radical_simplification`（seeds 2026071301／2002），機制分類：

**`ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API`**

> 以 frozen scaffold 注入的正式 Ops implementation，取代模型自訂的 active shadow implementation。

**不得**寫成 dead-code removal。

### D5 ranking 4→1

- Verdict：`SPEC_DRIVEN_ELIGIBILITY_CHANGE`
- 舊 C4 D5=4 = **pre-freeze exploratory**
- C5a D5=1 = **frozen-spec authoritative**
- 無 census implementation inconsistency

---

## 3. 回家後下一步（依序）

1. **Freeze** 完整 cumulative pipeline（C0→…→已實作 Tier D slices）
2. **原封不動**套用 **9B**
3. **原封不動**套用 **Gemini**
4. **不依**新模型結果改規則
5. 最後整合 Final Report／Jury Q&A

本階段**不要**再開 Tier D 新規則、不要重跑 4B 正式 Confirmatory。

---

## 4. 接續路徑索引

### Design／Protocol

| 路徑 | 用途 |
|---|---|
| `docs/experiments/design/math16_cumulative_healer_layering_protocol_v1.md` | 累積層級權威協議 |
| `docs/experiments/design/math16_tier_d_risk_accepting_repair_spec_v1.md` | Tier D 凍結規格 |
| `docs/experiments/design/math16_aggressive_healer_tier_a_v1_spec.md` | 結構規則套件規格（歷史目錄名） |
| `docs/experiments/design/math16_aggressive_healer_domain_api_binding_spec_v1.md` | Domain API binding |
| `docs/experiments/design/math16_domain_api_inventory_v1.md` | Domain API inventory |

### Mapping／Closure／Census／Compliance

| 路徑 | 用途 |
|---|---|
| `docs/experiments/manifests/math16_healer_rule_id_tier_mapping_v1.json` | Legacy rule_id → current_tier |
| `docs/experiments/manifests/math16_c4_final_source_closure_v1.json` | C4 final-source closure |
| `docs/experiments/manifests/math16_c5a_final_source_closure_v1.json` | C5a final-source（PASS 88） |
| `docs/experiments/manifests/math16_c4_c5_tier_d_supply_v1.json` | 舊 C4 Tier D supply（exploratory） |
| `docs/experiments/manifests/math16_c5a_tier_d_d5_d2_residual_supply_v1.json` | C5a D5/D2 residual（authoritative） |
| `docs/experiments/manifests/math16_ab2d_*`／`math16_domain_api_contract_registry_v1.json` | Compliance／contract |
| `docs/experiments/reports/math16_c5a_tier_d_d5_ranking_provenance_closure_v1.md` | D5 4→1 provenance |

### Implementations

| 路徑 | 用途 |
|---|---|
| `agent_tools/finals_rebuild/aggressive_healer_tier_a/` | 結構規則套件（mapping：多數為 Tier B legacy IDs） |
| `agent_tools/finals_rebuild/aggressive_healer_tier_c2/` | Tier C2 narrow default-optional cleanup |
| `agent_tools/finals_rebuild/aggressive_healer_tier_d/` | D3／D1／D5／D2 + ranking |

### Focused tests

- `tests/finals_rebuild/test_math16_aggressive_healer_tier_a_v1.py`
- `tests/finals_rebuild/test_math16_tier_c2_default_optional_cleanup_v1.py`
- `tests/finals_rebuild/test_math16_tier_d_d3_d1_v1.py`
- `tests/finals_rebuild/test_math16_tier_d_d5_ranked_binding_v1.py`
- `tests/finals_rebuild/test_math16_tier_d_d2_duplicate_selection_v1.py`

### Development replay／reports／results

| 層 | Manifest／Report／Results |
|---|---|
| C0→C1 | `…/math16_c0_c1_tier_a_reproducibility_v1*` |
| C1→C2 Tier B | `…/math16_c1_c2_tier_b_*` |
| Tier C residual／C2 replay | `…/math16_c2_c3_*`、`…/math16_c2_c4_*` |
| Tier D D3+D1 | `…/math16_c4_c5_tier_d_d3_d1_*`（含 supplemental closure） |
| Tier D D5／D2 | `…/math16_c5a_tier_d_d5_*`、`…/math16_c5a_tier_d_d2_*` |

Results 根目錄：`docs/experiments/results/math16_*`

---

## 5. 命名注意

- `rule_id` 字串中的 `TIER_A_`／`TIER_B_` **不**等於現行研究分層；以 mapping JSON 為準。
- 目錄名 `aggressive_healer_tier_a` 為歷史套件名；**不是**「再開 Aggressive Healer v2」。
- Tier D 全程標 **Development**；未進 Confirmatory。

---

## 6. 聲明

本 handoff 只整理已完成事實；不新增規則、不改既有統計、不重跑模型／正式 replay／evaluator。
