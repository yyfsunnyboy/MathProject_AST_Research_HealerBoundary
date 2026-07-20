def generate(level=1, **kwargs):
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    # Parse p1: probability of event A is 2/6 which simplifies to 1/3
    num_p1, den_p1 = frozen_params["p1"]
    
    # Parse p2: probability of event B (independent) is 1/5
    
    # Independent joint probability P(A and B) = P(A) * P(B)
    numerator = num_p1 * frozen_params["p2"][0]
    denominator = den_p1 * frozen_params["p2"][1]
    
    # Simplify fraction using GCD logic manually to ensure canonical form without imports if restricted, 
    # but standard math.gcd is available in Python 3.5+. Assuming standard env.
    from math import gcd
    
    common_divisor = gcd(numerator, denominator)
    simplified_numerator = numerator // common_divisor
    simplified_denominator = denominator // common_divisor
    
    canonical_latex = f"\\frac{{{simplified_numerator}}}{{{simplified_denominator}}}"
    
    question_text = (f"What is the probability of both Event A and independent Event B occurring?\n"
                     f"If $P(A) = \\frac{{{num_p1}}}{{{den_p1}}}$ and $P(B) = \\frac{{{{frozen_params['p2'][0]}}}}{{{frozen_params['p2'][1]}}}},$ "
                     f"find the joint probability in simplest form.")

    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": simplified_numerator,
            "denominator": simplified_denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }