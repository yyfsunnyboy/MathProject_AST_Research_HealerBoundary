def generate(level=1, **kwargs):
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    # Simplify p1: 2/6 -> 1/3
    num_p1, den_p1 = frozen_params["p1"][0] // (frozen_params["p1"][1] // gcd(frozen_params["p1"][0], frozen_params["p1"][1])), frozen_params["p1"][1] // gcd(frozen_params["p1"][0], frozen_params["p1"][1])
    # Actually, let's just simplify correctly: 2/6 = (2/gcd(2,6)) / (6/gcd(2,6)) = (2/2)/(6/2) = 1/3.
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    num_p1_simp, den_p1_simp = frozen_params["p1"][0] // gcd(frozen_params["p1"][0], frozen_params["p1"][1]), frozen_params["p1"][1] // gcd(frozen_params["p1"][0], frozen_params["p1"][1])
    num_p2, den_p2 = frozen_params["p2"][0], frozen_params["p2"][1] # 1/5 is already simplified
    
    # Independent probability: P(A and B) = P(A) * P(B)
    numerator = num_p1_simp * num_p2
    denominator = den_p1_simp * den_p2
    
    final_gcd = gcd(numerator, denominator)
    canonical_num = numerator // final_gcd
    canonical_den = denominator // final_gcd
    
    question_text = r"Given two independent events $A$ and $B$, where the probability of event $A$ is $\frac{" + str(frozen_params["p1"][0]) + "}{\\" + str(frozen_params["p1"][1]) + "\}$ and the probability of event $B$ is $\frac{" + str(frozen_params["p2"][0]) + "}{\\" + str(frozen_params["p2"][1]) + "\}$, what is the probability that both events occur?"
    
    canonical_latex = r"\frac{" + str(canonical_num) + "}{\\" + str(canonical_den) + "\}"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": canonical_num,
            "denominator": canonical_den,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }