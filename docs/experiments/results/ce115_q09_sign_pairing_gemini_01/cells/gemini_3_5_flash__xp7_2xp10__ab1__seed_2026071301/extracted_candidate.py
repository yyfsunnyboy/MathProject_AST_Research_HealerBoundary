from fractions import Fraction

def generate(level=1, **kwargs):
    # Frozen parameters
    leading_factor = 2
    linear_combination = {"a": 1, "b": 2}
    root_order = "a>b"
    shared_shift = 7
    subtracted_factor = -10

    # Calculate roots
    r1 = Fraction(shared_shift)
    r2 = Fraction(shared_shift) + Fraction(subtracted_factor, leading_factor)

    # Order roots
    if r1 > r2:
        a_frac = r1
        b_frac = r2
    else:
        a_frac = r2
        b_frac = r1

    # Calculate value
    val_frac = Fraction(linear_combination["a"]) * a_frac + Fraction(linear_combination["b"]) * b_frac

    def to_rational(frac):
        if frac.denominator == 1:
            return int(frac.numerator)
        else:
            return f"{frac.numerator}/{frac.denominator}"

    a_val = to_rational(a_frac)
    b_val = to_rational(b_frac)
    value_val = to_rational(val_frac)
    roots_val = [a_val, b_val]

    # Format equation
    def format_term(val):
        if val > 0:
            return f"(x - {val})"
        elif val < 0:
            return f"(x + {-val})"
        else:
            return "x"

    term1_base = format_term(shared_shift)
    if term1_base == "x":
        term1 = "x^2"
    else:
        term1 = f"{term1_base}^2"

    if leading_factor == 1:
        expr1 = term1
    elif leading_factor == -1:
        expr1 = f"-{term1}"
    else:
        expr1 = f"{leading_factor}{term1}"

    coeff = -subtracted_factor
    term2_base = format_term(shared_shift)

    if coeff > 0:
        sign = " + "
        val = coeff
    else:
        sign = " - "
        val = -coeff

    if val == 1:
        expr2 = f"{sign}{term2_base}"
    else:
        expr2 = f"{sign}{val}{term2_base}"

    equation = f"{expr1}{expr2} = 0"

    # Format linear combination
    ca = linear_combination["a"]
    cb = linear_combination["b"]
    parts = []
    if ca == 1:
        parts.append("a")
    elif ca == -1:
        parts.append("-a")
    elif ca != 0:
        parts.append(f"{ca}a")

    if cb == 1:
        parts.append(" + b" if parts else "b")
    elif cb == -1:
        parts.append(" - b" if parts else "-b")
    elif cb > 0:
        parts.append(f" + {cb}b" if parts else f"{cb}b")
    elif cb < 0:
        parts.append(f" - {-cb}b" if parts else f"{cb}b")

    lc_str = "".join(parts)

    question_text = (
        f"Solve the quadratic equation:\n"
        f"{equation}\n\n"
        f"Let the roots be a and b, where a > b. Find the value of {lc_str}."
    )

    correct_answer = {
        "roots": roots_val,
        "a": a_val,
        "b": b_val,
        "value": value_val
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
