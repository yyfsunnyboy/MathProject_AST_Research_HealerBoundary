# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification
    denominator_str = "4-sqrt(7)"
    numerator_int = 9
    radicand_int = 7
    
    # Rationalize the denominator of (numerator) / (a - sqrt(b))
    # Formula: n / (A - S) = n * (A + S) / ((A)^2 - b) where A=4, S=sqrt(7), b=7
    a_const = 4
    b_val = radicand_int
    
    # Calculate the new denominator value: A^2 - b
    denom_value = (a_const ** 2) - b_val
    
    # The numerator becomes n * (A + sqrt(b))
    # We need to extract coefficients for form x + y*sqrt(7)
    # Numerator part without root: n * A
    num_part_a = numerator_int * a_const
    
    # Coefficient of the radical part in the new numerator: n * 1 (since S=sqrt(b))
    num_part_b_coeff = numerator_int
    
    # The expression is now: [num_part_a + num_part_b_coeff*sqrt(7)] / denom_value
    # We need to divide both parts by denom_value to get final coefficients.
    # However, the task asks for integers a and b in result a + b*sqrt(radicand).
    # Let's check if it simplifies to integers or fractions.
    
    # Current fraction: (num_part_a / denom_value) + (num_part_b_coeff / denom_value)*sqrt(7)
    # If the problem implies integer coefficients, we might need to re-evaluate 
    # whether the division results in exact integers or if 'a' and 'b' refer to 
    # the unsimplified numerator components before dividing by a common factor?
    
    # Re-reading typical "rationalize denominator" tasks: usually they want the simplified form.
    # Let's calculate values first.
    
    val_a = num_part_a / denom_value
    val_b = num_part_b_coeff / denom_value
    
    # Check if these are integers (they might be fractions, but let's see)
    # 4^2 - 7 = 16 - 7 = 9
    # Numerator part a: 9 * 4 = 36 -> 36/9 = 4
    # Numerator part b coeff: 9 * 1 = 9 -> 9/9 = 1
    
    final_a = int(val_a) if val_a == int(val_a) else None
    final_b = int(val_b) if val_b == int(val_b) else None
    
    # Construct the question text with LaTeX delimiters
    latex_denom = r"4-\sqrt{7}"
    
    question_text = f"Simplify \\frac{{{numerator_int}}}{{{latex_denom}}} by rationalizing the denominator. Express your answer in the form a + b\\sqrt{{r}} where {b_val} is under the radical, and find the integer value of a + b."
    
    # Correct answer is sum of coefficients a + b
    correct_answer = final_a + final_b
    
    oracle_payload = {"denominator": denominator_str, "numerator": numerator_int, "radicand": radicand_int}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }