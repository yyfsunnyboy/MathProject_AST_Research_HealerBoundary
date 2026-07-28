from fractions import Fraction as PyFraction
import sys
sys.path.insert(0, '.')
try:
    from core.prompts.domain_function_library import FractionOps
except ImportError:
    class FractionOps:
        @staticmethod
        def create(value):
            if isinstance(value, str) and '.' in value:
                return PyFraction(int(round(float(value))), 1)
            elif isinstance(value, (int, float)):
                return PyFraction(str(int(value)), 1)
            else:
                raise ValueError("Unsupported input type")

        @staticmethod
        def mul(a, b):
            if hasattr(a, 'numerator') and hasattr(b, 'numerator'):
                n = a.numerator * b.numerator
                d = a.denominator * b.denominator
                return PyFraction(n, d)
            else:
                raise TypeError("Arguments must be Fraction objects")

        @staticmethod
        def add(a, b):
            if hasattr(a, 'numerator') and hasattr(b, 'numerator'):
                n = a.numerator * b.denominator + b.numerator * a.denominator
                d = a.denominator * b.denominator
                return PyFraction(n, d)
            else:
                raise TypeError("Arguments must be Fraction objects")

def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    p1_left = PyFraction("279", 100)
    p1_right = PyFraction("893", 10)
    
    p2_left = PyFraction("-21", 100)
    p2_right = PyFraction("893", 10)

    res1 = FractionOps.mul(p1_left, p1_right)
    if frozen_params["products"][0]["sign"] == -1:
        res1 = FractionOps.add(res1, PyFraction(0)) # Placeholder for sign logic in expression context usually implies subtraction or negation. Given the structure "left op right", let's assume standard multiplication with potential negative result handling based on 'sign'. 
    else:
        pass

    res2 = FractionOps.mul(p2_left, p2_right)
    
    total_sum = FractionOps.add(res1, res2)
    
    # Ensure irreducible form is handled by PyFraction automatically
    
    correct_answer_value = f"{total_sum.numerator}/{total_sum.denominator}"
    canonical_latex = r"\frac{" + str(total_sum.numerator) + "}{"} + str(total_sum.denominator) + r"}"

    question_text = r"Calculate the exact value of the expression: $2.79 \times 89.3 + (-0.21) \times 89.3$."
    
    return {
        "question_text": question_text,
        "correct_answer": {"value": correct_answer_value, "canonical_latex": canonical_latex},
        "oracle_payload": frozen_params
    }