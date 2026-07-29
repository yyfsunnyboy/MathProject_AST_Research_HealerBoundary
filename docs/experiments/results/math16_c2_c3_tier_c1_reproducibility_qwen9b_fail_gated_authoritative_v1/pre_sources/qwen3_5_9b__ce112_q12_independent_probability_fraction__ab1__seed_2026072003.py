def generate(level=1, **kwargs):
    p1 = kwargs.get("p1", [2, 6])
    p2 = kwargs.get("p2", [1, 5])
    
    num_p1 = p1[0]
    den_p1 = p1[1]
    num_p2 = p2[0]
    den_p2 = p2[1]
    
    # Probability of independent events: P(A and B) = P(A) * P(B)
    numerator = num_p1 * num_p2
    denominator = den_p1 * den_p2
    
    import math
    gcd_val = math.gcd(numerator, denominator)
    
    simplified_numerator = numerator // gcd_val
    simplified_denominator = denominator // gcd_val
    
    question_text = r"Given two independent events $A$ and $B$, where the probability of event $A$ is $\frac{" + str(num_p1) + "}{\\" + str(den_p1) + "\}$ and the probability of event $B$ is $\frac{" + str(num_p2) + "}{\\" + str(den_p2) + "\}$, calculate the probability that both events occur. Express your answer as an irreducible fraction."
    
    canonical_latex = r"\frac{" + str(simplified_numerator) + "}{\\" + str(simplified_denominator) + "\}"
    correct_answer_str = f"numerator: {simplified_numerator}, denominator: {simplified_denominator}, canonical_latex: {canonical_latex}"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_str,
        "oracle_payload": {"p1": p1, "p2": p2}
    }