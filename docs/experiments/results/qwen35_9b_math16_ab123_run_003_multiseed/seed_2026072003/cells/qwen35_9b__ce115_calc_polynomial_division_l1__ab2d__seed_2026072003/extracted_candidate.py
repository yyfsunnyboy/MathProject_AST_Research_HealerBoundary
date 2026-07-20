def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import PolynomialOps
    
    frozen_params = kwargs.get("frozen_sampled_parameters", {})
    
    if not frozen_params:
        # Fallback generation logic if parameters are missing in context
        dividend_coeffs = [6, 0, 6]
        divisor_coeffs = [1, -4]
    else:
        dividend_coeffs = frozen_params.get("dividend_coefficients", [])
        divisor_coeffs = frozen_params.get("divisor_coefficients", [])

    # Validate inputs for polynomial division (degree check)
    if len(dividend_coeffs) == 0 or len(divisor_coeffs) <= 1:
        raise ValueError("Invalid coefficients provided.")
    
    quotient, remainder = PolynomialOps.div_qr(
        dividend_coefficients=dividend_coeffs, 
        divisor_coefficients=divisor_coeffs
    )

    # Construct LaTeX strings for the polynomials
    def format_poly(coeffs):
        if not coeffs: return "0"
        terms = []
        for i in range(len(coeffs)):
            c = coeffs[i]
            power = len(coeffs) - 1 - i
            if c == 0: continue
            
            term_parts = [str(c)]
            
            # Handle coefficient formatting (e.g., 6 -> "6", -4 -> "-4")
            if abs(c) != 1 or power == 0:
                term_parts.insert(0, str(abs(c)))
                
            var_part = ""
            if power > 0:
                if power == 1 and len(term_parts[0]) == 1: # Simplify x^1 to x
                     pass 
                elif abs(int(term_parts[-2])) != 1 or power == 0: # Check last term before var part logic? No.
                    var_part = f"x^{power}" if not (power==1 and len(str(c))>1) else "x"
                
            terms.append("".join(term_parts + [var_part] if var_part else ""))
        
        return "+".join(terms[::-1]) # Reverse to get high degree first

    quotient_latex = format_poly(quotient)
    remainder_latex = format_poly(remainder)

    correct_answer = {
        "quotient_coefficients": list(quotient),
        "remainder_coefficients": list(remainder),
        "quotient_latex": f"$\\left({quotient_latex}\\right)$",
        "remainder_latex": f"$\\left({remainder_latex}\\right)$" if remainder else "$0$"
    }

    return {
        "question_text": 
            "Perform polynomial division for the dividend $P(x) = \\sum_{i=0}^{n-1} a_i x^i$ and divisor $D(x) = \\sum_{j=0}^{m-1} b_j x^j$. Find the quotient $Q(x)$ such that $P(x) = D(x)Q(x) + R(x)$ where $\deg(R) < \deg(D)$.\n\nGiven:\nDividend coefficients: " + str(dividend_coeffs).replace("[", "$\\left( ").replace("]", "\\right)") + "\nDivisor coefficients: " + str(divisor_coeffs).replace("[", "$\\left( ").replace("]", "\\right)) + ".\n\nCompute the quotient and remainder.",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params if isinstance(frozen_params, dict) else {}
    }