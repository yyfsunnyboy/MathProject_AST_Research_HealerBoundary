from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    leading_factor = 2
    linear_combination = {"a": 1, "b": 2}
    root_order = "a>b"
    shared_shift = -7
    subtracted_factor = -10

    # Roots are shared_shift and subtracted_factor
    r1 = shared_shift
    r2 = subtracted_factor

    r1_frac = FractionOps.create(r1)
    r2_frac = FractionOps.create(r2)

    # Order roots: a > b
    if r1_frac > r2_frac:
        a_frac = r1_frac
        b_frac = r2_frac
    else:
        a_frac = r2_frac
        b_frac = r1_frac

    coeff_a = linear_combination["a"]
    coeff_b = linear_combination["b"]

    coeff_a_frac = FractionOps.create(coeff_a)
    coeff_b_frac = FractionOps.create(coeff_b)

    term_a = FractionOps.mul(coeff_a_frac, a_frac)
    term_b = FractionOps.mul(coeff_b_frac, b_frac)
    value_frac = FractionOps.add(term_a, term_b)

    def to_exact_string(frac):
        if frac.denominator == 1:
            return int(frac.numerator)
        else:
            return f"{frac.numerator}/{frac.denominator}"

    a_val = to_exact_string(a_frac)
    b_val = to_exact_string(b_frac)
    value_val = to_exact_string(value_frac)
    roots_val = [a_val, b_val]

    # Construct the quadratic equation coefficients
    # A * (x - r1) * (x - r2) = A * (x^2 - (r1 + r2)x + r1 * r2)
    a2 = leading_factor
    a1 = -leading_factor * (r1 + r2)
    a0 = leading_factor * r1 * r2

    # Format quadratic equation
    term2 = f"{a2}x^2" if a2 != 1 else "x^2"

    if a1 > 0:
        term1 = f" + {a1}x" if a1 != 1 else " + x"
    elif a1 < 0:
        term1 = f" - {-a1}x" if a1 != -1 else " - x"
    else:
        term1 = ""

    if a0 > 0:
        term0 = f" + {a0}"
    elif a0 < 0:
        term0 = f" - {-a0}"
    else:
        term0 = ""

    equation_str = f"{term2}{term1}{term0} = 0"

    # Format linear combination
    parts = []
    if coeff_a == 1:
        parts.append("a")
    elif coeff_a == -1:
        parts.append("-a")
    elif coeff_a != 0:
        parts.append(f"{coeff_a}a")

    if coeff_b > 0:
        if parts:
            parts.append(f"+ {coeff_b}b" if coeff_b != 1 else "+ b")
        else:
            parts.append(f"{coeff_b}b" if coeff_b != 1 else "b")
    elif coeff_b < 0:
        if parts:
            parts.append(f"- {-coeff_b}b" if coeff_b != -1 else "- b")
        else:
            parts.append(f"{coeff_b}b" if coeff_b != -1 else "-b")
    lin_comb_str = " ".join(parts)

    question_text = (
        f"Find the roots of the quadratic equation {equation_str}. "
        f"Let the roots be a and b such that a > b. "
        f"What is the value of {lin_comb_str}?"
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
