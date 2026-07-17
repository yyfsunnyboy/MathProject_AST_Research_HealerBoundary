def generate(level=1, **kwargs):
    # Frozen parameters
    leading_factor = 2
    linear_combination = {"a": 1, "b": 2}
    root_order = "a>b"
    shared_shift = -7
    subtracted_factor = 10

    # Calculate roots
    r1 = shared_shift + subtracted_factor
    r2 = shared_shift - subtracted_factor

    # a is the larger root, b is the smaller root
    a = max(r1, r2)
    b = min(r1, r2)

    # Roots ordered a > b
    roots = [a, b]

    # Calculate value
    coeff_a = linear_combination["a"]
    coeff_b = linear_combination["b"]
    value = coeff_a * a + coeff_b * b

    # Construct quadratic equation coefficients
    A = leading_factor
    B = -leading_factor * (a + b)
    C = leading_factor * (a * b)

    # Format equation string
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

    eq_str = f"{term1}{term2}{term3} = 0"

    question_text = (
        f"Find the roots of the quadratic equation {eq_str}. "
        f"Let the roots be $a$ and $b$, where $a > b$. "
        f"What is the value of {coeff_a}a + {coeff_b}b?"
    )

    oracle_payload = {
        "leading_factor": leading_factor,
        "linear_combination": linear_combination,
        "root_order": root_order,
        "shared_shift": shared_shift,
        "subtracted_factor": subtracted_factor
    }

    correct_answer = {
        "roots": roots,
        "a": a,
        "b": b,
        "value": value
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }
