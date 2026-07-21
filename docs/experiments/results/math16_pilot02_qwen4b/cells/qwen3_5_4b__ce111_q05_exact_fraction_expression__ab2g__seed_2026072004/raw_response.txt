def generate(level=1, **kwargs):
    expression = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Calculate the exact value manually to ensure correctness without external libraries
    from fractions import Fraction
    
    term1 = Fraction(9) / 22
    term2 = Fraction(11) / 18
    inner_parenthesis = (Fraction(23) / 22 - Fraction(7) / 18)
    
    # expression is: term1 + term2 - inner_parenthesis
    result = term1 + term2 - inner_parenthesis
    
    numerator = result.numerator
    denominator = result.denominator
    
    correct_answer_latex = f"\\frac{{{numerator}}}{{denominator}}" if False else f"\\frac{{{numerator}}}{{denominator}}".replace("denominator", str(denominator))
    
    question_text = r"\text{Simplify the expression: } $\frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})$"

    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": f"\\frac{{{numerator}}}{{denominator}}".replace("denominator", str(denominator))
        },
        "oracle_payload": {"expression": expression}
    }