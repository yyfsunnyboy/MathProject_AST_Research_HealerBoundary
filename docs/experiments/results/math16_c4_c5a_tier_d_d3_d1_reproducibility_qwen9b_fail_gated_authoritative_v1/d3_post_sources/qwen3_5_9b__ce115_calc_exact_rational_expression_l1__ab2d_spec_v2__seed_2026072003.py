# -*- coding: utf-8 -*-

from fractions import Fraction


def generate(level=1, **kwargs):
    # Frozen sampled parameters as defined in the task specification
    frozen_params = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }

    # Helper to convert decimal string to Fraction exactly
    def str_to_frac(s):
        return Fraction(int(float(s) * 100), 100).limit_denominator() if '.' in s else int(s) / 1
    
    # Actually, for exact arithmetic with decimals like "2.79", we must treat them as fractions of integers directly to avoid float precision loss before conversion.
    # Better approach: parse string manually or use Fraction from decimal representation logic.
    def precise_str_to_frac(s):
        if '.' in s:
            int_part, frac_part = s.split('.')
            num = int(int_part) * (10 ** len(frac_part)) + int(frac_part)
            den = 10 ** len(frac_part)
            return Fraction(num, den).limit_denominator() # limit_denominator is safe here as numbers are small
        else:
            return Fraction(s)

    # Process the first product term
    left1_str = frozen_params["products"][0]["left"]
    right1_str = frozen_params["products"][0]["right"]
    sign1 = frozen_params["products"][0]["sign"]
    
    val_left_1 = precise_str_to_frac(left1_str)
    val_right_1 = precise_str_to_frac(right1_str)
    
    term1_val = Fraction(val_left_1 * sign1, 1).limit_denominator() # Actually just multiply by integer sign
    
    # Process the second product term
    left2_str = frozen_params["products"][1]["left"]
    right2_str = frozen_params["products"][1]["right"]
    sign2 = frozen_params["products"][1]["sign"]
    
    val_left_2 = precise_str_to_frac(left2_str)
    val_right_2 = precise_str_to_frac(right2_str)
    
    term2_val = Fraction(val_left_2 * sign2, 1).limit_denominator()

    # The task implies an expression. Based on "products" and signs, it looks like: (left1 * right1) + (sign2 * left2 * right2)? 
    # Or simply sum of terms? Let's assume the structure is a linear combination based on the list order.
    # Usually in these tasks, if given a list of products with signs, it implies Sum(sign_i * product_i).
    
    total_numerator = term1_val.numerator + (term2_val.numerator) 
    total_denominator = 1
    
    # Wait, let's re-evaluate the math.
    # Term 1: sign=1 -> left="2.79", right="89.3". Value = 2.79 * 89.3? Or is it just a term in an expression like A + B?
    # Given "products" list, usually implies multiplication within the item if not specified otherwise, but often these tasks are about evaluating expressions like (A op B) ... 
    # However, looking at similar patterns: "left", "right", "sign". It likely means `term = sign * left * right`.
    
    term1_val_exact = precise_str_to_frac(left1_str) * precise_str_to_frac(right1_str)
    term2_val_exact = -precise_str_to_frac(left2_str) * precise_str_to_frac(right2_str) # sign is -1
    
    exact_result = term1_val_exact + term2_val_exact
    exact_result_simplified = exact_result.limit_denominator()

    numerator = str(exact_result_simplified.numerator)
    denominator = str(exact_result_simplified.denominator)
    
    canonical_latex = f"\\frac{{{numerator}}}{{{denominator}}}"
    
    question_text = (f"Evaluate the expression: " + 
                     f"{precise_str_to_frac(left1_str)} \\times {precise_str_to_frac(right1_str)} " +
                     f"+ ({sign2}){precise_str_to_frac(left2_str)} \\times {precise_str_to_frac(right2_str)}.")

    correct_answer = {"value": f"\\frac{{{numerator}}}{{{denominator}}}", "canonical_latex": canonical_latex}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }