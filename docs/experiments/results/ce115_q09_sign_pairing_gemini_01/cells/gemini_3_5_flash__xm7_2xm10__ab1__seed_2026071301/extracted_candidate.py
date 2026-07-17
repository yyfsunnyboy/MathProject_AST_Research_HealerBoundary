def generate(level=1, **kwargs):
    from fractions import Fraction

    # Frozen parameters
    leading_factor = 2
    linear_combination = {"a": 1, "b": 2}
    root_order = "a>b"
    shared_shift = -7
    subtracted_factor = 10

    # Calculate roots
    # Equation: leading_factor * (x - shared_shift)^2 - subtracted_factor * (x - shared_shift) = 0
    r1 = shared_shift
    r2 = shared_shift + Fraction(subtracted_factor, leading_factor)

    if r1 > r2:
        a_val = r1
        b_val = r2
    else:
        a_val = r2
        b_val = r1

    def to_rational(val):
        f = Fraction(val).limit_denominator()
        if f.denominator == 1:
            return int(f.numerator)
        else:
            return f"{f.numerator}/{f.denominator}"

    a = to_rational(a_val)
    b = to_rational(b_val)
    roots = [a, b]

    coeff_a = linear_combination["a"]
    coeff_b = linear_combination["b"]

    val_exact = Fraction(coeff_a * Fraction(a_val) + coeff_b * Fraction(b_val)).limit_denominator()
    if val_exact.denominator == 1:
        value = int(val_exact.numerator)
    else:
        value = f"{val_exact.numerator}/{val_exact.denominator}"

    if shared_shift < 0:
        term = f"(x + {-shared_shift})"
    elif shared_shift > 0:
        term = f"(x - {shared_shift})"
    else:
        term = "x"

    equation = f"{leading_factor}{term}^2 - {subtracted_factor}{term} = 0"

    lc_parts = []
    if coeff_a == 1:
        lc_parts.append("a")
    elif coeff_a == -1:
        lc_parts.append("-a")
    else:
        lc_parts.append(f"{coeff_a}a")

    if coeff_b > 0:
        lc_parts.append(f"+ {coeff_b}b" if coeff_b != 1 else "+ b")
    elif coeff_b < 0:
        lc_parts.append(f"- {-coeff_b}b" if coeff_b != -1 else "- b")
    lc_str = " ".join(lc_parts)

    question_text = f"Solve the quadratic equation {equation} for x. Let its roots be a and b, ordered such that a > b. Find the roots a and b, and the value of the linear combination {lc_str}."

    correct_answer = {
        "roots": roots,
        "a": a,
        "b": b,
        "value": value
    }

    oracle_payload = {
        "leading_factor": leading_factor,
        "linear_combination": linear_combination,
        "root_order": root_order,
        "shared_shift": shared_shift,
        "subtracted_factor": subtracted_factor
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }
