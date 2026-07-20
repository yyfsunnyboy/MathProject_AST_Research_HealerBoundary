def generate(level=1, **kwargs):
    from fractions import Fraction as PyFraction
    
    expression = "3/7 - (-1/4)"
    
    # Parse terms manually based on frozen parameter for precision without external heavy imports if needed, 
    # but adhering to domain API constraints where possible. Since direct parsing of "-(-1/4)" requires care,
    # we will compute the value and ensure irreducible form.
    term_a = PyFraction(3) / PyFraction(7)
    term_b = PyFraction(-1) / PyFraction(4)
    
    # Calculate result: a - b
    result = term_a - term_b
    
    numerator, denominator = int(result.numerator), int(result.denominator)
    
    correct_answer_data = {
        "numerator": str(numerator),
        "denominator": str(denominator),
        "canonical_latex": f"${\\frac{{{numerator}}}{{{denominator}}}$}"
    }

    return {
        "question_text": r"Calculate the value of: \(\text{3/7} - (-\text{1/4})\).",
        "correct_answer": correct_answer_data,
        "oracle_payload": {"expression": expression}
    }