import sys
sys.path.insert(0, '..')
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = {"expression": "5*x*(5*x - 2) - 4*(5*x - 2)**2", "required_form": "fully_factored"}
    
    # Parse the expression manually to ensure exact arithmetic with Fractions
    # Expression: 5x(5x-2) - 4(5x-2)^2
    # Let u = (5x-2). Then expr = 5xu - 4u^2.
    # We need factors of the quadratic in terms of x directly or by expanding and factoring.
    
    # Expand: 
    # Term1 = 5*x*(5*x) - 5*x*2 = 25x^2 - 10x
    # Term2 = 4 * (25x^2 - 20x + 4) = 100x^2 - 80x + 16
    # Total = (25x^2 - 10x) - (100x^2 - 80x + 16)
    #       = 25x^2 - 10x - 100x^2 + 80x - 16
    #       = -75x^2 + 70x - 16
    
    # We need to factor: -75x^2 + 70x - 16
    # Multiply by -1 for easier factoring first, then adjust signs later if needed.
    # 75x^2 - 70x + 16 = (ax - b)(cx - d) => ac=75, bd=16, ad+bc=70
    
    # Factors of 75: (3, 25), (5, 15).
    # If a=5, c=15. Need bd=16 and 5d + 15b = 70 => d + 3b = 14.
    # Pairs for 16: (1,16), (2,8), (4,4).
    # Try b=2, d=8 -> 8+6=14 (Match!)
    # So factors are (5x - 2) and (15x - 8)? Wait.
    # Let's re-verify: (5x - 2)(15x - 8) = 75x^2 - 40x - 30x + 16 = 75x^2 - 70x + 16. Correct.
    
    # Original expression was -(75x^2 - 70x + 16).
    # So factors are (-1)*(5x-2)*(15x-8) or (-(5x-2))*(15x-8) etc.
    # The prompt asks for two linear factors {x_coefficient, constant}. 
    # Usually implies the form (ax+b)(cx+d). Since leading coeff is negative in original expansion (-75), one factor must carry the negative sign or we distribute it.
    # Let's look at the structure: -1 * (5x-2) * (15x-8).
    # Factors could be represented as [-1, 0] and [5, -2]? No, that's not standard linear factor form in this context usually implying monic or specific grouping.
    # However, the task asks for "two {x_coefficient, constant} linear factors". 
    # Let's represent them as (A*x + B) and (C*x + D).
    # Option 1: (-5x + 2)(15x - 8) -> expands to -75x^2 + ... Correct.
    # Option 2: (5x - 2)(-15x + 8)? No, that's same as above with sign flip on second term? 
    # (-5x+2)*(15x-8) = -75x^2 + 40x + 30x - 16. Correct.
    
    # Let's define the factors explicitly:
    factor1_x, factor1_c = FractionOps.create(-5), FractionOps.create(2)
    factor2_x, factor2_c = FractionOps.create(15), FractionOps.create(-8)
    
    correct_answer = {
        "factors": [
            {"x_coefficient": int(factor1_x.numerator // factor1_x.denominator), "constant": int(factor1_c.numerator // factor1_c.denominator)}, # -5, 2
            {"x_coefficient": int(factor2_x.numerator // factor2_x.denominator), "constant": int(factor2_c.numerator // factor2_c.denominator)}   # 15, -8
        ]
    }

    return {
        "question_text": f"Factorize the expression: {frozen_params['expression']} into two linear factors.",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }