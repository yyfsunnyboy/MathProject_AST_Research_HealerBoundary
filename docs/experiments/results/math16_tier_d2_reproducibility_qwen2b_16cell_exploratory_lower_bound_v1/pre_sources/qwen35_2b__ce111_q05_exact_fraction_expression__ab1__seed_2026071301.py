import json
from typing import Dict, Any

def generate(level=1, **kwargs) -> Dict[str, str]:
    """
    Generates the exact fraction expression problem based on frozen parameters.
    
    Args:
        level (int): Problem difficulty level (default 1).
        kwargs: Additional keyword arguments passed to the task specification.
        
    Returns:
        dict: A dictionary containing 'question_text', 'correct_answer', and 
              'oracle_payload'. The question text uses LaTeX delimiters, correct answer
              is a tuple of numerator/denominator/latex string, and oracle payload matches
              input kwargs exactly.
    """
    frozen_params = {
        "expression": "9/22 + 11/18 - (23/22 - 7/18)"
    }

    # Construct the question text using LaTeX delimiters as specified
    expression_str = json.dumps(frozen_params["expression"])
    
    def parse_fraction(s: str) -> tuple[int, int]:
        """Simple parser for 'numerator/denominator' format."""
        parts = s.split('/')
        if len(parts) == 2 and all(p.isdigit() or p == '-' for p in parts):
            return (int(parts[0]), int(parts[1]))
        raise ValueError(f"Invalid fraction string: {s}")

    numerator, denominator = parse_fraction(expression_str)
    
    # Calculate the exact value of the expression to find the simplest form
    from fractions import Fraction
    
    val = Fraction(numerator, denominator) + \
          Fraction(11, 18) - (Fraction(23, 22) - Fraction(7, 18))

    simplified_num = int(val.numerator)
    simplified_denom = int(val.denominator)
    
    # Ensure canonical form by checking if numerator and denominator share a common factor > 1
    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return abs(a)

    common_divisor = gcd(simplified_num, simplified_denom)
    
    if common_divisor != 1 and (simplified_num // common_divisor == 0 or 
                               simplified_denom // common_divisor == 0):
         # Handle edge cases where division results in zero denominator after reduction logic error prevention
        pass 

    canonical_latex = f"{simplified_num}/{simplified_denom}"

    return {
        "question_text": r"\text{9/22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})",
        "correct_answer": (simplified_num, simplified_denom, canonical_latex),
        "oracle_payload": frozen_params["expression"]
    }
