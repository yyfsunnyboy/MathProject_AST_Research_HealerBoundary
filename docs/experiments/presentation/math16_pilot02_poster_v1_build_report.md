# Math16 Pilot-02 Poster v1 建置報告 (Spec Build Report)

```text
MATH16_PILOT02_POSTER_V1_SPEC_COMPLETED
THREE_COLUMN_CONTENT_ARCHITECTURE_FROZEN
VISUAL_HIERARCHY_AND_FIGURE_PLACEMENT_DEFINED
PRIMARY_POSTHOC_ACCOUNTING_PRESERVED
POSTER_READY_FOR_RENDERING
```

## 一、 版控與基線 (Version Control & Baseline)
- **Starting / Ending HEAD**: `d17a086d55e27e9b2d60783004dfd4511fdabc1b`
- **Final Report v1.1 SHA-256**: `a9df82efc2424b3c4f15b9f6daa725d2f40371d2c3be659a70fc5f494166cfe7`
- **Output Spec File**: `docs/experiments/presentation/math16_pilot02_poster_v1_spec.md`
- **Poster Spec SHA-256**: `fc73a7c2f509e26e44e4909d324d4de286ce71e07b11dec83e36467d089293ee`

## 二、 三欄內容藍圖與視覺階層 (Three-Column Content Architecture)
1. **Header**: 主標題、研究問題短句、960 cells 規模標籤、三大數字卡（Gemini 289/320, 4B 83/320, 9B 101/320）。
2. **Left Column (研究設計)**：極簡短句與流程圖（動機、Healer定位、16題/4家族、3模型、4Prompts、干預流程、Primary/Post-hoc分帳）。
3. **Middle Column (主要證據 - 最大主視覺焦點)**：
   - **Figure 4 Tier 1 配對分析 (Hero Figure - 最大圖)**
   - **Figure 1 Baseline 總覽**
   - **Figure 5 Eligibility / Rescue 邊界**
4. **Right Column (解讀與邊界)**：
   - **Figure 3 Family 差異**
   - **Figure 2 Prompt 條件 (含 spec-v1/v2 警語)**
   - **Figure 6 安全介入概念圖**
   - **五項主要發現**
   - **三項精選展板限制**
   - **一句總結**

## 三、 Renderer 實測 BBox 方法學凍結 (Methodology Freeze)
- 未來展板實體渲染階段，**強制使用** Matplotlib Renderer `get_window_extent()` / `get_position()` 實測 BBox 及具名 Pairwise 零碰撞檢測（繼承 v2.3 標準），嚴禁使用硬編碼百分比。

## 四、 產物約束檢查 (Output Constraint Check)
- 本輪僅輸出藍圖規格 (`.md`) 與內容映射檔 (`.json`)，未生成任何 PNG、PDF、PPT 或 Slides。
