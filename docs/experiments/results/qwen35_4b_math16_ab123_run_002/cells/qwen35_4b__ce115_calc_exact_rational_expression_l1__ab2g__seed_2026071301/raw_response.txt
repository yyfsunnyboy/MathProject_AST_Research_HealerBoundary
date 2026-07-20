def generate(level=1, **kwargs):
    import sympy
    
    # Frozen sampled parameters from task specification
    frozen_params = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }

    # Parse inputs as SymRational to ensure exact arithmetic (no floats)
    left_1 = sympy.Rational("279") / 100
    right_1 = sympy.Rational("893") / 10
    
    left_2 = sympy.Rational("-21") / 100
    sign_2 = -1

    # Calculate exact values using SymPy rational arithmetic
    term1 = (left_1 * right_1) * sign_1
    term2 = (left_2 * right_1) * sign_2
    
    result = term1 + term2
    
    # Ensure irreducible form and correct formatting for answer
    numerator, denominator = sympy.fraction(result.as_numer_denom()[0], 1) if isinstance(result, int) else result.numerator, result.denominator
    
    p_str = str(numerator)
    q_str = str(denominator)
    
    # Construct LaTeX representations manually to ensure canonical form and exactness without markdown fences in output logic
    latex_value = f"\\frac{{{p_str}}}{{{q_str}}}" if denominator != 1 else str(result).replace("/", "\\over")
    if denominator == 1:
        latex_canonical = r"\dfrac{" + p_str.replace("+", "+").strip() + "}{1}"
    else:
        # Construct proper fraction LaTeX manually to avoid float conversion issues during string formatting
        numerator_val = result.numerator
        denom_val = result.denominator
        
        if num > 0 and den > 0:
            latex_canonical = r"\frac{" + str(numerator_val) + "}{"} + str(denom_val) + r"}" # Simplified for direct string concat safety in this context, assuming positive/neg handling via numerator sign
        else:
             if num < 0 and den > 0 or (num >= 0 and den < 0):
                 latex_canonical = "-" + str(abs(numerator_val)) + r"\frac{1}{"} + str(denom_val) # Wait, logic above was mixed. Let's redo strictly.
             else:
                 pass
        
        # Correct strict LaTeX construction for result (which is -23.54 -> -1177/50)
        num = int(result.numerator)
        den = abs(int(result.denominator)) if denominator < 0 else int(result.denominator)
        
        latex_canonical = r"\frac{" + str(num) + "}{"} + str(den) + r"}"

    question_text = (r"Calculate the exact rational value of: \n\n")
    
    # Build expression string carefully to match frozen params logic without floating point errors in text representation if needed, but prompt asks for LaTeX delimiters.
    expr_str_1 = f"{left_1} \\cdot {right_1}"
    expr_str_2 = f"({expr_str_1}) + ({left_2} \\cdot {right_1})" # sign is handled in calculation
    
    question_text += r"\n\nCompute the sum of these two products:"
    
    return_dict = {
        "question_text": question_text,
        "correct_answer": {
            "value": f"{p_str}/{q_str}",
            "canonical_latex": latex_canonical # Using standard \frac for clarity and correctness
        },
        "oracle_payload": frozen_params
    }

    return return_dict