from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    p1_num = kwargs.get("oracle_payload", {}).get("p1")[0]
    p1_den = kwargs.get("oracle_payload", {}).get("p1")[1]
    
    # Probability of first group: 2/6 -> simplify to 1/3
    prob_p1 = FractionOps.from_parts(p1_num, p1_den)

    p2_num = kwargs.get("oracle_payload", {}).get("p2")[0]
    p2_den = kwargs.get("oracle_payload", {}).get("p2")[1]
    
    # Probability of second group: 1/5 (already irreducible)
    prob_p2 = FractionOps.from_parts(p2_num, p2_den)

    # Multiply probabilities for independent events
    total_prob = FractionOps.mul(prob_p1, prob_p2)

    return {
        "question_text": kwargs.get("oracle_payload", {}).get("stem"),
        "correct_answer": {
            "numerator": int(total_prob.numerator),
            "denominator": int(total_prob.denominator),
            "canonical_latex": FractionOps.to_exact(total_prob) if total_prob.denominator == 1 else f"{total_prob.numerator}/{total_prob.denominator}"
        },
        "oracle_payload": kwargs.get("oracle_payload", {}),
    }
