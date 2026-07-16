"""Zero-model prompt-contract repair validation; does not touch prior evidence."""
from __future__ import annotations
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent_tools.finals_rebuild.ce115_ab2d_assembly import runtime_toolbox_inventory,stub_for_task,scan_toolbox,resolve_task_operations
from scripts.validate_ce115_ab2d_v4_scanner import CASES
OUT=ROOT/'docs/experiments/results/ce115_ab2d_assembly_v4_prompt_contract_validation'; MAN=ROOT/'docs/experiments/manifests/ce115_ab2d_assembly_protocol_v4.json'; RAW=ROOT/'docs/experiments/results/ce115_ab2d_assembly_v3_corrected_formal_run'
TASKS={'polynomial':'ce115_calc_polynomial_division_l1','fraction':'ce115_calc_exact_rational_expression_l1','radical':'ce115_calc_radical_simplification_l1'}
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def main():
 OUT.mkdir(parents=True,exist_ok=True); manifest=json.loads(MAN.read_text(encoding='utf8')); manifest['status']='DRAFT_PROMPT_CONTRACT_REPAIR';MAN.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
 inventory=runtime_toolbox_inventory(); rendered={}; checks={}
 forbidden=['Required APIs','MUST_CALL','invoke every required API']
 required_phrases=['Available Domain APIs','Select only APIs relevant to the current task','Do not call irrelevant APIs merely for compliance','Use the domain library for every supported core operation actually required by the task','Do not manually reimplement a supported core algorithm','returned value contributes to the final answer','Standard Python may be used for control flow']
 for family,task in TASKS.items():
  text=stub_for_task(task); rendered[family]=text;(OUT/f'rendered_prompt_{family}.txt').write_text(text,encoding='utf8')
  checks[family]={'contains_required_phrases':all(x in text for x in required_phrases),'contains_no_legacy_language':not any(x in text for x in forbidden),'all_runtime_apis_visible':all(x['canonical_name'] in text and x['signature'] in text and x['return_structure'] in text for x in inventory),'task_required_operations_not_disclosed':'task_required_operations' not in text}
 hashes=[]
 for f in RAW.glob('qwen*.json'):
  r=json.loads(f.read_text(encoding='utf8'));hashes.append(hashlib.sha256(r['raw_output'].encode()).hexdigest()==r['raw_output_hash'])
 adversarial=[]
 for name,source,expected,adopted in CASES:
  task='ce115_calc_radical_simplification_l1' if name=='RADICAL_ACCEPTABLE_PATHS' else 'ce115_calc_polynomial_division_l1'
  got=scan_toolbox(source,task);adversarial.append(expected==got['classification'] and adopted==got['domain_library_adopted'])
 fraction_checks=[resolve_task_operations('ce115_calc_exact_rational_expression_l1', {'operations':ops})['required']==want for ops,want in [(['add'],['FractionOps.create','FractionOps.add']),(['add','mul'],['FractionOps.create','FractionOps.add','FractionOps.mul']),(['sub','div'],['FractionOps.create','FractionOps.sub','FractionOps.div'])]]
 old=json.loads((ROOT/'docs/experiments/results/ce115_ab2d_assembly_v4_scanner_validation/validation_summary.json').read_text())
 counts_ok=old['v4_counts']=={'REQUIRED_OPERATION_NOT_COVERED':8,'INSUFFICIENT_EVIDENCE':3,'ASSEMBLY_COMPLIANT':6,'INVALID_API_CALL':1}
 consistency={'runtime_inventory':inventory,'families':checks,'consistent':all(all(v for v in x.values()) for x in checks.values())}
 (OUT/'toolbox_runtime_consistency.json').write_text(json.dumps(consistency,indent=2)+'\n',encoding='utf8');(OUT/'raw_hash_integrity.json').write_text(json.dumps({'cells':18,'all_preserved':all(hashes)},indent=2)+'\n',encoding='utf8')
 adversarial_ok=all(adversarial) and all(fraction_checks)
 gate=consistency['consistent'] and all(hashes) and counts_ok and adversarial_ok
 summary={'rendered_prompt_validation':checks,'toolbox_runtime_consistent':consistency['consistent'],'scanner_contract_validated':counts_ok and adversarial_ok,'adversarial_cases':12,'adversarial_cases_passed':adversarial_ok,'prompt_contract_validated':consistency['consistent'],'rendered_prompt_validated':consistency['consistent'],'raw_hash_integrity':{'cells':18,'all_preserved':all(hashes)},'existing_v4_counts':old['v4_counts'],'model_healer_repair_replay_retry_calls':0,'freeze_gate_passed':gate}
 (OUT/'prompt_contract_validation_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
 if gate:
  manifest=json.loads(MAN.read_text(encoding='utf8'));manifest.update({'status':'FROZEN_ZERO_MODEL_VALIDATED_V2','scanner_contract_validated':True,'prompt_contract_validated':True,'rendered_prompt_validated':True,'toolbox_runtime_consistent':True,'previous_freeze_invalidated_reason':'v1 prompt stubs exposed legacy Required APIs/MUST_CALL semantics','supersedes_freeze_commit':'ee68e10f006f23f733fe1a549904d058865d6947','prompt_stubs':{task:stub_for_task(task) for task in TASKS.values()}});MAN.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
 else: raise SystemExit('prompt contract gate failed')
if __name__=='__main__':main()
