# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    p1_num, p1_den = frozen_params["p1"]
    p2_num, p2_den = frozen_params["p2"]
    
    fraction_p1 = FractionOps.from_parts(p1_num, p1_den)
    fraction_p2 = FractionOps.from_parts(p2_num, p2_den)
    
    product_fraction = FractionOps.mul(fraction_p1, fraction_p2)
    
    numerator = product_fraction.numerator
    denominator = product_fraction.denominator
    
    latex_str = f"\\frac{{{numerator}}}{{denominator}}"
    
    question_text = r"\text{What is the probability of both events occurring? } \left( p_1=\frac{\text{" + str(p1_num) + "}}{\text{" + str(p1_den) + "}}, p_2=\frac{\text{" + str(p2_num) + "}}{\text{" + str(p2_den) + "}} \right)"
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": latex_str
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }