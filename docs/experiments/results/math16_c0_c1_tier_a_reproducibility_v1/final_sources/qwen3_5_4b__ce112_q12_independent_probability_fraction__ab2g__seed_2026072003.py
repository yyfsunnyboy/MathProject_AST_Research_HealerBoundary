def generate(level=1, **kwargs):
    p1_list = kwargs.get("p1", [2, 6]) if "p1" not in globals() else None
    p2_list = kwargs.get("p2", [1, 5]) if "p2" not in globals() else None
    
    # Use frozen parameters as per task specification
    f_p1 = (2, 6)
    f_p2 = (1, 5)

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    numerator_1 = p1_list[0] * p2_list[1]
    denominator_1 = p1_list[1] * p2_list[0]
    
    common = gcd(numerator_1, denominator_1)
    num_final = numerator_1 // common
    den_final = denominator_1 // common

    question_text = r"Let $P(A)$ and $P(B)$ be independent events with probabilities $\frac{p_{1a}}{p_{1b}}$ and $\frac{p_{2a}}{p_{2b}}$ respectively, where $(p_{1a}, p_{1b}) \in (2, 6)$ and $(p_{2a}, p_{2b}) \in (1, 5)$. If we select one probability from each set such that the product of numerators divided by the product of denominators yields a specific fraction, what is this irreducible fraction?"

    correct_answer = {
        "numerator": num_final,
        "denominator": den_final,
        "canonical_latex": f"\\frac{{{num_final}}}{{{{den_final}}}}"
    }

    oracle_payload = {"p1": list(f_p1), "p2": list(f_p2)}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }