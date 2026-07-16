"""Frozen-plan one-cell process orchestration; fake mode only for certification."""
from __future__ import annotations
import hashlib,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TASKS=[("polynomial","ce115_calc_polynomial_division_l1"),("fraction","ce115_calc_exact_rational_expression_l1"),("radical","ce115_calc_radical_simplification_l1")]
def plan():
 cells=[{"cell_id":f"process_{f}_2026071301","family":f,"task":t,"seed":2026071301,"max_model_calls":1,"retry":0,"replay":0,"repair":0,"healer":0} for f,t in TASKS];d={"run_id":"ce115_v4_process_isolated","cells":cells};d["hash"]=hashlib.sha256(json.dumps(d,sort_keys=True).encode()).hexdigest();return d
def run_cell(root,cell,mode="fake",interrupt=None):
 root=Path(root); intent=root/f"{cell['cell_id']}.intent.json"; artifact=root/f"{cell['cell_id']}.artifact.json"
 if intent.exists() or artifact.exists(): raise RuntimeError("duplicate cell invocation refused")
 intent.write_text(json.dumps({"cell":cell,"phase":"CALL_INTENT","timestamp":time.time()})+"\n")
 if interrupt=="after_intent": return {"status":"SYSTEM_INTERRUPTED_AFTER_CALL_INTENT"}
 raw=root/f"{cell['cell_id']}.raw.txt";raw.write_text("def generate(level=1, **kwargs):\n return {\"question_text\":\"q\",\"correct_answer\":0,\"oracle_payload\":{}}\n")
 if interrupt=="after_raw": return {"status":"RAW_SAVED_OFFLINE_ADJUDICATION_ONLY"}
 artifact.write_text(json.dumps({"cell":cell,"status":"FINALIZED","fake_transport_calls":1,"retry":0})+"\n");return {"status":"FINALIZED"}
def finalize(root):
 root=Path(root);p=json.loads((root/"frozen_run_plan.json").read_text());states=[]
 for c in p["cells"]:
  i=root/f"{c['cell_id']}.intent.json";a=root/f"{c['cell_id']}.artifact.json";r=root/f"{c['cell_id']}.raw.txt";states.append({"cell_id":c['cell_id'],"intent":i.exists(),"raw":r.exists(),"artifact":a.exists(),"status":"FINALIZED" if a.exists() else "SYSTEM_INTERRUPTED_AFTER_CALL_INTENT" if i.exists() else "MISSING"})
 return {"planned":3,"states":states,"verdict":"COMPLETE" if all(x['artifact'] for x in states) else "BLOCKED"}
