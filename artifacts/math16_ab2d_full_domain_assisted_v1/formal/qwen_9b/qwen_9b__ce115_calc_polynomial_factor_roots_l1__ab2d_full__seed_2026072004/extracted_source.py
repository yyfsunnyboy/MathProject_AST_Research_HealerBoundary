def generate(level=1, **kwargs):
    frozen_params = {
        "quadratic_coefficients": [1, 4, -12]
    }

    # Step 1: Factor the quadratic polynomial exactly.
    # The API expects coefficients for ax^2 + bx + c in that order (highest degree first).
    a, b, c = frozen_params["quadratic_coefficients"]
    
    factors_dict_list = PolynomialOps.factor_quadratic_exact(a, b, c)

    # Step 2: Convert factor dictionaries to roots and sort ascending.
    # Each dict has keys 'x_coefficient' (slope of line x - r => slope is 1 usually for monic) 
    # and 'constant'. The root r = constant / x_coefficient if form is (k*x + m).
    # However, standard factorization output often implies roots directly or via simple division.
    # Let's inspect the example logic: factor_quadratic_exact(1, -5, 6) -> factors for (x-2)(x-3)=0 => roots 2, 3.
    # If input is [a,b,c], output list of dicts { "x_coefficient": k, "constant": m } representing (k*x + m).
    
    raw_roots = []
    for factor in factors_dict_list:
        x_coef = factor["x_coefficient"]
        const_val = factor["constant"]
        
        # Calculate root r such that k*r + m = 0 => r = -m/k
        if isinstance(x_coef, str):
            from fractions import Fraction
            num_str = x_coef.split('/')[1] if '/' in x_coef else "1"
            den_str = x_coef.split('/')[0] if '/' in x_coef else "1"
            # Handle negative sign properly for parsing string fraction manually or assume API handles it? 
            # The example output uses 'p/q'. Let's parse carefully.
            try:
                num, denom = map(int, x_coef.split('/'))
                root_val = Fraction(-const_val * denom, num) if isinstance(const_val, str) else Fraction(-const_val * denom, num)
                # Wait, const_val might be string too? 
                # Let's assume standard parsing: factor is (num/den)*x + const. Root = -const / (num/den).
            except ValueError:
                 root_val = float(x_coef) if '/' not in x_coef else eval(f"-{float(const_val)} / {eval(x_coef)}") 
        elif isinstance(const_val, str):
             # Both are strings or one is. Let's try to evaluate safely.
             from fractions import Fraction as F
             root_val = -F(eval(str(const_val)), eval(str(x_coef))) if '/' in x_coef else float(-const_val / x_coef)
        elif isinstance(x_coef, int):
            # If const_val is string 'p/q' or int
            try:
                c_num, c_den = map(int, str(const_val).split('/')) if '/' in str(const_val) else (int(str(const_val)), 1)
                root_val = Fraction(-c_num * x_coef.denominator if hasattr(x_coef,'denominator') else -const_val / x_coef) # Logic flawed above.
            except:
                 pass
        
        # Robust calculation for roots given factor dict {x_coefficient, constant} representing (k*x + m)
        k = float(x_coef) if '/' not in str(x_coef) and isinstance(x_coef, int|float) else eval(str(x_coef))
        m = float(const_val) if '/' not in str(const_val) and isinstance(const_val, int|float) else eval(str(const_val))
        
        # Root is -m/k. Handle string fractions carefully for exactness before sorting? 
        # Sorting requires numeric comparison. We can use Fraction for precision then convert to float or keep as Fraction if sortable.
        try:
            from fractions import Fraction
            root = Fraction(-int(str(m).split('/')[1]) * int(str(k).split('/')[0]), 1) / k # This is getting messy with string parsing logic in head.
            
            # Simpler approach for the specific API behavior usually seen: 
            # If factor is (x - r), dict might be { "x_coefficient": 1, "constant": -r } -> root = -(-r)/1 = r? No, equation k*x + m = 0.
            # Example: x^2+4x-12 = (x+6)(x-2). Roots are -6, 2.
            # Factors likely returned as { "x_coefficient": 1, "constant": 6 } and { "x_coefficient": 1, "constant": -2 }.
            # Equation: 1*x + 6 = 0 -> x = -6. 
            # Equation: 1*x - 2 = 0 -> x = 2.
            
            if isinstance(x_coef, str):
                k_val = eval(str(x_coef))
            else:
                k_val = float(x_coef)
                
            if isinstance(const_val, str):
                m_val = eval(str(const_val))
            else:
                m_val = float(const_val)
            
            root = Fraction(-m_val * 10**6).limit_denominator() / (k_val/1.0) # Avoiding direct division of floats if possible? 
            # Actually, let's just use Python eval for the fraction string arithmetic safely.
            from fractions import Fraction as F
            try:
                k_f = F(str(x_coef))
                m_f = F(str(const_val))
                root = -m_f / k_f
            except ZeroDivisionError:
                continue
                
        except Exception:
             # Fallback for simple ints/floats if eval fails or strings are not fractions
             try:
                 root = Fraction(-int(m) * 1, int(k)) 
             except:
                 pass

    # Re-evaluating the robust way to get roots from factors without complex string parsing inside loop logic that might break.
    # Let's assume standard float conversion is acceptable for sorting if exact rational arithmetic isn't strictly enforced by sort order of floats (which matches math16 usually). 
    # But 'roots ordered ascending' implies deterministic ordering. Fractions are safer.
    
    roots = []
    for factor in factors_dict_list:
        k_str = str(factor["x_coefficient"])
        m_str = str(factor["constant"])
        
        try:
            from fractions import Fraction as F
            # Parse strings to Fraction safely
            if '/' not in k_str and '.' not in k_str:
                kf = F(int(k_str))
            else:
                kf = eval(f"F('{k_str}')")
                
            if '/' not in m_str and '.' not in m_str:
                mf = F(int(m_str))
            else:
                mf = eval(f"F('{m_str}')")
            
            root_val = -mf / kf
        except Exception as e:
             # If parsing fails, try float fallback (unlikely for this domain)
             k_f = float(k_str.replace('/', '/').replace('p/q', '')) 
             m_f = float(m_str.replace('/',''))
             if '/' in str(factor["x_coefficient"]):
                 parts_k = factor["x_coefficient"].split('/')
                 kf_num, kf_den = int(parts_k[0]), 1 if len(parts_k)==2 else (int(parts_k[-1]) if 'q' not in k_str else 1) # Heuristic fail. 
                 pass
            
            # Let's rely on the fact that eval works for p/q strings usually defined as "p/q"
            try:
                kf = F(eval(k_str))
                mf = F(eval(m_str))
                root_val = -mf / kf
            except:
                continue
        
        roots.append(root_val)

    # Sort ascending. Fractions sort correctly by value.
    roots.sort()

    # Step 3: Assemble correct_answer.
    # Need factorization_latex and roots_latex.
    
    # Construct LaTeX for factors to multiply them? Or just the factored form string? 
    # "factor_quadratic_exact" returns dicts. We need to format these into a product expression.
    # Example output of format_latex expects coeffs list.
    # To get factorization latex, we can reconstruct coefficients from roots or use mul on factors?
    # The domain API doesn't have a direct "format_factors". 
    # However, the question asks to decompose into rational numbers range (factor) and list roots.
    # We need `correct_answer` with keys: roots, factorization_latex, roots_latex.
    
    # Constructing latex for factors manually or via mul?
    # If we have factors like [1*x + 6] and [1*x - 2]. 
    # Can we use PolynomialOps.mul to combine them back into coefficients then format? Yes!
    # But wait, the factorization form is usually (x-r1)(x-r2).
    # Let's create coefficient lists for each linear factor.
    
    factors_latex_parts = []
    coeffs_for_mul = []
    
    for r in roots:
        # We need to reconstruct the integer/rational coefficients of the line corresponding to root r.
        # From original a,b,c and roots, we know sum of roots = -b/a, prod = c/a.
        # But simpler: The factor dict gave us k*x + m. 
        # Let's re-extract from the sorted list? No, dicts are lost after loop unless stored.
        
    # Better approach inside loop to store reconstructed linear coeffs for mul later if needed.
    # Actually, we can just format each root as a string and join with '*'.
    
    factor_latex_parts = []
    roots_floats = [float(r) for r in roots] # For latex formatting
    
    # Re-iterate factors to build LaTeX parts? 
    # We lost the dict list order if not stored. Let's store them before sorting or re-calculate from roots and original a,b,c.
    # Roots are unique. Factors correspond 1-to-1 with roots for monic quadratics (a=1). Here a=1.
    # So factors are (x - r) where r is root. 
    # Wait, factor dict might be { "x_coefficient": k, "constant": m }. For x^2+4x-12=(x+6)(x-2), roots are -6, 2.
    # Factors: (x + 6) -> k=1, m=6. Root = -6/1 = -6. Correct.
    # Factor: (x - 2) -> k=1, m=-2. Root = -(-2)/1 = 2. Correct.
    
    # So for each root r in sorted_roots, the factor is roughly x - r? 
    # If a != 1, we need to scale. Here a=1 always from frozen_params [1,4,-12].
    # So factors are simply (x - r). But wait, if roots were fractions like p/q, then k might be q.
    # Example: x^2 + x/3 = 0 -> x(x+1/3) -> not integer coeffs usually required for "rational range" factorization unless monic is forced? 
    # The API `factor_quadratic_exact` handles the rational scaling internally to ensure exact roots.
    
    # Let's rebuild the LaTeX string from the original factors dicts we had in memory (we need to keep them).
    pass

# Redoing logic cleanly within function scope
    
frozen_params = { "quadratic_coefficients": [1, 4, -12] }
a,b,c = frozen_params["quadratic_coefficients"]

factor_dicts = PolynomialOps.factor_quadratic_exact(a, b, c)

roots_list = []
latex_parts = []

for fd in factor_dicts:
    k_str = str(fd["x_coefficient"])
    m_str = str(fd["constant"])
    
    # Calculate root value for sorting and latex display
    try:
        from fractions import Fraction as F
        kf = eval(k_str) if '/' not in k_str else F(eval(k_str)) 
        mf = eval(m_str) if '/' not in m_str else F(eval(m_str))
        
        # Root r satisfies k*r + m = 0 => r = -m/k
        root_val = -mf / kf
        
        roots_list.append(root_val)
        
        # Build LaTeX for this factor: (k*x + m). 
        # Format: if k=1, "x+m". If k=-1, "-(x-m)". Else "(k x + m)" or similar.
        # Standard Latex formatting logic needed? Or use format_latex on coeffs [k, m]?
        # PolynomialOps.format_latex expects highest degree first list of numbers (ints/floats). 
        # It handles fractions internally if passed as Fraction objects? The doc says "numeric coefficients".
        # If we pass Fractions, it should work.
        
        factor_coeffs = [kf, mf] # Represents k*x + m
        latex_part = PolynomialOps.format_latex(factor_coeffs)
        latex_parts.append(latex_part)
    except Exception:
         # Fallback for simple types if eval fails (unlikely with p/q strings from API?)
         pass

# Sort roots ascending. Since root_val is Fraction, sort works naturally.
roots_list.sort()

# Construct factorization LaTeX string by joining parts with '*'
factor_latex = "*".join(latex_parts)

# Construct roots LaTeX list: "r_1, r_2" or similar? 
# Usually comma separated in a set/list context. The contract says `roots_latex`: str.
# Likely format like "-6, 2" or "\{-6, 2\}". Given the example stem uses standard math notation.
# Let's assume simple text representation of roots sorted: "r1, r2". 
# Or maybe a set? The prompt says "list two distinct real roots". 
# Common format in these tasks for `roots_latex` is comma separated values like "-6, 2".

from fractions import Fraction as F
def frac_to_str(f):
    if isinstance(f, str): return f # Should not happen after eval?
    try:
        n = int(str(f).split('/')[0])
        d = int(str(f).split('/')[1]) if '/' in str(f) else 1
        sgn = "-" if float(f) < 0 and (n>0 or d<0) else "" # Sign handling for Fraction string is tricky. 
        # Easier: use f.numerator, f.denominator? No, F object doesn't expose directly like that in all versions without .numerator attr check.
        return str(f).replace(' ', '')
    except:
        return str(float(f))

roots_latex_str = ", ".join([frac_to_str(r) for r in roots_list])

# Oracle payload must be exactly frozen_params provided in task block? 
# "oracle_payload: must exactly equal the frozen_params object provided in the task block."
# The task block provides: { "quadratic_coefficients": [1, 4, -12] }
# But wait, the example code shows `frozen` dict. We should use that structure.

return {
    "question_text": r"將一元二次方程式 $x^2+4x-12=0$ 的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。",
    "correct_answer": {
        "roots": [float(r) for r in roots_list], # Contract says list, usually floats or ints. Fractions might be safer but JSON safe? 
           # Wait, contract: `roots`: list. Type not specified strictly as int/str/fraction in snippet, but example uses numbers.
           # Let's use float if exact integer, else fraction string? Or keep Fraction objects which serialize to dict-like or str?
           # Usually Math16 answers expect numeric types (int/float) for roots unless symbolic. 
           # Given "rational range", maybe strings like "-6" and "2"? 
           # Let's check `roots` type in example contract: just `list`. I will provide list of floats or ints if exact.
        , "factorization_latex": factor_latex,
        "roots_latex": roots_latex_str
    },
    "oracle_payload": frozen_params
}