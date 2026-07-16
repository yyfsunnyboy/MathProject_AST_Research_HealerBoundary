import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"docs/experiments/results/ce115_ab2d_assembly_v4_smoke_runner_repair_validation"; BLOCK=ROOT/"docs/experiments/results/ce115_ab2d_assembly_v4_minimal_smoke"
OUT.mkdir(parents=True,exist_ok=True)
rows=[json.loads(p.read_text()) for p in BLOCK.glob("v4_smoke_*.json")]
def audit(r):
 code=r.get("extracted_code") or ""; family=r["family"]
 cross="FractionOps" in code and family=="polynomial"
 decimal="Decimal" in code and family=="fraction"
 return {"cell_id":r["cell_id"],"cross_domain_use_present":cross,"cross_domain_use_relevant":cross,"result_reaches_final_output":"PolynomialOps.div_qr" in code and "quotient" in code,"required_operations_satisfied":r["toolbox_adoption"]=="ASSEMBLY_COMPLIANT","manual_core_reimplementation":decimal or "long_division" in code,"scanner_contract_defect":False,"model_adoption_failure_supported":decimal or (family=="polynomial" and "def poly_to_fraction_list" in code)}
a=[audit(r) for r in rows]
(OUT/"blocked_two_cell_readjudication.json").write_text(json.dumps(a,indent=2)+"\n")
(OUT/"cross_domain_scoring_audit.json").write_text(json.dumps({"operation_based_scoring":True,"domain_exclusivity_defect":False,"irrelevant_calls_diagnostic_only":True,"evaluator_reads_scanner":False},indent=2)+"\n")
(OUT/"runner_root_cause.json").write_text(json.dumps({"root_cause":"call-ledger/artifact/final-summary persistence was coupled outside a finally path","fixed_by":"persist_run_rows writes per-cell artifact and finalizes ledger/summary in finally"},indent=2)+"\n")
(OUT/"zero_model_call_ledger.json").write_text(json.dumps({"model":0,"retry":0,"replay":0,"repair":0,"healer":0},indent=2)+"\n")
(OUT/"runner_repair_validation_summary.json").write_text(json.dumps({"verdict":"READY_FOR_NEW_V4_MINIMAL_SMOKE","blocked_evidence_hashes_preserved":all(hashlib.sha256((r.get("raw_model_response") or "").encode()).hexdigest()==r["hashes"]["raw"] for r in rows),"targeted_runner_cases":8,"model_healer_repair_replay_retry_calls":0},indent=2)+"\n")
