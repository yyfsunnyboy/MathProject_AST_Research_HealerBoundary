def generate(level=1, **kwargs):
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    # Calculate probabilities from p1=[numerator, denominator] and p2=[numerator, denominator]
    num_p1, den_p1 = frozen_params["p1"]
    num_p2, den_p2 = frozen_params["p2"]
    
    # Independent probability: P(A and B) = P(A) * P(B)
    numerator_result = num_p1 * num_p2
    denominator_result = den_p1 * den_p2
    
    # Simplify fraction (make irreducible) by dividing by GCD
    import math
    common_divisor = math.gcd(numerator_result, denominator_result)
    
    simplified_numerator = numerator_result // common_divisor
    simplified_denominator = denominator_result // common_divisor
    
    question_text = r"Given two independent events $A$ and $B$, where the probability of event $A$ is $\frac{%d}{%d}$ and the probability of event $B$ is $\frac{%d}{%d}$, what is the probability that both events occur? Express your answer as an irreducible fraction." % (num_p1, den_p1, num_p2, den_p2)
    
    correct_answer = {
        "numerator": simplified_numerator,
        "denominator": simplified_denominator,
        "canonical_latex": r"\frac{%d}{%d}" % (simplified_numerator, simplified_denominator)
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }