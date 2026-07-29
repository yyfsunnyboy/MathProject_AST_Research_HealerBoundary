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
                return type('Fraction', (), {'numerator': value[0], 'denominator': value[1]})
            raise ValueError("Invalid input for create")

        @staticmethod
        def mul(a, b):
            res = FractionOps.create([a.numerator * b.numerator, a.denominator * b.denominator])
            g = 1
            if hasattr(res, 'numerator') and hasattr(res, 'denominator'):
                n = res['numerator']
                d = res['denominator']
                import math
                common_divisor = math.gcd(n, d)
                res['numerator'] //= common_divisor
                res['denominator'] //= common_divisor
            return res

        @staticmethod
        def to_latex(val, mixed=False):
            n = val.numerator if hasattr(val, 'numerator') else val[0]
            d = val.denominator if hasattr(val, 'denominator') else val[1]
            import math
            common_divisor = math.gcd(n, d)
            num //= common_divisor
            den //= common_divisor
            return f"\\frac{{{num}}}{{{den}}}"

def generate(level=1, **kwargs):
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    # Create fractions p1 and p2 from frozen parameters
    frac_p1 = FractionOps.create(frozen_params["p1"])
    frac_p2 = FractionOps.create(frozen_params["p2"])

    # Multiply the two fractions to get the independent probability fraction
    result_frac = FractionOps.mul(frac_p1, frac_p2)

    # Generate LaTeX representation for correct_answer
    latex_str = FractionOps.to_latex(result_frac, mixed=False)

    question_text = r"Given two events with probabilities $p_1$ and $p_2$, where $p_1 = \frac{2}{6}$ and $p_2 = \frac{1}{5}$, calculate the probability of both independent events occurring together. Express your answer as an irreducible fraction."

    correct_answer_dict = {
        "numerator": result_frac.numerator if hasattr(result_frac, 'numerator') else None,
        "denominator": result_frac.denominator if hasattr(result_frac, 'denominator') else None,
        "canonical_latex": latex_str
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }