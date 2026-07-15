import json
from pathlib import Path
from scripts.preflight_ce115_ab2d_protocol_v3 import main
def test_v3_preflight_freezes_exactly_18_covered_cells():
    main()
    d=json.load(open(Path('docs/experiments/results/ce115_ab2d_protocol_v3_preflight.json')))
    assert d['verdict']=='FORMAL_RERUN_PREFLIGHT_READY'
    assert d['planned_cells']==18 and d['roots_exclusions']==6
