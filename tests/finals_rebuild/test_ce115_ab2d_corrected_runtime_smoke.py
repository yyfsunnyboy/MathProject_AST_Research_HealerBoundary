from scripts.run_ce115_ab2d_corrected_runtime_smoke import execute
def test_corrected_runtime_namespace_executes_polydiv_wrapper():
 assert execute('def generate(level=1,**kwargs):\n q,r=PolynomialOps.div_qr([1,0,-1],[1,-1]);return {}\n')[0]
