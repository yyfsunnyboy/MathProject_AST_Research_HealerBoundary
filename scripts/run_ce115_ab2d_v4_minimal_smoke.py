"""Three-call, first-attempt-only CE115 Ab2d v4 minimal smoke."""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess,sys,time,urllib.request
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent_tools.finals_rebuild.ce115_ab2d_assembly import resolve_task_operations,runtime_namespace,runtime_toolbox_inventory,scan_toolbox,stub_for_task
from agent_tools.finals_rebuild.extraction import extract_code
from agent_tools.finals_rebuild.math_boundary_pilot import load_pilot_tasks
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
OUT=ROOT/'docs/experiments/results/ce115_ab2d_assembly_v4_minimal_smoke';SRC=ROOT/'docs/experiments/results/ce115_ab2d_assembly_v3_corrected_formal_run';PROTOCOL=ROOT/'docs/experiments/manifests/ce115_ab2d_assembly_protocol_v4.json';TASKS=[('polynomial','ce115_calc_polynomial_division_l1'),('fraction','ce115_calc_exact_rational_expression_l1'),('radical','ce115_calc_radical_simplification_l1')];MODEL='qwen3.5:4b'
def h(x):return hashlib.sha256(x.encode()).hexdigest()
def old_cell(task):return next(json.loads(p.read_text(encoding='utf8')) for p in sorted(SRC.glob('qwen*.json')) if json.loads(p.read_text(encoding='utf8'))['task']==task)
def preflight():
 protocol=json.loads(PROTOCOL.read_text(encoding='utf8')); inventory=runtime_toolbox_inventory();checks={'head_protocol_status':protocol.get('status')=='FROZEN_ZERO_MODEL_VALIDATED_V2','model_call_budget':3,'retry_replay_repair_healer_disabled':True,'output_contract':'generate(level=1, **kwargs) -> dict(question_text, correct_answer, oracle_payload)','families':{}}
 for family,task in TASKS:
  prompt=stub_for_task(task); checks['families'][family]={'available_domain_apis':'Available Domain APIs' in prompt,'no_legacy':not any(x in prompt for x in ('Required APIs','MUST_CALL','invoke every required API')),'semantics':all(x in prompt for x in ('Select only APIs relevant to the current task','Do not call irrelevant APIs merely for compliance','Use the domain library for every supported core operation actually required by the task','Do not manually reimplement a supported core algorithm','returned value contributes to the final answer')),'inventory_consistent':all(x['canonical_name'] in prompt and x['signature'] in prompt and x['return_structure'] in prompt for x in inventory)}
 checks['passed']=checks['head_protocol_status'] and all(all(x.values()) for x in checks['families'].values())
 return checks
def payload_for(task):
 cell=old_cell(task);old=cell['complete_request_payload']['messages'][0]['content'];contract=old[old.index('## Task contract'):];prompt=stub_for_task(task)+'\n'+contract
 frozen=json.loads(re.search(r'## Frozen parameters\n(\{.*?\})\nReturn only',contract,re.S).group(1));return cell,prompt,frozen
def run():
 if OUT.exists():raise RuntimeError('refusing overwrite existing smoke directory')
 pf=preflight();OUT.mkdir(parents=True);(OUT/'preflight_summary.json').write_text(json.dumps(pf,indent=2)+'\n')
 if not pf['passed']:raise RuntimeError('preflight failed before model calls')
 listing=subprocess.run(['ollama','list'],capture_output=True,text=True,timeout=15)
 if listing.returncode or MODEL not in listing.stdout:raise RuntimeError('preflight failed: frozen formal model unavailable')
 formal={x['task_id']:x for x in load_pilot_tasks(ROOT/'tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl')};rows=[];calls=0
 manifest={'run_id':'ce115_ab2d_assembly_v4_minimal_smoke','planned_cells':3,'model':MODEL,'first_attempt_only':True,'retry':0,'replay':0,'repair':0,'healer':0,'source_cells':{},'runtime_inventory':runtime_toolbox_inventory()}
 for index,(family,task) in enumerate(TASKS):
  cell,prompt,frozen=payload_for(task); request={'model':MODEL,'messages':[{'role':'user','content':prompt}],'stream':False,'think':False,'options':{'temperature':0.0,'seed':cell['seed'],'num_ctx':65536,'num_predict':24576}};started=time.monotonic();calls+=1
  try:
   req=urllib.request.Request('http://127.0.0.1:11434/api/chat',data=json.dumps(request).encode(),headers={'Content-Type':'application/json'},method='POST')
   with urllib.request.urlopen(req,timeout=600) as response: reply=json.loads(response.read())
   raw=reply.get('message',{}).get('content'); assert isinstance(raw,str)
   extraction=extract_code(raw);code=extraction.extracted_code if extraction.extraction_status=='extracted' else None
   scan=scan_toolbox(code or '',task,frozen);completion='NATURAL_COMPLETE' if code else 'EXTRACTION_FAILURE'
   try:
    ns=runtime_namespace();exec(compile(code or '','<smoke>','exec'),ns,ns);value=ns['generate']();verdict=evaluate_math_task_oracle(formal[task]['oracle_type'],frozen,value.get('correct_answer')) if isinstance(value,dict) else {'is_correct':False}; evaluator='PASSED' if verdict.get('is_correct') else 'EXECUTION_FAILURE' if not isinstance(value,dict) else 'ANSWER_INCORRECT'
   except Exception as exc: evaluator='EXECUTION_FAILURE';value=None;verdict={'error':f'{type(exc).__name__}: {exc}'}
  except Exception as exc:
   raw='';code=None;scan={'classification':'INSUFFICIENT_EVIDENCE','system_defect':True};completion='MODEL_FAILURE';evaluator='SYSTEM_DEFECT';reply={'error':f'{type(exc).__name__}: {exc}'};value=None;verdict={}
  artifact={'cell_id':f'v4_smoke_{family}_{cell["seed"]}','family':family,'task_id':task,'source_frozen_cell_id':cell['cell_id'],'exact_rendered_prompt':prompt,'available_domain_apis':runtime_toolbox_inventory(),'task_required_operations':resolve_task_operations(task,frozen)['required'],'acceptable_canonical_paths':resolve_task_operations(task,frozen)['acceptable_canonical_paths'],'frozen_parameters':frozen,'request_payload':request,'raw_model_response':raw,'raw_transport_response':reply,'extracted_code':code,'model_metadata':{'model':MODEL,'prompt_eval_count':reply.get('prompt_eval_count'),'eval_count':reply.get('eval_count'),'total_duration':reply.get('total_duration'),'load_duration':reply.get('load_duration'),'prompt_eval_duration':reply.get('prompt_eval_duration'),'eval_duration':reply.get('eval_duration'),'wall_clock_seconds':time.monotonic()-started},'completion':completion,'scanner_diagnostics':scan,'toolbox_adoption':scan['classification'],'evaluator_verdict':evaluator,'evaluator_details':verdict,'returned_value':value,'provenance':{'first_attempt_only':True,'request_number':calls,'retry':0,'replay':0,'repair':0,'healer':0},'hashes':{'prompt':h(prompt),'payload':h(json.dumps(request,sort_keys=True)),'raw':h(raw),'extracted_code':h(code or '')}}
  (OUT/f'{artifact["cell_id"]}.json').write_text(json.dumps(artifact,indent=2,default=str)+'\n');rows.append(artifact);manifest['source_cells'][family]=cell['cell_id']
 manifest['executed_model_calls']=calls;(OUT/'smoke_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 comp=Counter(x['completion'] for x in rows);adopt=Counter(x['toolbox_adoption'] for x in rows);ev=Counter(x['evaluator_verdict'] for x in rows);hashes=all(all(v for v in x['hashes'].values()) for x in rows);system=any(x['evaluator_verdict']=='SYSTEM_DEFECT' or x['scanner_diagnostics'].get('system_defect') for x in rows);gate=len(rows)==calls==3 and comp['NATURAL_COMPLETE']==3 and adopt['ASSEMBLY_COMPLIANT']>=2 and not system and hashes
 summary={'planned':3,'executed':len(rows),'unique_artifacts':len({x['cell_id'] for x in rows}),'model_calls':calls,'completion_counts':dict(comp),'toolbox_adoption_counts':dict(adopt),'evaluator_counts':dict(ev),'prompt_runtime_inventory_consistency':'3/3','retry_replay_repair_healer_calls':0,'system_defects':int(system),'hashes_complete':hashes,'verdict':'V4_MINIMAL_SMOKE_PASSED' if gate else 'V4_MINIMAL_SMOKE_BLOCKED','eligible_for_formal_rerun':gate,'formal_rerun_not_started':True};(OUT/'smoke_summary.json').write_text(json.dumps(summary,indent=2)+'\n');(OUT/'hash_integrity.json').write_text(json.dumps({'cells':3,'all_hashes_present':hashes},indent=2)+'\n');return summary
def persist_run_rows(output, planned, executor):
 """Persist a ledger and one artifact per planned cell even when one cell fails."""
 output=Path(output)
 if output.exists(): raise RuntimeError('refusing overwrite existing smoke directory')
 output.mkdir(parents=True); rows=[]; ledger=[]
 try:
  for index, cell in enumerate(planned, 1):
   ledger.append({'request_number':index,'cell':cell,'retry':0,'status':'started'})
   try: row=executor(cell, index)
   except Exception as exc: row={'cell_id':f'failure_{index}','completion':'SYSTEM_EXCEPTION','toolbox_adoption':'INSUFFICIENT_EVIDENCE','evaluator_verdict':'SYSTEM_DEFECT','error':f'{type(exc).__name__}: {exc}','provenance':{'request_number':index,'retry':0,'replay':0,'repair':0,'healer':0}}
   (output/f'{row["cell_id"]}.json').write_text(json.dumps(row,indent=2,default=str)+'\n');rows.append(row);ledger[-1]['status']='persisted'
 finally:
  (output/'zero_model_call_ledger.json').write_text(json.dumps(ledger,indent=2)+'\n')
  (output/'smoke_summary.json').write_text(json.dumps({'planned':len(planned),'executed':len(rows),'artifacts':len(rows),'calls':len(ledger),'retry':0,'replay':0,'repair':0,'healer':0,'finalized':True},indent=2)+'\n')
 return rows
if __name__=='__main__':print(json.dumps(run(),indent=2))
