def generate(level=1, **kwargs):
    # Frozen parameters defined directly as per specification
    denominator_str = "4-sqrt(7)"
    numerator_val = 9
    radicand_val = 7
    
    # Rationalize the expression: numerator / (a - b*sqrt(r))
    # Here we have 9 / (4 - sqrt(7))
    # Multiply by conjugate (4 + sqrt(7)) / (4 + sqrt(7))
    
    a_base = 4
    b_base = 1
    
    # Numerator * Conjugate: 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7)
    new_numerator_real_part = numerator_val * a_base
    new_numerator_sqrt_part = numerator_val * b_base
    
    # Denominator becomes difference of squares: (a - b)^2? No, it's (4^2 - sqrt(7)^2)? 
    # Actually (A - B)(A + B) = A^2 - B^2. Here A=4, B=sqrt(7).
    # So denominator becomes 16 - 7 = 9
    
    denom_squared_part = a_base * a_base
    radicand_sq_val = b_base * b_base * radicand_val
    final_denominator = denom_squared_part - radicand_sq_val
    
    # The expression is now (new_numerator_real + new_numerator_sqrt) / final_denominator
    # We need to divide both parts by the denominator. Since 9/9=1, it simplifies nicely.
    
    simplified_num_real = new_numerator_real_part // final_denominator
    simplified_num_sqrt = new_numerator_sqrt_part // final_denominator
    
    # The result is in form a + b*sqrt(7) where:
    # a = 36 / 9 = 4
    # b = 9 / 9 = 1
    
    target_a = simplified_num_real
    target_b = simplified_num_sqrt
    
    # Task asks for integer value of a + b (the coefficients in the rationalized form)
    final_answer = target_a + target_b

    question_text = r"Rationalize the denominator of $\frac{9}{4-\sqrt{7}}$ and express it in the form $a+b\sqrt{r}$ where $a, b \in \mathbb{Z}$. What is the value of $a+b$?"
    
    correct_answer = final_answer
    
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
