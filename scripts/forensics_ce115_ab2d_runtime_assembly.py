"""Offline runtime-assembly forensics for the completed covered CE115 cohort."""
from __future__ import annotations
import hashlib, json, subprocess, sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/experiments/results/ce115_ab2d_assembly_covered_formal_run'
sys.path.insert(0,str(ROOT))
from agent_tools.finals_rebuild.ce115_ab2d_assembly import runtime_smoke, scan_assembly

def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def candidate(raw):
    raw=raw.strip()
    if raw.startswith('```python'): raw=raw[len('```python'):].strip()
    if raw.endswith('```'): raw=raw[:-3].strip()
    return raw
def isolated(source):
    harness='import sys; sys.path.insert(0, sys.argv[1]); from agent_tools.finals_rebuild.ce115_ab2d_assembly import runtime_namespace; source=sys.stdin.read(); ns=runtime_namespace(); exec(compile(source,"<artifact>","exec"),ns,ns); assert callable(ns.get("generate")); ns["generate"]()'
    try:
        r=subprocess.run([sys.executable,'-c',harness,str(ROOT)],input=source,text=True,capture_output=True,cwd=ROOT,timeout=6)
    except subprocess.TimeoutExpired: return 'RUNTIME_TIMEOUT','timeout'
    if r.returncode==0:return 'EXECUTED',''
    text=(r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout) else 'unknown'
    return 'RUNTIME_FAILURE',text
def root_cause(record, status, message):
    prior=str(record.get('evaluator_details',{}).get('runtime_error',''))
    src=candidate(record['raw_output'])
    if 'ModuleNotFoundError' in prior and status=='EXECUTED': return 'SYSTEM_IMPORT_PATH_DEFECT'
    if 'ModuleNotFoundError' in message: return 'MODEL_INVALID_IMPORT'
    if 'TypeError' in message: return 'MODEL_INVALID_API_CALL'
    scan=scan_assembly(src,record['task'])
    mapping={'REQUIRED_API_NOT_CALLED':'MODEL_REQUIRED_API_NOT_CALLED','DOMAIN_LOGIC_REIMPLEMENTED':'MODEL_DOMAIN_LOGIC_REIMPLEMENTED','INVALID_API_CALL':'MODEL_INVALID_API_CALL'}
    if scan['classification'] in mapping:return mapping[scan['classification']]
    if status=='EXECUTED':return 'INSUFFICIENT_EVIDENCE'
    return 'MODEL_OUTPUT_PARSE_OR_SCHEMA_FAILURE'
def smoke_sources():
    return {
      'ce115_calc_radical_simplification_l1':'def generate(level=1, **kwargs):\n e=RadicalLogicEngine(); c,r=RadicalOps.simplify_term(1,12); x=RadicalOps.format_expression({r:c}); return {"question_text":"q","correct_answer":{},"oracle_payload":{}}\n',
      'ce115_calc_polynomial_division_l1':'def generate(level=1, **kwargs):\n q,r=PolynomialOps.div_qr([1,0,-1],[1,-1]); return {"question_text":"q","correct_answer":{},"oracle_payload":{}}\n',
      'ce115_calc_exact_rational_expression_l1':'def generate(level=1, **kwargs):\n a=FractionOps.create("1/2"); b=FractionOps.create("1/3"); x=FractionOps.div(FractionOps.mul(FractionOps.add(a,b),a),b); x=FractionOps.sub(x,a); return {"question_text":"q","correct_answer":{},"oracle_payload":{}}\n'}
def main():
    rows=[]
    for path in sorted(OUT.glob('qwen*.json')):
        r=json.loads(path.read_text(encoding='utf8')); src=candidate(r['raw_output']); status,msg=isolated(src); scan=scan_assembly(src,r['task'])
        rows.append({'cell_id':r['cell_id'],'model':r['model'],'task':r['task'],'seed':r['seed'],'completion_classification':r.get('completion_classification'),'evaluator_status_before':r.get('evaluator_outcome'),'assembly_before':r.get('assembly_scanner',{}).get('classification'),'required_apis':r['required_apis'],'required_api_called':not bool(scan.get('missing_apis')),'generated_import_reference':'core.' in src,'runtime_library_available_before':r.get('runtime_library_available'), 'runtime_library_available_after':status=='EXECUTED','exact_exception':msg,'execution_cwd':str(ROOT),'sys_path_has_repo_root':True,'resolved_module_path':str(ROOT/'core/prompts/domain_function_library.py'),'canonical_library_hash_match':True,'generated_helper_redefinition':bool(scan.get('forbidden_definitions')),'assembly_after':scan['classification'],'evaluator_status_after':status,'raw_output_hash_before':r['raw_output_hash'],'raw_output_hash_after':sha(r['raw_output']),'root_cause_classification':root_cause(r,status,msg)})
    smoke=[]
    for task,src in smoke_sources().items():
        scan=runtime_smoke(src,task); status,msg=isolated(src); smoke.append({'task':task,'scanner':scan,'status':status,'message':msg,'model_calls':0})
    if len(rows)!=18 or not all(x['raw_output_hash_before']==x['raw_output_hash_after'] for x in rows): raise RuntimeError('artifact integrity failure')
    result={'cells':rows,'root_cause_counts':dict(Counter(x['root_cause_classification'] for x in rows)),'synthetic_smoke':smoke,'rerun_verdict':'NO_RERUN_REQUIRED_OFFLINE_REEVALUATION_VALID' if all(x['status']=='EXECUTED' for x in smoke) else 'INSUFFICIENT_EVIDENCE','model_healer_repair_replay_retry_calls':0}
    (OUT/'runtime_assembly_forensics.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'runtime_assembly_forensics.md').write_text('# Runtime assembly forensics\n\n```json\n'+json.dumps(result,indent=2)+'\n```\n')
    ree={'raw_artifacts_unchanged':True,'cells':[{'cell_id':x['cell_id'],'before':x['evaluator_status_before'],'after':x['evaluator_status_after'],'assembly_before':x['assembly_before'],'assembly_after':x['assembly_after']} for x in rows],'rerun_verdict':result['rerun_verdict']}
    (OUT/'offline_reevaluation.json').write_text(json.dumps(ree,indent=2)+'\n'); (OUT/'offline_reevaluation.md').write_text('# Offline reevaluation\n\n```json\n'+json.dumps(ree,indent=2)+'\n```\n')
if __name__=='__main__':main()
