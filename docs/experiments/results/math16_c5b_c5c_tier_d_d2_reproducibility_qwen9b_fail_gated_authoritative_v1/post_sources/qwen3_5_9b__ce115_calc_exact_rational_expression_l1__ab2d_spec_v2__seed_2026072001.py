# -*- coding: utf-8 -*-
from fractions import Fraction

def generate(level=1, **kwargs):
    # Frozen sampled parameters as defined in task specification
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    # Helper to convert decimal string to Fraction
    def str_to_frac(s):
        return Fraction(int(float(s) * 100), 100).limit_denominator() if '.' in s else int(s) / 1
    
    # Parse left and right operands from the first product term (index 0) as per typical expression structure for this task type
    # Term 1: sign=1, so + (left * right) -> but looking at standard rational arithmetic tasks of this format (ce115), 
    # it usually implies an addition/subtraction chain or a specific product sum. 
    # Given the parameters: {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, ...]}
    # This looks like two terms to be summed: (2.79 * 89.3) + (-0.21 * 89.3)? 
    # Or perhaps it's just a list of products where the sign applies to the product?
    # Let's assume the expression is sum(sign_i * left_i * right_i).
    
    terms = []
    for item in frozen_params["products"]:
        l_val = str_to_frac(item["left"])
        r_val = str_to_frac(item["right"])
        sign = int(item["sign"])
        
        # Calculate product exactly using Fraction arithmetic (native Python fractions are sufficient and exact)
        term_value = l_val * r_val
        
        if sign == 1:
            terms.append(term_value)
        else:
            terms.append(-term_value)

    # Sum all terms to get the final result
    total_sum = sum(terms, Fraction(0))
    
    # Simplify and ensure irreducible form (Fraction does this automatically on creation/ops)
    num = total_sum.numerator
    den = total_sum.denominator
    
    # Construct canonical LaTeX for p/q
    if den == 1:
        latex_ans = f"{num}"
    else:
        latex_ans = rf"\frac{{{num}}}{{{den}}}"

    question_text = (f"Calculate the exact value of the expression defined by the products. "
                     f"The terms are given as pairs with signs: {', '.join([str(t) for t in frozen_params['products']])}.")
    
    correct_answer_value = str(total_sum) # Irreducible p/q string (e.g., "-1/2" or "3")
    canonical_latex = latex_ans
    
    return {
        "question_text": question_text,
        "correct_answer": f"value={correct_answer_value}, canonical_latex={canonical_latex}",
        "oracle_payload": frozen_params
    }