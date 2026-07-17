from fractions import Fraction

def generate(level=1, **kwargs):
    # Default frozen parameters
    leading_factor = kwargs.get("leading_factor", 2)
    linear_combination = kwargs.get("linear_combination", {"a": 1, "b": 2})
    root_order = kwargs.get("root_order", "a>b")
    shared_shift = kwargs.get("shared_shift", 7)
    subtracted_factor = kwargs.get("subtracted_factor", -10)

    # Calculate roots
    # Equation: leading_factor * (x - shared_shift)^2 - subtracted_factor * (x - shared_shift) = 0
    # Roots are:
    # r1 = shared_shift
    # r2 = shared_shift + subtracted_factor / leading_factor
    r1 = Fraction(shared_shift)
    r2 = Fraction(shared_shift) + Fraction(subtracted_factor, leading_factor)

    if r1 > r2:
        a_val = r1
        b_val = r2
    else:
        a_val = r2
        b_val = r1

    def format_rational(f):
        if f.denominator == 1:
            return f.numerator
        else:
            return f"{f.numerator}/{f.denominator}"

    a_str = format_rational(a_val)
    b_str = format_rational(b_val)

    roots = [a_str, b_str]

    coeff_a = linear_combination["a"]
    coeff_b = linear_combination["b"]

    val_fraction = coeff_a * a_val + coeff_b * b_val
    val_str = format_rational(val_fraction)

    # Construct the equation string
    term1 = f"x - {shared_shift}" if shared_shift > 0 else f"x + {-shared_shift}"
    if shared_shift == 0:
        term1 = "x"

    eq_part1 = f"{leading_factor}({term1})^2" if term1 != "x" else f"{leading_factor}x^2"

    if subtracted_factor < 0:
        eq_part2 = f" + {-subtracted_factor}({term1})" if term1 != "x" else f" + {-subtracted_factor}x"
    elif subtracted_factor > 0:
        eq_part2 = f" - {subtracted_factor}({term1})" if term1 != "x" else f" - {subtracted_factor}x"
    else:
        eq_part2 = ""

    equation_str = f"{eq_part1}{eq_part2} = 0"

    # Linear combination string
    lc_str = ""
    if coeff_a == 1:
        lc_str += "a"
    elif coeff_a == -1:
        lc_str += "-a"
    else:
        lc_str += f"{coeff_a}a"

    if coeff_b > 0:
        lc_str += f" + {coeff_b}b" if coeff_b != 1 else " + b"
    elif coeff_b < 0:
        lc_str += f" - {-coeff_b}b" if coeff_b != -1 else " - b"

    question_text = (
        f"Solve the quadratic equation:\n"
        f"$${equation_str}$$\n\n"
        f"Find the roots $a$ and $b$, where $a > b$.\n"
        f"Then, calculate the value of {lc_str}."
    )

    correct_answer = {
        "roots": roots,
        "a": a_str,
        "b": b_str,
        "value": val_str
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
