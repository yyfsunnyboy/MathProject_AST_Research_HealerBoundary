# Math16 Pilot-02 One-Pager v2.1 Visual Hotfix 報告

```text
MATH16_PILOT02_ONE_PAGER_V21_VISUAL_HOTFIX_COMPLETED
TITLE_AND_WHITESPACE_FIXED
RIGHT_COLUMN_READABILITY_IMPROVED
BOTTOM_TEXT_READABILITY_IMPROVED
ORIGINAL_AND_PRIOR_VERSION_SHAS_PRESERVED
ONE_PAGER_V21_READY_FOR_FINAL_REVIEW
```

## v2 缺陷 → v2.1 修正

| v2 缺陷 | v2.1 修正 |
|---|---|
| 主標題對比低（淡藍字）| 深色帶(#0F172A) + 白字加粗 19pt |
| 頂部空白過多 | Header 縮至 19%，卡片上移 |
| 右側 Fig 太扁 | Fig1/5 各佔 36% 帶高，Fig3 佔 28% |
| Fig3 squashed bar chart | 改為 horizontal mini-bar table（4行）|
| 底部結論字淡 | 深灰 #111827 + 9.5pt bold |
| 統計行貼頁邊 | 上移，安全底部邊界 |

## v2.1 版面

| 區域 | 高度 | 內容 |
|---|---|---|
| Header | 19% | 深色帶 + 白字主標題 + 問題/設計 + 3 數字卡 |
| Fig4 (左 54.5%) | 61.5% | 2×2 矩陣大字 + 統計面板 |
| Fig1 (右上 36%) | 22% | Baseline 三柱 |
| Fig5 (右中 36%) | 22% | 安全修復窗口 |
| Fig3-table (右下 28%) | 17.5% | 水平 mini-bar 四行表 |
| Bottom | 19.5% | 3點結論 + 統計框 |

## SHA 驗證

| 項目 | 狀態 |
|---|---|
| 原始 Figure 1/3/4/5 PNG | ✅ 不變 |
| v1 PNG/PDF | ✅ 不變 |
| v2 PNG/PDF | ✅ 不變 |

## 輸出 SHA

| 檔案 | SHA-256 |
|---|---|
| one_pager_v21.png | `6ba225fad3ad33c61adf849520e2d6991b8168e94dc6196283a4f34e416b13e4` |
| one_pager_v21.pdf | `52a9fe4176f3550cc5e5eda9525ad7834a013e54f090dd2a869e7eef25eaf22f` |
