import json
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 100

def generate(level=1, **kwargs):
    frozen_params = {"expression": "9/(4 - sqrt(7))", "required_form": "a + b*sqrt(7)", "target_expression": "a + b"}
    
    numerator = Fraction(9)
    denom_rational = 4
    denom_radical_coeff = -1
    radicand = 7
    
    a, b, r = RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand)
    
    correct_answer_dict = {
        "a": int(a),
        "b": int(b),
        "radicand": int(r),
        "value": a + b
    }
    
    return {
        "question_text": f"Simplify the expression: 9/(4 - sqrt(7)) into the form a + b*sqrt({r}). Provide integers a, b and their sum.",
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }