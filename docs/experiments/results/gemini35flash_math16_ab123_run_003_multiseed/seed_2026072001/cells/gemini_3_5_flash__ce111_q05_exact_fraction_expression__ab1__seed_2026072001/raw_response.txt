def generate(level=1, **kwargs):
    expression = "9/22 + 11/18 - (23/22 - 7/18)"
    
    question_text = (
        "Evaluate the following expression and write the result as an irreducible fraction:\n"
        "\\[\n"
        "\\frac{9}{22} + \\frac{11}{18} - \\left(\\frac{23}{22} - \\frac{7}{18}\\right)\n"
        "\\]"
    )
    
    correct_answer = {
        "numerator": 4,
        "denominator": 11,
        "canonical_latex": "\\frac{4}{11}"
    }
    
    oracle_payload = {
        "expression": expression
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }