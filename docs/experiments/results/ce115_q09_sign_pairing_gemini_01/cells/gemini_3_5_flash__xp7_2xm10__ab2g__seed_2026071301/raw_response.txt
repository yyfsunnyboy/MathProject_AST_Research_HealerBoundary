def generate(level=1, **kwargs):
    from fractions import Fraction

    # Frozen parameters
    leading_factor = 2
    linear_combination = {"a": 1, "b": 2}
    root_order = "a>b"
    shared_shift = 7
    subtracted_factor = 10

    # Equation: leading_factor * (x - shared_shift)^2 - subtracted_factor * (x - shared_shift) = 0
    # Roots are:
    # r1 = shared_shift
    # r2 = shared_shift + subtracted_factor / leading_factor

    r1 = Fraction(shared_shift)
    r2 = Fraction(shared_shift) + Fraction(subtracted_factor, leading_factor)

    # Determine a and b based on root_order "a>b"
    if r1 > r2:
        a_frac = r1
        b_frac = r2
    else:
        a_frac = r2
        b_frac = r1

    # Format fraction helper
    def format_frac(f):
        if f.denominator == 1:
            return int(f.numerator)
        else:
            return f"{f.numerator}/{f.denominator}"

    a_val = format_frac(a_frac)
    b_val = format_frac(b_frac)

    roots = [a_val, b_val]

    # Calculate linear combination: coeff_a * a + coeff_b * b
    coeff_a = linear_combination["a"]
    coeff_b = linear_combination["b"]

    val_frac = coeff_a * a_frac + coeff_b * b_frac
    value = format_frac(val_frac)

    question_text = (
        f"Solve the quadratic equation by factoring:\n"
        f"{leading_factor}(x - {shared_shift})^2 - {subtracted_factor}(x - {shared_shift}) = 0\n\n"
        f"Let the roots be $a$ and $b$ with $a > b$.\n"
        f"Find the roots, and calculate the value of {coeff_a}a + {coeff_b}b."
    )

    correct_answer = {
        "roots": roots,
        "a": a_val,
        "b": b_val,
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
