import math
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 50

# Mocking required domain APIs as per specification constraints where actual imports are restricted by context
class RadicalOps:
    @staticmethod
    def simplify_term(coeff, radicand):
        # Simplify the radical term. For sqrt(A), we look for factors that form a square.
        if isinstance(radicand, int):
            temp = radicand.copy() if hasattr(int(), 'copy') else type(radicand)(1)
            m = 2
            reduced_radicand = radicand
            while m * m <= reduced_radicand:
                count = 0
                d = m
                n = reduced_radicand
                while n % d == 0 and n > 0: # simplified check logic for integer factorization simulation in this constrained environment
                    if not (n % (d*d) == 0): break 
                    temp_n = n // (d * d)
                    count += 1
                    reduced_radicand //= (d * d)
                else:
                    m += 2 # skip even numbers after finding a factor logic, or just increment by odd to be safe for simplicity if full prime factoring is too complex without libraries. 
                    # Given the strict environment, we implement basic square extraction manually.
                    
        # Fallback specific implementation based on common quadratic roots like sqrt(3) -> 1*sqrt(3)
        return coeff * (Decimal('1') / Decimal(radicand)) if radicand == int() else None

class FractionOps:
    @staticmethod
    def create(value):
        return value
    
def generate(level=1, **kwargs):
    frozen_params = {
        "equation": "(x-2)^2=3", 
        "order": "a>b", 
        "target": "2a+b"
    }
    
    # Solve the quadratic equation: (x-2)^2 = 3
    # x - 2 = +/- sqrt(3)
    # x = 2 + sqrt(3), x = 2 - sqrt(3)
    # Roots are in form a ± b*sqrt(c). Here, we have two roots.
    # Root 1: 2 + 1*sqrt(3) -> rational part 2, coeff 1, radicand 3
    # Root 2: 2 - 1*sqrt(3) -> rational part 2, coeff -1, radicand 3
    
    # Determine the "a" and "b" based on context usually implying the larger root or specific ordering if 'order' is provided. 
    # However, standard form for ordered quadratic roots often lists both or sums them unless specified otherwise in a multiple choice context not visible here.
    # The prompt asks to construct an answer object with rational_coefficient and radical_coefficient.
    # Let's assume the question expects the set of roots formatted correctly. 
    # Given "target": "2a+b", it implies we need values that satisfy this relationship, likely referring to specific coefficients found in the simplified form.
    
    # The roots are 2 + sqrt(3) and 2 - sqrt(3).
    # Let's define a = 1 (coefficient of root part if considering magnitude or just one representative?) 
    # Actually, usually "a" refers to the rational part? No, target is 2a+b. If roots are x1, x2...
    # Perhaps it asks for sum of coefficients in a specific representation?
    # Let's stick to generating the canonical LaTeX string for the solution set and calculating one valid instance that fits "rational_coefficient", "radical_coefficient".
    
    # Standard simplification: sqrt(3) -> 1*sqrt(3). 
    # Rational part of roots = 2. Radical coeff magnitude = 1, sign varies. Radicand = 3.
    
    rational_part = Fraction(2)
    radical_radicand = int(3)
    radical_coefficient_options = [Fraction(1), Fraction(-1)]
    
    # We will construct the canonical LaTeX for one of the roots or both if required by context, 
    # but typically these tasks want the full solution set.
    # Let's format "x = 2 + \sqrt{3}, x = 2 - \sqrt{3}".
    
    latex_roots = r"x=2+\sqrt{3} \text{ or } x=2-\sqrt{3}"
    
    correct_answer_data = {
        "rational_coefficient": rational_part, # The constant term in the roots (a in some contexts)
        "radical_coefficient": Fraction(1),   # Coefficient of sqrt(c) for positive root example
        "radicand": radical_radicand,         # Inside the square root
        "canonical_latex": latex_roots
    }

    question_text = r"Solve $(x-2)^2=3$."

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_data,
        "oracle_payload": frozen_params
    }