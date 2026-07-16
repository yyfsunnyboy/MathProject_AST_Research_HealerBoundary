from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    dividend = [6, 0, 6]
    divisor = [1, -4]
    
    # Use the domain API to perform polynomial division
    quotient, remainder = PolynomialOps.div_qr(dividend, divisor)
    
    # Convert coefficients to standard Python integers
    quotient_coefficients = [int(x) for x in quotient]
    remainder_coefficients = [int(x) for x in remainder]
    
    # Helper to format polynomial nicely for the question text
    def format_poly(coeffs):
        deg = len(coeffs) - 1
        terms = []
        for i, c in enumerate(coeffs):
            power = deg - i
            if c == 0:
                continue
            sign = "+" if c > 0 else "-"
            val = abs(c)
            
            if val == 1 and power > 0:
                val_str = ""
            else:
                val_str = str(val)
                
            if power == 0:
                term = val_str
            elif power == 1:
                term = f"{val_str}x"
            else:
                term = f"{val_str}x^{power}"
                
            terms.append((sign, term))
            
        if not terms:
            return "0"
            
        res = ""
        for i, (sign, term) in enumerate(terms):
            if i == 0:
                if sign == "-":
                    res += "-" + term
                else:
                    res += term
            else:
                res += f" {sign} {term}"
        return res

    dividend_str = format_poly(dividend)
    divisor_str = format_poly(divisor)
    
    question_text = (
        f"Divide the polynomial $P(x) = {dividend_str}$ by $D(x) = {divisor_str}$.\n"
        f"Find the quotient $Q(x)$ and the remainder $R(x)$."
    )
    
    correct_answer = {
        "quotient_coefficients": quotient_coefficients,
        "remainder_coefficients": remainder_coefficients
    }
    
    oracle_payload = {
        "dividend_coefficients": dividend,
        "divisor_coefficients": divisor
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }