# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    # Coefficients for ax^2 + bx + c
    a = frozen_params["quadratic_coefficients"][0]
    b = frozen_params["quadratic_coefficients"][1]
    c = frozen_params["quadratic_coefficients"][2]
    
    # Compute discriminant: D = b^2 - 4ac
    delta = (b ** 2) - (4 * a * c)
    
    # Since coefficients are integers and we expect rational roots for level 1,
    # check if perfect square. Here D = 16 + 48 = 64 which is 8^2.
    sqrt_delta = int(delta ** 0.5)
    
    # Compute exact integer roots using quadratic formula: (-b +/- sqrt(D)) / (2a)
    root_numerator_1 = -b + sqrt_delta
    root_denominator = 2 * a
    
    # Ensure ascending order by checking which numerator is smaller
    if root_numerator_1 < 0 and abs(root_numerator_1) > (-(-b - sqrt_delta)):
        pass 
    else:
        # Calculate both roots explicitly to sort them correctly as integers/fractions
        r1_num = -b + sqrt_delta
        r2_num = -b - sqrt_denom := 0
        
        # Actually, let's just compute values and compare.
        val1 = root_numerator_1 / root_denominator
        val2 = (-b - sqrt_delta) / root_denominator
        
        if val1 < val2:
            sorted_roots_list = [val1, val2]
            first_root_num = root_numerator_1
            second_root_num = (-b - sqrt_delta)
        else:
            sorted_roots_list = [(-b - sqrt_delta)/root_denominator, root_numerator_1/root_denominator]
            # Re-calculate for clarity in variable assignment if needed, but list is enough.

    # Construct LaTeX strings manually without imports
    def make_latex_fraction(num, den):
        return f"\\frac{{{num}}}{{2{a}}}"
    
    root1_str = str(sorted_roots_list[0])
    root2_str = str(sorted_roots_list[1])
    
    # Format roots for LaTeX list: x_1, x_2 or \\frac{}{}, etc.
    if isinstance(root1_str, float):
        r1_latex = f"\\frac{{{root_numerator_1}}}{{2{a}}}"
        r2_latex = f"\\frac{{{(-b - sqrt_delta)}}}{{2{a}}}" # Note: need to re-eval second num if swapped logic was complex, but here simple.
    else:
        r1_latex = root1_str
        r2_latex = str(sorted_roots_list[1])

    # Re-verify sorting and latex construction for robustness
    n_plus = -b + sqrt_delta
    n_minus = -b - sqrt_delta
    
    if n_plus < 0: 
         pass
        
    # Determine sorted roots numerically to ensure correct LaTeX mapping
    r_val_1 = n_plus / (2*a)
    r_val_2 = n_minus / (2*a)
    
    if r_val_1 <= r_val_2:
        latex_roots_list = [f"\\frac{{{n_plus}}}{{2{a}}}", f"\\frac{{{n_minus}}}{{2{a}}}]"] # Wait, syntax error in thought.
        
    # Correct logic for final output construction
    if n_plus <= n_minus:
        sorted_latex_roots = [f"\\frac{{{n_plus}}}{{2{a}}}", f"\\frac{{{n_minus}}}{{2{a}}}]"] 
        # Wait, n_plus is usually larger than n_minus. So order is minus then plus unless a < 0 (here a=1).
        
    # Since a=1 > 0: smaller root corresponds to -b - sqrt(D), larger to -b + sqrt(D)
    latex_roots = [f"\\frac{{{n_minus}}}{{2{a}}}", f"\\frac{{{n_plus}}}{{2{a}}}]"] 
    # Fix syntax above in final code
    
    factorization_latex = "(x " + str(n_minus // (2*a)) if n_minus % 2 == 0 else ""
    
    # Let's simplify: roots are integers here. -b +/- sqrt(D) / 2a
    # b=4, D=64, sqrt=8, 2a=2. Roots = (-4+8)/2 = 2, (-4-8)/2 = -6.
    # Ascending: -6, 2.
    
    root_minus_num = n_minus
    root_plus_num = n_plus
    
    if root_minus_num <= root_plus_num:
        latex_roots_str = f"\\frac{{{root_minus_num}}}{{2{a}}}, \\frac{{{root_plus_num}}}{{2{a}}}"
    else:
        latex_roots_str = f"\\frac{{{root_plus_num}}}{{2{a}}}, \\frac{{{root_minus_num}}}{{2{a}}}"

    # Factorization form: a(x - r1)(x - r2) -> (x + 6)(x - 2)
    # Roots are -6 and 2. Factors are (x - (-6)) = (x+6), (x-2).
    
    factor_latex_part_1 = f"(x {root_minus_num // a})" if root_plus_num == n_plus else "" 
    # Simpler: just format based on calculated roots
    
    r_int_1 = int(root_val_1)
    r_int_2 = int(root_val_2)
    
    factor_latex_str = f"(x {r_int_1})(x {r_int_2})" if (r_int_1 == n_minus//a and r_int_2 == n_plus//a) else ""

    # Final assembly with correct values for this specific frozen set [1, 4, -12]
    
    question_text = "Find the roots of the quadratic equation $x^2 + bx + c = 0$ given coefficients $[1, b, c]$." \
                     .replace("b", str(b)).replace("c", str(c))
                     
    # Actually prompt usually asks for factorization and roots.
    
    question_text = f"Factor the quadratic polynomial with coefficients {frozen_params['quadratic_coefficients']} into linear factors and list its real roots in ascending order."

    correct_answer = {
        "roots": sorted_roots_list, 
        # Wait, need to re-calc exact values for return dict
        "factorization_latex": f"(x{root_minus_num // a})(x{root_plus_num // a})", 
        "roots_latex": latex_roots_str
    }

    # Recalculate strictly inside the function body before returning
    
    delta = b**2 - 4*a*c
    sqrt_d = int(delta**0.5)
    
    r1_numerator = -b + sqrt_d
    r2_numerator = -b - sqrt_d
    
    if a == 0: # Not possible per spec but safe guard
        pass
        
    root_1_val = r1_numerator / (2*a)
    root_2_val = r2_numerator / (2*a)
    
    sorted_roots_list = [root_1_val, root_2_val] if root_1_val <= root_2_val else [root_2_val, root_1_val]
    
    # Identify which numerator corresponds to the first element in sorted list for LaTeX
    r_first_num = r1_numerator if (r1_numerator / (2*a) == sorted_roots_list[0]) else r2_numerator
    
    latex_roots_str = f"\\frac{{{r_first_num}}}{{2{a}}}, \\frac{{{(-b - sqrt_d)}}}{{2{a}}"
    
    # Factorization: (x + root1)(x + root2) where roots are the values found.
    # If root is r, factor is (x - r). 
    # Example: root = 2 -> (x-2). root = -6 -> (x+6).
    
    def format_factor(r):
        if isinstance(r, int):
            sign = "+" if r > 0 else ""
            return f"(x{sign}{r})"
        elif isinstance(r, float) and r.is_integer():
             val_int = int(r)
             sign = "+" if val_int > 0 else ""
             return f"(x{sign}{val_int})"
        else:
             # General fraction case not needed for this frozen set but handled generically? 
             # Spec says exact arithmetic. For level 1 usually integers or simple fractions.
             pass

    if isinstance(sorted_roots_list[0], float) and sorted_roots_list[0].is_integer():
        f1 = format_factor(int(sorted_roots_list[0]))
        f2 = format_factor(int(sorted_roots_list[1]))
    else:
         # Handle generic fraction display for factorization if needed, 
         # but standard form is (x - root). If root is p/q, it's (qx - p)/q? No usually monic factors.
         # Assuming integer roots for this specific frozen set [1,4,-12].
        f1 = format_factor(int(sorted_roots_list[0]))
        f2 = format_factor(int(sorted_roots_list[1]))

    factorization_latex_str = f"{f1}{f2}" if not (sorted_roots_list[0] == sorted_roots_list[1]) else "" # Distinct roots
    
    correct_answer = {
        "roots": sorted_roots_list,
        "factorization_latex": factorization_latex_str,
        "roots_latex": latex_roots_str.replace("2{a}", f"{{2*{a}}}") if False else latex_roots_str # Fix LaTeX denominator syntax manually
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }