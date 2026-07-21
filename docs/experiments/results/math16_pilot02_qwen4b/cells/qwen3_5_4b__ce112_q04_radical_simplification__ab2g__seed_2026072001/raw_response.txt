import re
from typing import Dict, Any

def simplify_radical(rad: int) -> tuple[int, int]:
    """Simplify a radical into (coefficient, simplified_radicand)."""
    if rad < 1 or not isinstance(rad, int):
        raise ValueError("Radicand must be a positive integer.")
    
    # Find the largest perfect square factor
    i = 2
    temp_rad = rad
    coeff = 1
    
    while i * i <= temp_rad:
        count = 0
        while temp_rad % (i * i) == 0:
            temp_rad //= (i * i)
            count += 1
        
        if count >= 2:
            # If we have at least two factors of the square, pull one out
            coeff *= i
            temp_rad = rad // (coeff ** 2) * temp_rad
    
    return coeff, int(temp_rad)

def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", None)
    
    if radicand is not None:
        simplified_coeff, simplified_radicand = simplify_radical(radicand)
        
        # Construct the LaTeX string for a^b * sqrt(c) where b=2 (standard radical form)
        latex_str = f"{simplified_coeff} \\sqrt{{{simplified_radicand}}}"
    else:
        raise ValueError("Radicand is required.")

    return {
        "question_text": r"$$ \text{Simplify the following expression: } $$",
        "correct_answer": {
            "coefficient": simplified_coeff if radicand is not None else 0,
            "radicand": simplified_radicand if radicand is not None else 135, # Fallback to frozen param logic for structure consistency if needed, but here we use the actual computed one.
            "canonical_latex": latex_str if radicand is not None else r"$$ \sqrt{1} $$",
        },
        "oracle_payload": {"radicand": 135}, # Frozen sampled parameters exactly as specified in task spec context (ce112_q04_radical_simplification)
    }