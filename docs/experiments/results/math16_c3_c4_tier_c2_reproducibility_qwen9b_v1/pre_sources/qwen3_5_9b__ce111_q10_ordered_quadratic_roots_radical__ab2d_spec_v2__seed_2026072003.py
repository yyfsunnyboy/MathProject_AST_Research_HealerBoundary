# -*- coding: utf-8 -*-
def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    equation = "(x-2)^2=3"
    order_constraint = "a>b"
    target_expression = "2a+b"
    
    # Parse the specific quadratic form (x-h)^2 = k to find roots directly without full expansion if desired, 
    # but standard formula works universally. Here we solve x-2 = +/- sqrt(3).
    h = 2
    k = 3
    
    import math

    # Calculate discriminant equivalent for the shifted form: (x-h) = +/- sqrt(k)
    # Roots are h + sqrt(k) and h - sqrt(k)
    root1_val = h + math.sqrt(k)
    root2_val = h - math.sqrt(k)
    
    # Order roots such that a > b
    if root1_val >= root2_val:
        a_float, b_float = root1_val, root2_val
    else:
        a_float, b_float = root2_val, root1_val
        
    # Compute target 2a + b
    result_value = 2 * a_float + b_float
    
    # Construct the radical representation for canonical_latex and radicand details.
    # The term is derived from sqrt(3). 
    # Result: (h+sqrt(k)) or (h-sqrt(k)). Since k=3, it's simple integer inside root.
    
    # Determine if we need to simplify coefficients outside the radical for 2a+b?
    # a = h + sqrt(k), b = h - sqrt(k)
    # 2a + b = 2(h + sqrt(k)) + (h - sqrt(k)) = 3h + sqrt(k)
    
    final_coefficient = 3 * h
    radical_term_value = math.sqrt(k)
    
    # Check if the result is purely rational or has a radical part.
    # Here, k=3 is not a perfect square, so we have a radical term.
    # The expression simplifies to: integer_part + coefficient_radical * sqrt(radicand)
    # However, in this specific case (2a+b), the coeff of sqrt(k) becomes 1.
    
    simplified_coeff = final_coefficient
    radicand_val = k
    
    # Check if radical term exists and its sign/coeff
    has_radical_part = True
    rad_sign = 1
    rad_coeff = 1
    
    # Construct canonical LaTeX: integer + coeff * sqrt(radicand) or just the value if rational.
    # Since radicand is 3, it stays as \sqrt{3}.
    
    latex_parts = []
    if simplified_coeff != 0:
        latex_parts.append(f"{simplified_coeff}")
        
    if has_radical_part and rad_sign == 1:
        latex_parts.append(rf"\sqrt{{{radicand_val}}}")
    elif has_radical_part and rad_sign == -1:
        latex_parts.append(rf"-\sqrt{{{radicand_val}}}")
    
    # Join parts. If only one part (e.g., just integer or just radical), handle spacing if needed, 
    # but standard math notation usually separates terms with + or -.
    # Here we have 6 + sqrt(3).
    
    canonical_latex = "+".join(latex_parts)
    # Ensure no leading '+' unless it's the only term (not applicable here as coeff!=0 and has_radical)
    if latex_parts[0] == "": 
        pass
        
    # Re-evaluate joining logic for standard LaTeX output: 6 + \sqrt{3}
    final_latex = canonical_latex
    
    question_text = f"Solve the equation {equation}. Let $a$ and $b$ be the roots ordered such that {order_constraint}. Compute the value of {target_expression}."
    
    correct_answer_dict = {
        "value": result_value, # The actual float/rational number if rationalizable exactly (here 6 + sqrt(3))
        "rational_part": simplified_coeff,
        "radical_coefficient": rad_sign * rad_coeff, 
        "radicand": radicand_val,
        "canonical_latex": final_latex
    }

    # Ensure correct_answer is JSON serializable. Floats are okay if exact or we represent the radical structurally.
    # The prompt asks for 'correct_answer' to include result with rational, etc. 
    # We will return a dict structure inside correct_answer as implied by "include result with...".
    
    oracle_payload = {
        "equation": equation,
        "order": order_constraint,
        "target": target_expression
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }