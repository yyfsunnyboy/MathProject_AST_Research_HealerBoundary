from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Parse frozen_params to create fractions for the two groups.
    oracle_payload = kwargs.get("oracle_payload", {})
    
    p1_num = oracle_payload["p1"][0]
    p1_den = oracle_payload["p1"][1]
    a = FractionOps.from_parts(p1_num, p1_den)  # Probability of success in group 1
    
    p2_num = oracle_payload["p2"][0]
    p2_den = oracle_payload["p2"][1]
    b = FractionOps.from_parts(p2_num, p2_den)  # Probability of success in group 2

    # Calculate the probability that both events occur (independent multiplication).
    result_fraction = FractionOps.mul(a, b)

    # Construct the correct answer according to the task-specific contract.
    canonical_latex = FractionOps.to_latex(result_fraction)
    
    return {
        "question_text": oracle_payload.get("description", 
            f"第一組有 {p1_den} 個等可能結果，其中 {p1_num} 個符合條件；第二組有 {p2_den} 個等可能結果，其中 {p2_num} 個符合條件。若兩次選擇彼此獨立，求兩組皆符合條件的機率，並以最簡分數表示。"),
        "correct_answer": {
            "numerator": result_fraction.numerator,
            "denominator": result_fraction.denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": oracle_payload
    }
