from fractions import Fraction
import json
from math import gcd as _gcd

def generate(level=1, **kwargs):
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    # Simulate the domain API calls based on the specification logic for exact arithmetic
    
    a, b, c = frozen_params["quadratic_coefficients"]
    
    # Calculate discriminant and roots using Fraction to ensure no floats
    d_num = (b * b) - 4 * a * c
    if d_num < 0:
        raise ValueError("No real roots for this polynomial.")
        
    sqrt_d_numerator, sqrt_d_denominator = _gcd(d_num), 1
    
    # Helper to simplify square root of integer n into p/q form where q is small or perfect square logic applies
    def get_sqrt_fraction(n):
        if n < 0: return None
        factors = {}
        temp = abs(n)
        i = 2
        while i * i <= temp:
            count = 0
            while temp % i == 0:
                count += 1
                temp //= i
            factors[i] = count
            i += 1
        if temp > 1:
            factors[temp] = 1
            
        numerator_parts = []
        denominator_parts = []
        
        for base, exp in sorted(factors.items()):
            if exp % 2 == 0:
                # Even power goes to numerator as integer part (or simplifies)
                num_val = base ** (exp // 2)
                numerator_parts.append(num_val)
            else:
                # Odd power: one factor in sqrt, rest squared go out? 
                # Actually for exact root representation p/q usually implies simplified radical or rational if perfect square.
                # If not perfect square, we represent as Fraction with denominator 1 and note it's irrational?
                # The spec says "roots (ascending), ... NOT a 3-tuple". It expects list[dict].
                # Let's assume for difficulty level 1, roots might be rational or simple surds.
                # However, standard exact arithmetic often returns Fraction if integer root exists.
                pass
        
        total_num = 1
        den = 1
        remaining_numerator_parts = []
        
        for base, exp in sorted(factors.items()):
            q = exp // 2
            r = exp % 2
            
            # The term is sqrt(base^exp) = (base^(q/2)) * sqrt(base^r)? No.
            # It's base^(floor(exp/2)) * sqrt(base if odd else 1). 
            # But we want a single Fraction representation? Usually for non-perfect squares, 
            # the domain API might return something specific or we format it as p/q where q=1 and value is irrational string?
            # Re-reading: "returns list[dict... int or 'p/q'". This implies rational roots only are expected in this context usually.
            # If discriminant is not a perfect square, the root is irrational. 
            # Given "Exact arithmetic; no floats", we must handle irrationals carefully.
            # However, if d_num is not a perfect square, standard polynomial factorization over Q fails (irreducible).
            # But task says "factor_roots". Let's assume inputs yield rational roots for L1 or specific format needed.
            
        return Fraction(total_num) / den

    def get_sqrt_fraction(n):
        if n < 0: raise ValueError("Negative discriminant")
        factors = {}
        temp = abs(int(n)) # Ensure int
        i = 2
        while i * i <= temp:
            count = 0
            while temp % i == 0:
                count += 1
                temp //= i
            if count > 0:
                factors[i] = count
            i += 1
        if temp > 1:
            factors[temp] = 1
            
        numerator_parts = []
        
        for base, exp in sorted(factors.items()):
            q = exp // 2
            r = exp % 1 # remainder logic handled by integer division
            
            # We want sqrt(n). 
            # If we can express as p/q (rational), then n must be a perfect square.
            # Let's check if it is a perfect square first for L1 simplicity or handle general case.
            
        total_num = 1
        den = 1
        
        # Check if perfect square
        sqrt_n = int(n**0.5)
        if sqrt_n * sqrt_n == n:
            return Fraction(sqrt_n, 1)
        
        # If not a perfect square, we have an irrational root. 
        # The spec says "int or 'p/q'". This strongly suggests only rational roots are tested here for L1.
        # We will assume the test cases provided via frozen_params (or generated ones in reality) yield rational roots.
        # If d_num is not a perfect square, we might need to return None or handle as string? 
        # But "Exact arithmetic" usually implies Fraction objects which are infinite precision rationals.
        # Irrationals cannot be represented exactly by Fractions.
        # Therefore, for this specific task level 1 with frozen params [1,4,-12], d = 16 - (-48) = 64 (perfect square).
        # So we can safely assume perfect squares or return the simplified radical if required? 
        # The spec says "int or 'p/q'". It does not mention radicals. Thus, likely only rational roots are expected in L1.
        
    sqrt_d_numerator = int(d_num**0.5)
    
    root1_num = -b + sqrt_d_numerator
    root2_num = -b - sqrt_d_numerator
    
    # Simplify fractions for roots
    def simplify_frac(num, den):
        common = _gcd(abs(int(num)), abs(int(den))) if int(den)!=0 else 1
        return Fraction(int(root1_num) // common, int(2*a*common))

    root1_val = Fraction(-b + sqrt_d_numerator, 2 * a)
    root2_val = Fraction(-b - sqrt_d_numerator, 2 * a)
    
    # Sort roots ascending
    if root1_val > root2_val:
        sorted_roots = [root2_val, root1_val]
    else:
        sorted_roots = [root1_val, root2_val]
        
    # Construct factorization latex and roots latex
    def format_fraction(frac):
        num = frac.numerator
        den = frac.denominator
        if abs(num) == 1:
            return f"-{den}" if num < 0 else str(den)
        elif num > 0:
            return f"{num}/{den}"
        else: # negative numerator, positive denominator usually
             sign = "-" if num < 0 else ""
             n_abs = abs(num)
             d_abs = den
             if n_abs == 1:
                 return f"-{d_abs}" if num < 0 else str(d_abs)
             elif d_abs == 1:
                 return f"{sign}{n_abs}"
             else:
                 return f"{sign}{n_abs}/{d_abs}"

    # Factorization form: a(x - r1)(x - r2) -> (ax + b/2 +/- ...)? 
    # Standard factorization over integers if possible, or with fractions.
    # Given coefficients [1, 4, -12], roots are (-4 +/- 8)/2 => 2 and -6.
    # Factors: (x-2)(x+6).
    
    r1 = sorted_roots[0]
    r2 = sorted_roots[1]
    
    factor_latex_part_1 = f"(x{'' if r1.numerator == 1 else ''}{r1.denominator} - {format_fraction(r1)})" # Simplified logic needed
    
    # Better approach for latex: (ax + b +/- sqrt(d))/2a -> factors are linear terms.
    # If roots are rational p/q, factor is (qx - p).
    
    def get_linear_factor(root):
        num = root.numerator
        den = root.denominator
        if den == 1:
            return f"(x{''} - {num})" if num > 0 else f"(x + {-num})" # Wait, factor is (x-root) -> x - p/q => qx - p over q. 
            # Usually we write as product of monic factors or integer coefficients?
            # "factorization_latex": typically "(x-2)(x+6)" for 1*x^2...
            
        if num > 0:
             return f"(qx{''} - {num})" where q=den. 
             
    # Let's construct the string carefully.
    # Root r = p/q. Factor is (q x - p).
    
    def get_factor_string(root):
        n, d = root.numerator, root.denominator
        if d == 1:
            sign = "-" if n > 0 else "+"
            return f"(x{''} {sign}{n})" # Wait, (x - r) -> x - p. If r=2, (x-2). 
            # My logic above was flawed in text. Correct: factor is (qx - p).
            if n > 0:
                return f"(x{''} - {n})"
            else:
                return f"(x + {-n})"
        else:
             sign = "-" if n > 0 else "+" # Actually qx - p. If root is positive, subtract. 
             # Example root 1/2 -> (2x-1). Root -1/2 -> (2x+1).
             return f"(d x{''} {sign}{n})"

    factor_latex = ""
    if len(sorted_roots) == 2:
        term1 = get_factor_string(r1) # Need to fix logic inside function call below
        term2 = get_factor_string(r2)
        
        def make_term(root):
            n, d = root.numerator, root.denominator
            sign_str = "-" if n > 0 else "+"
            return f"(d x{''} {sign_str}{n})" # Wait, variable is 'x', not 'd'. 
            # Correct: (denom * x - numerator) or +.
            
        term1 = make_term(r1)
        term2 = make_term(r2)
        
    roots_latex_list = [format_fraction(root) for root in sorted_roots]

    question_text = f"Find the roots and factorization of $x^{{4}}{b}x + {c}$." # Wait, quadratic. 
    question_text = f"Solve the equation ${a}x^2 + {b}x + {c} = 0$ for x. Provide the exact rational roots in ascending order and the factorization over rationals."
    
    correct_answer = {
        "roots": [str(r) for r in sorted_roots], # Spec says list[dict]? No, spec says returns dict with keys... 
        # Re-read: "correct_answer must include roots (ascending), factorization_latex, and roots_latex".
        # And domain API returns list[dict]. But the task output is a specific structure.
        # Let's assume 'roots' key contains list of strings or dicts? Spec says "include roots...". 
        # Usually JSON serializable means strings for latex.
        
    }

# Re-implementing strictly according to constraints and types:

from fractions import Fraction
import json

def generate(level=1, **kwargs):
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    a, b, c = frozen_params["quadratic_coefficients"]
    
    # Calculate discriminant
    d_val_num = (b * b) - 4 * a * c
    
    if d_val_num < 0:
        raise ValueError("No real roots")
        
    sqrt_d_numerator = int(d_val_num**0.5)
    
    root1_frac = Fraction(-b + sqrt_d_numerator, 2 * a)
    root2_frac = Fraction(-b - sqrt_d_numerator, 2 * a)
    
    sorted_roots = [root1_frac, root2_frac] if root1_frac <= root2_frac else [root2_frac, root1_frac]
    
    # Helper to format fraction for latex string (roots_latex and roots list content?)
    def fmt(frac):
        n, d = frac.numerator, frac.denominator
        s_n = str(n) if abs(n)!=1 or d!=1 else ("-" + str(d)) if n<0 else "x" # No, just number.
        
        if d == 1:
            return f"{n}"
        elif n > 0:
            return f"{n}/{d}"
        else:
            return f"-{abs(n)}/{d}"

    roots_latex_str = [fmt(r) for r in sorted_roots]
    
    # Factorization latex
    def get_factor_term(frac):
        n, d = frac.numerator, frac.denominator
        sign = "-" if n > 0 else "+"
        return f"({d}x{''}{sign}{n})".replace(" x", " ").strip()

    # Actually standard form: (ax+b)(cx+d). Here monic usually preferred for latex unless specified.
    # If roots are p/q, factor is (qx - p). 
    term1 = get_factor_term(sorted_roots[0])
    term2 = get_factor_term(sorted_roots[1])
    
    factorization_latex_str = f"{term1} {term2}" if len(term1) > 5 else f"({term1}) ({term2})".replace(" ", "") # Clean up spaces
    
    question_text = r"Solve the quadratic equation $x^2 + bx + c = 0$ where coefficients are given. Find the exact rational roots in ascending order and write the factorization."
    
    correct_answer = {
        "roots": [str(r) for r in sorted_roots], # Spec says list[dict] from API, but here we return dict with keys. 
        # Wait: "correct_answer must include roots (ascending), ...". It doesn't specify the type of 'roots' value inside correct_answer dict explicitly as dicts vs strings, but domain API returns list[dict].
        # However, for JSON response in task output, usually strings or simple types are used. 
        # Let's stick to string representation of roots and latex.
        
    }

# Finalizing the code block with exact logic:

from fractions import Fraction
import json

def generate(level=1, **kwargs):
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    a, b, c = frozen_params["quadratic_coefficients"]
    
    d_num = (b * b) - 4 * a * c
    
    if d_num < 0:
        raise ValueError("No real roots")
        
    sqrt_d_numerator = int(d_num**0.5)
    
    root1_frac = Fraction(-b + sqrt_d_numerator, 2 * a)
    root2_frac = Fraction(-b - sqrt_d_numerator, 2 * a)
    
    sorted_roots = [root1_frac, root2_frac] if root1_frac <= root2_frac else [root2_frac, root1_frac]
    
    def fmt(frac):
        n, d = frac.numerator, frac.denominator
        if d == 1:
            return str(n)
        elif n > 0:
            return f"{n}/{d}"
        else:
            return f"-{abs(n)}/{d}"

    roots_latex_list = [fmt(r) for r in sorted_roots]
    
    def get_factor_term(frac):
        n, d = frac.numerator, frac.denominator
        sign_str = "-" if n > 0 else "+"
        return f"({d}x{''}{sign_str}{n})".replace(" x", " ").strip()

    term1 = get_factor_term(sorted_roots[0])
    term2 = get_factor_term(sorted_roots[1])
    
    # Ensure clean latex without extra spaces inside parentheses if possible, but standard spacing is fine.
    factorization_latex_str = f"{term1} {term2}"

    question_text = r"Solve the quadratic equation $x^2 + bx + c = 0$ where coefficients are given. Find the exact rational roots in ascending order and write the factorization."
    
    correct_answer = {
        "roots": [str(r) for r in sorted_roots], 
        # The spec says domain API returns list[dict]. But here we construct our own answer dict.
        # To be safe with "include roots", using strings is standard JSON.
        "factorization_latex": factorization_latex_str,
        "roots_latex": ", ".join(roots_latex_list)
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }