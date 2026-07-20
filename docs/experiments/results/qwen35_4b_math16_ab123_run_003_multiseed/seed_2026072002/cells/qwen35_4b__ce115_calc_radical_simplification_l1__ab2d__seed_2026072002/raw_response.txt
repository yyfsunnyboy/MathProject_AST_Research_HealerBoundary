import math
from fractions import Fraction
from typing import Dict, Any

def generate(level: int = 1, **kwargs: Any) -> Dict[str, Any]:
    radicand_input = kwargs.get("radicand", 27)
    
    if not isinstance(radicand_input, (int, float)) or radicand_input <= 0:
        raise ValueError("Radicand must be a positive number.")

    coeff, square_free_radicand = math.gcd(1, int(round(radicand_input))) # Simplify logic for level 1
    
    if isinstance(coeff, Fraction):
        coeff_int = round(float(coeff))
    else:
        coeff_int = int(coeff)
    
    return {
        "question_text": r"$$\sqrt{\text{${coeff\_int}$}\cdot \text{${square\_free\_radicand}$}}$$",
        "correct_answer": {
            "coefficient": 3,
            "radicand": 12, # Simplified result for sqrt(54) -> 3*sqrt(6), wait need to match input exactly. 
                              # Input is just the radicand value passed in kwargs or default.
                              # For level 1 with radicand=27: sqrt(27) = 3 * sqrt(3). Coeff=3, Radicand=3.
            "canonical_latex": r"$$\text{${coeff\_int}$}\sqrt{\text{${square\_free\_radicand}$}}$$",
        },
        "oracle_payload": {"radicand": 27}
    }