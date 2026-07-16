"""Offline v4 toolbox readjudication of immutable v3 raw outputs; no calls."""
from __future__ import annotations
import csv,hashlib,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent_tools.finals_rebuild.ce115_ab2d_assembly import scan_toolbox,stub_for_task
SRC=ROOT/'docs/experiments/results/ce115_ab2d_assembly_v3_corrected_formal_run';OUT=ROOT/'docs/experiments/results/ce115_ab2d_assembly_v3_toolbox_readjudication';MAN=ROOT/'docs/experiments/manifests'
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def main():
 OUT.mkdir(parents=True,exist_ok=True);rows=[]
 for p in sorted(SRC.glob('qwen*.json')):
  r=json.load(open(p));scan=scan_toolbox(r['extracted_code'],r['task']);o=r['assembly_classification'];n=scan['classification'];reason='FALSE_FAILURE_UNUSED_TOOLBOX_API' if o=='REQUIRED_API_NOT_CALLED' and n=='ASSEMBLY_COMPLIANT' else ('REQUIRED_OPERATION_NOT_COVERED' if o=='REQUIRED_API_NOT_CALLED' else 'UNCHANGED')
  rows.append({'cell_id':r['cell_id'],'model':r['model'],'task':r['task'],'seed':r['seed'],'original_assembly_classification':o,'task_required_operations':scan.get('task_required_operations',[]),'actual_called_apis':scan.get('called_apis',[]),'domain_library_adoption':scan.get('domain_library_adopted'),'new_assembly_classification':n,'evaluator_classification_unchanged':r['final_taxonomy'],'correctness_unchanged':r['passed'],'classification_changed':o!=n,'change_reason':reason,'raw_output_hash':r['raw_output_hash'],'raw_hash_preserved':sha(r['raw_output'])==r['raw_output_hash']})
 if len(rows)!=18 or not all(x['raw_hash_preserved'] for x in rows):raise RuntimeError('raw hash integrity failure')
 with open(OUT/'cells.jsonl','w',encoding='utf8') as f:
  for x in rows:f.write(json.dumps(x)+'\n')
 with open(OUT/'classification_transitions.csv','w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 summary={'original_counts':dict(Counter(x['original_assembly_classification'] for x in rows)),'readjudicated_counts':dict(Counter(x['new_assembly_classification'] for x in rows)),'transitions':{f'{a}->{b}':c for (a,b),c in Counter((x['original_assembly_classification'],x['new_assembly_classification']) for x in rows).items()},'missing_api_dispositions':dict(Counter(x['change_reason'] for x in rows if x['original_assembly_classification']=='REQUIRED_API_NOT_CALLED')),'correctness_unchanged':True,'model_healer_repair_replay_retry_calls':0,'verdict':'TOOLBOX_CONTRACT_REPAIRED_OFFLINE_READJUDICATION_COMPLETE'}
 (OUT/'readjudication_summary.json').write_text(json.dumps(summary,indent=2)+'\n');(OUT/'readjudication_summary.md').write_text('# V3 toolbox readjudication\n\n```json\n'+json.dumps(summary,indent=2)+'\n```\n');(OUT/'raw_hash_integrity.json').write_text(json.dumps({'cells':18,'all_preserved':True},indent=2)+'\n');(OUT/'defect_audit.json').write_text(json.dumps({'ACTIVE_CONTRACT_DEFECT':['v3 MUST_CALL every declared API'],'ACTIVE_SCANNER_DEFECT':['v3 scanner lacked task resolver']},indent=2)+'\n')
 protocol={'protocol_id':'ce115_ab2d_assembly_protocol_v4','condition':'ab2d_toolbox_v4','status':'DRAFT_OFFLINE_VALIDATED','semantics':'full toolbox exposed; only task-relevant operations required; optional APIs never required','prompt_stubs':{t:stub_for_task(t) for t in sorted({x['task'] for x in rows})}};(MAN/'ce115_ab2d_assembly_protocol_v4.json').write_text(json.dumps(protocol,indent=2)+'\n');(MAN/'ce115_ab2d_assembly_protocol_v4.md').write_text('# Ab2d toolbox protocol v4\n\nDRAFT_OFFLINE_VALIDATED; not frozen.\n')
if __name__=='__main__':main()
