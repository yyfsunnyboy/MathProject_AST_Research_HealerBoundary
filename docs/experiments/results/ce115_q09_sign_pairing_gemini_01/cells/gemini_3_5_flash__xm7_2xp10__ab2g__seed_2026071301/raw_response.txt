def generate(level=1, **kwargs):
    # Frozen parameters
    leading_factor = 2
    linear_combination = {"a": 1, "b": 2}
    root_order = "a>b"
    shared_shift = -7
    subtracted_factor = -10

    # Roots
    r1 = shared_shift
    r2 = subtracted_factor

    # Order roots (a > b)
    if r1 > r2:
        a, b = r1, r2
    else:
        a, b = r2, r1

    # Linear combination
    coeff_a = linear_combination["a"]
    coeff_b = linear_combination["b"]
    value = coeff_a * a + coeff_b * b

    # Quadratic equation coefficients: leading_factor * (x - r1) * (x - r2) = 0
    A = leading_factor
    B = -leading_factor * (r1 + r2)
    C = leading_factor * r1 * r2

    # Format equation string
    def fmt_term(coeff, term):
        if coeff == 0:
            return ""
        if term == "":
            return f"{coeff:+}"
        if coeff == 1:
            return f"+{term}"
        if coeff == -1:
            return f"-{term}"
        return f"{coeff:+}{term}"

    eq_str = f"{A}x^2"
    if B != 0:
        eq_str += fmt_term(B, "x")
    if C != 0:
        eq_str += fmt_term(C, "")
    eq_str += " = 0"

    if eq_str.startswith("+"):
        eq_str = eq_str[1:]

    question_text = (
        f"Solve the quadratic equation {eq_str}.\n"
        f"Identify the roots a and b (where a > b), and find the value of {coeff_a}a + {coeff_b}b."
    )

    oracle_payload = {
        "leading_factor": leading_factor,
        "linear_combination": linear_combination,
        "root_order": root_order,
        "shared_shift": shared_shift,
        "subtracted_factor": subtracted_factor
    }

    correct_answer = {
        "roots": [a, b],
        "a": a,
        "b": b,
        "value": value
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }
