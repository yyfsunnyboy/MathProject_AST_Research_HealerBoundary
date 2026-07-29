def generate(level=1, **kwargs):
    import json
    
    # Frozen sampled parameters as specified in the task description
    frozen_params = {
        "expression": "9/22 + 11/18 - (23/22 - 7/18)"
    }
    
    # Compute the correct answer for the expression: 9/22 + 11/18 - (23/22 - 7/18)
    from fractions import Fraction
    
    term1 = Fraction(9, 22)
    term2 = Fraction(11, 18)
    inner_parenthesis = Fraction(23, 22) - Fraction(7, 18)
    
    # Calculate the full expression: term1 + term2 - inner_parenthesis
    result = term1 + term2 - inner_parenthesis
    
    numerator = result.numerator
    denominator = result.denominator
    
    canonical_latex = f"\\frac{{{numerator}}}{{{{{denominator}}}}}"
    
    # Construct the return dictionary with exactly three required keys
    question_text = r"The value of the expression $9/22 + 11/18 - (23/22 - 7/18)$ is:"
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": canonical_latex
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }