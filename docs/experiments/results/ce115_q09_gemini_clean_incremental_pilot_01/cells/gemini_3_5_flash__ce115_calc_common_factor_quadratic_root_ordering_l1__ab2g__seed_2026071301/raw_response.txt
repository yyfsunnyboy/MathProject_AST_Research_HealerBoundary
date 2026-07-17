from fractions import Fraction

def generate(level=1, **kwargs):
    # Frozen parameters
    leading_factor = kwargs.get("leading_factor", 2)
    linear_combination = kwargs.get("linear_combination", {"a": 1, "b": 2})
    root_order = kwargs.get("root_order", "a>b")
    shared_shift = kwargs.get("shared_shift", 7)
    subtracted_factor = kwargs.get("subtracted_factor", 10)

    a_val = Fraction(2 * shared_shift + subtracted_factor, 2)
    b_val = Fraction(2 * shared_shift - subtracted_factor, 2)

    def format_rational(f):
        if f.denominator == 1:
            return f.numerator
        else:
            return f"{f.numerator}/{f.denominator}"

    a_str_or_int = format_rational(a_val)
    b_str_or_int = format_rational(b_val)

    coeff_a = linear_combination["a"]
    coeff_b = linear_combination["b"]

    value_val = coeff_a * a_val + coeff_b * b_val
    value_str_or_int = format_rational(value_val)

    A = Fraction(leading_factor)
    B = -Fraction(leading_factor) * (a_val + b_val)
    C = Fraction(leading_factor) * a_val * b_val

    def format_term(coeff, power):
        if coeff == 0:
            return ""
        if power == 2:
            if coeff == 1:
                coeff_str = ""
            elif coeff == -1:
                coeff_str = "-"
            else:
                coeff_str = str(format_rational(coeff))
            return f"{coeff_str}x^2"
        elif power == 1:
            if coeff > 0:
                sign = "+ "
                val = coeff
            else:
                sign = "- "
                val = -coeff
            if val == 1:
                val_str = ""
            else:
                val_str = str(format_rational(val))
            return f"{sign}{val_str}x"
        elif power == 0:
            if coeff > 0:
                return f"+ {format_rational(coeff)}"
            else:
                return f"- {format_rational(-coeff)}"
        return ""

    term2 = format_term(A, 2)
    term1 = format_term(B, 1)
    term0 = format_term(C, 0)

    equation = f"{term2} {term1} {term0} = 0".replace("  ", " ").strip()

    def format_linear_combination(ca, cb):
        parts = []
        if ca == 1:
            parts.append("a")
        elif ca == -1:
            parts.append("-a")
        elif ca != 0:
            parts.append(f"{ca}a")

        if cb == 1:
            if parts:
                parts.append("+ b")
            else:
                parts.append("b")
        elif cb == -1:
            parts.append("- b")
        elif cb > 0:
            if parts:
                parts.append(f"+ {cb}b")
            else:
                parts.append(f"{cb}b")
        elif cb < 0:
            parts.append(f"- {-cb}b")
        return " ".join(parts)

    lc_str = format_linear_combination(coeff_a, coeff_b)

    question_text = (
        f"Consider the quadratic equation {equation}.\n"
        f"Find its roots, and let them be $a$ and $b$ such that $a > b$.\n"
        f"Calculate the value of {lc_str}."
    )

    correct_answer = {
        "roots": [a_str_or_int, b_str_or_int],
        "a": a_str_or_int,
        "b": b_str_or_int,
        "value": value_str_or_int
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