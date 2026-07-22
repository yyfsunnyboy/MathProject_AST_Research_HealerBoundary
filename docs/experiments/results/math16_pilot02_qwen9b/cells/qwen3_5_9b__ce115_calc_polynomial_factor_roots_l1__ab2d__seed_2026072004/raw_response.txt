from fractions import Fraction
import json

def generate(level=1, **kwargs):
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    # Import domain functions (simulating the environment where these are available)
    try:
        from core.prompts.domain_function_library import PolynomialOps, FractionOps
    except ImportError:
        # Fallback implementation if imports fail in this isolated context to ensure code runs
        class FakeFractionOps:
            @staticmethod
            def create(value):
                return value
        
        class FakePolynomialOps:
            @staticmethod
            def factor_quadratic_exact(a, b, c):
                # Solve ax^2 + bx + c = 0 exactly using fractions
                if a == 0:
                    raise ValueError("Not quadratic")
                
                discriminant_num = (b * b) - (4 * a * c)
                sqrt_discriminant = Fraction(discriminant_num).sqrt() # This might fail for non-squares in pure math, but problem implies solvable
                
                if not isinstance(sqrt_discriminant, int):
                    raise ValueError("Discriminant must be perfect square")

                x1_numerator = -b + sqrt_discriminant
                x2_numerator = -b - sqrt_discriminant
                
                # Simplify fractions for roots
                root1 = Fraction(x1_numerator).limit_denominator() if isinstance(sqrt_discriminant, int) else None 
                
                # Re-calculate strictly with integers since discriminant is perfect square
                d_int = (b * b) - (4 * a * c)
                import math
                sqrt_d = int(math.isqrt(d_int))
                
                root1_num = (-b + sqrt_d) // 2 if ((-b + sqrt_d) % 2 == 0 or False) else None # Simplification logic for ax^2+bx+c
                
                # Standard formula: x = (-b +/- sqrt(D)) / (2a)
                denom = 2 * a
                root1_num_val = -b + sqrt_d
                root2_num_val = -b - sqrt_d
                
                if root1_num_val % denom == 0:
                    r1 = Fraction(root1_num_val, denom).limit_denominator() # Ensure simplified
                else:
                     # It might not divide evenly by 2a directly in integer arithmetic without GCD reduction inside Fraction constructor logic implicitly handled? 
                     # Actually Fraction handles simplification automatically.
                    pass
                
                root1 = Fraction(-b + sqrt_d, denom)
                root2 = Fraction(-b - sqrt_d, denom)
                
                # Sort ascending
                if root1 > root2:
                    roots_sorted = [root2, root1]
                else:
                    roots_sorted = [root1, root2]

                return [{ "x_coefficient": root1 }, { "x_coefficient": root2 }]

    try_again_flag = False
    
    # Re-implement logic cleanly without external dependency assumption for the final output block if needed, 
    # but instructions say to use domain APIs. I will assume they exist in the target environment or provide a robust fallback that mimics them exactly as requested (returning dicts).
    
    # Since I cannot guarantee `core.prompts.domain_function_library` exists in this text-only generation without an actual runtime env, 
    # and the prompt says "Output complete Python source only", I must write code that *would* use it.
    # However, to ensure the script is valid Python here, I will define stubs or assume they are injected.
    # Given the strict constraint "Use the listed domain API", I will structure the call assuming availability.
    
    a, b, c = frozen_params["quadratic_coefficients"]

    try:
        from core.prompts.domain_function_library import PolynomialOps, FractionOps
        
        factor_result_list = PolynomialOps.factor_quadratic_exact(a, b, c)
        
        # The API returns list[dict] with keys x_coefficient. 
        # We need to construct the answer dict.
        root1_val = factor_result_list[0]["x_coefficient"]
        root2_val = factor_result_list[1]["x_coefficient"]
        
        sorted_roots_asc = [root1_val, root2_val] if root1_val <= root2_val else [root2_val, root1_val]
        
        # Construct LaTeX strings manually for exact arithmetic requirement (no floats)
        def frac_to_latex(frac):
            num = str(numerator(frac))
            den = str(denominator(frac))
            if int(num) == 0: return "0"
            sign = "-" if numerator(frac) < 0 else "" # Fraction handles negative denominator usually, but let's be safe. 
            # Actually standard latex for fraction is \frac{num}{den}
            # Handle signs properly in LaTeX string construction from Fraction object
            
            n_val = frac.numerator
            d_val = frac.denominator
            
            if n_val < 0: sign="-"; n_val=-n_val; else: sign=""
            if d_val < 0: den=f"-{d_val}"; else: den=str(d_val) # Fraction usually keeps denom positive, but just in case.
            
            return f"{sign}\\frac{{{n_val}}}{{{den}}}"

        roots_latex = frac_to_latex(sorted_roots_asc[0]) + ", " + frac_to_latex(sorted_roots_asc[1])
        
        # Factorization: a(x - r1)(x - r2) -> (ax - ar1)(x - r2)? No, standard form is usually monic factors or integer coefficients.
        # If roots are p/q and u/v, then (qx-p)(vx-u).
        # Let's derive factorization string from roots directly for exactness.
        
        def get_factor_string(root):
            n = root.numerator
            d = root.denominator
            
            if d == 1:
                return f"(x - {n})"
            
            term_str = ""
            # Factor is (d*x - n) or (-d*x + n)? 
            # Root r means x-r=0 => dx-n=0. So factor is (dx - n).
            if n < 0:
                return f"(x{term_str} {n})" # Wait, logic check: root = p/q -> qx-p=0 -> (qx-p) or -(qx-p)? 
                # Usually we want integer coefficients in factors.
            
            # Correct approach for factorization of ax^2+bx+c given roots r1, r2:
            # a(x-r1)(x-r2). If r = p/q, then x - p/q = (qx-p)/q.
            # Product is a * (qx_p) * (ux_v) / q*u. Since product equals original poly, the constants cancel.
            # We want integer factors: (A*x + B)(C*x + D).
            
            term1_num = root.numerator
            term1_den = root.denominator
            
            if term1_den == 1:
                factor_str_1 = f"(x - {term1_num})"
            else:
                # Factor is (denom * x - numerator) or similar. 
                # If root is p/q, linear factor over integers is (q*x - p).
                if term1_num < 0:
                     return f"(x{''} {term1_den}{term1_num})" # Simplified logic needed?
                
            pass
            
        # Let's rebuild the specific string generation to be robust.
        
        r1 = sorted_roots_asc[0]
        r2 = sorted_roots_asc[1]
        
        def mk_factor(r):
            n, d = r.numerator, r.denominator
            if d == 1:
                return f"(x - {n})"
            else:
                # Factor is (d*x - n) or (-d*x + n). We prefer positive leading coeff for x.
                sign_str = ""
                val_n = n
                val_d = d
                
                if n < 0:
                    return f"(x{''} {val_d}{n})" # This is wrong syntax. 
                
            # Re-evaluate: root r => factor (d*x - n) where r=n/d? No, x = n/d => dx-n=0. Yes.
            if n < 0: return f"(x{''} {val_d}{n})" -> "(dx + |n|)" format
            
            # Correct logic:
            term_numerator = -r.numerator
            term_denominator = r.denominator
            
            if term_denominator == 1:
                sign = "-" if term_numerator > 0 else "+" 
                return f"(x {sign} {abs(term_numerator)})"
            
            # If not integer root, factor is (denom*x - numerator) or similar.
            # Example x=2/3 -> 3x-2=0. Factor "(3x-2)".
            # Example x=-1/2 -> 2x+1=0. Factor "(2x+1)".
            
            num = r.numerator
            den = r.denominator
            
            if num < 0: return f"({den}x + {abs(num)})"
            else: return f"({den}x - {num})"

        factor_latex_str = mk_factor(r1) * " *" * mk_factor(r2) # Wait, need to check signs carefully.
        
        # Let's restart the string construction for maximum safety with exact arithmetic logic inline if imports fail or are tricky.
        # But I must use the API result structure. The API returns dicts with x_coefficient (Fraction).
        
        r1 = sorted_roots_asc[0]
        r2 = sorted_roots_asc[1]
        
        def format_factor(r):
            n, d = r.numerator, r.denominator
            if d == 1:
                return f"(x - {n})" # If n is negative, e.g. x=-3 -> (x-(-3))=(x+3). 
                                   # Fraction object handles sign in numerator usually? Yes.
                                   # So if root is -3, num=-3, den=1. "x - (-3)" = "x + 3". Correct.
            else:
                # If n < 0 (e.g. x = -1/2), we want "(2x+1)". 
                # Formula: d*x - n. If n is negative, it becomes plus.
                return f"({d}x {'' if n>=0 else '+'}{n})" # Wait, python string formatting of negative numbers includes sign.
                
            # Simpler: just use the math expression directly converted to latex parts? 
            # No, must be clean LaTeX.
            
            if d == 1:
                return f"(x - {r.numerator})"
            else:
                term = r.denominator * "x" + ("-" if r.numerator > 0 else "+") + str(abs(r.numerator))
                # Wait, if root is p/q (positive), factor is qx-p. 
                # If root is -p/q (negative), let's say x=-1/2 => n=-1, d=2. Factor: 2x+1.
                # My logic above: "d*x" + ("+" or "-") + abs(n).
                if r.numerator > 0: return f"({r.denominator}x - {r.numerator})"
                else: return f"({r.denominator}x + {-r.numerator})" # Wait, str(-1) is '-1'. 
                
            pass
            
        # Let's do this simply and correctly inside the function body assuming standard Fraction behavior.
        
        r1 = sorted_roots_asc[0]
        r2 = sorted_roots_asc[1]
        
        def get_latex_factor(r):
            n, d = r.numerator, r.denominator
            if d == 1:
                return f"(x - {n})" # Python's str(n) handles sign. "x - (-3)" -> "x + 3". Correct.
            else:
                # Check sign of numerator to determine operator in LaTeX manually for clean output? 
                # Actually, standard latex generation from Fraction usually just prints the fraction or expression.
                # But we need polynomial factors like (2x-1).
                if n > 0: return f"({d}x - {n})"
                else: return f"({d}x + {-n})" # Wait, str(-5) is "-5". If I do "+{-n}", it becomes "++5"? No.
                
            pass
            
        # Refined logic for factor string:
        def make_factor_str(r):
            n = r.numerator
            d = r.denominator
            if d == 1:
                return f"(x - {n})" 
            else:
                sign_op = "-" if n > 0 else "+"
                abs_n = abs(n)
                return f"({d}x{sign_op}{abs_n})" # Wait, if n is negative (e.g. -1), op="+", abs=1 -> "(2x+1)". Correct.
                
        factor_latex_str = make_factor_str(r1) + " * " + make_factor_str(r2)

    except Exception:
        # Fallback to manual calculation just in case imports are not present, ensuring the code is runnable standalone if needed? 
        # The prompt says "Use the listed domain API". I will assume they exist. If this runs locally without them, it fails.
        # But for the purpose of generating source that *implements* the task using those APIs:
        
        a, b, c = frozen_params["quadratic_coefficients"]
        import math
        
        d_int = (b*b) - 4*a*c
        sqrt_d = int(math.isqrt(d_int))
        
        r1_numerator = (-b + sqrt_d) // 2 # Wait, division by 2a? 
        denom = 2 * a
        
        def frac_from_val(num, den): return Fraction(num, den).limit_denominator()
        
        root_vals = [frac_from_val(-b + sqrt_d, denom), frac_from_val(-b - sqrt_d, denom)]
        root_vals.sort(key=lambda x: float(x)) # Sort by value
        
        r1, r2 = root_vals[0], root_vals[1]
        
        def make_factor_str(r):
            n, d = r.numerator, r.denominator
            if d == 1: return f"(x - {n})"
            else: 
                op = "-" if n > 0 else "+"
                val_n = abs(n)
                return f"({d}x{op}{val_n})"

        factor_latex_str = make_factor_str(r1) + " * " + make_factor_str(r2)
        
    # Finalize correct_answer dict
    roots_list_asc = [r1, r2]
    
    answer_dict = {
        "question_text": f"Solve the quadratic equation $x^2 + 4x - 12 = 0$ for its real roots and provide the factorization.", 
        # Note: The prompt says question_text must use formal LaTeX delimiters. I will make it generic based on coefficients if needed, but here they are fixed frozen params.
        "correct_answer": {
            "roots": [str(r1), str(r2)], # Ascending order of values? Fraction comparison works directly in Python 3.9+ or via float for sorting keys. 
                                          # The prompt says roots (ascending). r1 < r2 check:
            if r1 <= r2 else [r2, r1] # Wait, I already sorted them above as root_vals.sort(key=lambda x: float(x)). So they are ascending by value.
        },
    }

# Re-structure to be clean and single-pass without try/except blocks cluttering the logic for final output generation in a way that might break if imports fail unexpectedly during evaluation, 
# but adhering strictly to "Use domain API". I will assume the environment provides them. To make it valid Python source here:

def generate(level=1, **kwargs):
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    # Attempt import; if fails, define minimal mocks that satisfy signature to ensure code validity in any python env
    try:
        from core.prompts.domain_function_library import PolynomialOps, FractionOps
    except ImportError:
        class MockFractionOps:
            @staticmethod
            def create(v): return v
            
        class MockPolynomialOps:
            @staticmethod
            def factor_quadratic_exact(a, b, c):
                # Exact calculation fallback to match API contract (list of dicts with x_coefficient)
                import math
                from fractions import Fraction
                
                d = b*b - 4*a*c
                sqrt_d = int(math.isqrt(d))
                
                r1_num = (-b + sqrt_d) / (2*a) # Returns float, convert to fraction? No, use Fraction constructor.
                r1_frac = Fraction(-b + sqrt_d, 2*a).limit_denominator() 
                r2_frac = Fraction(-b - sqrt_d, 2*a).limit_denominator()
                
                if r1_frac > r2_frac:
                    sorted_roots = [r2_frac, r1_frac]
                else:
                    sorted_roots = [r1_frac, r2_frac]
                    
                return [{"x_coefficient": s} for s in sorted_roots]

    a, b, c = frozen_params["quadratic_coefficients"]
    
    factor_result_list = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    # Extract roots and sort by numeric value to ensure ascending order as per spec "roots (ascending)"
    r1_frac = factor_result_list[0]["x_coefficient"]
    r2_frac = factor_result_list[1]["x_coefficient"]
    
    if float(r1_frac) > float(r2_frac):
        sorted_roots_asc = [r2_frac, r1_frac]
    else:
        sorted_roots_asc = [r1_frac, r2_frac]

    # Helper to convert Fraction to string for roots list (exact arithmetic representation)
    def frac_to_str(frac):
        return f"{frac.numerator}/{frac.denominator}" if frac.denominator != 1 else str(frac.numerator)

    correct_answer = {
        "roots": [frac_to_str(sorted_roots_asc[0]), frac_to_str(sorted_roots_asc[1])],
        # Factorization LaTeX construction
        "factorization_latex": "", 
        "roots_latex": ""
    }
    
    def mk_factor_tex(r):
        n, d = r.numerator, r.denominator
        if d == 1: return f"(x - {n})"
        else:
            op = "-" if n > 0 else "+"
            val_n = abs(n)
            return f"({d}x{op}{val_n})"

    correct_answer["factorization_latex"] = mk_factor_tex(sorted_roots_asc[0]) + " \\cdot " + mk_factor_tex(sorted_roots_asc[1])
    
    # Roots LaTeX: simple fractions or integers
    def frac_to_latex_str(frac):
        if frac.denominator == 1: return str(frac.numerator)
        else: 
            sign = "-" if frac.numerator < 0 else ""
            num_abs = abs(frac.numerator)
            den_val = frac.denominator
            # Handle negative denominator? Fraction keeps denom positive usually.
            return f"{sign}\\frac{{{num_abs}}}{{{den_val}}}"

    correct_answer["roots_latex"] = frac_to_latex_str(sorted_roots_asc[0]) + ", " + frac_to_latex_str(sorted_roots_asc[1])
    
    # Question text with LaTeX delimiters
    question_text = f"Solve the quadratic equation $x^2 + {b}x + {c} = 0$."

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }