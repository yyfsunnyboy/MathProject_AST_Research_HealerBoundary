def generate(level=1, **kwargs):
    expression = "3/7 - (-1/4)"
    
    # Parse and compute: 3/7 + 1/4 = (12 + 7) / 28 = 19/28
    numerator = 19
    denominator = 28
    
    return {
        "question_text": f"Simplify the expression $\\frac{{{expression}}}$.",
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": r"\frac{19}{28}"
        },
        "oracle_payload": {"expression": expression}
    }