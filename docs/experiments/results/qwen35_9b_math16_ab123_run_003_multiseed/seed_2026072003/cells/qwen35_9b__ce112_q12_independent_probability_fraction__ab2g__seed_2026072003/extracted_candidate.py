def generate(level=1, **kwargs):
    p1_num = kwargs.get("p1", [2, 6])[0]
    p1_den = kwargs.get("p1", [2, 6])[1]
    p2_num = kwargs.get("p2", [1, 5])[0]
    p2_den = kwargs.get("p2", [1, 5])[1]

    # Independent probability: P(A and B) = P(A) * P(B)
    numerator = p1_num * p2_num
    denominator = p1_den * p2_den

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    common_divisor = gcd(numerator, denominator)
    reduced_numerator = numerator // common_divisor
    reduced_denominator = denominator // common_divisor

    correct_answer_dict = {
        "numerator": reduced_numerator,
        "denominator": reduced_denominator,
        "canonical_latex": f"\\frac{{{reduced_numerator}}}{{{reduced_denominator}}}"
    }

    question_text = (
        r"What is the probability of two independent events occurring together? "
        r"The first event has a probability of $\\frac{%d}{%d}$ and the second event has "
        r"a probability of $\\frac{%d}{%d}$. Express your answer as an irreducible fraction." % (p1_num, p1_den, p2_num, p2_den)
    )

    oracle_payload = {"p1": [p1_num, p1_den], "p2": [p2_num, p2_den]}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }