def generate(level=1, **kwargs):
    import math

    p1 = kwargs.get("p1", [2, 6])
    p2 = kwargs.get("p2", [1, 5])

    # Calculate the probability of both events occurring: P(A and B) = P(A) * P(B)
    num = p1[0] * p2[0]
    den = p1[1] * p2[1]

    g = math.gcd(num, den)
    ans_num = num // g
    ans_den = den // g

    question_text = (
        f"The probability of event $A$ is $\\frac{{{p1[0]}}}{{{p1[1]}}}$ and the "
        f"probability of event $B$ is $\\frac{{{p2[0]}}}{{{p2[1]}}}$. If $A$ and $B$ "
        f"are independent, what is the probability that both events occur?"
    )

    correct_answer = {
        "numerator": ans_num,
        "denominator": ans_den,
        "canonical_latex": f"\\frac{{{ans_num}}}{{{ans_den}}}"
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "p1": p1,
            "p2": p2
        }
    }