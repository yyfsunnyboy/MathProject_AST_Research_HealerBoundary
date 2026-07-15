import json
from pathlib import Path
from scripts.compare_ce115_ab2d_spec_vs_assembly import main

def test_covered_comparison_pairs_all_cells_without_roots():
    main(); p=Path('docs/experiments/results/ce115_ab2d_spec_vs_assembly_comparison.json'); d=json.load(open(p))
    assert d['pairing']['paired']==18 and d['pairing']['missing_pairs']==0
    assert d['pairing']['structural_exclusions']==6
