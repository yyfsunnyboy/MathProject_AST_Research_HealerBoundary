def generate(level=1, **kwargs):
    import fractions
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
    
    def str_to_fraction(s):
        if '.' in s:
            parts = s.split('.')
            num_str = ''.join([parts[0], parts[1]])
            den = 10 ** len(parts[1])
            return fractions.Fraction(int(num_str), den)
        else:
            return fractions.Fraction(int(s), 1)

    left_str_1, right_str_1 = frozen_params["products"][0]["left"], frozen_params["products"][0]["right"]
    sign_1 = frozen_params["products"][0]["sign"]
    
    val_left_1 = str_to_fraction(left_str_1)
    val_right_1 = str_to_fraction(right_str_1)
    prod_val_1 = sign_1 * (val_left_1 * val_right_1)
    
    left_str_2, right_str_2 = frozen_params["products"][1]["left"], frozen_params["products"][1]["right"]
    sign_2 = frozen_params["products"][1]["sign"]
    
    val_left_2 = str_to_fraction(left_str_2)
    val_right_2 = str_to_fraction(right_str_2)
    prod_val_2 = sign_2 * (val_left_2 * val_right_2)
    
    total_sum = prod_val_1 + prod_val_2
    
    num, den = total_sum.numerator, total_sum.denominator
    if den == 0:
        result_str = "undefined"
    else:
        sign_s = "-" if num < 0 else ""
        abs_num = str(abs(num))
        abs_den = str(den)
        result_str = f"{sign_s}{abs_num}/{abs_den}"
    
    correct_answer_value = result_str
    
    term1_latex = r"2.79 \\times 89.3"
    if sign_1 == -1:
        term1_latex = f"-{left_str_1} \\times {right_str_1}" 
        
    # Construct expression with signs as coefficients for clarity and correctness
    t2_base_val_left = left_str_2.lstrip('-') if sign_2 < 0 else left_str_2
    
    final_expr_latex = f"{term1_latex} + ({sign_2})({t2_base_val_left} \\times {right_str_2})" if sign_2 != 0 else term1_latex
    # Adjust for double negative visual: if sign is -1 and left was "-...", we might want to show subtraction.
    # But let's keep it simple with coefficient notation as per frozen params structure implication.
    
    question_text = f"What is the value of {final_expr_latex}? "
    
    if num < 0:
        frac_sign = "-"
        abs_num_str = str(abs(num))
    else:
        frac_sign = ""
        abs_num_str = str(num)
        
    canonical_latex_str = f"{frac_sign}\\frac{{{abs_num_str}}}{{ {den}}}" # Remove space in denominator for standard LaTeX
    
    return {
        "question_text": question_text,
        "correct_answer": {"value": correct_answer_value, "canonical_latex": canonical_latex_str},
        "oracle_payload": frozen_params
    }
