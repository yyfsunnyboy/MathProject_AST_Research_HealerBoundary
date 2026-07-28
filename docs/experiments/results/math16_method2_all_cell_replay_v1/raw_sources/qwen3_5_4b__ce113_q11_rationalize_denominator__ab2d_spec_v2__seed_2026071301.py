def generate(level=1, **kwargs):
    # Frozen parameters defined directly as per specification
    denominator_str = "4-sqrt(7)"
    numerator_val = 9
    radicand_val = 7
    
    # Rationalize the expression: numerator / (a - b*sqrt(r))
    # Here we have 9 / (4 - sqrt(7))
    # Multiply by conjugate (4 + sqrt(7)) / (4 + sqrt(7))
    
    a_conj = 4      # The rational part of the denominator
    b_conj = 1      # Coefficient of sqrt(radicand) in denominator
    
    numerator_val_int = int(numerator_val)
    radicand_val_int = int(radicand_val)
    
    # Denominator becomes: (a - b*sqrt(r)) * (a + b*sqrt(r)) = a^2 - r*b^2
    denom_sq_part = a_conj ** 2
    denom_radical_part = radicand_val_int * (b_conj ** 2)
    
    final_denominator = denom_sq_part - denom_radical_part
    
    # Numerator becomes: numerator * (a + b*sqrt(r))
    new_numerator_rational = int(numerator_val) * a_conj
    new_numerator_irrational_coefficient = int(numerator_val) * b_conj
    
    # The result is in the form A + B*sqrt(7) where:
    # A = (new_numerator_rational / final_denominator)
    # B = (new_numerator_irrational_coefficient / final_denominator)
    
    # We need to check if these are integers or fractions. 
    # The task asks for the integer value of a + b in the result form a + b*sqrt(7).
    # Let's compute A and B exactly.
    
    total_numerator = new_numerator_rational ** 2 - radicand_val_int * (new_numerator_irrational_coefficient ** 2)
    final_denominator_sq = denom_sq_part ** 2 + 2 * denom_radical_part
    
    # Actually, let's re-evaluate the structure. 
    # Result = [numerator * conjugate] / denominator_conjugated_product
    # Numerator part: (9)(4 + sqrt(7)) = 36 + 9sqrt(7)
    # Denominator product: (4)^2 - (1*sqrt(7))^2 = 16 - 7 = 9
    
    # So the expression simplifies to: (36 + 9sqrt(7)) / 9 
    # Which is exactly: 4 + sqrt(7)
    
    # Thus, a = 4 and b = 1.
    # The question asks for the integer value of a + b.
    
    result_a = new_numerator_rational // final_denominator
    result_b_coefficient = int(numerator_val * b_conj / denom_sq_part) if (denom_radical_part == 0 or radicand_val_int % denom_sq_part == 0 and ... ) else None
    
    # Let's stick to the direct calculation derived above:
    # Numerator after conjugation multiplication: numerator * a + numerator * sqrt(radicand)*b_conj
    # Denominator product: a^2 - b_conj^2 * radicand_val_int = 16 - 7 = 9
    
    num_part_a = int(numerator_val) * a_conj
    num_part_b = int(numerator_val) * b_conj
    den_product = denom_sq_part - (b_conj ** 2) * radicand_val_int # This is actually just the denominator of the fraction if we treat sqrt as separate? 
    # Wait, standard rationalization:
    # x / (a + bi) -> multiply by a-bi. Here b=1 for sqrt(7).
    # Denominator becomes a^2 - r*b^2 = 4^2 - 7*1^2 = 9.
    
    final_denom_val = den_product
    
    # The resulting numerator is (num * a + num * b * sqrt(r)) / denom_val? 
    # No, the form is: [numerator * conjugate] / denominator_conjugated_value
    # Numerator part rational: 9 * 4 = 36
    # Numerator part irrational coeff: 9 * 1 = 9
    
    final_rational_num = num_part_a
    final_irrational_coeff = num_part_b
    
    if final_denom_val == 0:
        raise ValueError("Zero denominator in rationalization")
        
    a_final = int(final_rational_num / final_denom_val) # Should be integer division check first? 
    b_final = int(final_irrational_coeff / final_denom_val)
    
    # Check divisibility to ensure exact integers as per "exact integer" requirement for correct_answer
    if (final_rational_num % final_denom_val != 0):
        raise ValueError("Rational part is not an integer")
    if (final_irrational_coeff % final_denom_val != 0):
        # In this specific case: 36/9 = 4, 9/9 = 1. Both are integers.
        pass
        
    correct_answer_int = a_final + b_final
    
    question_text = r"Rationalize the denominator of $\frac{9}{4-\sqrt{7}}$ and find $a+b$ where the result is in the form $a+b\sqrt{7}$."
    
    oracle_payload = {
        "denominator": "4-sqrt(7)", 
        "numerator": 9, 
        "radicand": 7
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_int,
        "oracle_payload": oracle_payload
    }
