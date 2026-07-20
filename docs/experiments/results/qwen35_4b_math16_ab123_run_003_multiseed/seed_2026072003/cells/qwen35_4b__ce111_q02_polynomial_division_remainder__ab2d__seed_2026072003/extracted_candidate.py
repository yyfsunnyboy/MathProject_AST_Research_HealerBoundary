def generate(level=1, **kwargs):
    from importlib.resources import files
    
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    try:
        domain_lib = __import__("core.prompts.domain_function_library", fromlist=["PolynomialOps"])
        PolynomialOps = getattr(domain_lib, "PolynomialOps")
        
        quotient_coeffs, remainder_coeffs = PolynomialOps.div_qr(dividend_coefficients, divisor_coefficients)
        latex_quotient = PolynomialOps.format_latex(quotient_coeffs) if isinstance(quotient_coeffs[0], (int, str)) else ""
    except Exception:
        # Fallback for environments without the specific module structure but with standard math capabilities
        import sympy as sp
        
        dividend_poly = sum(c * sp.Symbol('x')**i for i, c in enumerate(dividend_coefficients) if c != 0)
        divisor_poly = sum(c * sp.Symbol('x')**i for i, c in enumerate(divisor_coefficients) if c != 0)
        
        try:
            q, r = divmod(sp.Poly(dividend_poly), sp.Poly(divisor_poly))
            quotient_coeffs = [int(coeff.evalf()) for coeff in q.all_coeffs()] + [0] * (len(quotient_coeffs)-1-len(q.degree())) if len(quotient_coeffs) > 0 else [] # Normalize to match input length style roughly, but standard is degree+1. Let's stick to raw coeffs from sp.Poly
            remainder_coeffs = r.all_coefficients() + [0]*(len(divisor_poly)-r.degree()-1) if not isinstance(r.all_coefficients(), list) or len([c for c in (r.all_coefficients())]) == 0 else r.all_coefficients() # Re-evaluating: sp.Poly returns degree n poly with n+1 coeffs.
            
            q = sp.Poly(q, 'x')
            rem_poly = sp.Poly(r, 'x')
            quotient_coeffs_list = [int(c) for c in list(q.coeffs())] + ([0]*(len(divisor_coefficients)-q.degree()-1)) if len(quotient_coeffs_list)<3 else quotient_coeffs_list # Align to divisor degree? No, just return what the library would.
            
            # Re-implementation strictly using sympy's Poly structure which is standard for polynomial division in Python without external libs sometimes being missing
            dividend = sp.Poly([6,4,0], 'x')
            divisor = sp.Poly([2,0,0], 'x')
            q, r_poly = divmod(dividend, divisor)
            
            quotient_coeffs_list = list(q.all_coefficients()) # This returns coefficients in order of descending degree. Input was [6,4,0] (deg 2). Output should be deg 1 -> [3]. 
            remainder_coeffs_list = list(r_poly.all_coefficients()) # Deg -inf or empty? Remainder is constant 0 here because divisor divides exactly?
            
            # Let's re-calculate manually to ensure correctness since sympy might vary in output format of all_coefficients vs coeffs
            dividend_val = lambda x: 6*x**2 + 4*x + 0
            divisor_val = lambda x: 2*x^2
            
            quotient_coeffs_list = [3] # (6x^2+4x)/2x^2 -> wait, remainder is not zero. 
            # Manual division of 6x^2+4x by 2x^2?
            # Actually divisor is 2*0*x + 1*x^2 ? No [2,0,0] means coeff x^2=2, x^1=0, x^0=0. So 2x^2.
            # Dividend: 6x^2+4x. 
            # (6x^2)/2x^2 = 3. Remainder = 4x - 0*? No remainder is 4x + constant? 
            # Wait, polynomial division requires same degree terms to cancel highest term first.
            # Dividend: 6x^2+4x. Divisor: 2x^2.
            # Quotient coeff for x^2: 3. New dividend = (6x^2+4x) - 3*(2x^2) = 0 + 4x + 0? No, remainder is just 4x.
            
            quotient_coeffs_list = [3] 
            remainder_coeffs_list = [4] # Remainder polynomial: 4*x
            
        except Exception as e:
            raise RuntimeError(f"Polynomial division failed: {e}")

    correct_answer_str = f"The remainder of the polynomial division is $\{latex_quotient}$. The canonical LaTeX for the quotient (not scored) would be ${latex_quotient}$." if latex_quotient else "The remainder of the polynomial division is $4x$."
    
    # Correct answer format based on task spec: include only remainder and canonical_latex. 
    # If we assume standard math16 context, it expects LaTeX for remainder.
    remainder_str = "$$" + str(remainder_coeffs_list[0]) if len(remainder_coeffs_list) > 0 else "0"
    
    correct_answer_dict = {
        "question_text": r"\text{Find the polynomial division of } [6x^2+4x] \text{ by } [2x^2].",
        "correct_answer": f"The remainder is ${remainder_str}$.",
        "oracle_payload": {"dividend_coefficients": dividend_coefficients, "divisor_coefficients": divisor_coefficients}
    }

    return correct_answer_dict