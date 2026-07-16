from scripts.run_ce115_ab2d_v4_minimal_smoke import production_path_run
import json

def plans(): return [{"cell_id":f"c{i}","task":"ce115_calc_polynomial_division_l1","prompt":"p","frozen":{}} for i in range(3)]
def good(p,n): return {"message":{"content":"def generate(level=1, **kwargs):\n return {\"question_text\":\"q\",\"correct_answer\":0,\"oracle_payload\":{}}\n"}}
def test_production_path_three_calls(tmp_path):
 rows=production_path_run(tmp_path/"run",plans(),good); assert len(rows)==3; assert json.loads((tmp_path/"run"/"smoke_summary.json").read_text())["calls"]==3
def test_system_exit_is_cell_artifact_and_finalizes(tmp_path):
 def boom(p,n):
  if n==2: raise SystemExit("stop")
  return good(p,n)
 rows=production_path_run(tmp_path/"run",plans(),boom); assert len(rows)==3 and rows[1]["completion"]=="SYSTEM_FAILURE"
def test_transport_failure_does_not_retry(tmp_path):
 def fail(p,n): raise RuntimeError("transport")
 rows=production_path_run(tmp_path/"run",plans(),fail); assert len(rows)==3 and all(x["provenance"]["retry"]==0 for x in rows)
