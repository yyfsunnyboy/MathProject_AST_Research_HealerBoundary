from fractions import Fraction
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    expression_str = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Calculate using FractionOps
    t1 = FractionOps.create(Fraction(9, 22))
    t2 = FractionOps.create(Fraction(11, 18))
    t3 = FractionOps.create(Fraction(-23, 22))
    t4 = FractionOps.create(Fraction(7, 18))
    
    res = FractionOps.add(t1, t2)
    res = FractionOps.add(res, t3)
    res = FractionOps.add(res, t4)
    
    numerator = res.numerator
    denominator = res.denominator
    canonical_latex = FractionOps.to_latex(res)
    
    question_text = r"Evaluate the following expression: \[\frac{9}{22} + \frac{11}{18} - \left(\frac{23}{22} - \frac{7}{18}\right)\]"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {
            "expression": expression_str
        }
    }