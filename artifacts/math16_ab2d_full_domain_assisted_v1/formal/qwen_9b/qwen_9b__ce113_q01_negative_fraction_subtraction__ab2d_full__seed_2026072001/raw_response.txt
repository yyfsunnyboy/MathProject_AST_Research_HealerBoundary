from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Construct left operand: 3/7
    num_left = 3
    den_left = 7
    a = FractionOps.from_parts(num_left, den_left)
    
    # Construct right operand: -1/4 (preserve negative numerator as per instructions)
    num_right = -1
    den_right = 4
    b = FractionOps.from_parts(num_right, den_right)
    
    # Compute subtraction: left - right
    result_fraction = FractionOps.sub(a, b)
    
    # Assemble correct_answer according to the contract
    numerator = result_fraction.numerator
    denominator = result_fraction.denominator
    
    return {
        "question_text": r"精確計算 \[\frac{3}{7}-\left(-\frac{1}{4}\right).\] 答案須化為最簡分數。",
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": FractionOps.to_latex(result_fraction)
        },
        "oracle_payload": frozen_params
    }