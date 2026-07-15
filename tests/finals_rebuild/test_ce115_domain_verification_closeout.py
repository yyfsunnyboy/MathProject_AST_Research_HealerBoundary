import json
from pathlib import Path
from scripts.build_ce115_ab2d_formal_rerun_gate import main
def test_closeout_gate_requires_200_cases_and_no_blockers():
    main()
    d=json.load(open(Path('docs/experiments/results/ce115_ab2d_formal_rerun_gate.json')))
    assert d['verdict']=='FORMAL_RERUN_GATE_READY'
    assert d['checks']['property_200_each'] and d['checks']['synthetic_3_of_3']
