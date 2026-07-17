def generate(level=1, **kwargs):
    # Frozen parameters
    leading_factor = 2
    linear_combination = {"a": 1, "b": 2}
    root_order = "a>b"
    shared_shift = -7
    subtracted_factor = -10

    # Roots
    r1 = shared_shift
    r2 = shared_shift - subtracted_factor

    # Order roots (a > b)
    if r1 > r2:
        a = r1
        b = r2
    else:
        a = r2
        b = r1

    # Linear combination
    ca = linear_combination["a"]
    cb = linear_combination["b"]
    value = ca * a + cb * b

    # Coefficients
    A = leading_factor
    B = -leading_factor * (r1 + r2)
    C = leading_factor * r1 * r2

    # Format equation
    def format_quadratic(A, B, C):
        term1 = f"{A}x^2" if A != 1 else "x^2"
        if B > 0:
            term2 = f" + {B}x" if B != 1 else " + x"
        elif B < 0:
            term2 = f" - {abs(B)}x" if B != -1 else " - x"
        else:
            term2 = ""

        if C > 0:
            term3 = f" + {C}"
        elif C < 0:
            term3 = f" - {abs(C)}"
        else:
            term3 = ""
        return f"{term1}{term2}{term3} = 0"

    equation = format_quadratic(A, B, C)

    def format_linear_combination(ca, cb):
        if ca == 1:
            ta = "a"
        elif ca == -1:
            ta = "-a"
        else:
            ta = f"{ca}a"

        if cb > 0:
            tb = f" + {cb}b" if cb != 1 else " + b"
        elif cb < 0:
            tb = f" - {abs(cb)}b" if cb != -1 else " - b"
        else:
            tb = ""
        return f"{ta}{tb}"

    expr = format_linear_combination(ca, cb)

    question_text = f"Solve the quadratic equation ${equation}$. Let its roots be $a$ and $b$ such that $a > b$. Find the value of ${expr}$."

    correct_answer = {
        "roots": [a, b],
        "a": a,
        "b": b,
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
