def generate(level=1, **kwargs):
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    # Simplify fractions for calculation if needed, though problem implies direct use or standard interpretation
    # p1: probability of event A is 2/6 -> simplifies to 1/3? 
    # The task says "independent_probability_fraction". Usually this means P(A and B) = P(A)*P(B).
    # However, the frozen params are lists [numerator, denominator].
    # Let's assume we must use them as given or simplify. Standard math problems often expect simplified fractions for answers but inputs might be raw.
    # Given "rational_arithmetic", let's calculate P(A) = 2/6 and P(B) = 1/5.
    # If the question asks for probability of both independent events: (2/6) * (1/5).
    
    from math import gcd
    
    def simplify(n, d):
        common = gcd(abs(n), abs(d))
        return n // common, d // common

    num_p1, den_p1 = frozen_params["p1"]
    num_p2, den_p2 = frozen_params["p2"]
    
    # Calculate product: (num_p1 * num_p2) / (den_p1 * den_p2)
    final_num = num_p1 * num_p2
    final_den = den_p1 * den_p2
    
    # Simplify the result for canonical_latex and correct_answer structure
    common_final = gcd(abs(final_num), abs(final_den))
    canon_num = final_num // common_final
    canon_den = final_den // common_final
    
    question_text = r"Two independent events $A$ and $B$ have probabilities $\frac{%d}{%d}$ and $\frac{%d}{%d}$ respectively. What is the probability that both events occur?" % (num_p1, den_p1, num_p2, den_p2)
    
    # Construct canonical LaTeX for fraction: \frac{numerator}{denominator}
    canon_latex = r"\frac{" + str(canon_num) + "}" + r"}" + r"\{" + str(canon_den) + "}"
    
    correct_answer_dict = {
        "numerator": canon_num,
        "denominator": canon_den,
        "canonical_latex": canon_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }