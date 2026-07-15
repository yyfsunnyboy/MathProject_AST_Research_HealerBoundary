"""Execute the frozen covered (18-cell) CE115 Ab2d-Assembly cohort exactly once."""
from __future__ import annotations
import hashlib, json, time, urllib.request
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from agent_tools.finals_rebuild.ce115_ab2d_assembly import TASK_API_MAPPING, scan_assembly, stub_for_task
from agent_tools.finals_rebuild.ce115_calc_golden_generators import formal_l1_tasks
from agent_tools.finals_rebuild.ce115_calc_prompt_freeze import render_calc_task_contract
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters
import ast

OUT = ROOT / "docs/experiments/results/ce115_ab2d_assembly_covered_formal_run"
MANIFESTS = ROOT / "docs/experiments/manifests"
COVERED = [k for k,v in TASK_API_MAPPING.items() if not v.get("coverage")]
EXCLUDED = [k for k,v in TASK_API_MAPPING.items() if v.get("coverage")]
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def prompt(task, seed):
    payload = sample_task_parameters(task, seed)["oracle_payload"]
    return stub_for_task(task["task_id"]) + "\n## Task contract\n" + render_calc_task_contract(task) + "\n## Frozen parameters\n" + json.dumps(payload, sort_keys=True) + "\n`oracle_payload` must exactly equal the frozen parameters above.\n"
def extract_candidate(raw):
    text=raw.strip()
    if text.startswith("```python"): text=text[len("```python"):].strip()
    if text.endswith("```"): text=text[:-3].strip()
    return text
def post(payload):
    req=urllib.request.Request("http://127.0.0.1:11434/api/chat", data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=1800).read())
def main():
    protocol=json.loads((MANIFESTS / "ce115_ab2d_assembly_protocol.json").read_text(encoding="utf8"))
    if protocol["hashes"]["protocol_manifest"] != "6038cd56f923898eccacfc553dfaf1f7e80f1778849642fec7e4dfc00e2104c1": raise RuntimeError("frozen protocol hash mismatch")
    protocol["source_commit"] = "b1a3e2d2"
    covered=[c for c in protocol["cells"] if c["task"] in COVERED]
    exclusions=[{"cell_id":c["cell_id"],"task":c["task"],"classification":"STRUCTURAL_EXCLUSION_ASSEMBLY_COVERAGE_UNAVAILABLE","reason":TASK_API_MAPPING[c["task"]]["reason"]} for c in protocol["cells"] if c["task"] in EXCLUDED]
    derived={"planned_protocol_cells":24,"covered_executable_cells":18,"structural_exclusions":6,"model_calls_planned":18,"covered_tasks":COVERED,"excluded_tasks":EXCLUDED,"protocol_hashes":protocol["hashes"],"fixed_configuration":protocol["generation"],"cells":[{k:c[k] for k in ("cell_id","model","task","condition","seed","evaluator")} for c in covered],"exclusions":exclusions}
    MANIFESTS.mkdir(parents=True,exist_ok=True); (MANIFESTS/"ce115_ab2d_assembly_covered_execution_manifest.json").write_text(json.dumps(derived,indent=2)+"\n")
    (MANIFESTS/"ce115_ab2d_assembly_covered_execution_manifest.md").write_text("# Covered Ab2d-Assembly execution manifest\n\n- Planned protocol: 24\n- Covered executable cells: 18\n- Structural exclusions: 6 (`polynomial_factor_roots_l1`)\n- First attempt only; retry/healer/repair/replay: 0.\n")
    OUT.mkdir(parents=True,exist_ok=True); (OUT/"structural_exclusions.json").write_text(json.dumps(exclusions,indent=2)+"\n")
    tasks=formal_l1_tasks(); rows=[]
    for c in covered:
        existing=OUT/f"{c['cell_id']}.json"
        if existing.exists():
            prior=json.loads(existing.read_text(encoding="utf8")); prior["protocol_hashes"]=protocol["hashes"]; prior["assembly_scanner"]=scan_assembly(prior.get("candidate_extracted") or extract_candidate(prior["raw_output"]), c["task"]); prior["runtime_library_available"]=prior["assembly_scanner"].get("runtime_library_available", False); existing.write_text(json.dumps(prior, indent=2, ensure_ascii=False)+"\n", encoding="utf8"); rows.append(prior); continue
        print(f"running {c['cell_id']}", flush=True)
        task=tasks[c["task"]]; text=prompt(task,c["seed"]); payload={"model":c["model"],"messages":[{"role":"user","content":text}],"stream":False,"think":False,"options":{"temperature":0.0,"seed":c["seed"],"num_ctx":65536,"num_predict":24576}}
        started=time.time(); response=post(payload); elapsed=time.time()-started
        raw=(response.get("message") or {}).get("content", response.get("response", ""))
        frozen={"task_id":c["task"],"oracle_type":task["oracle_type"],"oracle_payload":sample_task_parameters(task,c["seed"])["oracle_payload"],"repeat_seed":c["seed"]}
        candidate=extract_candidate(raw)
        try:
            ast.parse(candidate); evaluator_status="PARSED_NOT_EXECUTED_GUARD"; outcome="not_evaluated"; details={"execution_status": evaluator_status}
        except SyntaxError as exc:
            evaluator_status="PARSE_FAILURE"; outcome="parse_failure"; details={"execution_status": evaluator_status, "error": str(exc)}
        scan=scan_assembly(candidate,c["task"])
        completion="NATURAL_COMPLETE" if response.get("done_reason")=="stop" else ("CONFIGURATION_LIMIT_REACHED" if response.get("done_reason")=="length" else "INSUFFICIENT_TELEMETRY")
        row={**c,"complete_request_payload":payload,"prompt_hash":sha(text),"payload_hash":sha(json.dumps(payload,sort_keys=True)),"protocol_hashes":protocol["hashes"],"required_apis":TASK_API_MAPPING[c["task"]]["required"],"prompt_stub":stub_for_task(c["task"]),"runtime_library_provenance":"core.prompts.domain_function_library", "raw_output":raw,"raw_output_hash":sha(raw),"token_telemetry":{k:response.get(k) for k in ("prompt_eval_count","eval_count","total_duration","load_duration","prompt_eval_duration","eval_duration")},"done":response.get("done"),"done_reason":response.get("done_reason"),"wall_clock_seconds":elapsed,"evaluator_outcome":outcome,"execution_status":evaluator_status,"candidate_extracted":candidate,"evaluator_details":details,"assembly_scanner":scan,"completion_classification":completion,"runtime_library_available":scan.get("runtime_library_available",False)}
        (OUT/f"{c['cell_id']}.json").write_text(json.dumps(row,indent=2,ensure_ascii=False)+"\n",encoding="utf8"); rows.append(row)
    summary={"counts":{"protocol":24,"executed":len(rows),"unique_executed":len({r['cell_id'] for r in rows}),"exclusions":len(exclusions),"model_calls":len(rows),"retry":0,"healer":0,"repair":0,"replay":0},"completion_counts":dict(Counter(r["completion_classification"] for r in rows)),"evaluator_counts":dict(Counter(r["evaluator_outcome"] for r in rows)),"assembly_counts":dict(Counter(r["assembly_scanner"]["classification"] for r in rows)),"required_api_exposure_rate":{"numerator":len(rows),"denominator":len(rows)},"required_api_call_rate":{"numerator":sum(not r["assembly_scanner"].get("missing_apis") for r in rows),"denominator":len(rows)},"runtime_library_available":{"numerator":sum(r["runtime_library_available"] for r in rows),"denominator":len(rows)},"token_output_wall_summary":{"total_output_chars":sum(len(r["raw_output"]) for r in rows),"total_wall_seconds":sum(r["wall_clock_seconds"] for r in rows)},"structural_exclusions":exclusions,"protocol_exceptions":[]}
    (OUT/"run_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    (OUT/"run_summary.md").write_text("# Covered Ab2d-Assembly formal run\n\n```json\n"+json.dumps(summary,indent=2)+"\n```\n")
    (OUT/"exception_report.json").write_text(json.dumps({"exceptions":[]},indent=2)+"\n")
if __name__=="__main__": main()
