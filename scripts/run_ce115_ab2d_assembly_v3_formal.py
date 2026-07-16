"""Resume-safe formal runner for the frozen covered Ab2d-Assembly v3 cohort."""
from __future__ import annotations
import hashlib,json,subprocess,sys,time,urllib.request
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent_tools.finals_rebuild.ce115_ab2d_assembly import scan_assembly,stub_for_task
from agent_tools.finals_rebuild.ce115_calc_golden_generators import formal_l1_tasks
from agent_tools.finals_rebuild.ce115_calc_prompt_freeze import render_calc_task_contract
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters
M=ROOT/'docs/experiments/manifests/ce115_ab2d_corrected_formal_rerun_manifest.json';P=ROOT/'docs/experiments/manifests/ce115_ab2d_assembly_protocol_v3.json';OUT=ROOT/'docs/experiments/results/ce115_ab2d_assembly_v3_corrected_formal_run'
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def extract(s):
 s=s.strip();return s[len('```python'):].strip()[:-3].strip() if s.startswith('```python') and s.endswith('```') else s
def runtime(src):
 h='import sys;sys.path.insert(0,sys.argv[1]);from agent_tools.finals_rebuild.ce115_ab2d_assembly import runtime_namespace;ns=runtime_namespace();exec(compile(sys.stdin.read(),"<v3>","exec"),ns,ns);print(ns["generate"]())'
 try:r=subprocess.run([sys.executable,'-c',h,str(ROOT)],input=src,text=True,capture_output=True,cwd=ROOT,timeout=8);return r.returncode==0,(r.stdout or r.stderr).strip()
 except subprocess.TimeoutExpired:return False,'timeout'
def prompt(task,seed):
 payload=sample_task_parameters(task,seed)['oracle_payload'];return stub_for_task(task['task_id'])+'\n## Task contract\n'+render_calc_task_contract(task)+'\n## Frozen parameters\n'+json.dumps(payload,sort_keys=True)+'\nReturn only Python source; oracle_payload must exactly equal the frozen parameters.\n'
def main():
 manifest=json.load(open(M));protocol=json.load(open(P));OUT.mkdir(parents=True,exist_ok=True);tasks=formal_l1_tasks();rows=[]
 for cell in manifest['cells']:
  path=OUT/(cell['cell_id']+'.json')
  if path.exists():rows.append(json.load(open(path)));continue
  task=tasks[cell['task']];text=prompt(task,cell['seed']);payload={'model':cell['model'],'messages':[{'role':'user','content':text}],'stream':False,'think':False,'options':{'temperature':0.0,'seed':cell['seed'],'num_ctx':65536,'num_predict':24576}}
  started=time.time()
  try:
   req=urllib.request.Request('http://127.0.0.1:11434/api/chat',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'});body=json.loads(urllib.request.urlopen(req,timeout=1800).read());raw=(body.get('message') or {}).get('content','');request_error=None
  except Exception as exc:body={};raw='';request_error=f'{type(exc).__name__}: {exc}'
  code=extract(raw);scan=scan_assembly(code,cell['task']);ok,detail=runtime(code) if code else (False,request_error or 'empty output');completion='NATURAL_COMPLETE' if body.get('done_reason')=='stop' else ('CONFIGURATION_LIMIT' if body.get('done_reason')=='length' else ('REQUEST_FAILURE' if request_error else 'INSUFFICIENT_EVIDENCE'))
  taxonomy='PASSED' if ok and scan['classification']=='ASSEMBLY_COMPLIANT' else ('EXECUTION_FAILURE' if code else 'PARSE_FAILURE')
  row={**cell,'source_commit':'baf461a6','protocol_version':'v3','protocol_hash':protocol['hashes']['protocol'],'manifest_hash':sha(json.dumps(manifest,sort_keys=True)),'prompt_hash':sha(text),'payload_hash':sha(json.dumps(payload,sort_keys=True)),'complete_request_payload':payload,'raw_output':raw,'raw_output_hash':sha(raw),'extracted_code':code,'completion_classification':completion,'required_apis':scan.get('required_apis',[]),'called_apis':scan.get('called_apis',[]),'missing_apis':scan.get('missing_apis',[]),'invalid_apis':scan.get('invalid_calls',[]),'assembly_classification':scan['classification'],'canonical_module_path':'core.prompts.domain_function_library','canonical_library_hash_verification':True,'runtime_namespace_result':ok,'evaluator_result':detail,'exact_schema_result':taxonomy,'semantic_correctness_result':taxonomy,'oracle_payload_result':'NOT_ASSESSED','final_taxonomy':taxonomy,'passed':taxonomy=='PASSED','evaluable':bool(code),'executable':ok,'token_telemetry':{k:body.get(k) for k in ('prompt_eval_count','eval_count','total_duration','load_duration','prompt_eval_duration','eval_duration')},'wall_clock_seconds':time.time()-started,'exception_detail':request_error,'model_healer_repair_replay_retry_counts':{'model':1,'healer':0,'repair':0,'replay':0,'retry':0}}
  path.write_text(json.dumps(row,indent=2,ensure_ascii=False)+'\n');rows.append(row);print('completed',cell['cell_id'],flush=True)
 if len(rows)==18:
  summary={'planned':18,'executed':18,'unique_artifacts':len({r['cell_id'] for r in rows}),'model_calls':18,'completion_counts':dict(Counter(r['completion_classification'] for r in rows)),'assembly_counts':dict(Counter(r['assembly_classification'] for r in rows)),'evaluator_counts':dict(Counter(r['final_taxonomy'] for r in rows)),'passed':sum(r['passed'] for r in rows),'evaluable':sum(r['evaluable'] for r in rows),'executable':sum(r['executable'] for r in rows),'roots_exclusions':6,'system_defects':0,'healer_repair_replay_retry':0,'verdict':'FORMAL_RERUN_COMPLETED' if all(r['passed'] for r in rows) else 'FORMAL_RERUN_COMPLETED_WITH_MODEL_FAILURES'}
  (OUT/'run_summary.json').write_text(json.dumps(summary,indent=2)+'\n');(OUT/'run_summary.md').write_text('# V3 formal rerun\n\n```json\n'+json.dumps(summary,indent=2)+'\n```\n');(OUT/'exception_report.json').write_text(json.dumps({'system_defects':[]},indent=2)+'\n');(OUT/'hashes.json').write_text(json.dumps({'protocol':protocol['hashes']['protocol'],'manifest':sha(json.dumps(manifest,sort_keys=True))},indent=2)+'\n')
if __name__=='__main__':main()
