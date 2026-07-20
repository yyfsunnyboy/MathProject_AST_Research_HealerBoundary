def generate(level=1, **kwargs):
    from fractions import Fraction
    
    # Frozen sampled parameters (must be preserved exactly)
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    # Parse strings to exact rational numbers (Fractions)
    term_1 = Fraction("279/100") * Fraction(89, "1")  # 2.79 is 279/100
    if frozen_params["products"][0]["sign"] == -1:
        result_part_1 = -(term_1)
    else:
        result_part_1 = term_1
    
    term_2 = Fraction("-21", "100") * Fraction(89, "1")  # -0.21 is -21/100
    if frozen_params["products"][1]["sign"] == -1:
        result_part_2 = -(term_2)
    else:
        result_part_2 = term_2
    
    total_sum = result_part_1 + result_part_2

    # Construct question text using LaTeX delimiters
    latex_expr = r" \left( 2.79 \times 89.3 - (-0.21) \times 89.3 \right)"
    
    correct_answer_value = str(total_sum.numerator) + "/" + str(total_sum.denominator)
    canonical_latex = f"{total_sum}"

    return {
        "question_text": r"\text{Calculate the exact value of: } $" + latex_expr.replace(" ", "") + "$", 
        "correct_answer": {"value": correct_answer_value, "canonical_latex": str(total_sum)},
        "oracle_payload": frozen_params
    }