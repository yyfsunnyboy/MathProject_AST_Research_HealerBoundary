from core.prompts.domain_function_library import RadicalOps, FractionOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    expression = "9/(4 - sqrt(7))"
    required_form = "a + b*sqrt(7)"
    target_expression = "a + b"
    
    oracle_payload = {
        "expression": expression,
        "required_form": required_form,
        "target_expression": target_expression
    }
    
    # Parameters for the expression 9 / (4 - 1*sqrt(7))
    numerator = 9
    denom_rational = 4
    denom_radical_coeff = -1
    radicand = 7
    
    # Rationalize the denominator using the domain API
    a_frac, b_frac, rad = RadicalOps.rationalize_linear_denominator(
        numerator, denom_rational, denom_radical_coeff, radicand
    )
    
    # Convert Fraction results to exact representation (ints)
    a = FractionOps.to_exact(a_frac)
    b = FractionOps.to_exact(b_frac)
    value = FractionOps.to_exact(a_frac + b_frac)
    
    # Construct the question text
    question_text = (
        f"Rationalize the denominator of the expression: \\frac{{9}}{{4 - \\sqrt{{7}}}}. "
        f"Write the result in the form {required_form}, and find the value of {target_expression}."
    )
    
    correct_answer = {
        "a": a,
        "b": b,
        "radicand": rad,
        "value": value
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }