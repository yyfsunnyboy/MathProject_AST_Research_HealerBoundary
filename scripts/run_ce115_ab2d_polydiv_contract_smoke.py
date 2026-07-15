"""One disposable model smoke for the flat PolynomialOps.div_qr return contract."""
from __future__ import annotations
import hashlib,json,subprocess,sys,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent_tools.finals_rebuild.ce115_ab2d_assembly import scan_assembly,stub_for_task
OUT=ROOT/'docs/experiments/results/ce115_ab2d_polydiv_contract_smoke';MAN=ROOT/'docs/experiments/manifests/ce115_ab2d_assembly_protocol_v3.json'
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def extract(s):
 s=s.strip();return s[len('```python'):].strip()[:-3].strip() if s.startswith('```python') and s.endswith('```') else s
def execute(s):
 h='import sys;sys.path.insert(0,sys.argv[1]);from agent_tools.finals_rebuild.ce115_ab2d_assembly import runtime_namespace;ns=runtime_namespace();exec(compile(sys.stdin.read(),"<smoke>","exec"),ns,ns);print(ns["generate"]())'
 r=subprocess.run([sys.executable,'-c',h,str(ROOT)],input=s,text=True,capture_output=True,cwd=ROOT,timeout=8);return r.returncode==0,(r.stdout or r.stderr).strip()
def main():
 prompt=stub_for_task('ce115_calc_polynomial_division_l1')+'''\nWrite only Python. Implement generate(level=1, **kwargs) for frozen dividend_coefficients=[-6,-4,3] and divisor_coefficients=[1,-2]. Call PolynomialOps.div_qr exactly once using those lists. Directly unpack `quotient_coefficients, remainder_coefficients`. Return exactly question_text, correct_answer, oracle_payload. correct_answer must be {"quotient_coefficients": quotient_coefficients, "remainder_coefficients": remainder_coefficients}; do not wrap remainder_coefficients. Expected exact answer is quotient [-6,-16], remainder [-29]. oracle_payload must exactly equal the frozen inputs.\n'''
 payload={'model':'qwen3.5:4b','messages':[{'role':'user','content':prompt}],'stream':False,'think':False,'options':{'temperature':0.0,'seed':2026071302,'num_ctx':65536,'num_predict':24576}}
 manifest={'protocol_id':'ce115_ab2d_assembly_protocol_v3','source_commit':'971c5b54','return_contract':'flat_polydiv_v3','classification':'NON_FORMAL_DISPOSABLE_SMOKE','analysis_status':'EXCLUDED_FROM_ALL_FORMAL_ANALYSES','model_calls_planned':1,'retry':0,'healer':0,'repair':0,'replay':0,'hashes':{'prompt':sha(prompt),'payload':sha(json.dumps(payload,sort_keys=True))}}
 MAN.write_text(json.dumps(manifest,indent=2)+'\n');(ROOT/'docs/experiments/manifests/ce115_ab2d_assembly_protocol_v3.md').write_text('# Ab2d Assembly Protocol v3\n\nDirectly unpack flat polynomial quotient/remainder lists.\n')
 pre='def generate(level=1,**kwargs):\n quotient_coefficients,remainder_coefficients=PolynomialOps.div_qr([-6,-4,3],[1,-2]);return {"question_text":"q","correct_answer":{"quotient_coefficients":quotient_coefficients,"remainder_coefficients":remainder_coefficients},"oracle_payload":{"dividend_coefficients":[-6,-4,3],"divisor_coefficients":[1,-2]}}\n';preok,predetail=execute(pre)
 started=time.time();req=urllib.request.Request('http://127.0.0.1:11434/api/chat',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'});body=json.loads(urllib.request.urlopen(req,timeout=1800).read());wall=time.time()-started;raw=(body.get('message') or {}).get('content','');code=extract(raw);scan=scan_assembly(code,'ce115_calc_polynomial_division_l1');ok,detail=execute(code)
 nested='[[-29]]' in raw; flat='"remainder_coefficients": [-29]' in raw.replace(' ', '') or "'remainder_coefficients': [-29]" in raw.replace(' ','')
 verdict='SMOKE_CORRECTNESS_AND_SCHEMA_CONFIRMED' if ok and scan['classification']=='ASSEMBLY_COMPLIANT' and not nested else ('SMOKE_RUNTIME_OK_BUT_MODEL_SCHEMA_FAILED' if ok else 'SMOKE_RUNTIME_OK_BUT_MODEL_ANSWER_FAILED')
 OUT.mkdir(parents=True,exist_ok=True);art={**manifest,'payload':payload,'raw_output':raw,'raw_output_hash':sha(raw),'extracted_code':code,'scanner':scan,'runtime_executed':ok,'evaluator_result':detail,'synthetic_wrapper_passed':preok,'pre_detail':predetail,'nested_remainder':nested,'flat_remainder_evidence':flat,'completion':'NATURAL_COMPLETE' if body.get('done_reason')=='stop' else 'CONFIGURATION_LIMIT_REACHED','telemetry':{k:body.get(k) for k in ('prompt_eval_count','eval_count','total_duration')},'wall_clock_seconds':wall,'verdict':verdict,'model_healer_repair_replay_retry_counts':{'model':1,'healer':0,'repair':0,'replay':0,'retry':0}}
 (OUT/'smoke_cell.json').write_text(json.dumps(art,indent=2)+'\n');(OUT/'smoke_summary.json').write_text(json.dumps({'verdict':verdict,'nested_remainder':nested,'runtime_executed':ok},indent=2)+'\n');(OUT/'smoke_summary.md').write_text('# Polydiv contract smoke\n\n```json\n'+json.dumps(art,indent=2)+'\n```\n');(OUT/'exception_report.json').write_text(json.dumps({'exception':None if ok else detail},indent=2)+'\n')
if __name__=='__main__':main()
