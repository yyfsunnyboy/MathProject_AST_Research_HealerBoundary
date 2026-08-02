from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen params
    frozen_params = {
        "expression": "9/22 + 11/18 - (23/22 - 7/18)"
    }
    
    # Question text
    question_text = (
        "精確計算\n"
        "\\[\n"
        "\\frac{9}{22}+\\frac{11}{18}\n"
        "-\\left(\\frac{23}{22}-\\frac{7}{18}\\right).\n"
        "\\]\n"
        "答案須化為最簡分數。"
    )
    
    # Calculate using FractionOps
    f1 = FractionOps.from_parts(9, 22)
    f2 = FractionOps.from_parts(11, 18)
    f3 = FractionOps.from_parts(23, 22)
    f4 = FractionOps.from_parts(7, 18)
    
    sub1 = FractionOps.sub(f3, f4)
    add1 = FractionOps.add(f1, f2)
    result = FractionOps.sub(add1, sub1)
    
    # Construct correct_answer
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