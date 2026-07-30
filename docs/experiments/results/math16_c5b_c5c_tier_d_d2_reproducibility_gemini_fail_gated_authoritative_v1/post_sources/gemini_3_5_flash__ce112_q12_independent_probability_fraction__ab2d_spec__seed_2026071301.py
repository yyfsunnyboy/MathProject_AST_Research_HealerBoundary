from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    p1 = [2, 6]
    p2 = [1, 5]

    # Compute using FractionOps
    f1 = FractionOps.create(p1[0], p1[1])
    f2 = FractionOps.create(p2[0], p2[1])
    res = FractionOps.mul(f1, f2)

    num = res.numerator
    den = res.denominator
    latex = FractionOps.to_latex(res)

    question_text = (
        f"Two independent events \\(A\\) and \\(B\\) have probabilities "
        f"\\(P(A) = \\frac{{{p1[0]}}}{{{p1[1]}}}\\) and \\(P(B) = \\frac{{{p2[0]}}}{{{p2[1]}}}\\). "
        f"What is the probability that both events occur?"
    )

    correct_answer = {
        "numerator": num,
        "denominator": den,
        "canonical_latex": latex
    }

    oracle_payload = {
        "p1": p1,
        "p2": p2
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }