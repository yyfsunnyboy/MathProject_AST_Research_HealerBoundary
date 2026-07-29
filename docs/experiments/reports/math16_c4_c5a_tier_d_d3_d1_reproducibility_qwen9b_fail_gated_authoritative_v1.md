# Math16 C4→C5a Tier D D3→D1 Reproducibility — qwen9b_fail_gated_authoritative_v1

> **AUTHORITY:** `AUTHORITATIVE_FAIL_GATED_CUMULATIVE_V1`
> **HEAD:** `72117d3facd48b8e78af534290dc7dcd2001149a`
> **Order:** D3→D1 (fixed)

## Core counts

- gated FAIL／preserved PASS: **218／102**
- C4 PASS／C5a PASS: **102／102**
- verified_rescue／regression: **0／0**
- parse_gain／execution_gain／blocker_removal／modified_still_failed: **0／3／3／12**
- PASS→PASS modification: **0**
- D1 shadow classes: `{'ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API': 11, 'DEAD_SHADOW_REMOVAL': 1}`
- Second replay zero-diff: **True**

## Active shadow formal phrase

> 以 frozen scaffold 注入的正式 Ops implementation，取代模型自訂的 active shadow implementation。

## Declarations

- D5／D2 executed: **No**
- Model calls: **0**
- Commit／push: **No**
