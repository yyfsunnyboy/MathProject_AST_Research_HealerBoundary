def generate(level=1, **kwargs):
    import json
    
    # Frozen parameters from specification
    frozen_params = {
        "denominator": "4-sqrt(7)", 
        "numerator": 9, 
        "radicand": 7
    }
    
    a = 4
    b = 1
    r = 7
    
    # Calculate the rationalized denominator magnitude: a^2 - r*b^2
    # For (a - sqrt(r)), this is a^2 - r. 
    # Here, conjugate of (4-sqrt(7)) is (4+sqrt(7)). Product with original gives 16-7=9.
    
    rationalized_denom_val = a**2 - r * b**2
    
    question_text = f"Simplify the expression $\\frac{{{frozen_params['numerator']}}}{{{frozen_params['denominator']}}}$ by multiplying both numerator and denominator by its conjugate, then determine the integer value of the resulting rationalized denominator."
    
    correct_answer = rationalized_denom_val
    
    oracle_payload = json.dumps(frozen_params)

    return {
        "question_text": question_text,
        "correct_answer": int(correct_answer),
        "oracle_payload": oracle_payload
    }
