from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Construct operands: 3/7 and -1/4 (using negative numerator for the second term)
    left = FractionOps.from_parts(3, 7)
    right = FractionOps.from_parts(-1, 4)
    
    # Compute subtraction: left - right => 3/7 - (-1/4)
    result = FractionOps.sub(left, right)
    
    return {
        "question_text": "精確計算\n\\[ \\frac{3}{7}-\\left(-\\frac{1}{4}\\right). \\]\n答案須化為最簡分數。",
        "correct_answer": {
            "numerator": result.numerator,
            "denominator": result.denominator,
            "canonical_latex": FractionOps.to_latex(result)
        },
        "oracle_payload": frozen_params
    }