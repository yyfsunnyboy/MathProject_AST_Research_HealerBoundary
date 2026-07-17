from fractions import Fraction

def generate(level=1, **kwargs):
    # Frozen parameters
    leading_factor = 2
    linear_combination = {"a": 1, "b": 2}
    root_order = "a>b"
    shared_shift = 7
    subtracted_factor = 10

    # Calculate roots
    # Equation: leading_factor * (x - shared_shift)^2 - subtracted_factor * (x - shared_shift) = 0
    r1 = Fraction(shared_shift)
    r2 = Fraction(shared_shift) + Fraction(subtracted_factor, leading_factor)

    # Order roots such that a > b
    if r1 > r2:
        a_val = r1
        b_val = r2
    else:
        a_val = r2
        b_val = r1

    # Calculate linear combination
    coeff_a = linear_combination["a"]
    coeff_b = linear_combination["b"]
    val_frac = coeff_a * a_val + coeff_b * b_val

    def format_rational(val):
        if val.denominator == 1:
            return val.numerator
        else:
            return f"{val.numerator}/{val.denominator}"

    a_formatted = format_rational(a_val)
    b_formatted = format_rational(b_val)
    value_formatted = format_rational(val_frac)
    roots_formatted = [a_formatted, b_formatted]

    # Format equation
    if shared_shift == 0:
        term = "x"
    elif shared_shift > 0:
        term = f"(x - {shared_shift})"
    else:
        term = f"(x + {-shared_shift})"

    equation = f"{leading_factor}{term}^2 - {subtracted_factor}{term} = 0"

    # Linear combination expression for question text
    parts = []
    if coeff_a == 1:
        parts.append("a")
    elif coeff_a == -1:
        parts.append("-a")
    elif coeff_a != 0:
        parts.append(f"{coeff_a}a")

    if coeff_b > 0:
        if parts:
            parts.append("+")
        if coeff_b == 1:
            parts.append("b")
        else:
            parts.append(f"{coeff_b}b")
    elif coeff_b < 0:
        if coeff_b == -1:
            parts.append("- b")
        else:
            parts.append(f"- {-coeff_b}b")

    expr = " ".join(parts).replace("+ -", "- ").replace("  ", " ")

    question_text = f"Solve the quadratic equation {equation}. Let its roots be a and b, where a > b. Find the value of {expr}."

    correct_answer = {
        "roots": roots_formatted,
        "a": a_formatted,
        "b": b_formatted,
        "value": value_formatted
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