from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    leading_factor = 2
    linear_combination = {"a": 1, "b": 2}
    root_order = "a>b"
    shared_shift = 7
    subtracted_factor = -10

    # Calculate roots using FractionOps
    r1_frac = FractionOps.create(shared_shift)
    r2_frac = FractionOps.add(FractionOps.create(shared_shift), FractionOps.create(subtracted_factor))

    # Compare roots to order them (a > b)
    if r1_frac > r2_frac:
        a_frac = r1_frac
        b_frac = r2_frac
    else:
        a_frac = r2_frac
        b_frac = r1_frac

    # Calculate linear combination value
    coeff_a = FractionOps.create(linear_combination["a"])
    coeff_b = FractionOps.create(linear_combination["b"])

    term_a = FractionOps.mul(coeff_a, a_frac)
    term_b = FractionOps.mul(coeff_b, b_frac)
    val_frac = FractionOps.add(term_a, term_b)

    def to_str_or_int(f):
        if f.denominator == 1:
            return int(f.numerator)
        return f"{f.numerator}/{f.denominator}"

    a_val = to_str_or_int(a_frac)
    b_val = to_str_or_int(b_frac)
    value_val = to_str_or_int(val_frac)

    roots = [a_val, b_val]

    # Format equation
    def format_shift(shift):
        if shift >= 0:
            return f"x - {shift}"
        else:
            return f"x + {-shift}"

    shift_str = format_shift(shared_shift)
    coeff_second_term = -leading_factor * subtracted_factor
    if coeff_second_term >= 0:
        equation_str = f"{leading_factor}({shift_str})^2 + {coeff_second_term}({shift_str}) = 0"
    else:
        equation_str = f"{leading_factor}({shift_str})^2 - {-coeff_second_term}({shift_str}) = 0"

    # Format linear combination string
    parts = []
    if linear_combination["a"] != 0:
        if linear_combination["a"] == 1:
            parts.append("a")
        elif linear_combination["a"] == -1:
            parts.append("-a")
        else:
            parts.append(f"{linear_combination['a']}a")
    if linear_combination["b"] != 0:
        c_b = linear_combination["b"]
        if c_b > 0:
            sign = " + " if parts else ""
            coeff_str = "" if c_b == 1 else str(c_b)
            parts.append(f"{sign}{coeff_str}b")
        else:
            sign = " - " if parts else "-"
            coeff_str = "" if c_b == -1 else str(-c_b)
            parts.append(f"{sign}{coeff_str}b")
    linear_comb_str = "".join(parts)

    question_text = (
        f"Solve the quadratic equation {equation_str} for x. "
        f"Let the roots be a and b such that a > b. "
        f"Find the value of {linear_comb_str}."
    )

    correct_answer = {
        "roots": roots,
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
