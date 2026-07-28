def generate(level=1, **kwargs):
    import fractions
    
    expression = "3/7 - (-1/4)"
    
    # Calculate correct answer manually to ensure accuracy without external libraries for the core logic demonstration
    # 3/7 - (-1/4) = 3/7 + 1/4
    # Common denominator is 28
    # (3*4)/28 + (1*7)/28 = 12/28 + 7/28 = 19/28
    
    numerator = 19
    denominator = 28
    
    canonical_latex = f"\\frac{{{numerator}}}{{denominator}}"
    
    return {
        "question_text": r"\text{Calculate the difference: } \frac{3}{7} - \left(-\frac{1}{4}\right)",
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {"expression": expression}
    }