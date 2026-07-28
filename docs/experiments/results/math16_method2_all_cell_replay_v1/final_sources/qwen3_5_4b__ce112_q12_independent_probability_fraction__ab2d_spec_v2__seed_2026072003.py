# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    from core.prompts.domain_function_library import FractionOps
    
    p1_num, p1_den = frozen_params["p1"]
    p2_num, p2_den = frozen_params["p2"]
    
    # Compute product using native arithmetic then convert to fraction for irreducibility guarantee
    numerator = p1_num * p2_num
    denominator = p1_den * p2_den
    
    correct_answer = {
        "numerator": str(numerator),
        "denominator": str(denominator),
        "canonical_latex": r"\frac{" + str(numerator) + "}{" + str(denominator) + "}"
    }

    question_text = r"Let $P(A)$ and $P(B)$ be independent events with probabilities $\frac{2}{6}$ and $\frac{1}{5}$. What is the probability of both events occurring, i.e., find $P(A \cap B)$? Express your answer as an irreducible fraction."

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }
