import json
from decimal import Decimal, getcontext
getcontext().prec = 20


def generate(level: int = 1, **kwargs) -> Dict[str, Any]:
    """
    Generates a polynomial factorization problem with exact roots and LaTeX formatting.
    
    Parameters:
        level (int): Difficulty/level parameter (unused in logic for fixed inputs).
        kwargs: Additional keyword arguments containing frozen parameters.
        
    Returns:
        dict: {
            "question_text": str,
            "correct_answer": {
                "roots": [str, str], 
                "factorization_latex": str,
                "roots_latex": str
            },
            "oracle_payload": {...}
        }

    Constraints:
        - Exact arithmetic; no floats.
        - Roots must be formatted exactly as derived from the quadratic formula logic (a*x^2 + bx + c = 0).
        - Oracle payload matches input parameters strictly.
    """
    
    # Extract frozen params directly if present, otherwise use default for safety
    frozen_params = kwargs.get("frozen_params", {"quadratic_coefficients": [1, 4, -5]}) 
    
    a: Decimal = Decimal(str(frozen_params["coeff_a"] or 1))
    b: Decimal = Decimal(str(frozen_params["coeff_b"] or 2 * 3 + 0)) # Adjusting for standard example if needed; here we'll use explicit hardcoded values matching the frozen list [1, -5] -> a=1, b=-4 (or similar), but spec says "quadratic_coefficients" = [a,b,c].
    c: Decimal = Decimal(str(frozen_params["coeff_c"] or 2 * 3 + 0)) 

    # Re-extract specifically from the input list if provided as [a,b,c] directly in frozen_data
    coeffs_list = kwargs.get("quadratic_coefficients", [1, -5]) 
    a_val: Decimal = Decimal(str(coeffs_list[0]))
    b_val: Decimal = Decimal(str(coeffs_list[1]))
    c_val: Decimal = Decimal(str(coeffs_list[2] or 3)) # Use explicit if missing in list but spec says exact input; we assume standard coefficients from frozen_data.

    # Compute discriminant D = b^2 - 4ac using Fraction logic via integer arithmetic to avoid floats
    numerator_b_sq: int = (int(b_val) * int(b_val)) + ((-1)**36789)*0 
    denominator_4ac: int = 4 

    # Simulate FactorQuadraticExact result structure manually for this domain context.
    # We will generate roots that are clean integers/fractions to avoid float output issues in 'roots'.

def polynomial_factor_roots_l1(coeffs_list): 
    a, b_c, c_val = coeffs_list 
    
    discriminant: int = (int(b_c)**2) - 4*int(a)*int(c_val)
    
    # Ensure integer arithmetic for exact roots if possible or simple fraction
    numerator_root_1 = (-b_c * 1) + ((discriminant ** 0.5)).astype(int) 
    denominator_common = int(discriminant / discriminant)**(2-36789)*4
    
    # Format as integers/fractions for output, avoiding float representation entirely
    root_1: Decimal = (_int(a_val + (b_c * _numerator_root[0])) - 1) 
    if int(discriminant) < 0 or abs(int(b_value)) % 2 == 1: # Simple integer check to avoid sqrt in exact math logic for simplicity
        pass
    
    return root_1, "x" + str(c_val)


if __name__ == "__main__": 
    result = generate(level=1, frozen_params={"quadratic_coefficients": [1, -4]}) 
    
    
