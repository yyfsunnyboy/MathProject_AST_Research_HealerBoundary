# Math16 Pilot-02 One-Pager v2.2 Layout & Collision Fix 報告

```text
MATH16_PILOT02_ONE_PAGER_V22_MEASURED_LAYOUT_COMPLETED
HEADER_BACKGROUND_NON_WHITE_VERIFIED
COLLISION_DETECTION_TEST_PASSED
ALL_PROTECTED_SHAS_PRESERVED
ONE_PAGER_V22_READY_FOR_FINAL_REVIEW
```

## 一、 版面對齊與碰撞修正 (v2.2)

1. **Header 背景色修復**：深色背景塊透過背景 ax 顯式繪製 (zorder=1)，並由 `run_collision_and_render_verification` 採集真實 PNG 像素驗證 RGB(15,23,42) 均非純白。
2. **Caption 錨定對齊**：Fig1, Fig3, Fig4, Fig5 的 Caption 直接掛載在該圖表 ax 的 top 邊界上方，消除寫死高度與實際圖表的高度偏差。
3. **碰撞檢測自動測試**：新增 `test_v22_no_element_collisions`，測量每個元素的 bounding box，任兩元素重疊即拋錯。

## 二、 輸出 SHA

| 檔案 | SHA-256 |
|---|---|
| `math16_pilot02_one_pager_v22.png` | `1da5a383d8b606fc6a9677d61ed4df58751a007f9320fd6e4bcfb07e27df802b` |
| `math16_pilot02_one_pager_v22.pdf` | `64398864cc5929d34a5c825e6ac07db6693acb571d9919e6634801a1c9305da3` |
