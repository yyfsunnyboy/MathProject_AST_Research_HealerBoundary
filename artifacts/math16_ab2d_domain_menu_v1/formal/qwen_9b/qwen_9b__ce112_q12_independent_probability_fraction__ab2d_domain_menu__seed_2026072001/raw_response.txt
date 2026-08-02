from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Parse frozen_params to get numerator and denominator for each independent event probability
    p1_num = kwargs.get("frozen_params", {}).get("p1")[0]  # favorable outcomes of first group
    p1_den = kwargs.get("frozen_params", {}).get("p1")[1]  # total possible outcomes of first group
    
    p2_num = kwargs.get("frozen_params", {}).get("p2")[0]  # favorable outcomes of second group
    p2_den = kwargs.get("frozen_params", {}).get("p2")[1]  # total possible outcomes of second group

    # Create Fraction objects for the probabilities of each independent event
    prob_1 = FractionOps.from_parts(p1_num, p1_den)
    prob_2 = FractionOps.from_parts(p2_num, p2_den)

    # Calculate the joint probability (product rule for independent events)
    combined_prob = FractionOps.mul(prob_1, prob_2)

    return {
        "question_text": kwargs.get("frozen_params", {}).get("description"),
        "correct_answer": {
            "numerator": combined_prob.numerator,
            "denominator": combined_prob.denominator,
            "canonical_latex": FractionOps.to_latex(combined_prob),
        },
        "oracle_payload": kwargs.get("frozen_params", {}),
    }