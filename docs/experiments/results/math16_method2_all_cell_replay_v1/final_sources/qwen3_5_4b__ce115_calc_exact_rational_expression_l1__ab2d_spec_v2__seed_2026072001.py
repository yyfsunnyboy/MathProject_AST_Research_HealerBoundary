# -*- coding: utf-8 -*-

from core.prompts.domain_function_library import FractionOps, LaTeXFormatter


def generate(level=1, **kwargs):
    # Frozen parameters extracted directly from task specification (not kwargs)
    frozen_params = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }

    # Parse decimal strings to Fractions exactly
    f_279 = FractionOps.create("2.79")
    f_893 = FractionOps.create("89.3")
    f_neg021 = FractionOps.create("-0.21")

    # Compute first product: 2.79 * 89.3
    prod1_num, prod1_den = FractionOps.mul(f_279, f_893)

    # Compute second product: -0.21 * 89.3 (sign is already included in the negative fraction)
    prod2_num, prod2_den = FractionOps.mul(f_neg021, f_893)

    # Perform subtraction based on sign logic from frozen params
    # First term has sign +1 -> add to result accumulator? 
    # Actually looking at structure: [ {left:A, right:B, sign:+}, {left:C, right:D, sign:-} ]
    # Interpretation: (A * B) - (C * D) where C and D are magnitudes from the second dict's values
    # But wait, 'sign' is part of the product definition. 
    # Let's re-read carefully: "products": [{"left": "-0.21", ...}] -> left already has sign.
    # The operation implied by typical arithmetic expression generation with these fields:
    # Term 1: (2.79) * (89.3) [sign +1 means positive term]
    # Term 2: (-0.21) * (89.3) [sign -1? Or is sign the operator?]
    
    # Re-evaluating based on "math16_exact_rational_expression" context usually involving sums/diffs of products.
    # If 'sign' indicates whether to add or subtract from a base, but there's no base...
    # Most likely interpretation for this specific frozen set pattern in these tasks:
    # Expression = (left_0 * right_0) - (abs(left_1) * right_1) ? 
    # Or simply sum the signed products? 
    # Given "sign": 1 and "-1", it often denotes +A - B.
    
    # Let's assume standard arithmetic expression construction:
    # Term A = left0 * right0 (positive contribution due to sign=1)
    # Term B = abs(left1) * right1 (negative contribution due to sign=-1, or just the product itself if negative)
    # However, 'left' in second item is "-0.21". 
    # If we treat it as: Result = (2.79 * 89.3) + (-0.21 * 89.3)? That would be simple distribution.
    # Let's look at the signs provided: sign=1 for first, sign=-1 for second. 
    # This likely implies: Term1 - Term2 where Term2 uses magnitude of left/right?
    
    # Alternative strict interpretation matching common dataset patterns (e.g., GSM8K/Math datasets):
    # The 'sign' field dictates the operation between two products or modifies a term.
    # Let's assume the expression is: P1 * sign1 + P2 * sign2 ? No, that's redundant if left has sign.
    
    # Most robust interpretation for "exact rational": 
    # Calculate T1 = 2.79 * 89.3
    # Calculate T2 = |-0.21| * 89.3 (magnitude) because the second item is subtracted?
    # Or simply: Result = (2.79 * 89.3) - (-0.21 * 89.3)? That would be addition of magnitudes.
    
    # Let's try to infer from typical difficulty level 1 math problems involving decimals converted to fractions.
    # Often it is: A * B + C * D or similar. 
    # If we take the literal values and apply operations based on 'sign':
    # Term 1 value = 2.79 * 89.3 (positive)
    # Term 2 value = -0.21 * 89.3 (already negative in left, but sign=-1 might mean subtract this term?)
    
    # Let's assume the operation is: 
    # Result = (Fraction(279/100) * Fraction(893/10)) + (-Fraction(21/100) * Fraction(893/10))?
    # That simplifies to 2.58*... - ...?
    
    # Let's go with the most direct arithmetic interpretation of a list of products where sign indicates addition/subtraction from zero:
    # Sum = (left[0] * right[0]) + (sign[1] * left[1] * right[1]) 
    # But wait, if left[1] is -0.21 and sign[1] is -1... that's double negative?
    
    # Let's reconsider the "products" list as defining terms in a sum:
    # Term 1: + (2.79 * 89.3)
    # Term 2: - (-0.21 * 89.3) -> This would be adding two positives? Unlikely for a subtraction problem.
    
    # Hypothesis B: The expression is simply the sum of the products as defined by their signed values, 
    # but 'sign' overrides or indicates direction relative to a positive base?
    
    # Let's try this specific logic often found in such generated tasks:
    # Expression = (left_0 * right_0) - (abs(left_1) * right_1) if sign is negative indicator for subtraction.
    # But left_1 is already "-0.21". 
    # If the task implies "Calculate A and B, then do op", but we have a list...
    
    # Let's assume the simplest exact arithmetic: 
    # Result = (Fraction(279/100) * Fraction(893/10)) - (Fraction(-21/100) * Fraction(893/10))? 
    # No, that would be A + B.
    
    # Let's assume the 'sign' field is the operator between two positive magnitudes derived from left/right?
    # Magnitude 1: |2.79| * 89.3
    # Magnitude 2: |-0.21| * 89.3 = 0.21 * 89.3
    # Operation based on sign[1]: if -1, subtract? 
    # So Result = (2.79 * 89.3) - (0.21 * 89.3)?
    
    # Let's calculate:
    # T1_num, T1_den = mul(279/100, 893/10) -> 249147 / 1000
    # T2_mag_num, T2_mag_den = mul(21/100, 893/10) -> 18753 / 1000
    
    # If we subtract: (249147 - 18753) / 1000 = 230394 / 1000
    # Simplify by dividing by GCD(230394, 1000). 
    # Both even. -> 115197 / 500.
    
    # Let's verify if this makes sense as a "level 1" problem. Yes, simple decimal multiplication and subtraction converted to fractions.
    
    t2_mag = FractionOps.create("0.21")
    prod2_num, prod2_den = FractionOps.mul(t2_mag, f_893)

    # Perform subtraction: T1 - T2_magnitude (assuming sign=-1 implies subtraction of the magnitude term formed by abs(left))
    res_num, res_den = FractionOps.sub(prod1_num, prod2_num)

    # Simplify fraction if needed (Fraction usually handles this internally or we can ensure irreducible via GCD logic in ops)
    # Assuming FractionOps creates irreducible fractions. If not, reduce manually:
    from math import gcd
    common = gcd(res_num, res_den)
    res_num //= common
    res_den //= common

    # Format for correct_answer schema: "p/q" and LaTeX
    value_str = f"{res_num}/{res_den}"
    
    latex_val = LaTeXFormatter.to_latex(frac=res_num, denom=res_den)
    canonical_latex = r"\frac{" + str(res_num) + "}{" + str(res_den) + r"}"

    # Construct Question Text with formal LaTeX delimiters
    term1_latex = f"{LaTeXFormatter.to_decimal(2.79)} \\times {LaTeXFormatter.to_decimal(89.3)}"
    term2_latex = f"|{-0.21}| \\times 89.3" # Using absolute value to handle the negative input as magnitude for subtraction
    
    question_text = r"\text{Calculate: } " + latex_val.replace(" ", "") 
    # Wait, need full expression in text
    q_latex_expr = f"{LaTeXFormatter.to_decimal(2.79)} \\cdot {LaTeXFormatter.to_decimal(89.3)} - |{-0.21}| \\cdot 89.3"
    
    question_text = r"\text{Compute the exact value of: } " + q_latex_expr

    correct_answer_obj = {
        "value": value_str,
        "canonical_latex": canonical_latex
    }

    # Ensure return structure matches spec exactly
    result_dict = {
        "question_text": question_text,
        "correct_answer": correct_answer_obj,
        "oracle_payload": frozen_params
    }

    return result_dict
