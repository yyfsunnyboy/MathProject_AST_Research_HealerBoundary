from scripts.run_ce115_ab2d_assembly_v3_formal import runtime
def test_v3_runner_runtime_loader_executes_wrapper():
 assert runtime('def generate(level=1,**kwargs):\n q,r=PolynomialOps.div_qr([1,0,-1],[1,-1]);return {}\n')[0]
