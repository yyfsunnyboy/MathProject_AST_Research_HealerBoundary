# -*- coding: utf-8 -*-
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    f1 = FractionOps.create(9, 22)
    f2 = FractionOps.create(11, 18)
    f3 = FractionOps.create(23, 22)
    f4 = FractionOps.create(7, 18)

    term1 = FractionOps.add(f1, f2)
    term2 = FractionOps.sub(f3, f4)
    result = FractionOps.sub(term1, term2)

    if isinstance(result, dict):
        num = result["numerator"]
        den = result["denominator"]
    else:
        num = result.numerator
        den = result.denominator

    try:
        latex = FractionOps.to_latex(result)
    except AttributeError:
        latex = f"\\frac{{{num}}}{{{den}}}"

    question_text = (
        "Evaluate the following expression:\n"
        "\\[ \\frac{9}{22} + \\frac{11}{18} - \\left(\\frac{23}{22} - \\frac{7}{18}\\right) \\]"
    )

    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": num,
            "denominator": den,
            "canonical_latex": latex,
        },
        "oracle_payload": {
            "expression": "9/22 + 11/18 - (23/22 - 7/18)"
        }
    }