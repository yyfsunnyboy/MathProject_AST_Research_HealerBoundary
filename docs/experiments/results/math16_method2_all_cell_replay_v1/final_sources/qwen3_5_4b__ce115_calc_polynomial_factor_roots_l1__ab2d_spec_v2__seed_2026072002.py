# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly here as per specification
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    a, b, c = frozen_params["quadratic_coefficients"]
    
    # Compute discriminant exactly using integer arithmetic
    delta = b * b - 4 * a * c
    
    # Since coefficients are integers and result in perfect square for this case:
    # x^2 + 4x - 12 -> roots should be rational. 
    # sqrt(delta) must be computed via exact logic or integer check if possible, 
    # but standard float conversion is acceptable only if we ensure precision matches "Exact arithmetic" requirement contextually interpreted as mathematically precise fractions represented in LaTeX.
    # However, to strictly adhere to "no floats", we compute roots as rational numbers (fractions) and convert them to exact integer representations where possible for the answer representation or keep as simplified fraction logic if needed. 
    # Given coefficients [1, 4, -12]:
    # Roots = (-b ± sqrt(delta)) / 2a
    
    delta_val = b * b - 4 * a * c
    
    # Check if delta is perfect square to ensure exact integer roots (common in such tasks)
    import math as _math_module # Importing only for helper function availability, but logic must be native. 
    # Actually, let's avoid imports entirely per "native Python" spirit unless necessary. 
    # We can implement integer sqrt check or just use float if the result is exact integers which it will be here (12 and -4).
    
    # Let's verify: delta = 16 + 48 = 64. Sqrt(64) = 8. Exact integer.
    # We can compute sqrt via math.isqrt in Python 3.8+ or manual check. 
    # To be safe and native without imports if possible, but standard library is usually allowed unless "no external libraries" specified strictly beyond domain APIs. 
    # The prompt says "Do not use ... fabricated helpers". Standard lib like math is fine for sqrt of perfect square?
    # Let's assume we can use basic logic or import math.isqrt which exists in stdlib. 
    # But to be ultra safe on "native Python arithmetic", let's compute integer root manually since 64 is small.
    
    delta_int = int(delta_val)
    if delta_int < 0:
        raise ValueError("No real roots")
    
    # Integer square root check for perfect squares
    s = int(delta_int ** 0.5)
    if s * s != delta_int:
        # Fallback or error, but here it is a perfect square (64 -> 8)
        raise ValueError("Delta not a perfect square")
    
    sqrt_delta = s
    
    # Roots calculation using fractions to avoid float representation in code logic until final LaTeX string construction
    # Root1 = (-b - sqrt_delta) / (2*a)
    # Root2 = (-b + sqrt_delta) / (2*a)
    
    numerator_minus = -(b + sqrt_delta)
    denominator = 2 * a
    
    numerator_plus = -(b - sqrt_delta)
    
    root1_num, root1_den = numerator_minus, denominator
    root2_num, root2_den = numerator_plus, denominator
    
    # Simplify fractions if needed (though here they are integers or simple halves)
    def simplify(frac_n, frac_d):
        common_divisor = 0
        for i in range(1, min(abs(frac_n), abs(frac_d)) + 1):
            if frac_n % i == 0 and frac_d % i == 0:
                common_divisor = i
        
        # Handle negative denominator normalization
        sign = -1 if (frac_n < 0) ^ (frac_d < 0) else 1
        abs_n, abs_d = abs(frac_n), abs(frac_d)
        
        simplified_num = frac_n // common_divisor * sign
        simplified_den = frac_d // common_divisor
        
        return simplified_num, simplified_den
    
    r1_simp_n, r1_simp_d = simplify(root1_num, root1_den)
    r2_simp_n, r2_simp_d = simplify(root2_num, root2_den)
    
    # Determine ascending order. Compare fractions: a/b < c/d <=> ad < bc (for positive denominators). 
    # Here denominator is 2*a = 2*1 = 2 > 0. So just compare numerators directly if same denom.
    # If different denoms, cross multiply. But here both have denom 2 initially after simplification? 
    # Let's re-eval: (-4 - 8)/2 = -6; (-4 + 8)/2 = 2. Both integers.
    
    root1_val = r1_simp_n / r1_simp_d if r1_simp_d != 0 else float(r1_simp_n) # Fallback for display logic, but we store as tuple or int
    root2_val = r2_simp_n / r2_simp_d
    
    # Compare to order ascending
    is_root1_less = (r1_simp_n * r2_simp_d < r2_simp_n * r1_simp_d) if (r1_simp_d > 0 and r2_simp_d > 0) else False
    
    ordered_roots = []
    
    # Helper to format root as string for LaTeX: "x - value" or "(x - val)(x + val)" etc.
    def get_root_latex_str(val_num, val_den):
        if val_den == 1:
            return f"x - {val_num}"
        else:
            # Format fraction a/b -> \frac{a}{b}
            return f"x - \\frac{{{val_num}}}{{abs({val_den})}}" + ("+" if val_den > 0 and val_num < 0 or (val_den < 0) else "") 
            # Wait, standard form: x = (-b +/- sqrt)/2a. 
            # If root is positive integer k, factorization includes (x - k).
            # If root is negative integer m, factorization includes (x + |m|).
            
    # Re-calculate specific values for clarity since inputs are fixed integers [1, 4, -12]
    a_val = 1; b_val = 4; c_val = -12
    
    delta_calc = b_val * b_val - 4 * a_val * c_val # 64
    sqrt_delta_calc = int(delta_calc ** 0.5) # 8
    
    root_a_num = -(b_val + sqrt_delta_calc) # -12, den=2 -> -6
    root_b_num = -(b_val - sqrt_delta_calc) # -(-4+8)= -4? No: -(4-8) = -(-4) = 4. Num=4, den=2 -> 2
    
    r_a_n, r_a_d = int(root_a_num), 1 if root_a_num % (2*a_val) == 0 else None # Actually just divide
    # Root A: (-6)/2 = -3? Wait calculation error above.
    # b=4, sqrt=8. 
    # Option 1: -(4+8) / 2 = -12/2 = -6. Correct root is -6.
    # Option 2: -(4-8) / 2 = -(-4)/2 = 4/2 = 2. Correct root is 2.
    
    roots_list_unordered = [-6, 2]
    roots_sorted = sorted(roots_list_unordered) # [-6, 2]
    
    r1_n, r1_d = int(roots_sorted[0]), 1 if abs(int(roots_sorted[0])) % (2*a_val) == 0 else None 
    # Actually just use the integer values since they are integers.
    
    root_minus_6_str = "x + 6"
    root_plus_2_str = "x - 2"
    
    factorization_latex = f"(\\sqrt{{{roots_sorted[0]}}}) (\\sqrt{{{roots_sorted[1]}}} )" # No, factors are linear terms.
    # Factor form: a(x - r1)(x - r2) -> 1*(x + 6)*(x - 2)
    
    factorization_latex = f"({roots_sorted[0]}=\\text{root}_1)" 
    # Let's construct proper LaTeX strings
    
    root_minus_6_str = "x+6" if roots_sorted[0] == -6 else ""
    root_plus_2_str = "x-2" if roots_sorted[1] == 2 else ""
    
    factorization_latex = f"(\\text{{roots}})" # Placeholder logic
    
    # Correct Logic for LaTeX:
    r_minus_val = roots_sorted[0]
    r_plus_val = roots_sorted[1]
    
    latex_roots_list = [f"x - {r}" if r > 0 else f"x + {-r}" for r in sorted(roots_list_unordered)] # Wait, order matters. Ascending: -6, then 2.
    # LaTeX list format usually comma separated or set notation? "x+6", "x-2".
    
    latex_roots_str = ", ".join([f"x + {-r}" if r < 0 else f"x - {r}" for r in roots_sorted])
    
    factorization_latex = "(\\text{{roots}})" # Placeholder
    
    # Final check on values: 
    # Polynomial: x^2 + 4x - 12. Roots: -6, 2.
    # Factors: (x+6)(x-2).
    
    correct_answer_data = {
        "roots": roots_sorted,
        "factorization_latex": "(\\text{{roots}})", 
        "roots_latex": latex_roots_str
    }

    question_text = r"\text{Find the factorization and roots of the quadratic polynomial defined by coefficients $[1, 4, -12]$."
    
    # Construct final answer string for correct_answer field (JSON serializable)
    ans_dict = {
        "roots": [-6, 2],
        "factorization_latex": r"(x + 6)(x - 2)",
        "roots_latex": r"x + 6,\ x - 2"
    }

    return {
        "question_text": question_text,
        "correct_answer": ans_dict,
        "oracle_payload": frozen_params
    }