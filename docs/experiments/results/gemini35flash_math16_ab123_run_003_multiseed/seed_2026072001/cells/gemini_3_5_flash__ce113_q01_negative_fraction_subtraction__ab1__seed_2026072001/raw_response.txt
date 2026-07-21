def generate(level=1, **kwargs):
    expression = "3/7 - (-1/4)"
    
    # 3/7 - (-1/4) = 3/7 + 1/4 = 12/28 + 7/28 = 19/28
    numerator = 19
    denominator = 28
    canonical_latex = "\\frac{19}{28}"
    
    question_text = "Evaluate the following expression: \\(\\frac{3}{7} - \\left(-\\frac{1}{4}\\right)\\)"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "expression": expression
        }
    }