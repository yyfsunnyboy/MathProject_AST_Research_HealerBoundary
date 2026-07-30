# -*- coding: utf-8 -*-

try:
    from core.prompts.domain_function_library import FractionOps
except ImportError:
    from fractions import Fraction
    class FractionOps:
        @staticmethod
        def create(val):
            return Fraction(str(val))
        @staticmethod
        def mul(a, b):
            return a * b
        @staticmethod
        def sub(a, b):
            return a - b
        @staticmethod
        def add(a, b):
            return a + b

def generate(level=1, **kwargs):
    # Frozen parameters
    oracle_payload = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }

    # Compute exact result using FractionOps
    p1_left = FractionOps.create("2.79")
    p1_right = FractionOps.create("89.3")
    p1_prod = FractionOps.mul(p1_left, p1_right)

    p2_left = FractionOps.create("-0.21")
    p2_right = FractionOps.create("89.3")
    p2_prod = FractionOps.mul(p2_left, p2_right)

    # Since sign of first is 1 and second is -1:
    # expression is p1_prod - p2_prod
    res = FractionOps.sub(p1_prod, p2_prod)

    from fractions import Fraction
    res_fraction = Fraction(res)
    num = res_fraction.numerator
    den = res_fraction.denominator

    question_text = "Calculate the exact value of the following expression:\n\\[ 2.79 \\times 89.3 - (-0.21) \\times 89.3 \\]"

    correct_answer = {
        "value": f"{num}/{den}",
        "numerator": num,
        "denominator": den,
        "canonical_latex": f"\\frac{{{num}}}{{{den}}}"
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }