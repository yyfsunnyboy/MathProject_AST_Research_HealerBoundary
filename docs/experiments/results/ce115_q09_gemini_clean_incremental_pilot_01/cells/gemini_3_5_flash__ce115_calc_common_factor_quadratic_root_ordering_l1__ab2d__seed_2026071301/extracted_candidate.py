from core.prompts.domain_function_library import FractionOps
from fractions import Fraction

def generate(level=1, **kwargs):
    leading_factor = 2
    linear_combination = {"a": 1, "b": 2}
    root_order = "a>b"
    shared_shift = 7
    subtracted_factor = 10

    # Roots of leading_factor * (x - shared_shift)^2 - subtracted_factor * (x - shared_shift) = 0
    # are x = shared_shift and x = shared_shift + subtracted_factor / leading_factor
    r1 = Fraction(shared_shift)
    r2 = Fraction(shared_shift) + Fraction(subtracted_factor, leading_factor)

    # Since root_order is "a>b", a is the larger root, b is the smaller root
    roots_sorted = sorted([r1, r2], reverse=True)
    a_frac = roots_sorted[0]
    b_frac = roots_sorted[1]

    # Use FractionOps to compute the value
    a_val = FractionOps.create(str(a_frac))
    b_val = FractionOps.create(str(b_frac))
    coeff_a_val = FractionOps.create(str(linear_combination['a']))
    coeff_b_val = FractionOps.create(str(linear_combination['b']))

    term1 = FractionOps.mul(coeff_a_val, a_val)
    term2 = FractionOps.mul(coeff_b_val, b_val)
    val_val = FractionOps.add(term1, term2)

    # Compute val_frac using standard Fraction to format it easily
    val_frac = Fraction(linear_combination['a']) * a_frac + Fraction(linear_combination['b']) * b_frac

    def format_fraction(f):
        if f.denominator == 1:
            return f.numerator
        else:
            return f"{f.numerator}/{f.denominator}"

    def format_shift(shift):
        if shift == 0:
            return "x"
        elif shift > 0:
            return f"(x - {shift})"
        else:
            return f"(x + {abs(shift)})"

    def format_linear_combination(ca, cb):
        parts = []
        if ca == 1:
            parts.append("a")
        elif ca == -1:
            parts.append("-a")
        elif ca != 0:
            parts.append(f"{ca}a")

        if cb > 0:
            if cb == 1:
                parts.append("+ b")
            else:
                parts.append(f"+ {cb}b")
        elif cb < 0:
            if cb == -1:
                parts.append("- b")
            else:
                parts.append(f"- {abs(cb)}b")
        return " ".join(parts).replace(" + -", " - ").replace(" - ", " - ").strip()

    term_str = format_shift(shared_shift)
    if shared_shift == 0:
        eq_str = f"{leading_factor}x^2 - {subtracted_factor}x = 0"
    else:
        eq_str = f"{leading_factor}{term_str}^2 - {subtracted_factor}{term_str} = 0"

    question_text = (
        f"Solve the quadratic equation {eq_str} by factoring. "
        f"Let the roots be $a$ and $b$ such that $a > b$. "
        f"Find the value of {format_linear_combination(linear_combination['a'], linear_combination['b'])}."
    )

    correct_answer = {
        "roots": [format_fraction(a_frac), format_fraction(b_frac)],
        "a": format_fraction(a_frac),
        "b": format_fraction(b_frac),
        "value": format_fraction(val_frac)
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