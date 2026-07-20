def generate(level=1, **kwargs):
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    # Simplify fractions for internal logic if needed, but keep original for oracle
    p1_num, p1_den = frozen_params["p1"][0], frozen_params["p1"][1]
    p2_num, p2_den = frozen_params["p2"][0], frozen_params["p2"][1]
    
    # Independent probability calculation: P(A and B) = P(A) * P(B)
    numerator = p1_num * p2_num
    denominator = p1_den * p2_den
    
    # Compute GCD for irreducible fraction
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    common_divisor = gcd(numerator, denominator)
    
    simplified_numerator = numerator // common_divisor
    simplified_denominator = denominator // common_divisor
    
    # Construct LaTeX for the fraction
    canonical_latex = f"\\frac{{{simplified_numerator}}}{{{simplified_denominator}}}"
    
    question_text = (f"What is the probability of two independent events occurring, "
                     f"given that the first event has a probability of $\\\\frac{{{p1_num}}}{{{p1_den}}}$ and "
                     f"the second event has a probability of $\\\\frac{{{p2_num}}}{{{p2_den}}}$? Express your answer as an irreducible fraction.")
    
    correct_answer = {
        "numerator": simplified_numerator,
        "denominator": simplified_denominator,
        "canonical_latex": canonical_latex
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }