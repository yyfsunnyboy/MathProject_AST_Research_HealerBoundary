# -*- coding: utf-8 -*-
from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per task specification
    frozen_params = {"expression": "3/7 - (-1/4)"}

    # Parse the first fraction from the expression string manually to avoid eval/exec on full expr if needed,
    # but since we have specific logic for this exact case: 3/7 - (-1/4), let's parse components.
    # The task is specifically "math16_negative_fraction_subtraction" with expression "3/7 - (-1/4)".
    
    # We need to compute 3/7 - (-1/4) which equals 3/7 + 1/4.
    # However, the instruction says: Use FractionOps.sub for computation.
    # Let's parse the operands based on the frozen expression string provided in kwargs or hardcoded?
    # Rule: "Do not read frozen parameters from kwargs". So we use the hardcoded value defined above.
    
    expr = frozen_params["expression"]  # "3/7 - (-1/4)"
    
    # We must implement parsing logic to extract operands for FractionOps without using eval/exec on arbitrary strings if possible, 
    # but given the strict constraint and specific expression, we can hardcode the extraction or use a safe parser.
    # Since this is a generated task with fixed frozen params in this context:
    
    # Extracting numbers from "3/7 - (-1/4)" safely for FractionOps usage.
    import re
    
    # Pattern to match fractions like 3/7 and -1/4 (including negative sign before parenthesis)
    parts = re.findall(r'(-?\d+)/(\d+)', expr.replace(' ', '')) 
    # This regex might miss the second fraction if it's inside parens or has a minus.
    # Let's try to split by ' - ' and handle signs carefully.
    
    # Better approach for this specific known expression:
    # Expression is "3/7 - (-1/4)". 
    # Operand 1: 3/7 -> num=3, den=7
    # Operator: subtraction '-'
    # Operand 2: inside parens "-(-1/4)"? No, it's minus negative one fourth.
    # The string is "3/7 - (-1/4)". 
    # We need to extract the second fraction which is effectively +1/4 mathematically but represented as subtracting a negative.
    
    # Let's use a robust regex split or manual parsing for this specific format: num/den op (num/den)
    match = re.search(r'(-?\d+)/(\d+)\s*-\s*\((-?\d+)/(\d+)\)', expr)
    
    if not match:
        raise ValueError("Expression format mismatch")

    n1, d1 = int(match.group(1)), int(match.group(2))
    n2, d2 = int(match.group(3)), int(match.group(4)) # This captures -1 from (-1/4)
    
    # The operation is subtraction: FractionOps.sub(frac1, frac2) where frac2 includes the negative sign.
    f1 = FractionOps.from_parts(n1, d1)
    f2 = FractionOps.from_parts(n2, d2)
    
    result_frac = FractionOps.sub(f1, f2)
    
    # Construct correct_answer dict with numerator, denominator, canonical_latex
    num_ans = result_frac.numerator
    den_ans = result_frac.denominator
    
    # Canonical LaTeX for fraction: \frac{num}{den}
    import math
    if den_ans < 0:
        num_ans = -num_ans
        den_ans = -den_ans
        
    canonical_latex = f"\\frac{{{num_ans}}}{{{den_ans}}}"
    
    correct_answer_dict = {
        "numerator": num_ans,
        "denominator": den_ans,
        "canonical_latex": canonical_latex
    }

    # Construct question_text using formal LaTeX delimiters
    q_tex_n1 = f"\\frac{{{n1}}}{{{d1}}}"
    q_tex_op = "-"
    q_tex_paren2_start = "("
    q_tex_neg_num2 = str(n2) if n2 < 0 else "" # If negative, include sign. Note: regex captured -1 as string "-1" usually? 
    # Let's reconstruct the second fraction LaTeX carefully.
    
    # Re-extracting to ensure correct signs for display
    s_expr = expr.replace(' ', '')
    parts_list = re.findall(r'(-?\d+)/(\d+)', s_expr)
    if len(parts_list) < 2:
        raise ValueError("Could not parse two fractions")
    
    # The regex above might have missed the second one due to parens. 
    # Let's rely on the match object groups which worked for "3/7 - (-1/4)"?
    # Wait, re.search with that pattern expects exactly: num/den op (num/den)
    # If n2 is negative, it matches "-1".
    
    q_tex_n2 = f"\\frac{{{n2}}}{{{d2}}}" if d2 != 0 else "undefined" 
    # Actually for display we want the LaTeX of -1/4 as \frac{-1}{4} or (-\frac{1}{4})? Usually standard is \frac{-1}{4}.
    
    question_text = f"{q_tex_n1} {q_tex_op} ({q_tex_n2})"

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }