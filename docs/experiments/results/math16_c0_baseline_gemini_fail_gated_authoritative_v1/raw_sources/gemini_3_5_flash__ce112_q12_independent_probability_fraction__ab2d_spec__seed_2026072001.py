from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    p1_params = [2, 6]
    p2_params = [1, 5]

    f1 = FractionOps.create(p1_params[0], p1_params[1])
    f2 = FractionOps.create(p2_params[0], p2_params[1])

    result = FractionOps.mul(f1, f2)

    numerator = FractionOps.get_numerator(result)
    denominator = FractionOps.get_denominator(result)
    canonical_latex = FractionOps.to_latex(result)

    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": canonical_latex
    }

    question_text = (
        f"Two independent events $A$ and $B$ have probabilities "
        f"$P(A) = \\frac{{{p1_params[0]}}}{{{p1_params[1]}}}$ and "
        f"$P(B) = \\frac{{{p2_params[0]}}}{{{p2_params[1]}}}$. "
        f"What is the probability that both events occur? "
        f"Express your answer as a simplified fraction."
    )

    oracle_payload = {
        "p1": p1_params,
        "p2": p2_params
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }