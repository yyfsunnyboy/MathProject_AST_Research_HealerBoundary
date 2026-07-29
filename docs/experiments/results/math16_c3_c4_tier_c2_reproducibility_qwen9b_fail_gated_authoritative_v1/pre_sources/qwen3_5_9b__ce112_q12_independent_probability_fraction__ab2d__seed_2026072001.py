from typing import Dict, Any
import sys
sys.path.insert(0, '.')
try:
    from core.prompts.domain_function_library import FractionOps
except ImportError:
    class FractionOps:
        @staticmethod
        def create(value):
            if isinstance(value, list) and len(value) == 2:
                return value[0] / value[1]
            raise ValueError("Invalid input for create")

        @staticmethod
        def mul(a, b):
            num_a = a.numerator * b.numerator
            den_a = a.denominator * b.denominator
            if isinstance(num_a, int) and isinstance(den_a, int):
                from fractions import Fraction as F
                return F(num_a, den_a)
            raise TypeError("Expected Fractions")

        @staticmethod
        def to_latex(val, mixed=False):
            num = val.numerator
            den = val.denominator
            if isinstance(num, float) or isinstance(den, float):
                from fractions import Fraction as F
                f_val = F(float(num), float(den))
                return r"\frac{" + str(f_val.numerator) + "}{"}" + str(f_val.denominator) + r"}"
            if mixed:
                whole = num // den
                rem_num = abs(num % den)
                latex_str = f"{whole} \\frac{{{rem_num}}}{{{den}}}"
            else:
                latex_str = fr"\frac{{{num}}}{{{den}}}"
            return latex_str

def generate(level=1, **kwargs):
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    # Create fractions from p1 and p2 lists
    f_p1 = FractionOps.create(frozen_params["p1"])
    f_p2 = FractionOps.create(frozen_params["p2"])
    
    # Multiply the two probabilities to get independent probability fraction
    result_fraction = FractionOps.mul(f_p1, f_p2)
    
    # Generate LaTeX representation (default mixed=False for standard improper or proper fractions unless specified otherwise in typical math contexts, but usually simple fractions are preferred over mixed numbers for raw calculation results unless asked. We will stick to the default behavior which handles integers and floats gracefully).
    latex_str = FractionOps.to_latex(result_fraction)
    
    # Construct correct_answer dict with numerator, denominator, canonical_latex
    # Ensure we handle float conversion if necessary for JSON serialization of numer/denom in some contexts, 
    # but standard math problems expect ints. The to_exact adapter logic implies returning a structured object or dict.
    # We will construct the answer as a dictionary containing these fields.
    
    numerator = result_fraction.numerator
    denominator = result_fraction.denominator
    
    correct_answer = {
        "numerator": int(numerator),
        "denominator": int(denominator),
        "canonical_latex": latex_str
    }
    
    return {
        "question_text": r"Given two independent events with probabilities $p_1$ and $p_2$, where $p_1 = \frac{2}{6}$ and $p_2 = \frac{1}{5}$, calculate the probability of both events occurring. Express your answer as an irreducible fraction.",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }