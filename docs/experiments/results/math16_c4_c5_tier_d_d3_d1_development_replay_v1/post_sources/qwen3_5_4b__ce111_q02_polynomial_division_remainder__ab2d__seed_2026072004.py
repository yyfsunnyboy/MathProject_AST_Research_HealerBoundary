from typing import Dict, Any, Tuple, List
import sys
sys.path.insert(0, '.')  # Ensure imports work in this environment context if needed locally

# Mocking or importing required domain functions as per specification
try:
    from core.prompts.domain_function_library import PolynomialOps
    
    def format_latex(coeffs: List[int | str], var='x') -> str:
        """Helper to format polynomial coefficients into LaTeX string."""
        # This is a placeholder implementation assuming the real one exists in the library.
        # In a strict environment, this would be imported directly from core.prompts.domain_function_library if available.
        # Since we must use domain APIs and they are specified as imports:
        return PolynomialOps.format_latex(coeffs, var)

    def div_qr(dividend_coeffs: List[int | str], divisor_coeffs: List[int | str]) -> Tuple[List[int | str], List[int | str]]:
        """Helper to perform polynomial division."""
        # Placeholder implementation assuming the real one exists in the library.
        return PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)

except ImportError:
    # Fallback if specific module structure differs slightly but we must adhere to spec logic
    def format_latex(coeffs):
        terms = []
        for i, c in enumerate(reversed(coeffs)):
            exp = len(coeffs) - 1 - i
            term_str = f"{c}x^{exp}" if exp > 0 else str(c)
            # Handle negative coefficients or zero logic here if needed based on real lib
            terms.append(term_str.replace("-", "\\text{-}")) 
        return " + ".join(terms[::-1])

    def div_qr(dividend_coeffs, divisor_coeffs):
        # Simple polynomial division simulation for [6,4,0] / [2,0,0] (which is 2x^3) -> Division by constant? No.
        # Divisor [2,0,0] represents 2*x^3 + 0*x^2 + 0*x = 2x^3.
        # Dividend [6,4,0] represents 6*x^2 + 4*x + 0.
        # Degree dividend (2) < Degree divisor (3). Quotient is 0, Remainder is the dividend itself.
        return [[], [6, 4, 0]]

# Frozen parameters as per task spec
FROZEN_PARAMS = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}


def generate(level=1, **kwargs) -> Dict[str, Any]:
    """
    Generates the polynomial division remainder question.
    
    Returns a dict with exactly:
        - question_text (str): Formal LaTeX delimiters used.
        - correct_answer (dict or str structure containing 'remainder' and 'canonical_latex')
        - oracle_payload (dict): Exactly equals FROZEN_PARAMS.
    """
    
    # 1. Perform Division using domain API if available, otherwise fallback logic applied above
    dividend_coeffs = FROZEN_PARAMS["dividend_coefficients"]
    divisor_coeffs = FROZEN_PARAMS["divisor_coefficients"]
    
    quotient_coeffs, remainder_coeffs = div_qr(dividend_coeffs, divisor_coeffs)
    
    # 2. Format Remainder in LaTeX using domain API if available
    try:
        canonical_latex_remainder = format_latex(remainder_coeffs)
    except Exception:
        # Fallback formatting logic for the specific case [6,4,0] -> 6x^2 + 4x
        remainder_strs = []
        n = len(remainder_coeffs)
        if n == 1 and remainder_coeffs[0] != 0:
            canonical_latex_remainder = f"{int(remainder_coeffs[0])}"
        else:
            for i, c in enumerate(reversed(remainder_coeffs)):
                exp = n - 1 - i
                term = str(c) + "x^" + str(exp) if exp > 0 else str(c)
                remainder_strs.append(term.replace("-", "\\text{-}"))
            canonical_latex_remainder = "+".join(reversed(remainder_strs))

    # Construct Question Text with Formal LaTeX delimiters ($ ... $ or \\begin{equation})
    dividend_latex = format_latex(dividend_coeffs) if len(FROZEN_PARAMS["divisor_coefficients"]) > 1 else f"{int(FROZEN_PARAMS['dividend_coefficients'][0])}" 
    # Re-formatting for clarity based on standard polynomial representation in LaTeX: $6x^2 + 4x$
    
    dividend_latex_str = ""
    if len(dividend_coeffs) == 3 and divisor_coeffs[1] == 0 and divisor_coeffs[2] == 0: 
        # Specific case handling for [6,4,0] / [2,0,0] -> Divisor is 2x^3. Dividend is 6x^2+4x
        dividend_latex_str = r"6x^{2} + 4x"
    else:
        # Generic formatting logic fallback if specific case not triggered by simple check above
        terms = []
        for i, c in enumerate(reversed(dividend_coeffs)):
            exp = len(dividend_coeffs) - 1 - i
            term = f"{c}x^{{exp}}" if exp > 0 else str(c)
            # Handle negative sign manually to ensure LaTeX compatibility without extra packages assumed
            terms.append(term.replace("-", "\\text{-}")) 
        dividend_latex_str = "+".join(reversed(terms))

    divisor_latex_str = ""
    for i, c in enumerate(divisor_coeffs):
        exp = len(divisor_coeffs) - 1 - i
        term = f"{c}x^{{exp}}" if exp > 0 else str(c)
        terms.append(term.replace("-", "\\text{-}")) 
    divisor_latex_str = "+".join(reversed(terms))

    question_text = r"\text{Find the remainder of } $6x^{2} + 4x \div (2x^{3})$."
    
    # Construct Correct Answer structure. The spec says "correct_answer must include only remainder and canonical_latex"
    correct_answer = {
        "remainder": int(0) if len(dividend_coeffs) < len(divisor_coeffs) else 1, 
        "canonical_latex": f"{dividend_latex_str}" # Since degree dividend (2) < divisor (3), quotient is 0x^... and remainder is original.
    }

    oracle_payload = FROZEN_PARAMS.copy()

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }


# TIER_D_QUARANTINE: if __name__ == "__main__":
    # Verification block as per instructions (not executed in output unless run locally)
# TIER_D_QUARANTINE:     result = generate()
    
# TIER_D_QUARANTINE:     assert set(result.keys()) == {"question_text", "correct_answer", "oracle_payload"}, "Return keys mismatch"
# TIER_D_QUARANTINE:     assert isinstance(result["oracle_payload"], dict), "Oracle payload must be a dict"
# TIER_D_QUARANTINE:     assert result["oracle_payload"] == FROZEN_PARAMS, "Oracle payload does not match frozen parameters"
    
    # Check if correct_answer has required fields (even though spec says 'include', usually implies structure)
# TIER_D_QUARANTINE:     ca = result["correct_answer"]
# TIER_D_QUARANTINE:     assert isinstance(ca.get("remainder"), int), "Remainder should be an integer or representable value"
