def generate(level=1, **kwargs):
    import json
    
    # Frozen sampled parameters from task specification
    params = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }
    
    # Parse the equation to find roots in form (sqrt(a) + b) or (-sqrt(a) + b)
    # Equation: (x - 2)^2 = 3 => x - 2 = +/- sqrt(3) => x = 2 +/- sqrt(3)
    # Roots are a1 = 2 + sqrt(3), a2 = 2 - sqrt(3)
    
    # Identify coefficients for canonical form: b + c*sqrt(d) or similar structure
    # Here, root format is integer_part + radical_coefficient * sqrt(radicand)
    # Root 1: 2 + 1*sqrt(3) -> a = 2+sqrt(3), coeff=1, radicand=3
    # Root 2: 2 - 1*sqrt(3) -> b = 2-sqrt(3), coeff=-1, radicand=3
    
    radical_coefficient_1 = 1
    radical_coefficient_2 = -1
    radicand = 3
    integer_part = 2
    
    # Construct canonical LaTeX for the roots based on order "a>b"
    # a corresponds to larger value: 2 + sqrt(3)
    # b corresponds to smaller value: 2 - sqrt(3)
    
    latex_a = f"{integer_part}+{radical_coefficient_1}\\sqrt{{{radicand}}}"
    latex_b = f"{integer_part}{'' if radical_coefficient_2 == 0 else '+' + str(radical_coefficient_2)}\\sqrt{{{radicand}}}".replace("+ -", "-").replace("- ", "")
    
    # Refine LaTeX for b to ensure canonical form (no double signs)
    if radical_coefficient_1 > 0:
        latex_a = f"{integer_part}+{radical_coefficient_1}\\sqrt{{{radicand}}}"
    else:
        latex_a = f"{integer_part}{radical_coefficient_1}\\sqrt{{{radicand}}}".replace("+ -", "-").replace("- ", "")

    if radical_coefficient_2 > 0:
        latex_b = f"{integer_part}+{radical_coefficient_2}\\sqrt{{{radicand}}}"
    else:
        # Handle negative coefficient carefully for LaTeX canonical form
        sign_str = "+" + str(radical_coefficient_2) if radical_coefficient_2 > 0 else ""
        latex_b = f"{integer_part}{sign_str}{{-1}}}\\sqrt{{{radicand}}}"

    # Correct logic to build strings properly without markdown or complex parsing errors in thought trace:
    # Root A (larger): 2 + sqrt(3) -> "2+\\sqrt{3}"
    # Root B (smaller): 2 - sqrt(3) -> "2-\\sqrt{3}"
    
    latex_a = f"{integer_part}+{radical_coefficient_1}\\sqrt{{{radicand}}}".replace("+", "+").replace("-", "-") if radical_coefficient_1 > 0 else f"{integer_part}{'' + str(radical_coefficient_1)}\\sqrt{{{radicand}}}"
    # Simpler approach for this specific case:
    
    term_a = f"+{radical_coefficient_1}\\sqrt{{{radicand}}}".replace("+", "+") if radical_coefficient_1 > 0 else ""
    latex_a_str = str(integer_part) + (term_a.lstrip('+') or '') # Remove leading plus for canonical math
    
    term_b_sign = "+" if radical_coefficient_2 > 0 else "-"
    term_b_val = abs(radical_coefficient_2) * "\\sqrt{{{radicand}}}"
    latex_b_str = str(integer_part) + (term_b_sign + term_b_val).replace("+", "+") # Ensure single sign
    
    # Re-evaluating strictly for canonical LaTeX: "a>b" means a is the larger root.
    # Root 1: 2 + sqrt(3), Root 2: 2 - sqrt(3)
    # Canonical A: 2+\\sqrt{3}
    # Canonical B: 2-\\sqrt{3}
    
    canonical_latex_a = f"{integer_part}+{radical_coefficient_1}\\sqrt{{{radicand}}}".replace("+", "+") if radical_coefficient_1 > 0 else str(integer_part) + ("-" if radical_coefficient_1 < 0 else "") + "\\sqrt{" + str(-radical_coefficient_1*radical_coefficient_1 * radicand // (integer_part**2)) # This is getting too complex for mental scratchpad.
    
    # Let's just construct the strings directly based on known values:
    val_a = 2 + 3**0.5
    val_b = 2 - 3**0.5
    
    latex_a_str = "2+\\sqrt{3}"
    latex_b_str = "2-\\sqrt{3}"
    
    # Calculate target expression value: 2a + b where a is the larger root, b is the smaller root? 
    # Or does 'target' refer to variables in the answer string? Usually it's evaluating the algebraic sum.
    # If question asks for "2a+b", and roots are r1, r2 with r1 > r2 (since order a>b), then:
    # Let root_set = {r1, r2} where r1 = 2+sqrt(3), r2 = 2-sqrt(3).
    # Order constraint "a>b" implies we assign a=r1, b=r2.
    # Target value = 2*r1 + r2 = 2*(2+sqrt(3)) + (2-sqrt(3)) = 4 + 2*sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3).
    
    target_value_numeric = 6 + 3**0.5
    
    # Construct correct_answer dict structure
    answer_dict = {
        "rational": 6,
        "radical_coefficient": 1,
        "radicand": 3,
        "canonical_latex": f"{answer_dict['rational']}+{answer_dict['radical_coefficient']}\\sqrt{{{answer_dict['radicand']}}}"
    }
    
    # Format question_text with LaTeX delimiters
    equation_display = r"\((x-2)^2=3\)"
    order_desc = "a>b"
    target_expr = "2a+b"
    
    q_text = f"Solve the quadratic equation {equation_display} for x. Let $a$ and $b$ be the roots satisfying the condition that ${order_desc}. Calculate the value of ${target_expr}$."
    
    # Oracle payload must exactly equal frozen sampled parameters
    oracle_payload = params
    
    return {
        "question_text": q_text,
        "correct_answer": answer_dict,
        "oracle_payload": oracle_payload
    }