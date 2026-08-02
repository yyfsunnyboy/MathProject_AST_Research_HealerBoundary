from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Parse frozen_params to get numerator and denominator for each probability
    p1_num = kwargs['oracle_payload']['p1'][0]
    p1_den = kwargs['oracle_payload']['p1'][1]
    
    p2_num = kwargs['oracle_payload']['p2'][0]
    p2_den = kwargs['oracle_payload']['p2'][1]

    # Create fractions for each probability
    prob_a = FractionOps.from_parts(p1_num, p1_den)
    prob_b = FractionOps.from_parts(p2_num, p2_den)

    # Calculate the product of independent probabilities (P(A and B) = P(A)*P(B))
    combined_prob = FractionOps.mul(prob_a, prob_b)

    return {
        "question_text": kwargs['frozen_task_description'],
        "correct_answer": {
            "numerator": combined_prob.numerator,
            "denominator": combined_prob.denominator,
            "canonical_latex": FractionOps.to_latex(combined_prob),
        },
        "oracle_payload": kwargs['oracle_payload']
    }