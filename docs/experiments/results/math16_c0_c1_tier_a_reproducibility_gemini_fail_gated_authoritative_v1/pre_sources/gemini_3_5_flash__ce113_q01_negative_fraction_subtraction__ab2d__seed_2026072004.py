from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    expression = "3/7 - (-1/4)"
    
    a = FractionOps.create("3/7")
    b = FractionOps.create("-1/4")
    result = FractionOps.sub(a, b)
    
    numerator = result.numerator
    denominator = result.denominator
    canonical_latex = FractionOps.to_latex(result)
    
    question_text = (
        "Evaluate the following expression:\n"
        "\\[ \\frac{3}{7} - \\left(-\\frac{1}{4}\\right) \\]\n"
        "Express your answer as an irreducible fraction."
    )
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "expression": expression
        }
    }