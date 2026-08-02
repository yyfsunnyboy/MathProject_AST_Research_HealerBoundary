from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    oracle_payload = kwargs.get("oracle_payload", {})
    
    # Extract parameters from frozen_params (p1: [favorable_1, total_1], p2: ...)
    favorable_1 = oracle_payload["p1"][0]
    total_1 = oracle_payload["p1"][1]
    favorable_2 = oracle_payload["p2"][0]
    total_2 = oracle_payload["p2"][1]

    # Step 1: Create fractions for each group's probability (favorable/total)
    prob_1 = FractionOps.from_parts(favorable_1, total_1)
    prob_2 = FractionOps.from_parts(favorable_2, total_2)

    # Step 2: Multiply the probabilities to get joint probability of independent events
    result_fraction = FractionOps.mul(prob_1, prob_2)

    # Prepare correct_answer according to Task-specific answer contract
    canonical_latex = FractionOps.to_latex(result_fraction)
    
    return {
        "question_text": oracle_payload["p1"][0] + "/" + str(oracle_payload["p1"][1]) + "\n" + 
                         oracle_payload["p2"][0] + "/" + str(oracle_payload["p2"][1]),
        "correct_answer": {
            "numerator": result_fraction.numerator,
            "denominator": result_fraction.denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": oracle_payload
    }
