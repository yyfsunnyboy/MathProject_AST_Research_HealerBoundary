def generate(level=1, **kwargs):
    base = 7
    expression_str = "7**10 * 7**2 / 7**4"
    
    # Calculate the exponent: 10 + 2 - 4 = 8
    final_exponent = 8
    
    question_text = f"Simplify {expression_str}."
    correct_answer = {"base": base, "exponent": final_exponent}
    oracle_payload = {"base": base, "expression": expression_str, "required_form": "power_of_same_base"}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }