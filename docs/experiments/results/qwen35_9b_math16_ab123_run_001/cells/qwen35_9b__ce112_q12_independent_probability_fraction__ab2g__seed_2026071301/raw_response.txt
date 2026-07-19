def generate(level=1, **kwargs):
    import math
    
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    numerator = (frozen_params["p1"][0] * frozen_params["p2"][0]) + ((7 - frozen_params["p1"][0]) * (7 - frozen_params["p2"][0]))
    denominator = 49
    
    gnumerator = math.gcd(numerator, denominator)
    
    final_numerator = numerator // gnumerator
    final_denominator = denominator // gnumerator
    
    canonical_latex = f"\\frac{{{final_numerator}}}{{{final_denominator}}}"
    
    question_text = (f"What is the probability of obtaining exactly one success in two independent trials, "
                     f"given that trial 1 succeeds with probability $P_1 = \\frac{{{frozen_params['p1'][0]}}}{{{frozen_params['p1'][1]}}}$ and "
                     f"trial 2 succeeds with probability $P_2 = \\frac{{{frozen_params['p2'][0]}}}{{{frozen_params['p2'][1]}}}$? Express your answer as an irreducible fraction.")

    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": final_numerator,
            "denominator": final_denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }