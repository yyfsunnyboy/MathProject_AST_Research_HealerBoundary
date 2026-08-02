from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = {
        "expression": "9/22 + 11/18 - (23/22 - 7/18)"
    }
    
    # Construct fractions
    a = FractionOps.from_parts(9, 22)
    b = FractionOps.from_parts(11, 18)
    c = FractionOps.from_parts(23, 22)
    d = FractionOps.from_parts(7, 18)
    
    # Evaluate expression: a + b - (c - d)
    sum_ab = FractionOps.add(a, b)
    diff_cd = FractionOps.sub(c, d)
    result = FractionOps.sub(sum_ab, diff_cd)
    
    question_text = "精確計算\n\\[\n\\frac{9}{22}+\\frac{11}{18}\n-\\left(\\frac{23}{22}-\\frac{7}{18}\\right).\n\\]\n答案須化為最簡分數。"
    
    correct_answer = {
        "numerator": result.numerator,
        "denominator": result.denominator,
        "canonical_latex": FractionOps.to_latex(result)
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }