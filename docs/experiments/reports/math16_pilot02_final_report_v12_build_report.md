# Math16 Pilot-02 Final Report v1.2 全文一致性建置報告

## 1. Primary／Post-hoc 四處核對
- 摘要、第10節、第11節、第19節 Q5 均明確記錄：Baseline `78/320`；Primary rescue `5`、final `83/320`；Post-hoc **total rescue `6`**、final `84/320`；相較 Primary 僅增加 `1` 個 PASS。
- 未出現 `83+6`、Post-hoc 冒充 Primary、或將 total rescue=6 誤寫為額外增加 6 格。

## 2. Fraction 三處核對
- 第13節、第14節、第19節 Q8 均記錄：`NINE_B_ONLY=21`、`L1–L4=15`、`L5=6`。
- 三處均說明 L1–L4 涵蓋語法、契約、API 與執行問題，且不可解讀為純數學能力差異。

## 3. Corrected-chain 核對
- Eligible replay=`10`、unchanged=`8`、disposition changed=`2`、PASS/FAIL changed=`1`。
- 所有 `84/320` 提及均維持 Post-hoc total rescue=6、僅較 Primary 增加 1 個 PASS 的分帳。

## 4. 第18節 10 項限制
- 項目數：`10`。
- 逐項標題、適用範圍、探索性定位與 observed regression=0 邊界均與 v1.1／Evidence Complete 對照保留；未改成確認性主張或保證。

## 5. 禁語與重複數字全文搜尋
| 搜尋詞 | v1.2 行號 |
|---|---|
| `83/320` | 18, 126, 138, 142, 239, 279, 280, 297 |
| `84/320` | 18, 127, 138, 142, 279, 280, 297 |
| `rescue_5` | 18, 125, 239, 280, 297 |
| `rescue_6_total` | 18, 127, 138, 280, 297 |
| `standalone_21` | 20, 180, 182, 189, 194, 252, 254, 289 |
| `standalone_15` | 20, 182, 194, 198, 208, 252, 289 |
| `standalone_6` | 18, 20, 67, 127, 138, 178, 182, 194, 225, 252, 255, 273, 280, 282, 289, 297 |
| `eligible_zero` | 18, 258, 270, 271 |
| `本研究證明` | 0 occurrences |
| `額外救回6格` | 0 occurrences |
| `語法與格式標點缺失` | 0 occurrences |
| `保證不倒退` | 0 occurrences |

禁語 `本研究證明`、`額外救回6格`、`語法與格式標點缺失`、`保證不倒退` 均為 0。

## 6. 實際修改位置
1. **title and report marker**：version label v1.1 -> v1.2；marker 更新為 `V12_FULL_TEXT_VERIFIED`
2. **Section 1 abstract**：Post-hoc rescue explicitly labeled total rescue=6
3. **Section 10**：added Baseline PASS=78/320; normalized Primary=5/final=83/320 and Post-hoc total=6/final=84/320/+1
4. **Section 11**：Post-hoc table column and Qwen row explicitly labeled total rescue=6
5. **Section 13**：added Fraction 21/15/6 interpretation sentence
6. **Section 19 Q5**：made 78/5/83/6/84/+1 and 10/8/2/1 accounting explicit
7. **Section 20 conclusion**：made Baseline/Primary/Post-hoc total accounting explicit

## 7. SHA 保護與來源未修改
- v1 SHA-256：`1a168805bfd8f2c076d2e8fd0556e90b049648e771d3481cc35abaeac250e730`
- v1.1 SHA-256：`a9df82efc2424b3c4f15b9f6daa725d2f40371d2c3be659a70fc5f494166cfe7`
- Evidence Complete manifest SHA-256：`de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225`
- Integrated report SHA-256：`a13f0e0b71a1d1f0f0bc0ab0fdcecfc330c18238d0bd434218447939568992ca`
- Q&A SHA-256：`b2b0d2a750e5edf0a8b88cf31c2b238fa502d92787f220a9ca2d270e9e116741`
- v1.2 SHA-256：`1e10eb3319272421f4866712a01c40eea12c4140d7264124c0fba4fb54c787b4`
- v1、v1.1、Evidence Complete、Integrated report、Q&A、六張核心圖均未修改。
