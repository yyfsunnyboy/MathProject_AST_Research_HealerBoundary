from pathlib import Path
from agent_tools.finals_rebuild.ce115_ab2d_assembly import scan_toolbox
from scripts.run_ce115_ab2d_v4_minimal_smoke import persist_run_rows

def test_cross_domain_helper_is_not_a_compliance_failure():
 s="def generate():\n q,r=PolynomialOps.div_qr([1,0],[1])\n f=FractionOps.create(q[0])\n return {\"correct_answer\":(q,r,f)}\n"
 x=scan_toolbox(s,"ce115_calc_polynomial_division_l1")
 assert x["classification"]=="ASSEMBLY_COMPLIANT"

def test_irrelevant_call_is_diagnostic_only():
 s="def generate():\n q,r=PolynomialOps.div_qr([1,0],[1])\n x=FractionOps.create(1)\n return {\"correct_answer\":(q,r)}\n"
 x=scan_toolbox(s,"ce115_calc_polynomial_division_l1")
 assert x["classification"]=="ASSEMBLY_COMPLIANT" and "FractionOps.create" in x["irrelevant_api_calls"]

def test_runner_persists_after_failure(tmp_path):
 def f(cell,n):
  if n==1: raise RuntimeError("boom")
  return {"cell_id":f"c{n}","completion":"NATURAL_COMPLETE"}
 rows=persist_run_rows(tmp_path/"new",["a","b","c"],f)
 assert len(rows)==3 and (tmp_path/"new"/"smoke_summary.json").is_file()
