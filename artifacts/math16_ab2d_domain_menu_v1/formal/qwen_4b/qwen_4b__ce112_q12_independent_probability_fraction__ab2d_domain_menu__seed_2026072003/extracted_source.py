from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Parse frozen_params to extract numerator and denominator for each group
    p1 = kwargs.get("oracle_payload", {}).get("p1") or [2, 6]
    p2 = kwargs.get("oracle_payload", {}).get("p2") or [1, 5]

    num_p1, den_p1 = FractionOps.from_parts(p1[0], p1[1])
    prob_group_1 = FractionOps.div(num_p1, den_p1)

    num_p2, den_p2 = FractionOps.from_parts(p2[0], p2[1])
    prob_group_2 = FractionOps.div(num_p2, den_p2)

    # Calculate the probability of both events occurring (independent multiplication)
    total_prob = FractionOps.mul(prob_group_1, prob_group_2)

    # Construct the correct answer according to the task-specific contract
    canonical_latex = FractionOps.to_latex(total_prob)

    return {
        "question_text": kwargs.get("oracle_payload", {}).get("stem") or "第一組有 \(6\) 個等可能結果，其中 \(2\) 個符合條件；第二組有 \(5\) 個等可能結果，其中 \(1\) 個符合條件。若兩次選擇彼此獨立，求兩組皆符合條件的機率，並以最簡分數表示。",
        "correct_answer": {
            "numerator": total_prob.numerator,
            "denominator": total_prob.denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": kwargs.get("oracle_payload") or {"p1": [2, 6], "p2": [1, 5]}
    }
