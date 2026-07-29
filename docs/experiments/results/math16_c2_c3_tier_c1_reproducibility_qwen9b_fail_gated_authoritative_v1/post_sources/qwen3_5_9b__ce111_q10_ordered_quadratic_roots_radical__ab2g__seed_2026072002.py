def generate(level=1, **kwargs):
    import math
    
    # Frozen sampled parameters from task specification
    frozen_params = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }
    
    # Parse the equation to extract roots and coefficients for validation logic
    # Equation: (x-2)^2 = 3 => x^2 - 4x + 1 = 0
    # Roots are derived from quadratic formula or expansion.
    # Let's simulate parsing based on the frozen "equation" string provided.
    
    # Hardcoded extraction for this specific frozen instance to ensure correctness without external libs like sympy
    # Equation: (x-2)^2 = 3 -> x^2 - 4x + 1 = 0
    a_coeff = 1
    b_coeff = -4
    c_coeff = 1
    
    discriminant = b_coeff**2 - 4*a_coeff*c_coeff
    sqrt_discriminant = math.sqrt(discriminant)
    
    root_a = (-b_coeff + sqrt_discriminant) / (2 * a_coeff)
    root_b = (-b_coeff - sqrt_discriminant) / (2 * a_coeff)
    
    # Ensure order 'a > b' as per frozen params "order": "a>b"
    if root_a <= root_b:
        temp = root_a
        root_a = root_b
        root_b = temp
        
    # Construct the radical representation for canonical_latex
    # Format: \frac{-b \pm \sqrt{D}}{2a} -> specifically for roots a and b here.
    # We need to represent them in form rational + coefficient * sqrt(radicand) or similar if needed, 
    # but standard quadratic root is usually just the radical expression.
    # However, task asks for 'radical_coefficient' (may be +/-1), 'radicand'.
    
    # For x = 2 ± sqrt(3):
    rational_part_a = 2
    coefficient_a = 1
    radicand_a = 3
    
    rational_part_b = 2
    coefficient_b = -1
    radicand_b = 3
    
    # Build canonical_latex for the set of roots {a, b} ordered a > b
    # Example: "x_1=2+\sqrt{3}, x_2=2-\sqrt{3}" or similar structured string.
    latex_a = f"\\frac{{{rational_part_a}}+{{coefficient_a}}\\\\sqrt{{{radicand_a}}}}{{1}}" if coefficient_a != 0 else str(rational_part_a)
    # Simplify LaTeX for integer rational part + radical
    def make_latex_root(q, c, r):
        sign = "+" if c > 0 else "-"
        abs_c = abs(c)
        latex_str = f"\\frac{{{q}}{sign}{{abs_c}}\\\\sqrt{{{r}}}}{{1}}" # Denom is 2*1=2 usually but here simplified? 
        # Actually roots of (x-2)^2=3 are x = 2 +/- sqrt(3).
        return f"x_1={q}{c:+d}\\sqrt{{{r}}}, \\quad x_2={q}{(-c):+d}\\sqrt{{{r}}}" if c != -abs_c else None
        
    # Correct LaTeX construction for roots of (x-2)^2=3 -> x = 2 ± √3
    latex_root_a_str = f"x_1=2{'+\\sqrt{{' + str(radical_coefficient) + '\\sqrt{{{radicand}}'}}}}" 
    # Let's build it precisely: "x_1=2+\\sqrt{3}, x_2=2-\\sqrt{3}"
    
    radical_str_a = f"2+\\\\sqrt{{{radicand_a}}}" if coefficient_a == 1 else f"{rational_part_a}{coefficient_a:+d}\\\\sqrt{{{radicand_a}}}"
    # Wait, standard form is usually just the value. 
    # Let's stick to: "x_1=2+\\sqrt{3}, x_2=2-\\sqrt{3}"
    
    canonical_latex = f"x_1={rational_part_a}{'+' if coefficient_b < 0 else ''}{abs(coefficient_b)}\\\\sqrt{{{radicand}}}, \\quad x_2={rational_part_a}-{'-' if coefficient_b > 0 else ''}{abs(coefficient_b)}\\\\sqrt{{{radicand}}}"
    # Correction: root a is +, root b is -. 
    # Since coeff was -1 for the second term in my logic above (x = 2 - sqrt(3))
    
    final_latex_a = f"2+\\\\sqrt{{3}}"
    final_latex_b = f"2-\\\\sqrt{{3}}"
    canonical_latex = f"x_1={final_latex_a}, \\quad x_2={final_latex_b}"

    # Calculate target value: 2a + b where a and b are the roots (values) or coefficients? 
    # Task says "target": "2a+b". Usually in these contexts, if 'order' is specified on roots,
    # it implies algebraic manipulation of root values. But often 'a' and 'b' refer to specific variables defined in a hidden context.
    # Given the frozen params don't define what 'a' and 'b' are numerically other than being roots or coefficients.
    # Re-reading: "target": "2a+b". If a, b are roots x1, x2? 
    # Or if it refers to standard quadratic ax^2+bx+c=0 where target is expression of coeffs?
    # Given the specific equation (x-2)^2=3 -> 1*x^2 -4*x +1 =0. Coeffs: a_q=1, b_q=-4, c_q=1.
    # If 'a' and 'b' in target refer to roots x1, x2? 
    # Let's assume the question asks for an expression involving the roots or specific values derived from them.
    # However, without explicit definition of what variables a and b map to in the text generation phase beyond "roots",
    # we must infer. Common pattern: If order is 'a>b', then a=root1 (larger), b=root2 (smaller).
    # Target = 2*a + b? 
    # Let's compute numeric target based on roots being x1, x2 with x1 > x2.
    
    val_a = root_a
    val_b = root_b
    
    computed_target_val = 2 * val_a + val_b
    
    # The correct_answer dict needs: result (numeric or symbolic?), radical_coefficient, radicand, canonical_latex.
    # Since the target is an expression "2a+b", and we need a structured answer.
    # If the question asks to evaluate 2x1+x2 given x^2-4x+1=0? 
    # Let's provide the numeric result rounded or exact if possible, but usually these tasks want symbolic verification.
    # However, "correct_answer" must include 'result'. Let's assume it wants the evaluated value of the target expression using roots a,b.
    
    # Exact calculation:
    # x1 = 2 + sqrt(3)
    # x2 = 2 - sqrt(3)
    # Target = 2*(2+sqrt(3)) + (2-sqrt(3)) = 4 + 2*sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3).
    
    result_val = "6+\\\\sqrt{{3}}"
    
    # Construct the answer object
    correct_answer_dict = {
        "result": result_val,
        "radical_coefficient": 1, 
        "radicand": 3,
        "canonical_latex": f"x_1=2+\\\\sqrt{{{3}}}, \\quad x_2=2-\\\\sqrt{{3}}" # Or include the target evaluation in latex? Usually canonical refers to roots.
    }

    return {
        "question_text": r"Given the equation $(x-2)^2=3$, let $a$ and $b$ be its two real roots such that $a>b$. Calculate the value of $2a+b$.",
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }