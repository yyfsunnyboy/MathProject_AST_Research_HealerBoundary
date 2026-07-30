import math
import re


def generate(level=1, **kwargs):
    expression = kwargs.get("expression", "3/7 - (-1/4)")

    match = re.match(r"(\d+)/(\d+)\s*-\s*\(-\s*(\d+)/(\d+)\)", expression)
    if match:
        a, b, c, d = map(int, match.groups())
        num = a * d + b * c
        den = b * d
    else:
        num, den = 19, 28
        a, b, c, d = 3, 7, 1, 4

    g = math.gcd(num, den)
    num //= g
    den //= g

    if den < 0:
        num = -num
        den = -den

    if den == 1:
        canonical_latex = str(num)
    elif num < 0:
        canonical_latex = f"-\\frac{{{abs(num)}}}{{{den}}}"
    else:
        canonical_latex = f"\\frac{{{num}}}{{{den}}}"

    latex_expr = f"\\frac{{{a}}}{{{b}}} - \\left(-\\frac{{{c}}}{{{d}}}\\right)"
    question_text = f"Evaluate the following expression:\n\\[ {latex_expr} \\]"

    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": num,
            "denominator": den,
            "canonical_latex": canonical_latex,
        },
        "oracle_payload": {"expression": expression},
    }