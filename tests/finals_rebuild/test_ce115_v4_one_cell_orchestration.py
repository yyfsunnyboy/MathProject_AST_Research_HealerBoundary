import json
from scripts.ce115_v4_one_cell_orchestrator import plan,run_cell,finalize
def test_three_cells_and_duplicate_refusal(tmp_path):
 p=plan();(tmp_path/"frozen_run_plan.json").write_text(json.dumps(p))
 for c in p["cells"]: assert run_cell(tmp_path,c)["status"]=="FINALIZED"
 assert finalize(tmp_path)["verdict"]=="COMPLETE"
 try: run_cell(tmp_path,p["cells"][0])
 except RuntimeError: pass
 else: assert False
def test_intent_interruption_blocks_rerun(tmp_path):
 p=plan();(tmp_path/"frozen_run_plan.json").write_text(json.dumps(p));assert run_cell(tmp_path,p["cells"][1],interrupt="after_intent")["status"]=="SYSTEM_INTERRUPTED_AFTER_CALL_INTENT"
 assert finalize(tmp_path)["verdict"]=="BLOCKED"
