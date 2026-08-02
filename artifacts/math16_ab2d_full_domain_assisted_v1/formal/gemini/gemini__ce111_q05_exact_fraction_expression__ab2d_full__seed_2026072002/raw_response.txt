from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen params
    frozen_params = {
        "expression": "9/22 + 11/18 - (23/22 - 7/18)"
    }
    
    # Construct fractions
    f1 = FractionOps.from_parts(9, 22)
    f2 = FractionOps.from_parts(11, 18)
    f3 = FractionOps.from_parts(23, 22)
    f4 = FractionOps.from_parts(7, 18)
    
    # Evaluate expression: f1 + f2 - (f3 - f4)
    sum1 = FractionOps.add(f1, f2)
    diff1 = FractionOps.sub(f3, f4)
    result = FractionOps.sub(sum1, diff1)
    
    # Extract numerator and denominator
    numerator = result.numerator
    denominator = result.denominator
    
    # Generate canonical latex
    canonical_latex = FractionOps.to_latex(result)
    
    question_text = (
        "精確計算\n"
        "\\[\n"
        "\\frac{9}{22}+\\frac{11}{18}\n"
        "-\\left(\\frac{23}{22}-\\frac{7}{18}\\right).\n"
        "\\]\n"
        "答案須化為最簡分數。"
    )
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }