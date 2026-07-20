def generate(level=1, **kwargs):
    frozen_params = {
        "expression": "9/22 + 11/18 - (23/22 - 7/18)"
    }

    # Parse the expression manually based on the frozen string to ensure exact structure
    # Expression: 9/22 + 11/18 - (23/22 - 7/18)
    # Terms: 
    # A = 9/22
    # B = 11/18
    # C = -(23/22 - 7/18) = -23/22 + 7/18
    
    val_a = create(9, 22)
    val_b = create(11, 18)
    
    inner_parenthesis = create(23, 22) - create(7, 18)
    # Wait, the expression is A + B - (C_inner). 
    # So it's A + B + (-C_inner) which equals A + B - C_inner.
    
    val_c_inner = create(23, 22) - create(7, 18)
    
    result = add(val_a, add(val_b, PyFraction(-1)) * (add(create(23, 22), PyFraction(-1)) * ... # No, let's do it simply
    
    val_c_inner = create(23, 22) - create(7, 18)
    
    result_val_a_plus_b = add(val_a, val_b)
    final_result = sub(result_val_a_plus_b, val_c_inner)

    # Let's re-calculate carefully using the provided API logic. 
    # A + B - (C - D) = A + B - C + D
    
    term1 = create(9, 22)
    term2 = create(11, 18)
    
    inner_group = sub(create(23, 22), create(7, 18))
    
    total = add(add(term1, term2), PyFraction(-inner_group).numerator / ... # No need to mix. Just sum all terms with signs.
    
    final_result_num = (9 * 18) + (11 * 22) - ((23 * 18) - (7 * 22)) 
    denominator_base = 22 * 18
    
    # Actually, let's use the Fraction class directly for calculation to ensure correctness before formatting.
    f_a = PyFraction(9, 22)
    f_b = PyFraction(11, 18)
    
    inner_part = PyFraction(23, 22) - PyFraction(7, 18)
    
    final_val = add(f_a, f_b) + sub(inner_part.__neg__(), ... # Wait, simpler: A+B-C+D
    
    total_sum = f_a + f_b - inner_part
    
    numerator, denominator = total_sum.numerator, total_sum.denominator
    
    correct_answer_num = str(total_sum.numerator)
    correct_answer_denom = str(total_sum.denominator)
    
    canonical_latex = to_latex(total_sum)

    question_text = r"$\frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})$"

    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": correct_answer_num,
            "denominator": correct_answer_denom,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }