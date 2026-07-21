from fractions import Fraction as F
import sys
sys.path.insert(0, 'core')
from prompts.domain_function_library import PolynomialOps, FractionOps

def generate(level=1, **kwargs):
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    a, b, c = frozen_params["quadratic_coefficients"]
    
    # Factorization using domain API
    factor_result = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    x_coeffs_list = []
    constants_list = []
    for item in factor_result:
        coeff_val = str(item['x_coefficient']) if isinstance(item['x_coefficient'], F) else int(item['x_coefficient'])
        const_val = str(item['constant']) if isinstance(item['constant'], F) else int(item['constant'])
        
        # Construct fraction string for exact representation (e.g., "1/3") or integer
        def to_fraction_str(val):
            if isinstance(val, F):
                return f"{val.numerator}/{val.denominator}"
            elif val == 0:
                return "0"
            else:
                # Ensure positive denominator and handle negative numerators correctly for display
                sign = "-" if val < 0 else ""
                abs_val = -val if val < 0 else val
                num, den = divmod(abs_val, 1)
                if den == 1:
                    return str(int(val))
                elif int(num) > 0 and den != 1: # Mixed number logic simplified for exact fraction output requirement usually implies improper or mixed form based on context. 
                    # Given the constraint "int or 'p/q'", we stick to p/q if not integer, but standard math notation prefers integers when possible.
                    # However, factor_quadratic_exact returns coefficients of factors like (x + r).
                    pass
                
                return f"{val.numerator}/{val.denominator}"

        x_coeffs_list.append(to_fraction_str(coeff_val))
        constants_list.append(to_fraction_str(const_val))
    
    roots = []
    for i in range(len(factor_result)):
        # Roots are -constant / coefficient of x (since factor is ax + b => root = -b/a)
        if isinstance(factor_result[i]['x_coefficient'], F):
            num = int(-factor_result[i]['constant'].numerator * factor_result[i]['x_coefficient'].denominator)
            den = abs(factor_result[i]['x_coefficient'].numerator * factor_result[i]['constant'].denominator) # Handle signs carefully for root calculation: -b/a
            
            # Correct logic: Root r satisfies a*x + b = 0 => x = -b/a
            neg_b_num = -factor_result[i]['constant'].numerator if isinstance(factor_result[i]['constant'], F) else (-1 * factor_result[i]['constant'])
            
            num_root = int(neg_b_num * factor_result[i]['x_coefficient'].denominator)
            den_root = abs(factor_result[i]['x_coefficient'].numerator * (factor_result[i]['constant'].denominator if isinstance(factor_result[i]['constant'], F) else 1)) # Simplified for integer case
            
            # Re-evaluating root calculation precisely with Fractions
            x_c = factor_result[i]['x_coefficient']
            const_val = factor_result[i]['constant']
            
            if not (isinstance(x_c, int) and isinstance(const_val, int)):
                r_num = -const_val.numerator * x_c.denominator
                r_den = abs(x_c.numerator * const_val.denominator) # Ensure positive denominator for canonical form usually, but let's stick to exact arithmetic representation.
            else:
                if x_c < 0 and const_val > 0:
                    num_root = -const_val / (-x_c)
                elif x_c > 0 and const_val < 0:
                    num_root = -const_val / x_c
                else: # signs match, root is positive or zero? No. ax+b=0 -> x=-b/a. If a,b same sign, result negative.
                     r_num = -(x_c * const_val) if isinstance(const_val, int) and isinstance(x_c, int) else -const_val / x_c
            
            # Let's recalculate roots directly from the factors (ax+b)(cx+d). Roots are -b/a and -d/c.
            root1 = F(-factor_result[0]['constant']) / factor_result[0]['x_coefficient'] if isinstance(factor_result[0]['x_coefficient'], F) else (-factor_result[0]['constant']) // factor_result[0]['x_coefficient'] # Integer division might fail for fractions, use float logic then convert? No, exact arithmetic.
            
            # Robust root calculation: -b/a where a is x-coeff of first term in (ax+b), b is constant part.
            def get_root(factor):
                if isinstance(factor['x_coefficient'], F) and isinstance(factor['constant'], F):
                    return -(factor['constant']) / factor['x_coefficient']
                elif not isinstance(factor['x_coefficient'], F) or not isinstance(factor['constant'], F): # Mixed case unlikely in exact integer factors but handle safely
                     if isinstance(factor['x_coefficient'], int) and isinstance(factor['constant'], (int, str)):
                         val = -factor['constant'] / factor['x_coefficient']
                         return val
                else:
                    pass
            
            r1 = get_root(factor_result[0])
            r2 = get_root(factor_result[1])
            
            roots.append(r1)
            roots.append(r2)

    # Sort ascending (exact comparison for Fractions or ints)
    if all(isinstance(x, F) for x in roots):
        sorted_roots = sorted(roots)
    else:
        mixed_ints_fractions = []
        for r in roots:
            try:
                float_r = float(r)
                # Convert back to Fraction or int for sorting stability if needed, but F supports comparison.
                # If some are ints and some Fractions, convert all to Fraction? 
                # Actually, the problem guarantees exact arithmetic. Roots of integer polynomials with rational coeffs might be fractional.
                # Let's assume roots can be mixed types (int or Fraction).
                if isinstance(r, F):
                    float_r = r.numerator / r.denominator
                else:
                    float_r = int(r)
                
                # Reconstruct comparable object? 
                # Simpler approach: convert all to Fraction for sorting then back.
                pass
            
            except Exception as e:
                print(e, file=sys.stderr)
        
        sorted_roots = []
        for r in roots:
            if isinstance(r, F):
                f_r = r
            else:
                # If it's an int or string representation of a number that isn't Fraction? 
                # The domain API returns Fractions. So all should be Fractions unless the input was integer and result is integer (which is also a subclass in some libs, but here F).
                f_r = r if isinstance(r, F) else F(int(r))
            sorted_roots.append(f_r)
        sorted_roots.sort()

    # Construct LaTeX strings for roots ascending
    def to_latex_root(root):
        if root == 0: return "0"
        num = str(abs(root.numerator)) if isinstance(root, F) else abs(int(root))
        den = str(abs(root.denominator)) if isinstance(root, F) else "" # Denom is always 1 for int
        
        sign = "-" if (isinstance(root, F) and root < 0) or (not isinstance(root, F) and int(root) < 0) else "+"
        
        if den == "": return f"{num}"
        elif num % den != 0: # Mixed number logic? Usually LaTeX uses improper fraction for exactness unless specified. 
            # Standard math16 format often prefers mixed numbers or simple fractions. Let's use proper fraction form a/b with sign prefix.
            if isinstance(root, F):
                return f"{sign}{num}/{den}"
        else:
             val = int(num) // den
             rem = num % den
             if rem == 0: return str(val * (1 if not root < 0 or len(str(root))>2 and 'F' in str(type(root))) else -1) # This logic is getting messy. 
             # Let's rely on the fact that roots of integer polynomials are either integers or simple fractions p/q where q divides leading coeff? Not necessarily for general quadratics with rational coeffs, but here input is int.
             pass
        
        return f"{sign}{num}/{den}" if den != "" else str(int(root))

    # Re-implementing root formatting cleanly based on Fraction properties
    roots_latex = []
    factorization_latex_parts = ["("]
    
    for i, fr in enumerate(factor_result):
        x_c_str = to_fraction_str(fr['x_coefficient']) if isinstance(fr['x_coefficient'], F) else str(int(fr['x_coefficient']))
        const_str = to_fraction_str(fr['constant']) if isinstance(fr['constant'], F) else str(int(fr['constant']))
        
        # Factor form: (ax + b). If a is negative, we might want positive leading term? 
        # Standard factorization usually keeps integer coefficients. 
        # e.g., x^2 - 4 = (x-2)(x+2). Here coeffs are [1,0,-4].
        # Our input: [1, 4, -12] -> (x+6)(x-2) or (-x-6)(x+2)? 
        # factor_quadratic_exact returns factors such that product is original.
        
        if isinstance(fr['x_coefficient'], F):
            x_c_str = f"{fr['x_coefficient'].numerator}/{fr['x_coefficient'].denominator}"
            const_str = f"{fr['constant'].numerator}/{fr['constant'].denominator}"
            
            # Determine sign for mixed number display if denominator > 1 and numerator divisible? 
            # Let's stick to improper fraction or integer. The prompt says "int or 'p/q'".
            pass
        
        factorization_latex_parts.append(f"{x_c_str}+{const_str}")
        
    roots_latex = [to_latex_root(r) for r in sorted_roots]

    # Finalize correct_answer structure
    correct_answer = {
        "roots": [str(int(r)) if isinstance(r, F) and r.denominator == 1 else f"{r.numerator}/{r.denominator}" for r in sorted_roots], 
        "factorization_latex": "".join(factorization_latex_parts), # Simplified join logic assuming standard form
        "roots_latex": ",".join(roots_latex)
    }

    question_text = r"\text{Factor the polynomial with coefficients $1, 4, -12$ into linear factors and find its roots."}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }