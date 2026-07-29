# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per contract
    denominator_str = "4-sqrt(7)"
    numerator_val = 9
    radicand_val = 7
    
    # Rationalize the denominator of (numerator) / (a - sqrt(b))
    # Formula: n / (A - R) = n * (A + R) / ((A)^2 - (R)^2)
    # Here A=4, R=sqrt(7), so denom^2 = 16 - 7 = 9.
    
    a_term = 4      # The rational part of the denominator term 'a' in (a - sqrt(b))
    b_val = radicand_val  # The value under the radical
    
    # Calculate new numerator: n * (A + R) -> we only need integer parts for sum later, 
    # but let's compute exact form first.
    # Resulting expression is [n*A / D] + [n*R / D] where D = A^2 - b_val
    denominator_squared_minus_radicand = a_term * a_term - b_val  # 16 - 7 = 9
    
    new_numerator_rational_part = numerator_val * a_term   # n*A
    new_numerator_irrational_coefficient = numerator_val    # n*1 (coefficient of R)
    
    final_rational_coef = new_numerator_rational_part // denominator_squared_minus_radicand  # Integer division is safe here as result is integer? 
    # Wait, let's check: 9 * 4 / 9 = 36/9 = 4. Yes.
    # And irrational part coeff: (n) / D -> coefficient of sqrt(b).
    
    final_irrational_coef_num = new_numerator_irrational_coefficient
    final_denom_val = denominator_squared_minus_radicand
    
    # The term is (final_rational_coef) + (final_irrational_coef_num // final_denom_val)*sqrt(b)? 
    # No, the coefficient of sqrt(7) is (n / D). Since n=9 and D=9, coeff is 1.
    
    rational_part = new_numerator_rational_part // denominator_squared_minus_radicand
    irrational_coefficient_num = numerator_val
    
    final_irrational_coef = irrational_coefficient_num // denominator_squared_minus_radicand
    
    # The result form requested: a + b*sqrt(7) where a and b are integers.
    val_a = rational_part
    val_b = final_irrational_coef
    
    correct_answer = val_a + val_b
    
    question_text = r"The expression $\frac{9}{4-\sqrt{7}}$ simplifies to $a+b\sqrt{7}$ where $a$ and $b$ are integers. What is the value of $a+b$?"
    
    oracle_payload = {
        "denominator": denominator_str,
        "numerator": numerator_val,
        "radicand": radicand_val
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }