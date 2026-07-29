# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    term1 = FractionOps.from_parts(9, 22)
    term2 = FractionOps.from_parts(11, 18)
    sub_term_inner = FractionOps.sub(FractionOps.from_parts(23, 22), FractionOps.from_parts(7, 18))
    
    result = FractionOps.add(term1, FractionOps.add(term2, FractionOps.neg(sub_term_inner)))

    numerator = result.numerator
    denominator = result.denominator
    
    question_text = r"\text{Compute the exact value of: } $\frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})$"
    
    canonical_latex = f"\\frac{{{numerator}}}{{denominator}}"

    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }