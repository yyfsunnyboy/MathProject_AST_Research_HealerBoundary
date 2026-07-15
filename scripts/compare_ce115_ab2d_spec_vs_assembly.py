"""Derived, no-call paired comparison of Ab2d-Spec and Ab2d-Assembly covered cells."""
from __future__ import annotations
import csv, json, statistics
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=ROOT/'docs/experiments/results/ce115_corrected_context_formal_run/cells'
ASM=ROOT/'docs/experiments/results/ce115_ab2d_assembly_covered_formal_run'
OUT=ROOT/'docs/experiments/results'
COVERED={'ce115_calc_radical_simplification_l1','ce115_calc_polynomial_division_l1','ce115_calc_exact_rational_expression_l1'}
def key(r): return (r['model'],r['task'],r['seed'])
def load_spec(): return [json.load(open(p,encoding='utf8')) for p in SPEC.glob('*__ab2d__*.jsonl') if json.load(open(p,encoding='utf8'))['task'] in COVERED]
def load_asm(): return [json.load(open(p,encoding='utf8')) for p in ASM.glob('qwen*.json')]
def median(xs): return statistics.median(xs) if xs else None
def main():
    specs=load_spec(); assemblies=load_asm(); sm={key(r):r for r in specs}; am={key(r):r for r in assemblies}
    if len(specs)!=18 or len(assemblies)!=18 or set(sm)!=set(am): raise RuntimeError('paired coverage mismatch')
    forensic=json.load(open(ASM/'runtime_assembly_forensics.json',encoding='utf8')); fm={x['cell_id']:x for x in forensic['cells']}
    rows=[]
    for k in sorted(sm):
        s,a=sm[k],am[k]; f=fm[a['cell_id']]
        spec_pass=None # corrected artifacts record completion/validity, not semantic evaluator outcome
        assembly_pass=a.get('evaluator_outcome')=='passed'
        rows.append({'model':k[0],'task':k[1],'seed':k[2],'spec_cell_id':s['cell_id'],'assembly_cell_id':a['cell_id'],'spec_completion':s['validity_classification'],'assembly_completion':a['completion_classification'],'spec_evaluator_status':'NOT_COMPARABLE_NO_SEMANTIC_EVALUATOR_RECORD','assembly_evaluator_status':f['evaluator_status_after'],'spec_pass':'NOT_COMPARABLE','assembly_pass':assembly_pass,'assembly_executable':f['evaluator_status_after']=='EXECUTED','required_api_exposed':True,'required_api_called':f['required_api_called'],'assembly_classification':f['assembly_after'],'runtime_system_defect_after_fix':False,'assembly_raw_hash':a['raw_output_hash'],'assembly_offline_provenance':'runtime_assembly_forensics.json','spec_output_tokens':s['eval_count'],'assembly_output_tokens':a['token_telemetry'].get('eval_count'),'spec_output_chars':s['output_character_count'],'assembly_output_chars':len(a['raw_output']),'spec_wall_seconds':s['wall_clock_seconds'],'assembly_wall_seconds':a['wall_clock_seconds']})
    fields=list(rows[0]);
    with open(OUT/'ce115_ab2d_spec_vs_assembly_paired_cells.csv','w',newline='',encoding='utf8') as fh:
        w=csv.DictWriter(fh,fieldnames=fields);w.writeheader();w.writerows(rows)
    ac=Counter(r['assembly_classification'] for r in rows); trans={'NOT_COMPARABLE_SPEC_PASS_TO_ASSEMBLY_PASS':sum(r['assembly_pass'] for r in rows),'NOT_COMPARABLE_SPEC_PASS_TO_ASSEMBLY_FAIL':sum(not r['assembly_pass'] for r in rows)}
    telemetry={}
    for name in ('output_tokens','output_chars','wall_seconds'):
        telemetry[name]={'spec_total':sum(r['spec_'+name] or 0 for r in rows),'assembly_total':sum(r['assembly_'+name] or 0 for r in rows),'spec_median':median([r['spec_'+name] for r in rows if r['spec_'+name] is not None]),'assembly_median':median([r['assembly_'+name] for r in rows if r['assembly_'+name] is not None]),'note':'WALL_CLOCK_NOT_DIRECTLY_COMPARABLE' if name=='wall_seconds' else 'different evaluator/runtime conditions'}
    result={'pairing':{'spec_cells':18,'assembly_cells':18,'paired':18,'duplicates':0,'missing_pairs':0,'covered_tasks':sorted(COVERED),'structural_exclusions':6,'exclusion_reason':'STRUCTURAL_EXCLUSION_ASSEMBLY_COVERAGE_UNAVAILABLE'},'spec_outcomes':{'natural_complete':sum(r['spec_completion']=='NATURAL_COMPLETE' for r in rows),'semantic_pass':'NOT_COMPARABLE'},'assembly_outcomes':{'passed':sum(r['assembly_pass'] for r in rows),'executable_after_fix':sum(r['assembly_executable'] for r in rows),'assembly_classifications':dict(ac),'api_exposure_rate':'18/18','api_call_rate':f"{sum(r['required_api_called'] for r in rows)}/18"},'paired_transitions':trans,'telemetry':telemetry,'model_task_summary':[{ 'model':m,'task':t,'cells':sum(r['model']==m and r['task']==t for r in rows),'assembly_compliant':sum(r['model']==m and r['task']==t and r['assembly_classification']=='ASSEMBLY_COMPLIANT' for r in rows)} for m in sorted({r['model'] for r in rows}) for t in sorted(COVERED)],'main_verdict':'ASSEMBLY_REDUCED_CORE_REIMPLEMENTATION_BUT_INTRODUCED_API_USE_FAILURES','rerun_needed':False,'ab2d_spec_remains_formal':False,'ab2d_assembly_becomes_formal':False,'proceed_to_5b8_ab3':True,'model_healer_repair_replay_retry_calls':0,'methods':'Paired by model, task, and seed; no raw artifact or generation changed.','results':'Assembly compliance is measurable after offline runtime repair, while Spec lacks comparable semantic evaluator records.','interpretation':'API exposure did not guarantee valid API use.','limitation':'Pass-rate transitions are not comparable because the Spec artifacts do not contain matching semantic evaluator outcomes.'}
    (OUT/'ce115_ab2d_spec_vs_assembly_comparison.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'ce115_ab2d_spec_vs_assembly_comparison.md').write_text('# Ab2d-Spec vs Ab2d-Assembly covered-subset comparison\n\n```json\n'+json.dumps(result,indent=2)+'\n```\n')
if __name__=='__main__':main()
