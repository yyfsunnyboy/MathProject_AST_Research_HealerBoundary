# -*- coding: utf-8 -*-
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # 2. Define frozen parameters directly. Do not read kwargs.
    expression = "3/7 - (-1/4)"

    # 3. Compute the exact result using FractionOps.
    f1 = FractionOps.create(3, 7)
    f2 = FractionOps.create(-1, 4)
    res = FractionOps.sub(f1, f2)

    num = res.numerator
    den = res.denominator
    canonical_latex = f"\\frac{{{num}}}{{{den}}}"

    question_text = f"Evaluate the following expression:\n\n\\[ {expression} \\]"

    correct_answer = {
        "numerator": num,
        "denominator": den,
        "canonical_latex": canonical_latex,
    }

    oracle_payload = {
        "expression": expression,
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }