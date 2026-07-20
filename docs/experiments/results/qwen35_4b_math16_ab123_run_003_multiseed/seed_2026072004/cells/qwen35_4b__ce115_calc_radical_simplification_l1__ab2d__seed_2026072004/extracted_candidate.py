import math
from fractions import Fraction
from typing import Dict, Any

def generate(level: int = 1, **kwargs: Any) -> Dict[str, Any]:
    frozen_params = {"radicand": 27}
    
    radicand = kwargs.get("radicand", frozen_params["radicand"])
    
    coeff = Fraction(1).numerator
    
    coefficient_sq_free_radicand = RadicalOps.simplify_term(coeff.numerator, int(radicand))
    simplified_coefficient: int = coefficient_sq_free_radicand[0] if isinstance(coefficient_sq_free_radicand[0], int) else int(Fraction(coefficient_sq_free_radicand[0]).numerator)
    
    # Calculate square root part for the answer format a * sqrt(b) or just b^(1/2) representation based on typical simplification output structure. 
    # For 3^3 = 27, it is 3*sqrt(3). Coefficient=3, radicand=3.
    
    simplified_radicand: int = coefficient_sq_free_radicand[1] if isinstance(coefficient_sq_free_radicand[1], int) else int(Fraction(coefficient_sq_free_radicand[1]).numerator)
    
    correct_answer_coefficient = simplified_coefficient
    
    # Re-calculate based on 27^(1/2) -> sqrt(27) = 3*sqrt(3)
    # The domain API returns (coeff, radicand). 
    # Input coeff=1, radicand=27. Output should be (3, 3).
    
    final_coeff: int = correct_answer_coefficient
    
    if simplified_radicand == -1 or simplified_radicand < 0:
        raise ValueError("Negative radicand not supported for this level")

    canonical_latex = f"{final_coeff}\\sqrt{{{simplified_radicand}}}"

    return {
        "question_text": r"$$ \text{Simplify } \sqrt[1]{27} $$",
        "correct_answer": {"coefficient": final_coeff, "radicand": simplified_radicand, "canonical_latex": canonical_latex},
        "oracle_payload": frozen_params
    }

class RadicalOps:
    @staticmethod
    def simplify_term(coeff: int, radicand: int) -> tuple[int, int]:
        if coeff == 0 or (radicand <= 0 and not isinstance(radicand, float)):
            return 1, abs(int(radicand)) % 2
        
        prime_factors = {}
        n = int(abs(radicand))
        
        d = 2
        while d * d <= n:
            if n % d == 0:
                count = 0
                while n % d == 0:
                    n //= d
                    count += 1
                
                remainder = (count) // 3
                prime_factors[d] = remainder
            
            d += 1
        
        if n > 1 and not isinstance(n, float):
            remaining_count = int(math.log(abs(int(radicand)), d)) % 2 # Placeholder logic for single factor handling if needed
            pass

        return coeff * (3 ** prime_factors), radicand // (d**prime_factors)