# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification
    denominator_str = "4-sqrt(7)"
    numerator_val = 9
    radicand_val = 7
    
    # Rationalize the expression: numerator / (a - b*sqrt(r))
    # Here we have 9 / (4 - sqrt(7))
    # Multiply by conjugate (4 + sqrt(7)) / (4 + sqrt(7))
    
    a_base = 4      # The rational part of the denominator
    b_base = 1      # Coefficient of sqrt(radicand) in denominator
    
    numerator_val_int = int(numerator_val)
    radicand_val_int = int(radicand_val)
    
    # Denominator becomes: (a - b*sqrt(r)) * (a + b*sqrt(r)) = a^2 - r*b^2
    denom_sq_part = a_base ** 2 - radicand_val_int * (b_base ** 2)
    
    if denom_sq_part == 0:
        raise ValueError("Zero denominator in rationalization")
    
    # Numerator becomes: numerator * (a + b*sqrt(r))
    new_num_rational = int(numerator_val_int * a_base)
    new_num_irrational_coeff = int(numerator_val_int * b_base)
    
    # Final form is (new_num_rational / denom_sq_part) + (new_num_irrational_coeff / denom_sq_part)*sqrt(radicand)
    # We need to check if the denominator divides cleanly or just return a+b based on task spec "Return the integer value of a + b" where result is A + B*sqrt(7). 
    # The prompt asks for correct_answer as a single exact integer. Usually in these math problems, after rationalization and simplification, we get something like X + Y*sqrt(K).
    # However, looking at the specific request: "Identify the integers a and b in the result a + b\sqrt{7}. ... Return the integer value of a + b."
    # Let's calculate the simplified fraction.
    
    common_denom = denom_sq_part
    
    rational_part_num = new_num_rational / common_denom  # This might not be an integer immediately, let's check divisibility or if it simplifies to integers in this specific case.
    irrational_part_coeff = new_num_irrational_coeff / common_denom
    
    # Check for exact division to ensure the result is strictly of form A + B*sqrt(7) with integer coefficients as implied by "single exact integer" answer being a+b.
    if rational_part_num % 1 != 0 or irrational_part_coeff % 1 != 0:
        # If not integers, perhaps we need to simplify the fraction first? 
        # Let's re-evaluate: 9 / (4 - sqrt(7)) * (4 + sqrt(7))/(4 + sqrt(7)) = (36 + 9*sqrt(7)) / (16 - 7) = (36 + 9*sqrt(7)) / 9
        # Simplifying by dividing numerator and denominator by GCD of coefficients? 
        # Here we can divide the whole fraction by 9.
        
        g_rational = rational_part_num // common_denom if isinstance(rational_part_num, int) else None
        
        # Actually let's do integer arithmetic to be safe:
        # Result = (36 + 9*sqrt(7)) / 9 = 4 + sqrt(7).
        # So a=4, b=1. Sum = 5.
        
        pass
    
    # Recalculate using pure integers for clarity and correctness
    num_rational_part = numerator_val_int * a_base      # 36
    num_irrational_coeff = numerator_val_int * b_base     # 9
    denom_sq = a_base ** 2 - radicand_val_int * (b_base ** 2) # 16 - 7 = 9
    
    # The expression is (num_rational_part + num_irrational_coeff*sqrt(radicand)) / denom_sq
    # We can simplify by dividing numerator and denominator if they share a common factor.
    
    def gcd(x, y):
        while y:
            x, y = y, x % y
        return abs(x)
    
    total_gcd = gcd(num_rational_part + num_irrational_coeff * radicand_val_int, denom_sq) # Not quite right for mixed types
    
    # Let's just simplify the fraction term by term if possible.
    # Term 1: (num_rational_part / denom_sq). If divisible -> integer A. Else keep as float? 
    # But task says "single exact integer" answer. This implies a and b are integers in the final simplified form.
    
    # Check divisibility of num_irrational_coeff by denom_sq first, or simplify fraction globally.
    # 36/9 = 4 (integer)
    # 9/9 = 1 (integer)
    
    if num_rational_part % denom_sq == 0:
        a_final = int(num_rational_part // denom_sq)
    else:
        # If not divisible, we might have fractions. But the prompt implies integers. 
        # Let's assume standard simplification where common factors cancel out completely to yield integers for this specific test case.
        pass
    
    if num_irrational_coeff % denom_sq == 0:
        b_final = int(num_irrational_coeff // denom_sq)
    else:
        # If not divisible, we have fractions like (9/9)*sqrt(7). 
        # Let's construct the answer based on simplified form.
        pass
    
    # Re-verify calculation manually to ensure no logic error in code flow above
    # 36 / 9 = 4 -> a_final = 4
    # 9 / 9 = 1 -> b_final = 1
    
    if num_rational_part % denom_sq != 0:
        raise ValueError("Rational part not integer")
    
    if num_irrational_coeff % denom_sq != 0:
        raise ValueError("Irrational coefficient not integer after simplification of this specific case")

    a_final = int(num_rational_part // denom_sq)
    b_final = int(num_irrational_coeff // denom_sq)
    
    correct_answer_int = a_final + b_final
    
    # Format question text with LaTeX delimiters as requested: $4-\sqrt{7}$ and $\frac{9}{4-\sqrt{7}}$
    latex_denom = r"$4-\sqrt{{\text{{{radicand_val_int}}}"}}"  # Wait, standard \sqrt{n} syntax. 
    # Correct LaTeX for sqrt(7) is \sqrt{7}. The prompt says "formal LaTeX delimiters".
    
    question_text = r"Rationalize the denominator of $\frac{\text{{{{{numerator_val_int}}}}}}{{4-\sqrt{{\text{{radicand_val_int}}}}}$ and express it in the form $a + b\sqrt{7}$. Find the value of $a + b$."
    
    # Ensure oracle_payload matches frozen parameters exactly as a dict or string? 
    # "oracle_payload must exactly equal the frozen sampled parameters" which is {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    oracle_payload = {
        "denominator": denominator_str,
        "numerator": numerator_val_int,
        "radicand": radicand_val_int
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_int,
        "oracle_payload": oracle_payload
    }