from core.prompts.domain_function_library import FractionOps, PolynomialOps

def generate(level=1, **kwargs):
    dividend_coefficients = kwargs.get("dividend_coefficients", [6, 0, 6])
    divisor_coefficients = kwargs.get("divisor_coefficients", [1, -4])
    
    # Convert inputs to Fraction to ensure exact arithmetic
    dividend_fracs = [FractionOps.create(c) for c in dividend_coefficients]
    divisor_fracs = [FractionOps.create(c) for c in divisor_coefficients]
    
    # Perform division using the domain API
    quot, rem = PolynomialOps.div_qr(dividend_fracs, divisor_fracs)
    
    def format_coeff(c):
        frac = FractionOps.create(c)
        num = frac.numerator
        den = frac.denominator
        if den == 1:
            return int(num)
        else:
            return f"{num}/{den}"
            
    quotient_coefficients = [format_coeff(c) for c in quot]
    remainder_coefficients = [format_coeff(c) for c in rem]
    
    dividend_str = PolynomialOps.format_latex(dividend_coefficients)
    divisor_str = PolynomialOps.format_latex(divisor_coefficients)
    
    question_text = f"Divide the polynomial ${dividend_str}$ by ${divisor_str}$. Find the quotient and the remainder."
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "quotient_coefficients": quotient_coefficients,
            "remainder_coefficients": remainder_coefficients
        },
        "oracle_payload": {
            "dividend_coefficients": dividend_coefficients,
            "divisor_coefficients": divisor_coefficients
        }
    }