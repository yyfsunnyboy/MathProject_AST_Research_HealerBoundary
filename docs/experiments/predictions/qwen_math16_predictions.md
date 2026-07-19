# Qwen Math16 Three-Condition Pre-Run Predictions

**Status:** PRE-RUN (recorded before any formal Math16 Qwen cell)  
**Benchmark reference:** Gemini 3.5 Flash Math16 confirmatory (`evaluation_revision_003`): **40/48** total; Ab1/Ab2g/Ab2d = **13/14/13**.  
**Models:** `qwen3.5:4b` then `qwen3.5:9b` (sequential, independent run dirs).  
**Adapter sampling (frozen):** `ollama show` Parameters — temperature=1.0, top_p=0.95, top_k=20, presence_penalty=1.5; seed=2026071301; num_predict=24576; num_ctx=65536.

## H1 — 4B total pass rate significantly below Gemini 40/48

`qwen3.5:4b` overall pass rate will be **materially lower** than Gemini’s confirmatory **40/48**.  
Expect a clear gap (not a near-tie): 4B is smaller, local-quantized, and historically weaker on schema/API assembly cells even when sampling is non-greedy.

## H2 — Among failures, L2/L3 share higher than Gemini

Conditional on failures, `qwen3.5:4b` will show a **higher share of L2/L3** (schema / contract–adjacent / incomplete assembly) than the Gemini Math16 failure mix, which is more answer-semantic (L5-like) after confirmatory adjudication.  
Infrastructure L0 should remain rare if Ollama stays healthy; do not treat L0 as the main story unless the host fails.

## H3 — 9B between 4B and Gemini; same failure direction, smaller magnitude

`qwen3.5:9b` pass rate will sit **between 4B and Gemini 40/48**. Failure modes will **point the same way as 4B** (elevated L2/L3 relative to Gemini) but with **smaller absolute counts / milder rates**.

## Non-predictions (explicitly out of scope)

- No claim that Ab2d will beat Ab1/Ab2g for either Qwen size.
- No healer execution; eligibility may be marked only.
- Predictions are directional; exact cell IDs are not pre-specified.
