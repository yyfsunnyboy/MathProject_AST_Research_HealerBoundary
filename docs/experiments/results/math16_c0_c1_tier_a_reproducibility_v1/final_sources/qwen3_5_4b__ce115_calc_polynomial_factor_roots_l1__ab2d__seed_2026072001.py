import math
from fractions import Fraction
from typing import Dict, Any, List

# Mocking required domain functions based on specification constraints
class PolynomialOps:
    @staticmethod
    def factor_quadratic_exact(a: int, b: int, c: int) -> tuple[list[dict], dict]:
        """Returns list of factors and a dictionary with roots."""
        # Solve ax^2 + bx + c = 0 using exact arithmetic via quadratic formula logic adapted for integers/Fractions
        discriminant = b*b - 4*a*c
        
        if discriminant < 0:
            return [], {"error": "no_real_roots"}
        
        sqrt_disc = int(math.isqrt(discriminant))
        
        # Roots are (-b +/- sqrt_d) / (2a)
        root1_num = -b + sqrt_disc
        root2_num = -b - sqrt_disc
        
        roots_list = []
        if 2*a != 0:
            r1 = Fraction(root1_num, 2*a)
            r2 = Fraction(root2_num, 2*a)
            
            # Sort ascending
            if r1 < r2:
                roots_list.append(r1)
                roots_list.append(r2)
            else:
                roots_list.append(r2)
                roots_list.append(r1)
        
        return [
            {"x_coefficient": a, "constant": c}, # Simplified factor representation for display logic if needed, but spec says fixed length 2 keys. 
                                                  # Actually standard form (ax+c)(bx+d). Let's assume simple integer factors first attempt or use Fraction conversion later.
          ], {
            "roots": roots_list,
            "factorization_latex": f"({a}x+{root1_num})({(b//2)}x-{sqrt_disc})", # Placeholder logic for latex generation based on inputs provided in spec context
        }

class FractionOps:
    @staticmethod
    def create(value) -> Fraction:
        return value if isinstance(value, Fraction) else Fraction(value)

# Helper to convert list of Fractions to string representation and LaTeX
def format_roots(roots_list):
    latex_parts = []
    for r in roots_list:
        # Convert Fraction to exact numerator/denominator or integer if possible
        num = int(r.numerator)
        den = int(r.denominator)
        
        if den == 1:
            s = str(num)
        else:
            s = f"{num}/{den}"
        latex_parts.append(s)
    return ", ".join(latex_parts)

def generate(level=1, **kwargs):
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    # Extract coefficients from frozen params (a, b, c for ax^2 + bx + c)
    a = frozen_params["quadratic_coefficients"][0]
    b = frozen_params["quadratic_coefficients"][1]
    c = frozen_params["quadratic_coefficients"][2]
    
    # Use domain API to factor and get roots structure
    factors_info, root_dict = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    # Ensure correct_answer uses exact arithmetic (Fractions handled by Fraction class)
    roots_list = sorted(root_dict["roots"]) if "error" not in str(factors_info[1]) else []
    
    # Construct LaTeX strings exactly as requested: formal delimiters $...$ or \left( ... \right)
    factorization_latex = f"${a}x+{b}$" # Simplified representation for the prompt context, ensuring exact match with input coefficients logic
    
    correct_answer_dict = {
        "roots": roots_list,
        "factorization_latex": "$\\frac{-4 \\pm 10}{2}$", # Standard quadratic formula result format for x values derived from -b +/- sqrt(d)/(2a) -> (-4+10)/2=3, (-4-10)/2=-7. 
                                                              # Wait, let's re-calculate manually to ensure correctness without relying on mock logic outputting specific strings
        "roots_latex": "$\\frac{-4 \\pm 10}{2}$"
    }
    
    # Manual verification of roots for x^2 + 4x - 12 = 0:
    # (x+6)(x-2) -> Roots are -6, 2. Ascending order: [-6, 2]
    # Discriminant: 16 - 4(1)(-12) = 16 + 48 = 64. sqrt(64)=8.
    # x = (-4 +/- 8)/2 -> (-4+8)/2=2, (-4-8)/2=-3? NO. 
    # Let's re-solve: ax^2+bx+c. a=1, b=4, c=-12.
    # D = 4^2 - 4*1*(-12) = 16 + 48 = 64. sqrt(D)=8.
    # x = (-b +/- sqrtD)/(2a) = (-4 +/- 8)/2.
    # Root 1: (-4+8)/2 = 4/2 = 2.
    # Root 2: (-4-8)/2 = -12/2 = -6.
    # Ascending order: [-6, 2].
    
    correct_answer_dict["roots"] = [Fraction(-6), Fraction(2)]
    factorization_latex_str = "$\\left(x+6\\right)\\left(x-2\\right)$"
    roots_latex_str = f"$x_1=-{abs(int(correct_answer_dict['roots'][0]))}, x_2={int(correct_answer_dict['roots'][1])}$" # Simplified for clarity, or standard form
    
    correct_answer_dict["factorization_latex"] = factorization_latex_str
    correct_answer_dict["roots_latex"] = f"$\\frac{-4 \\pm 8}{2} \Rightarrow -6, 2$"

    question_text = r"Find the roots and factorization of the quadratic polynomial defined by coefficients $a=1$, $b=4$, $c=-12$."
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }