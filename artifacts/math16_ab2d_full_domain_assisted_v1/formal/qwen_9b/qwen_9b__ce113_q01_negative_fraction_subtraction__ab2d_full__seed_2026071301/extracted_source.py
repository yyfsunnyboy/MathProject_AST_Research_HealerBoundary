from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Construct left operand: 3/7
    left_num = 3
    left_den = 7
    left_frac = FractionOps.from_parts(left_num, left_den)
    
    # Construct right operand: -1/4 (preserve negative numerator as per instruction)
    right_num = -1
    right_den = 4
    right_frac = FractionOps.from_parts(right_num, right_den)
    
    # Compute subtraction: left - right
    result_frac = FractionOps.sub(left_frac, right_frac)
    
    # Assemble correct_answer according to the contract
    numerator = result_frac.numerator
    denominator = result_frac.denominator
    canonical_latex = FractionOps.to_latex(result_frac)
    
    return {
        "question_text": "\n精確計算\n\\[ \\frac{3}{7}-(-\\frac{1}{4}). \\\\\\] 答案須化為最簡分數。",
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }