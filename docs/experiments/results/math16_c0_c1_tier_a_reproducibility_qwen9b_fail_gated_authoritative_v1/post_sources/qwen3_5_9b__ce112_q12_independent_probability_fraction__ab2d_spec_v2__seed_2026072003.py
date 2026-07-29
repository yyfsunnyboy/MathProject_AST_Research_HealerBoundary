# -*- coding: utf-8 -*-
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly per contract
    p1_parts = [2, 6]
    p2_parts = [1, 5]

    # Construct fractions from parts using the specified API signature
    frac_p1 = FractionOps.from_parts(p1_parts[0], p1_parts[1])
    frac_p2 = FractionOps.from_parts(p2_parts[0], p2_parts[1])

    # Compute product exactly
    result_frac = FractionOps.mul(frac_p1, frac_p2)

    numerator = int(result_frac.numerator)
    denominator = int(result_frac.denominator)

    # Build canonical LaTeX for irreducible fraction: \frac{num}{den}
    question_text = r"Two independent events have probabilities $p_1$ and $p_2$. If the probability of event 1 is $\frac{%d}{%d}$ and the probability of event 2 is $\frac{%d}{%d}$, what is the probability that both events occur? Express your answer as an irreducible fraction." % (numerator // gcd(numerator, denominator), denominator // gcd(numerator, denominator))

    # Correct answer structure
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": r"\frac{%d}{%d}" % (numerator, denominator)
    }

    oracle_payload = {"p1": p1_parts, "p2": p2_parts}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }