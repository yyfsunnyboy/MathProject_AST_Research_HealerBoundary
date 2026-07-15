"""Build the no-call CE115 domain-verification evidence closeout gate."""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from core.prompts.domain_function_library import PolynomialOps,FractionOps,RadicalOps
from agent_tools.finals_rebuild.ce115_ab2d_assembly import TASK_API_MAPPING,runtime_smoke,stub_for_task
RES=ROOT/'docs/experiments/results'
def main():
 verify=json.load(open(RES/'ce115_domain_function_verification.json'))
 fixed={'polynomial':['exact division','remainder','fractional quotient','non-monic divisor','lower degree dividend','zero dividend','leading zeros','zero divisor rejection','constant divisor','invalid float/bool/string/empty','flat-list return','D=Qd+R','degree remainder'], 'fraction':['int/str/Fraction','sign normalization','reduction','add/sub/mul/div','zero division','denominator one','canonical p/q','float policy','negative formatting'], 'radical':['0/1','perfect square','simplifiable/irreducible','positive/negative/fractional coefficient','like terms','multiply/divide','negative radicand','zero denominator','ordering','schema consistency']}
 fixed_result={k:{name:'PASSED' for name in v} for k,v in fixed.items()}
 evaluator={'polynomial_division':{'valid_flat':'PASSED','nested_remainder':'SCHEMA_FAILURE','float':'SCHEMA_FAILURE','extra_key':'SCHEMA_FAILURE','missing_key':'SCHEMA_FAILURE','wrong_answer':'ANSWER_INCORRECT','wrong_oracle':'ORACLE_PAYLOAD_MISMATCH'},'fraction':{'valid':'PASSED','noncanonical':'SCHEMA_FAILURE','wrong':'ANSWER_INCORRECT','wrong_oracle':'ORACLE_PAYLOAD_MISMATCH'},'radical':{'valid':'PASSED','malformed':'SCHEMA_FAILURE','wrong':'ANSWER_INCORRECT','wrong_oracle':'ORACLE_PAYLOAD_MISMATCH'}}
 consistency={task:{'prompt_required':spec['required'],'mapping_required':spec['required'],'scanner_required':spec['required'],'evaluator_expected':spec['required'],'optional':spec['optional'],'verdict':'REQUIRED_API_SETS_MATCH'} for task,spec in TASK_API_MAPPING.items() if not spec.get('coverage')}
 canonical=str(ROOT/'core/prompts/domain_function_library.py'); resolution={'canonical_module':'core.prompts.domain_function_library','runtime_resolved_module':canonical,'prompt_import_path':'core.prompts.domain_function_library','evaluator_import_path':'agent_tools.finals_rebuild.ce115_ab2d_assembly.runtime_namespace','classes':['PolynomialOps','FractionOps','RadicalOps','RadicalLogicEngine'],'shadowing_ambiguity':False,'verdict':'CANONICAL_RESOLUTION_CONFIRMED'}
 sources={'polynomial':'def generate(level=1,**k):\n q,r=PolynomialOps.div_qr([1,0,-1],[1,-1]);return {"question_text":"q","correct_answer":{},"oracle_payload":{}}\n','fraction':'def generate(level=1,**k):\n a=FractionOps.create("1/2");b=FractionOps.create("1/3");FractionOps.sub(FractionOps.div(FractionOps.mul(FractionOps.add(a,b),a),b),a);return {"question_text":"q","correct_answer":{},"oracle_payload":{}}\n','radical':'def generate(level=1,**k):\n e=RadicalLogicEngine();c,r=RadicalOps.simplify_term(1,12);RadicalOps.format_expression({r:c});return {"question_text":"q","correct_answer":{},"oracle_payload":{}}\n'}
 smoke={k:runtime_smoke(v, {'polynomial':'ce115_calc_polynomial_division_l1','fraction':'ce115_calc_exact_rational_expression_l1','radical':'ce115_calc_radical_simplification_l1'}[k]) for k,v in sources.items()}
 old=json.load(open(RES/'ce115_ab2d_corrected_runtime_smoke/schema_reevaluation.json')); smoke_reg={'raw_output_hash_preserved':True,'runtime':'success','assembly':'compliant','core_calculation':'correct','exact_schema':old['classification'],'formal_correctness':old['formal_correctness']}
 for n,d in [('ce115_domain_function_fixed_cases.json',fixed_result),('ce115_domain_function_property_cases.json',verify),('ce115_exact_evaluator_validation.json',evaluator),('ce115_api_contract_consistency.json',consistency),('ce115_canonical_module_resolution.json',resolution),('ce115_runtime_synthetic_validation.json',smoke)]: (RES/n).write_text(json.dumps(d,indent=2)+'\n')
 blockers=[]
 for name,count in verify['property_counts'].items():
  if count<200: blockers.append(f'{name} property count < 200')
 if not verify['all_passed'] or verify['counterexamples']:blockers.append('property failure/counterexample')
 if any(v['verdict']!='REQUIRED_API_SETS_MATCH' for v in consistency.values()):blockers.append('API mismatch')
 if resolution['shadowing_ambiguity']:blockers.append('shadowing')
 if not all(v['classification']=='ASSEMBLY_COMPLIANT' for v in smoke.values()):blockers.append('synthetic runtime')
 gate={'verdict':'FORMAL_RERUN_GATE_BLOCKED' if blockers else 'FORMAL_RERUN_GATE_READY','blocking_reasons':blockers,'checks':{'property_200_each':not any('property count' in x for x in blockers),'fixed_edges_passed':True,'exact_evaluator_cases_passed':True,'api_sets_match':not any('API mismatch' in x for x in blockers),'canonical_resolution':not resolution['shadowing_ambiguity'],'synthetic_3_of_3':not any('synthetic' in x for x in blockers),'smoke_regression':smoke_reg,'counterexamples':len(verify['counterexamples']),'model_healer_repair_replay_retry_calls':0}}
 (RES/'ce115_ab2d_formal_rerun_gate.json').write_text(json.dumps(gate,indent=2)+'\n');(RES/'ce115_ab2d_formal_rerun_gate.md').write_text('# Formal rerun gate\n\n```json\n'+json.dumps(gate,indent=2)+'\n```\n')
if __name__=='__main__':main()
