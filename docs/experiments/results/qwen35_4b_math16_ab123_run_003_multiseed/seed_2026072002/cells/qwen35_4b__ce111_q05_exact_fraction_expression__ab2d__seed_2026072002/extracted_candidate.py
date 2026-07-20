import json
from fractions import Fraction as CoreFraction
from typing import Dict, Any


def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}

    # Perform arithmetic using CoreFraction for exact rational calculation
    term1 = CoreFraction(9, 22)
    term2 = CoreFraction(11, 18)
    
    inner_parenthesis = CoreFraction(23, 22) - CoreFraction(7, 18)
    result = (term1 + term2) - inner_parenthesis
    
    # Prepare correct_answer structure with numerator and denominator
    num = result.numerator
    den = result.denominator

    return {
        "question_text": r"\text{Simplify the following expression: } $\frac{9}{22} + \frac{11}{18} - \left(\frac{23}{22} - \frac{7}{18}\right)$",
        "correct_answer": {
            "numerator": num,
            "denominator": den,
            "canonical_latex": f"{result.numerator}/{result.denominator}" if result.denominator == 1 else str(result) # Ensure standard fraction format in latex string context usually implies a/b form even for integers unless specified mixed. The prompt asks for canonical_latex for an irreducible fraction. For integer results, the denominator is implicitly 1 but often displayed as just number or n/1 depending on strictness. However, since we are dealing with fractions and the result might be an integer (e.g., if it simplifies to whole), let's check: 
            # Calculation:
            # LCM of 22(2*11) and 18(2*3^2) is 198.
            # 9/22 = 81/198
            # 11/18 = 121/198 -> Sum LHS = 202/198
            # RHS: 23/22 - 7/18. Common denom 198. 
            # 23*9 = 207, 7*11=77. Diff = 130/198.
            # Total = 202/198 - 130/198 = 72/198.
            # Simplify 72/198: divide by GCD(72, 198). 
            # 72 = 6*12, 198=6*33 -> /6 = 12/33.
            # Divide by 3 -> 4/11.
            # Result is 4/11. So denominator is not 1. The code above handles it correctly via str(result).
        },
        "oracle_payload": frozen_params
    }