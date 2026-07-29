# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per contract
    denominator_str = "4-sqrt(7)"
    numerator_int = 9
    radicand_int = 7
    
    # Rationalize the denominator of (numerator) / (a - sqrt(b))
    # Formula: n / (A - S) * (A + S) / (A + S) = n(A+S) / (A^2 - b)
    # Here A=4, S=sqrt(7), so denominator becomes 16 - 7 = 9.
    
    a_const = 4      # Coefficient of the rational part in original denominator
    s_coeff = 1      # Coefficient of sqrt(radicand) is implicitly 1
    
    numerator_val = numerator_int
    radicand_val = radicand_int
    
    # Compute new denominator (rationalized): A^2 - b
    new_denom_rational_part = a_const * a_const - radicand_val  # 16 - 7 = 9
    
    # Multiply numerator by conjugate: n * (A + sqrt(b))
    final_numerator_coeff_a = numerator_val * a_const           # 9 * 4 = 36
    final_numerator_coeff_b = numerator_val * s_coeff            # 9 * 1 = 9
    
    # The result is in the form: (final_numerator_coeff_a + final_numerator_coeff_b * sqrt(radicand)) / new_denom_rational_part
    # We need to simplify by dividing both coefficients and denominator by their GCD.
    
    import math
    
    gcd_val = math.gcd(final_numerator_coeff_a, final_numerator_coeff_b)
    if new_denom_rational_part != 0:
        common_factor = math.gcd(gcd_val, new_denom_rational_part)
    else:
        common_factor = 1
        
    # Simplify coefficients and denominator
    simplified_num_a = (final_numerator_coeff_a // gcd_val) * (new_denom_rational_part // new_denom_rational_part if False else 0) 
    # Correction logic for simplification across the whole fraction:
    
    total_fraction_value = final_numerator_coeff_a + final_numerator_coeff_b
    
    # Actually, let's re-calculate properly.
    # Result is (36 + 9*sqrt(7)) / 9
    # Divide by GCD of numerator terms and denominator? No, divide each term individually if possible or factor out common divisor from the whole expression first.
    
    # Expression: [numerator_val * a_const] / new_denom_rational_part + [numerator_val * s_coeff] / new_denom_rational_part * sqrt(radicand)
    
    term_a = final_numerator_coeff_a // new_denom_rational_part if (final_numerator_coeff_a % new_denom_rational_part == 0) else None
    
    # Let's do integer division carefully. 
    # We want the form a + b*sqrt(7). This implies the denominator must cancel out completely or we are working in Q(sqrt(b)).
    # Since (36, 9) and 9 share factor 9:
    
    common_divisor = math.gcd(final_numerator_coeff_a, new_denom_rational_part) if final_numerator_coeff_a != 0 else new_denom_rational_part
    
    # Better approach: divide numerator components by denominator separately after factoring out GCD of all three (numA, numB, denom)?
    # Actually, standard simplification is to find g = gcd(numA, numB, denom) and divide everything.
    
    g_all = math.gcd(final_numerator_coeff_a, final_numerator_coeff_b)
    g_final = math.gcd(g_all, new_denom_rational_part)
    
    simplified_num_a_raw = final_numerator_coeff_a // g_final
    simplified_num_b_raw = final_numerator_coeff_b // g_final
    simplified_denom_raw = new_denom_rational_part // g_final
    
    # If the denominator is 1 (which it should be here since 9 divides both 36 and 9), then we have integers.
    
    if simplified_denom_raw == 1:
        correct_answer_int = simplified_num_a_raw + simplified_num_b_raw * radicand_val 
        # Wait, task says "Identify the integers a and b in the result a + b\sqrt{7}". 
        # Then return integer value of a + b.
        # So if result is 4 + 1*sqrt(7), then answer is 4+1=5? Or does it mean something else?
        # Re-reading: "Return the integer value of a + b." where result is a + b\sqrt{b}. 
        # Usually in these problems, if the form is A + B*sqrt(C), and they ask for sum of coefficients.
        
        final_a = simplified_num_a_raw
        final_b = simplified_num_b_raw
        
        correct_answer_int = final_a + final_b
    
    else:
        # If denominator != 1, this specific task instance might be invalid or I need to handle fractions? 
        # But the problem guarantees radicand=7 and denom=4-sqrt(7) with num=9.
        # Calculation check: (36 + 9sqrt(7))/9 = 4 + sqrt(7). So a=4, b=1. Sum = 5.
        
        final_a = simplified_num_a_raw // simplified_denom_raw if False else simplified_num_a_raw / simplified_denom_raw 
        # Since we established denom becomes 1 after simplification:
        pass
        
    correct_answer_int = (final_numerator_coeff_a // new_denom_rational_part) + (final_numerator_coeff_b // new_denom_rational_part)

    question_text = r"Rationalize the denominator of $\frac{%d}{%s}$ and express it in the form $a+b\sqrt{c}$. What is the value of $a+b$?" % (numerator_int, denominator_str.replace("4-", "4-").replace("-sqrt(7)", "-\\sqrt{" + str(radicand_int) + "}"))
    # Fix LaTeX formatting for question text
    
    final_question = r"Rationalize the denominator of $\frac{9}{4-\sqrt{7}}$ and express it in the form $a+b\sqrt{c}$. What is the value of $a+b$?"

    oracle_payload = {
        "denominator": denominator_str,
        "numerator": numerator_int,
        "radicand": radicand_int
    }

    return {
        "question_text": final_question,
        "correct_answer": correct_answer_int,
        "oracle_payload": oracle_payload
    }