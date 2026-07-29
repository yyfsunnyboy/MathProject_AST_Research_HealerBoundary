# -*- coding: utf-8 -*-
import math
from typing import Dict, Any

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    frozen_params = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }

    # Parse the equation to find roots of (x - 2)^2 = 3
    # x - 2 = sqrt(3) or x - 2 = -sqrt(3)
    # Roots: a = 2 + sqrt(3), b = 2 - sqrt(3) since order is "a>b" and sqrt(3)>0
    
    radical_coefficient = 1
    radicand = 3
    rational_part = 2
    
    # Compute the target expression: 2a + b
    # a = rational_part + radical_coefficient * math.sqrt(radicand)
    # b = rational_part - radical_coefficient * math.sqrt(radicand) (since order is a>b and we assume standard sqrt>0)
    
    val_a = rational_part + radical_coefficient * math.sqrt(radicand)
    val_b = rational_part - radical_coefficient * math.sqrt(radicand)
    
    # Calculate 2a + b
    result_value = 2 * val_a + val_b
    
    # Construct the canonical LaTeX for the answer: (4+3sqrt(3)) or similar simplified form? 
    # Let's re-calculate carefully.
    # a = 2 + sqrt(3)
    # b = 2 - sqrt(3)
    # 2a + b = 2*(2 + sqrt(3)) + (2 - sqrt(3)) = 4 + 2sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3)
    
    final_rational_part = 6
    final_radical_coefficient = 1
    
    # Construct canonical LaTeX string for the answer
    if final_radical_coefficient == 0:
        canonical_latex = f"{final_rational_part}"
    else:
        sign_str = "+" if final_radical_coefficient > 0 else "-"
        abs_coef = abs(final_radical_coefficient)
        # Format radical part: coef sqrt(radicand). If coef is 1, omit it.
        rad_latex = f"{abs_coef}\\sqrt{{{radicand}}}" if abs_coef != 1 else f"\\sqrt{{{radicand}}}"
        
        canonical_latex = f"{final_rational_part}{sign_str}{rad_latex}"

    # Construct question text using LaTeX delimiters
    equation_display = frozen_params["equation"]
    order_desc = frozen_params["order"]
    target_expr = frozen_params["target"]
    
    question_text = (f"Solve the quadratic equation {equation_display} for its roots. "
                     f"Let $a$ and $b$ be the two real roots ordered such that {order_desc}. "
                     f"Compute the value of ${target_expr}$.")

    # Construct correct_answer dict with required fields
    correct_answer = {
        "value": result_value,  # This is a float for JSON serialization compatibility if needed, but spec says rational/radical. 
                               # However, structured comparison usually implies exact types or specific string representations.
                               # Given the instruction "correct_answer must include result with rational, radical_coefficient...",
                               # we should return a dict structure inside correct_answer? Or is 'value' enough?
                               # Re-reading: "correct_answer must include result with rational, radical_coefficient (may be +1 or -1), radicand, and canonical_latex."
    }
    
    # Adjusting correct_answer to match the specific schema requested in text description of fields.
    # The prompt says: "correct_answer must include result with rational, radical_coefficient..., radicand, and canonical_latex"
    # This implies 'correct_answer' itself might be a dict or we need to embed these. 
    # Looking at typical patterns for such tasks: often correct_answer is the string latex OR a structured object.
    # Let's assume correct_answer should contain the breakdown as described if it says "must include".
    # However, usually in these API contexts, 'correct_answer' is the final answer value (string or number). 
    # But the instruction explicitly lists fields: rational, radical_coefficient, radicand, canonical_latex.
    # I will structure correct_answer as a dictionary containing these if that's what "include" implies strictly, 
    # OR perhaps 'correct_answer' is the string and those are separate? No, it says "must include".
    # Let's make correct_answer an object with these keys to be safe against structured comparison.
    
    final_rational = 6
    
    corrected_correct_answer = {
        "rational": final_rational,
        "radical_coefficient": final_radical_coefficient,
        "radicand": radicand,
        "canonical_latex": canonical_latex
    }

    # Oracle payload must exactly equal frozen sampled parameters
    oracle_payload = frozen_params.copy()

    return {
        "question_text": question_text,
        "correct_answer": corrected_correct_answer,
        "oracle_payload": oracle_payload
    }