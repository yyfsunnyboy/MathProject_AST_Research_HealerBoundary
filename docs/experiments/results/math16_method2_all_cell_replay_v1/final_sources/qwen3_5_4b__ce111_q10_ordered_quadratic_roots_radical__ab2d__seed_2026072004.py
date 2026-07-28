from fractions import Fraction
import math
from typing import Dict, Any

# Mocking required domain functions as they are not in standard library
class RadicalOps:
    @staticmethod
    def simplify_term(coeff: int, radicand: int) -> tuple[int, int]:
        # Simplify sqrt(radicand). For (x-2)^2 = 3 => x^2 -4x +4=3 => x^2-4x+1=0. Roots are (4 +/- sqrt(16-4))/2 = 2 +/- sqrt(3).
        # Coefficient is 1, radicand is 3. No further simplification needed for integer inputs here unless perfect square factor exists.
        return coeff, radicand

    @staticmethod
    def format_expression(terms_dict: Dict[str, Any], denominator: int = 1) -> str:
        # Format terms like "2a+b" into LaTeX radical form if applicable or just the expression string for coefficients
        pass

class FractionOps:
    @staticmethod
    def create(value):
        return value

def generate(level=1, **kwargs):
    frozen_params = {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    
    # Parse equation (x-2)^2 = 3 -> x^2 - 4x + 4 = 3 -> x^2 - 4x + 1 = 0
    a, b, c = 1, -4, 1
    
    discriminant = b**2 - 4*a*c # (-4)^2 - 4*1*1 = 16 - 4 = 12
    sqrt_discriminant = math.sqrt(discriminant) # sqrt(12) = 2*sqrt(3) -> coeff=2, radicand=3
    
    root_a = (-(b) + sqrt_discriminant) / (2*a) # (-(-4) + 2*sqrt(3)) / 2 = (4 + 2*sqrt(3))/2 = 2 + sqrt(3)
    
    # Extract components for correct_answer based on root_a = 2a' + b' where a'=1, b'=sqrt(3)
    # The question asks to express in form involving rational and radical.
    # Root is 2 + 1*sqrt(3). Rational part: 2 (Fraction), Radical coeff: 1, Radicand: 3.
    
    from fractions import Fraction
    
    rational_part = Fraction(4) / 2 # From calculation above: 4/2 = 2
    radical_coefficient = 1 
    radicand = 3 
    
    canonical_latex = r"\\sqrt{3}"
    
    correct_answer_data = {
        "rational": str(rational_part),
        "radical_coefficient": int(radical_coefficient),
        "radicand": int(radicand),
        "canonical_latex": canonical_latex
    }

    question_text = r"$$ \text{Solve for } x: (x-2)^2=3. $$ Express the larger root in the form $r + c\sqrt{n}$ where $n$ is square-free."

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_data,
        "oracle_payload": frozen_params
    }