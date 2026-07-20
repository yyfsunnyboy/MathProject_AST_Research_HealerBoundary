def generate(level=1, **kwargs):
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Calculate correct answer: 3/7 + 1/4 = (12+7)/28 = 19/28
    numerator = 19
    denominator = 28
    
    return {
        "question_text": r"Compute the result of $\\frac{3}{7} - \\left(-\\frac{1}{4}\\right)$.",
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": f"$\\\\frac{{{numerator}}}{{{{{denominator}}}}}$"
        },
        "oracle_payload": frozen_params
    }