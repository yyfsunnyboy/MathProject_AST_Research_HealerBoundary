def generate(level=1, **kwargs):
    # Frozen parameters defined directly as per specification
    denominator_str = "4-sqrt(7)"
    numerator = 9
    radicand = 7
    
    # Rationalize the expression: numerator / (a - b*sqrt(radicand))
    # Here we have 9 / (4 - sqrt(7)). To rationalize, multiply by conjugate (4 + sqrt(7)).
    # Result form is A + B * sqrt(R). We need to find integer a and b such that result = a + b*sqrt(radicand)
    
    a_base = 4      # The 'a' part in the denominator's real component before conjugation logic affects sign, but let's derive properly.
    b_base = -1     # Coefficient of sqrt(7) in (4 - sqrt(7)) is -1
    
    # Conjugate multiplication: (numerator * ((denom_real + denom_imag*sqrt(r))) / (real^2 - imag^2*radicand))
    # Denominator term D = 4^2 - (-1)^2 * 7 = 16 - 7 = 9
    
    real_part_numerator = numerator * a_base**2
    imaginary_part_coefficient = numerator * b_base * a_base
    
    denominator_value = a_base**2 - (b_base**2) * radicand
    
    # Final Real part of the rationalized fraction:
    final_real_num = real_part_numerator + imaginary_part_coefficient * 0 # Wait, standard formula for A/(B-Cr): 
    # Multiply by (B+Cr)/(B^2 - C^2*r). Numerator becomes A*(B+Cr) = AB + ACr.
    
    final_real_num_val = numerator * a_base
    final_imag_coefficient_val = numerator * b_base
    
    denominator_value_calc = a_base**2 - (b_base**2) * radicand
    
    # The result is (final_real_num / denom) + (final_imag_coeff / denom)*sqrt(radicand)
    
    common_denom = denominator_value_calc
    
    final_a_numerator = numerator * a_base
    final_b_numerator = numerator * b_base
    
    # We need the form: X + Y*sqrt(7). The problem asks for integers a and b in result.
    # Let's re-calculate carefully.
    # Expression: 9 / (4 - sqrt(7))
    # Multiply by conjugate: 9 * (4 + sqrt(7)) / ((4)^2 - (-1)^2*7) 
    # Denominator = 16 - 7 = 9
    
    # Numerator expansion: 9*(4 + sqrt(7)) = 36 + 9sqrt(7)
    
    # So the result is (36/9) + (9/9)sqrt(7) = 4 + 1*sqrt(7).
    # Thus a = 4, b = 1.
    
    final_a_val = numerator * a_base // denominator_value_calc
    final_b_val = numerator * b_base // denominator_value_calc
    
    # The question asks for the integer value of a + b from the form result = a + b*sqrt(radicand)
    answer_sum = final_a_val + final_b_val

    correct_answer = str(answer_sum)
    
    # Construct LaTeX formatted question text using formal delimiters $...$ or \(...\) as requested by "formal LaTeX delimiters" context usually implying math mode. 
    # The prompt says "Use formal LaTeX delimiters where math appears". Standard is \( ... \) for inline, $$ ... $$ for display.
    # Given the structure of a single question text string:
    
    question_text = r"$\frac{9}{4-\sqrt{7}}$"

    oracle_payload = {
        "denominator": denominator_str,
        "numerator": numerator,
        "radicand": radicand
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }
