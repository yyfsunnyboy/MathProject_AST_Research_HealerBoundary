from fractions import Fraction as F
import sys
sys.path.insert(0, '.')
try:
    from core.prompts.domain_function_library import FractionOps
except ImportError:
    class FractionOps:
        @staticmethod
        def create(value):
            return F(str(value))
        @staticmethod
        def mul(a, b):
            return a * b
        @staticmethod
        def add(a, b):
            return a + b

def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    p1_left = F("2.79")
    p1_right = F("89.3")
    
    # Calculate first product: 2.79 * 89.3
    res1 = FractionOps.mul(p1_left, p1_right)
    
    p2_left = F("-0.21")
    p2_right = F("89.3")
    
    # Calculate second product: -0.21 * 89.3
    res2 = FractionOps.mul(p2_left, p2_right)

    # Expression: (2.79 * 89.3) + (-0.21 * 89.3)
    final_result = FractionOps.add(res1, res2)

    question_text = r"\text{Calculate the exact value of } x \cdot y - z \cdot w \\ \text{where } (x=2.79, y=89.3), (z=-0.21, w=89.3)."
    
    # Format answer as p/q string and LaTeX
    numerator = final_result.numerator
    denominator = final_result.denominator
    
    correct_answer_str = f"{numerator}/{denominator}"
    canonical_latex = r"\frac{" + str(numerator) + "}{"} + str(denominator) + r"}"

    return {
        "question_text": question_text,
        "correct_answer": {"value": correct_answer_str, "canonical_latex": canonical_latex},
        "oracle_payload": frozen_params
    }