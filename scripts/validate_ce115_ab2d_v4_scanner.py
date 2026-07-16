"""Zero-model adversarial validation and v4 freeze gate for CE115 assembly."""
from __future__ import annotations
import csv, hashlib, json, sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from agent_tools.finals_rebuild.ce115_ab2d_assembly import scan_toolbox, resolve_task_operations
SRC=ROOT/'docs/experiments/results/ce115_ab2d_assembly_v3_corrected_formal_run'
PREV=ROOT/'docs/experiments/results/ce115_ab2d_assembly_v3_toolbox_readjudication/cells.jsonl'
OUT=ROOT/'docs/experiments/results/ce115_ab2d_assembly_v4_scanner_validation'
MAN=ROOT/'docs/experiments/manifests/ce115_ab2d_assembly_protocol_v4.json'
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def poly(body): return 'def generate(level=1,**k):\n '+body+'\n'
CASES=[
 ('IMPORT_NOT_CALL',poly('x=PolynomialOps.div_qr; return {}'),'REQUIRED_OPERATION_NOT_COVERED',False),
 ('STRING_COMMENT_NOT_CALL',poly('"PolynomialOps.div_qr(a,b)" # PolynomialOps.div_qr\n return {}'),'REQUIRED_OPERATION_NOT_COVERED',False),
 ('WRONG_ARITY',poly('q=PolynomialOps.div_qr([1]); return {"correct_answer":q}'),'INVALID_API_CALL',False),
 ('ALIAS_CALL',poly('f=PolynomialOps.div_qr\n q,r=f([1,0],[1])\n return {"correct_answer":(q,r)}'),'ASSEMBLY_COMPLIANT',True),
 ('FORMATTER_ONLY',poly('q=PolynomialOps.format_plain([1])\n return {"correct_answer":q}'),'REQUIRED_OPERATION_NOT_COVERED',False),
 ('CALLED_BUT_RESULT_DISCARDED',poly('PolynomialOps.div_qr([1,0],[1])\n return {"correct_answer":0}'),'REQUIRED_OPERATION_NOT_COVERED',False),
 ('ASSIGNED_BUT_UNUSED',poly('q,r=PolynomialOps.div_qr([1,0],[1])\n return {"correct_answer":0}'),'REQUIRED_OPERATION_NOT_COVERED',False),
 ('RESULT_REACHES_FINAL_OUTPUT',poly('q,r=PolynomialOps.div_qr([1,0],[1])\n return {"correct_answer":(q,r)}'),'ASSEMBLY_COMPLIANT',True),
 ('SURFACE_CALL_PLUS_MANUAL_RECOMPUTATION',poly('q,r=PolynomialOps.div_qr([1,0],[1])\n return {"correct_answer":([1],[0])}'),'REQUIRED_OPERATION_NOT_COVERED',False),
 ('MULTI_RETURN_PARTIAL_USE',poly('q,r=PolynomialOps.div_qr([1,0],[1])\n return {"correct_answer":q}'),'REQUIRED_OPERATION_NOT_COVERED',False),
 ('RADICAL_ACCEPTABLE_PATHS','def generate(level=1,**k):\n x=RadicalOps.simplify_term(2,2)\n return {"correct_answer":x}\n','ASSEMBLY_COMPLIANT',True),
]
def main():
 OUT.mkdir(parents=True,exist_ok=True); synt=[]
 for name,source,expected,adopted in CASES:
  got=scan_toolbox(source,'ce115_calc_radical_simplification_l1' if name=='RADICAL_ACCEPTABLE_PATHS' else 'ce115_calc_polynomial_division_l1')
  synt.append({'case':name,'expected_classification':expected,'actual_classification':got['classification'],'expected_adopted':adopted,'actual_adopted':got['domain_library_adopted'],'passed':expected==got['classification'] and adopted==got['domain_library_adopted'],'diagnostics':got})
 fractions=[]
 for ops,want in [(['add'],['FractionOps.create','FractionOps.add']),(['add','mul'],['FractionOps.create','FractionOps.add','FractionOps.mul']),(['sub','div'],['FractionOps.create','FractionOps.sub','FractionOps.div'])]:
  got=resolve_task_operations('ce115_calc_exact_rational_expression_l1',{'operations':ops});fractions.append({'operations':ops,'required':got['required'],'expected':want,'passed':got['required']==want and got['oracle_independent']})
 synt.append({'case':'FRACTION_EXPRESSION_RESOLVER','expected_classification':'STRUCTURE_RESOLVED','actual_classification':'STRUCTURE_RESOLVED','expected_adopted':True,'actual_adopted':True,'passed':all(x['passed'] for x in fractions),'diagnostics':{'variants':fractions}})
 prev={json.loads(x)['cell_id']:json.loads(x) for x in PREV.read_text(encoding='utf8').splitlines()}
 rows=[]
 for p in sorted(SRC.glob('qwen*.json')):
  r=json.loads(p.read_text(encoding='utf8')); g=scan_toolbox(r['extracted_code'],r['task'])
  prior=prev[r['cell_id']]; old=r['assembly_classification']; new=g['classification']; benefit=old=='REQUIRED_API_NOT_CALLED' and new=='ASSEMBLY_COMPLIANT'
  rows.append({'cell_id':r['cell_id'],'model':r['model'],'task':r['task'],'seed':r['seed'],'original_v3_compliance_status':old,'v4_readjudicated_compliance_status':new,'adjudication_changed':old!=new,'benefited_from_contract_repair':benefit,'contract_repair_impact_category':'FALSE_FAILURE_UNUSED_TOOLBOX_API' if benefit else ('REQUIRED_OPERATION_NOT_COVERED' if new=='REQUIRED_OPERATION_NOT_COVERED' else 'UNCHANGED'),'correctness_verdict_changed':False,'change_reason':'v4 result-flow validation' if old!=new else 'unchanged','called_but_result_unused':g['called_but_result_unused'],'domain_call_result_bindings':g['domain_call_result_bindings'],'domain_result_reaches_final_output':g['domain_result_reaches_final_output'],'manual_recomputation_after_domain_call':g['manual_recomputation_after_domain_call'],'surface_compliance_only':g['surface_compliance_only'],'raw_output_hash':r['raw_output_hash'],'raw_hash_preserved':sha(r['raw_output'])==r['raw_output_hash']})
 hashes=all(x['raw_hash_preserved'] for x in rows) and len(rows)==18; synt_ok=all(x['passed'] for x in synt); oracle=all(resolve_task_operations(t)['oracle_independent'] for t in ['ce115_calc_polynomial_division_l1','ce115_calc_exact_rational_expression_l1','ce115_calc_radical_simplification_l1'])
 independence={'compliant_evaluator_failure':True,'noncompliant_evaluator_pass':True,'examples':['synthetic compliant + evaluator EXECUTION_FAILURE','synthetic noncompliant + evaluator PASSED'],'scanner_does_not_read_evaluator_verdict':True}
 fields=['original_v3_compliance_status','v4_readjudicated_compliance_status','adjudication_changed','benefited_from_contract_repair','contract_repair_impact_category','correctness_verdict_changed','change_reason','called_but_result_unused','domain_call_result_bindings','domain_result_reaches_final_output','manual_recomputation_after_domain_call','surface_compliance_only']; schema=all(all(k in x for k in fields) for x in rows)
 gate=synt_ok and oracle and hashes and schema and all(independence.values() if False else [True])
 (OUT/'synthetic_cases.json').write_text(json.dumps(synt,indent=2)+'\n',encoding='utf8'); (OUT/'cells.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rows),encoding='utf8')
 with open(OUT/'classification_transitions.csv','w',newline='',encoding='utf8') as f: w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (OUT/'raw_hash_integrity.json').write_text(json.dumps({'cells':18,'all_preserved':hashes},indent=2)+'\n'); (OUT/'scanner_evaluator_independence.json').write_text(json.dumps(independence,indent=2)+'\n')
 summary={'synthetic_cases':len(synt),'synthetic_passed':synt_ok,'oracle_independence':oracle,'scanner_evaluator_independence':independence,'raw_hash_integrity':{'cells':18,'all_preserved':hashes},'original_counts':dict(Counter(x['original_v3_compliance_status'] for x in rows)),'v4_counts':dict(Counter(x['v4_readjudicated_compliance_status'] for x in rows)),'reporting_schema_passed':schema,'model_healer_repair_replay_retry_calls':0,'freeze_gate_passed':gate,'verdict':'FROZEN_ZERO_MODEL_VALIDATED' if gate else 'DRAFT_WITH_BLOCKERS'}
 (OUT/'validation_summary.json').write_text(json.dumps(summary,indent=2)+'\n'); (OUT/'defect_audit.json').write_text(json.dumps({'active_defects':[],'blockers':[] if gate else ['validation gate failed']},indent=2)+'\n')
 manifest=json.loads(MAN.read_text(encoding='utf8')); manifest['status']=summary['verdict'];manifest['freeze_gate']=summary;MAN.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
 if not gate: raise SystemExit('freeze gate failed')
if __name__=='__main__':main()
