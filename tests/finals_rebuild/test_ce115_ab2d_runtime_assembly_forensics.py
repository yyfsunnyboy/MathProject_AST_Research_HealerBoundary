from scripts.forensics_ce115_ab2d_runtime_assembly import isolated, smoke_sources

def test_synthetic_wrappers_execute_through_canonical_runtime_loader():
    for source in smoke_sources().values():
        assert isolated(source)[0]=='EXECUTED'
