def generate(level=1, **kwargs):
    base = 7
    expression = "7**10 * 7**2 / 7**4"
    required_form = "power_of_same_base"
    
    exponent = 8
    
    question_text = (
        "Simplify the following expression and write the result as a power of 7:\n"
        "$$7^{10} \\times 7^2 \\div 7^4$$"
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