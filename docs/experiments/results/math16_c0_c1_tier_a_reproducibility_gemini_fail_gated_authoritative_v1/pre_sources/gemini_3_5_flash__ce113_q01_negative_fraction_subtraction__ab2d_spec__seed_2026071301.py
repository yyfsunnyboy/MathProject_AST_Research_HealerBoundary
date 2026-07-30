from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    oracle_payload = {"expression": "3/7 - (-1/4)"}
    
    a = FractionOps.create(3, 7)
    b = FractionOps.create(-1, 4)
    res = FractionOps.sub(a, b)
    
    num = res.numerator
    den = res.denominator
    
    canonical_latex = f"\\frac{{{num}}}{{{den}}}"
    
    question_text = r"Evaluate the following expression: \[ \frac{3}{7} - \left(-\frac{1}{4}\right) \]"
    
    correct_answer = {
        "numerator": num,
        "denominator": den,
        "canonical_latex": canonical_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }