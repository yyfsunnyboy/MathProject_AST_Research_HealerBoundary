# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # 2. Define frozen parameters directly. Do not read kwargs.
    p1_parts = [2, 6]
    p2_parts = [1, 5]
    
    numerator_p1, denominator_p1 = p1_parts[0], p1_parts[1]
    numerator_p2, denominator_p2 = p2_parts[0], p2_parts[1]
    
    # Create fractions from parts using the specified API signature
    frac1 = FractionOps.from_parts(numerator_p1, denominator_p1)
    frac2 = FractionOps.from_parts(numerator_p2, denominator_p2)
    
    # 3. Compute the exact result (independent probability -> multiplication)
    product_frac = FractionOps.mul(frac1, frac2)
    
    num_res = product_frac.numerator
    den_res = product_frac.denominator
    
    # Construct canonical LaTeX for irreducible fraction: \frac{num}{den}
    question_text = r"Given two independent events with probabilities $p_1 = \frac{%d}{%d}$ and $p_2 = \frac{%d}{%d}$, what is the probability that both events occur? Express your answer as an irreducible fraction." % (numerator_p1, denominator_p1, numerator_p2, denominator_p2)
    
    correct_answer = {
        "numerator": num_res,
        "denominator": den_res,
        "canonical_latex": r"\frac{%d}{%d}" % (num_res, den_res),
    }
    
    oracle_payload = {"p1": p1_parts, "p2": p2_parts}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }