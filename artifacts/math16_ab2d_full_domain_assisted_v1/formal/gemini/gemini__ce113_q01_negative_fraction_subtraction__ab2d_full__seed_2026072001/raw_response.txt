from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = {
        "expression": "3/7 - (-1/4)"
    }
    
    left = FractionOps.from_parts(3, 7)
    right = FractionOps.from_parts(-1, 4)
    
    result = FractionOps.sub(left, right)
    
    correct_answer = {
        "numerator": result.numerator,
        "denominator": result.denominator,
        "canonical_latex": FractionOps.to_latex(result)
    }
    
    question_text = "精確計算\n\\[\n\\frac{3}{7}-\\left(-\\frac{1}{4}\right).\n\\]\n答案須化為最簡分數。"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }