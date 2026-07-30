import math


def generate(level=1, **kwargs):
    # Frozen parameters
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3

    # Support overriding via kwargs if needed
    factor_order_policy = kwargs.get("factor_order_policy", factor_order_policy)
    quadratic_coefficients = kwargs.get(
        "quadratic_coefficients", quadratic_coefficients
    )
    template_left_x_coefficient = kwargs.get(
        "template_left_x_coefficient", template_left_x_coefficient
    )

    A, B, C = quadratic_coefficients
    d = template_left_x_coefficient

    b = A // d
    disc = B**2 - 4 * A * C
    sqrt_disc = int(math.isqrt(disc))

    a_candidates = []
    if sqrt_disc * sqrt_disc == disc:
        for sign in [-1, 1]:
            num = B + sign * sqrt_disc
            den = 2 * b
            if num % den == 0:
                a_candidates.append(num // den)

    a = None
    c = None
    for a_cand in a_candidates:
        if a_cand != 0:
            if C % a_cand == 0:
                c_cand = C // a_cand
                if d * c_cand + a_cand * b == B:
                    a = a_cand
                    c = c_cand
                    break
        else:
            if C == 0:
                if B % d == 0:
                    a = 0
                    c = B // d
                    break

    if a is None or c is None:
        raise ValueError("No integer solution found")

    ans = a + 2 * c

    # Format polynomial
    parts = []
    if A == 1:
        parts.append("x^2")
    elif A == -1:
        parts.append("-x^2")
    elif A != 0:
        parts.append(f"{A}x^2")

    if B > 0:
        sign = " + " if parts else ""
        val = "" if B == 1 else str(B)
        parts.append(f"{sign}{val}x")
    elif B < 0:
        sign = " - " if parts else "-"
        val = "" if B == -1 else str(abs(B))
        parts.append(f"{sign}{val}x")

    if C > 0:
        sign = " + " if parts else ""
        parts.append(f"{sign}{C}")
    elif C < 0:
        sign = " - " if parts else "-"
        parts.append(f"{sign}{abs(C)}")

    poly_str = "".join(parts)

    question_text = (
        f"The polynomial ${poly_str}$ can be factored in the form "
        f"$({d}x + a)(bx + c)$ where $a$, $b$, and $c$ are integers. "
        f"Find the value of $a + 2c$."
    )

    correct_answer = str(ans)

    oracle_payload = {
        "factor_order_policy": factor_order_policy,
        "quadratic_coefficients": quadratic_coefficients,
        "template_left_x_coefficient": template_left_x_coefficient,
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }