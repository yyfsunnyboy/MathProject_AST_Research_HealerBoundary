def generate(level=1, **kwargs):
    import math
    
    # Frozen sampled parameters from task specification context
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    p1_num, p1_den = frozen_params["p1"]
    p2_num, p2_den = frozen_params["p2"]
    
    # Calculate independent probability fraction: (p1 * p2) / (denom_total^2) conceptually or simply product of fractions
    # Interpretation for "independent_probability_fraction": P(A and B) where A=p1/6, B=5/? 
    # Based on frozen params structure [numerator, denominator]:
    # Fraction 1: p1_num / p1_den = 2/6 (simplified usually expected in math but let's keep raw for oracle logic or simplify?)
    # The task asks for an irreducible fraction as correct_answer.
    
    num_total = p1_num * p2_num
    den_total = p1_den * p2_den
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    common_divisor = gcd(num_total, den_total)
    
    final_numerator = num_total // common_divisor
    final_denominator = den_total // common_divisor
    
    # Construct LaTeX for the fraction
    canonical_latex = f"\\frac{{{final_numerator}}}{{{final_denominator}}}"
    
    question_text = (f"What is the probability of two independent events occurring, "
                     f"where the first event has a probability of $\\frac{{{p1_num}}}{{{p1_den}}}$ and "
                     f"the second event has a probability of $\\frac{{{p2_num}}}{{{p2_den}}}$? "
                     f"Express your answer as an irreducible fraction.")
    
    correct_answer = {
        "numerator": final_numerator,
        "denominator": final_denominator,
        "canonical_latex": canonical_latex
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }