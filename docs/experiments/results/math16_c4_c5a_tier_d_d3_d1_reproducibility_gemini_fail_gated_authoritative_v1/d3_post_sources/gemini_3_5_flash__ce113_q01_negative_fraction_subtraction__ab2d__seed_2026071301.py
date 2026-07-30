from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    expression = "3/7 - (-1/4)"
    
    a = FractionOps.create("3/7")
    b = FractionOps.create("-1/4")
    result = FractionOps.sub(a, b)
    
    question_text = (
        "Evaluate the following expression:\n"
        "\\[ \\frac{3}{7} - \\left(-\\frac{1}{4}\\right) \\]\n"
        "Express your answer as an irreducible fraction."
    )
    
    correct_answer = {
        "numerator": result.numerator,
        "denominator": result.denominator,
        "canonical_latex": FractionOps.to_latex(result)
    }
    
    oracle_payload = {
        "expression": expression
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }