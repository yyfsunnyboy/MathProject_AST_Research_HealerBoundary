# 📊 CE115 Corrected Output Size and Token-Budget Census Report
    
This report presents the census of output sizes for the corrected confirmatory cohort run (`num_ctx = 65536`, `num_predict = 24576`).

---

## 1. Natural Completion Token Statistics (Level A Telemetry)

| Cohort | Count (N) | Median (Out) | P90 (Out) | P95 (Out) | P99 (Out) | Max (Out) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Overall** | 50 | 487.5 | 1481.2 | 2345.0 | 2609.2 | 2646.0 |
| **Ab1** | 17 | 458.0 | 1415.2 | 1746.8 | 2216.6 | 2334.0 |
| **Ab2g** | 14 | 413.5 | 2088.2 | 2429.9 | 2542.8 | 2571.0 |
| **Ab2d** | 19 | 541.0 | 1441.6 | 1571.4 | 2431.1 | 2646.0 |

---

## 2. Degeneration Analysis

- In this run, **22 cells** hit the prediction limit of 24576 tokens because of infinite repetition loops, and are classified as `MODEL_DEGENERATIVE_NONTERMINATION`.
- These degenerative runs generated exactly 24576 output tokens, which have been excluded from the natural completion statistics above.

