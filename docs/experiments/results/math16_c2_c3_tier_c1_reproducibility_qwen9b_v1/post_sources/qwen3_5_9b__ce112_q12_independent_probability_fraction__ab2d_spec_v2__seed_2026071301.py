# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # 2. Define frozen parameters directly. Do not read kwargs.
    p1_numerator = 2
    p1_denominator = 6
    p2_numerator = 1
    p2_denominator = 5

    # Create fractions using the specified API signatures
    f_p1 = FractionOps.from_parts(p1_numerator, p1_denominator)
    f_p2 = FractionOps.from_parts(p2_numerator, p2_denominator)

    # Compute the exact result using FractionOps.mul for computation.
    res = FractionOps.mul(f_p1, f_p2)

    correct_answer = {
        "numerator": int(res.numerator),
        "denominator": int(res.denominator),
        "canonical_latex": rf"\frac{{{res.numerator}}}{{{res.denominator}}}"
    }
    
    question_text = r"Given two independent events with probabilities $p_1 = \frac{2}{6}$ and $p_2 = \frac{1}{5}$, what is the probability that both events occur? Express your answer as an irreducible fraction."

    oracle_payload = {
        "p1": [2, 6], 
        "p2": [1, 5]
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }