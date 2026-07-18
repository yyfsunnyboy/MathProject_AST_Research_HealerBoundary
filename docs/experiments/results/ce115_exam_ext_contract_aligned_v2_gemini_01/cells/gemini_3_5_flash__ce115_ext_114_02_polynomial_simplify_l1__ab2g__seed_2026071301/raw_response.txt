def generate(level=1, **kwargs):
    expression = "(5*x**2 - 2*x) - (4 - 3*x)"
    question_text = f"Simplify the following polynomial expression:\n\n{expression}"
    
    correct_answer = {
        "coefficients": {
            "2": 5,
            "1": 1,
            "0": -4
        }
    }
    
    oracle_payload = {
        "expression": expression
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }