from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    leading_factor = 2
    linear_combination = {"a": 1, "b": 2}
    root_order = "a>b"
    shared_shift = -7
    subtracted_factor = 10

    # Calculate roots
    # Since subtracted_factor > 0, shift + sub_fact > shift - sub_fact
    # So a (larger) is shift + sub_fact, b (smaller) is shift - sub_fact
    a_val = shared_shift + subtracted_factor
    b_val = shared_shift - subtracted_factor

    a_frac = FractionOps.create(a_val)
    b_frac = FractionOps.create(b_val)

    coeff_a = linear_combination["a"]
    coeff_b = linear_combination["b"]

    coeff_a_frac = FractionOps.create(coeff_a)
    coeff_b_frac = FractionOps.create(coeff_b)

    term_a = FractionOps.mul(coeff_a_frac, a_frac)
    term_b = FractionOps.mul(coeff_b_frac, b_frac)
    value_frac = FractionOps.add(term_a, term_b)

    def format_fraction(f):
        if f.denominator == 1:
            return int(f.numerator)
        else:
            return f"{f.numerator}/{f.denominator}"

    a_formatted = format_fraction(a_frac)
    b_formatted = format_fraction(b_frac)
    value_formatted = format_fraction(value_frac)

    roots = [a_formatted, b_formatted]

    # Quadratic equation coefficients
    # Equation: leading_factor * (x - a) * (x - b) = 0
    # = leading_factor * (x^2 - (a+b)x + ab) = 0
    A = leading_factor
    B = -leading_factor * (a_val + b_val)
    C = leading_factor * a_val * b_val

    def format_quadratic(A, B, C):
        term1 = f"{A}x^2" if A != 1 else "x^2"

        if B > 0:
            term2 = f" + {B}x" if B != 1 else " + x"
        elif B < 0:
            term2 = f" - {-B}x" if B != -1 else " - x"
        else:
            term2 = ""

        if C > 0:
            term3 = f" + {C}"
        elif C < 0:
            term3 = f" - {-C}"
        else:
            term3 = ""

        return f"{term1}{term2}{term3} = 0"

    def format_linear_combination(coeff_a, coeff_b):
        parts = []
        if coeff_a == 1:
            parts.append("a")
        elif coeff_a == -1:
            parts.append("-a")
        elif coeff_a != 0:
            parts.append(f"{coeff_a}a")

        if coeff_b > 0:
            sign = " + " if parts else ""
            val = f"{coeff_b}b" if coeff_b != 1 else "b"
            parts.append(f"{sign}{val}")
        elif coeff_b < 0:
            sign = " - " if parts else "-"
            val = f"{-coeff_b}b" if coeff_b != -1 else "b"
            parts.append(f"{sign}{val}")

        return "".join(parts)

    eq_str = format_quadratic(A, B, C)
    lc_str = format_linear_combination(coeff_a, coeff_b)

    question_text = f"Solve the quadratic equation ${eq_str}$ for $x$. Let the roots be $a$ and $b$, ordered such that $a > b$. Find the value of ${lc_str}$."

    correct_answer = {
        "roots": roots,
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
