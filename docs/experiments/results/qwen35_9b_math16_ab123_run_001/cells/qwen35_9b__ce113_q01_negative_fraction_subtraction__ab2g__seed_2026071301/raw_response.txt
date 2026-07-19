def generate(level=1, **kwargs):
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Calculate correct answer for 3/7 - (-1/4) which is 3/7 + 1/4
    # Common denominator: 28
    # 3*4 / 28 + 1*7 / 28 = (12 + 7) / 28 = 19/28
    numerator = 19
    denominator = 28
    
    correct_answer_numer = numerator
    correct_answer_denom = denominator
    canonical_latex = f"\\frac{{{numerator}}}{{{denominator}}}"
    
    question_text = (f"Simplify the following expression:\n\n$$ {frozen_params['expression']} $$")
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": correct_answer_numer,
            "denominator": correct_answer_denom,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }