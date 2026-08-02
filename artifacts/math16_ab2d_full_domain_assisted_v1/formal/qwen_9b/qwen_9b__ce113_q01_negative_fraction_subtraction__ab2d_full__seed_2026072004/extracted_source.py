from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Construct left operand: 3/7
    num_left = 3
    den_left = 7
    
    # Construct right operand: -1/4 (preserve negative numerator as per instructions)
    num_right = -1
    den_right = 4
    
    a = FractionOps.from_parts(num_left, den_left)
    b = FractionOps.from_parts(num_right, den_right)
    
    result = FractionOps.sub(a, b)
    
    return {
        "question_text": r"精確計算 \[\frac{3}{7}-\left(-\frac{1}{4}\right).\] 答案須化為最簡分數。",
        "correct_answer": {
            "numerator": result.numerator,
            "denominator": result.denominator,
            "canonical_latex": FractionOps.to_latex(result)
        },
        "oracle_payload": frozen_params
    }