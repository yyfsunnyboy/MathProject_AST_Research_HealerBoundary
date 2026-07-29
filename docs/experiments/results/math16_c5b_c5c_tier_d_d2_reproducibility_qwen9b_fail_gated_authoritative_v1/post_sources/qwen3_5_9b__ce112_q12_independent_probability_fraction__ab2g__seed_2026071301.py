def generate(level=1, **kwargs):
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    # Simplify fractions for probability calculation
    from math import gcd
    
    def simplify(numerator, denominator):
        common_divisor = gcd(abs(numerator), abs(denominator))
        return numerator // common_divisor, denominator // common_divisor

    p1_num, p1_den = frozen_params["p1"]
    p2_num, p2_den = frozen_params["p2"]

    # Calculate independent probability: P(A and B) = P(A) * P(B)
    simplified_p1_n, simplified_p1_d = simplify(p1_num, p1_den)
    simplified_p2_n, simplified_p2_d = simplify(p2_num, p2_den)

    final_numer = simplified_p1_n * simplified_p2_n
    final_denom = simplified_p1_d * simplified_p2_d
    
    # Ensure irreducible (gcd should already be 1 due to individual simplification, but double check)
    common_divisor_final = gcd(abs(final_numer), abs(final_denom))
    canonical_numer = final_numer // common_divisor_final
    canonical_denom = final_denom // common_divisor_final

    question_text = r"Given two independent events $A$ and $B$, where the probability of event $A$ is $\frac{%d}{%d}$ and the probability of event $B$ is $\frac{%d}{%d}$, what is the probability that both events occur? Express your answer as an irreducible fraction." % (simplified_p1_n, simplified_p1_d, simplified_p2_n, simplified_p2_d)

    correct_answer = {
        "numerator": canonical_numer,
        "denominator": canonical_denom,
        "canonical_latex": rf"\frac{{{canonical_numer}}}{{{canonical_denom}}}"
    }

    oracle_payload = frozen_params

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }