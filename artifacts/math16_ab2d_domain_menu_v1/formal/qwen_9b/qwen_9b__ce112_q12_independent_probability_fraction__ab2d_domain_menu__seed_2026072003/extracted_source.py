from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    p1_num = kwargs.get("frozen_params", {}).get("p1")[0]
    p1_den = kwargs.get("frozen_params", {}).get("p1")[1]
    p2_num = kwargs.get("frozen_params", {}).get("p2")[0]
    p2_den = kwargs.get("frozen_params", {}).get("p2")[1]

    prob_a = FractionOps.from_parts(p1_num, p1_den)
    prob_b = FractionOps.from_parts(p2_num, p2_den)

    combined_prob = FractionOps.mul(prob_a, prob_b)

    return {
        "question_text": kwargs.get("frozen_params", {}).get("description"),
        "correct_answer": {
            "numerator": int(combined_prob.numerator),
            "denominator": int(combined_prob.denominator),
            "canonical_latex": FractionOps.to_latex(combined_prob)
        },
        "oracle_payload": kwargs.get("frozen_params", {})
    }