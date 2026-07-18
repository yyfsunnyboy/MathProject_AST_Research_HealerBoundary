def generate(level=1, **kwargs):
    # Frozen parameters
    base = 7
    expression = "7**10 * 7**2 / 7**4"
    required_form = "power_of_same_base"
    
    # Calculate exponent: 10 + 2 - 4 = 8
    exponent = 8
    
    question_text = (
        f"Simplify the expression: {expression.replace('**', '^')}. "
        f"Write your answer as a power of the same base."
    )
    
    correct_answer = {
        "base": base,
        "exponent": exponent
    }
    
    oracle_payload = {
        "base": base,
        "expression": expression,
        "required_form": required_form
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }