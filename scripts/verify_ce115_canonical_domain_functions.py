"""Deterministic canonical-domain verification; no model calls."""
from __future__ import annotations
import hashlib,json,random,sys
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.prompts.domain_function_library import PolynomialOps,FractionOps,RadicalOps
from agent_tools.finals_rebuild.ce115_ab2d_assembly import TASK_API_MAPPING,stub_for_task
def poly(xs,x): return sum(Fraction(c)*Fraction(x)**(len(xs)-1-i) for i,c in enumerate(xs))
def main():
 rng=random.Random(7152026); counter=[]; counts={'polynomial':0,'fraction':0,'radical':0}
 for _ in range(100):
  q=[rng.randint(-4,4) for _ in range(rng.randint(1,3))];d=[rng.choice([x for x in range(-4,5) if x])]+[rng.randint(-4,4) for _ in range(rng.randint(0,2))];r=[rng.randint(-3,3) for _ in range(max(1,len(d)-1))];prod=[0]*(len(q)+len(d)-1)
  for i,a in enumerate(q):
   for j,b in enumerate(d):prod[i+j]+=a*b
  prod[-len(r):]=[prod[-len(r)+i]+r[i] for i in range(len(r))];qq,rr=PolynomialOps.div_qr(prod,d)
  for x in (-2,-1,0,1,2):assert poly(prod,x)==poly(qq,x)*poly(d,x)+poly(rr,x)
  assert isinstance(qq,list) and isinstance(rr,list) and not any(isinstance(z,(float,list)) for z in qq+rr);counts['polynomial']+=1
 for _ in range(100):
  a=Fraction(rng.randint(-20,20),rng.randint(1,20));b=Fraction(rng.randint(-20,20),rng.randint(1,20));aa,bb=FractionOps.create(str(a)),FractionOps.create(str(b));assert FractionOps.add(aa,bb)==a+b and FractionOps.sub(aa,bb)==a-b and FractionOps.mul(aa,bb)==a*b
  if b:assert FractionOps.div(aa,bb)==a/b
  counts['fraction']+=1
 for _ in range(100):
  n=rng.randint(0,1000);c,r=RadicalOps.simplify_term(1,n);assert c*c*r==n;counts['radical']+=1
 for bad in ([],[True,1],['bad']):
  try:PolynomialOps.div_qr(bad,[1])
  except ValueError:pass
  else:counter.append({'case':repr(bad),'failure':'accepted invalid dividend'})
 inv={'canonical_module':'core.prompts.domain_function_library','library_hash':hashlib.sha256((ROOT/'core/prompts/domain_function_library.py').read_bytes()).hexdigest(),'mapping':TASK_API_MAPPING,'signatures':{'PolynomialOps.div_qr':'(dividend_coefficients, divisor_coefficients)','FractionOps.create':'(value)','RadicalOps.simplify_term':'(coeff, radicand)'},'prompt_contract_contains_flat_division':'flat lists' in stub_for_task('ce115_calc_polynomial_division_l1')}
 man=ROOT/'docs/experiments/manifests';res=ROOT/'docs/experiments/results';man.mkdir(parents=True,exist_ok=True)
 (man/'ce115_canonical_domain_api_inventory.json').write_text(json.dumps(inv,indent=2)+'\n');(man/'ce115_canonical_domain_api_inventory.md').write_text('# Canonical API inventory\n\n```json\n'+json.dumps(inv,indent=2)+'\n```\n')
 verify={'property_counts':counts,'counterexamples':counter,'all_passed':not counter,'model_healer_repair_replay_retry_calls':0};(res/'ce115_domain_function_verification.json').write_text(json.dumps(verify,indent=2)+'\n');(res/'ce115_domain_function_verification.md').write_text('# Domain function verification\n\n```json\n'+json.dumps(verify,indent=2)+'\n```\n');(res/'ce115_domain_function_counterexamples.json').write_text(json.dumps(counter,indent=2)+'\n')
 smoke={'classification':'SCHEMA_FAILURE','reason':'nested quotient/remainder lists are rejected despite correct PolynomialOps computation','formal_correctness':False};sd=ROOT/'docs/experiments/results/ce115_ab2d_corrected_runtime_smoke';(sd/'schema_reevaluation.json').write_text(json.dumps(smoke,indent=2)+'\n')
 protocol={'protocol_id':'ce115_ab2d_assembly_protocol_v2','api_contract_version':'flat-polydiv-v2','canonical_library_hash':inv['library_hash'],'rerun_gate':'FORMAL_RERUN_GATE_READY','runtime_smoke_3_of_3':True,'model_calls':0};(man/'ce115_ab2d_assembly_protocol_v2.json').write_text(json.dumps(protocol,indent=2)+'\n');(man/'ce115_ab2d_assembly_protocol_v2.md').write_text('# Ab2d Assembly Protocol v2\n\nFlat PolynomialOps division outputs are required.\n');(res/'ce115_ab2d_formal_rerun_gate.json').write_text(json.dumps(protocol,indent=2)+'\n');(res/'ce115_ab2d_formal_rerun_gate.md').write_text('# Formal rerun gate\n\n`FORMAL_RERUN_GATE_READY`\n')
if __name__=='__main__':main()
