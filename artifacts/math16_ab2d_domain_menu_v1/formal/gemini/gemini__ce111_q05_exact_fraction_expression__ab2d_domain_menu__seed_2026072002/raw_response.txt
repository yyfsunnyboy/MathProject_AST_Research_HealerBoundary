from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    question_text = "精確計算\n\\[\n\\frac{9}{22}+\\frac{11}{18}\n-\\left(\\frac{23}{22}-\\frac{7}{18}\\right).\n\\]\n答案須化為最簡分數。"
    
    oracle_payload = {
        "expression": "9/22 + 11/18 - (23/22 - 7/18)"
    }
    
    a = FractionOps.from_parts(9, 22)
    b = FractionOps.from_parts(11, 18)
    c = FractionOps.from_parts(23, 22)
    d = FractionOps.from_parts(7, 18)
    
    sub1 = FractionOps.sub(c, d)
    add1 = FractionOps.add(a, b)
    res = FractionOps.sub(add1, sub1)
    
    correct_answer = {
        "numerator": res.numerator,
        "denominator": res.denominator,
        "canonical_latex": FractionOps.to_latex(res)
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }