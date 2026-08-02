from core.prompts.domain_function_library import PolynomialOps


def generate(level=1, **kwargs):
    frozen_params = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }

    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]

    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)

    # Convert coefficients to strings for the 'remainder' field as per contract expectation (str type)
    remainder_strs = [str(c) if isinstance(c, str) else c.__class__.__name__ + "(" + repr(c).__replace("Fraction(", "frac").replace(")", ")") 
                     for c in remainder]

    # For JSON-safe string representation of the coefficients list
    def coeff_to_latex_list(coeffs):
        latex_parts = []
        if not coeffs:
            return ""
        
        is_zero_poly = all(c == 0 or (isinstance(c, str) and "p/q" in c.lower()) for c in coeffs[:1]) # simplified check
        
        result_strs = [str(c).replace("Fraction(", "").replace("/", "") if isinstance(c, Fraction) else 
                       f"{c}" if not hasattr(c, '__class__') or 'Fraction' not in str(type(c)) else "p/q" for c in coeffs]
        
        # Re-evaluate based on actual types returned by div_qr which are int | str (for p/q)
        latex_parts = []
        for i, coeff in enumerate(coeffs):
            if isinstance(coeff, Fraction):
                val_str = f"{coeff.numerator}/{coeff.denominator}"
            elif hasattr(coeff, '__class__') and 'Fraction' in type(coeff).__name__: # Fallback check
                 pass 
            else:
                val_str = str(coeff)

        latex_parts.append(val_str if i == 0 or (i > 0 and coeffs[i-1] != 0) else "")
        
    return {
        "question_text": f"計算多項式 \\({dividend_coeffs[0]}x^2+{dividend_coeffs[1]}x\\) 除以 \\({divisor_coeffs[0]}x^{len(divisor_coeffs)-1}\\) 所得的餘式。",
        "correct_answer": {
            "remainder": str(remainder), # div_qr returns list[int | str], converting to string representation for JSON compatibility if needed, but contract says 'str' type. 
                                         # Since remainder is a list of int/str (e.g., [0] or ['p/q']), we need the specific format expected by oracle_type='polynomial_division_remainder_only'.
                                         # The example in generic code shows q and r as lists. Contract asks for 'remainder': str. 
                                         # Assuming it wants a string representation of the list elements joined, e.g., "0" or "p/q".
            "canonical_latex": PolynomialOps.format_latex(remainder) if isinstance(remainder, (list)) else ""
        },
        "oracle_payload": frozen_params
    }

# Correction for specific answer contract requirements based on typical polynomial division outputs:
# The 'correct_answer' expects remainder as a string and canonical_latex. 
# Since the input coefficients are integers [6, 4, 0] divided by [2, 0, 0], 
# PolynomialOps.div_qr will return quotient=[3, 2, -1] (representing 3x^2 + 2x - x = 3x^2+x) and remainder=[] or similar?
# Wait: Dividend is 6x^2+4x. Divisor is 2x^2. 
# Quotient calculation: (6/2)x^(2-2) = 3. Remainder after subtracting 3*2x^2 = 0 + 4x - 0?
# Actually, standard polynomial division of degree n by m where deg(dividend)=deg(divisor):
# Dividend P(x) = a_n x^n + ... 
# Divisor Q(x) = b_m x^m + ... (here m=n=2).
# Leading term: 6x^2 / 2x^2 = 3. So quotient starts with 3.
# Multiply divisor by 3: 3 * [2, 0, 0] -> [6, 0, 0].
# Subtract from dividend [6, 4, 0]: [6-6, 4-0, 0-0] = [0, 4, 0].
# Degree of remainder is less than divisor (1 < 2). 
# So quotient coefficients: [3], remainder coefficients: [0, 4, 0]? No.
# Remainder should be the result after subtraction which has degree < deg(divisor).
# The list returned by div_qr for inputs ([6,4,0], [2,0,0]) will likely be q=[3] (or similar depending on normalization) and r=[0, 4]. 
# Let's rely on the API to compute exactly.

    # Re-implementing logic strictly using provided APIs without manual calculation errors
    from fractions import Fraction
    
    def get_remainder_string(coeffs_list):
        if not coeffs_list:
            return "0"
        
        # Convert list of ints/strs to a format suitable for 'remainder' field (string)
        # If the remainder is [4], string should be "4". 
        # The API returns int or str. We join them? Or just convert each element?
        # Given contract: {"remainder": str, ...} -> likely expects a single string representation of the polynomial coefficients list.
        
        parts = []
        for c in coeffs_list:
            if isinstance(c, Fraction):
                val = f"{c.numerator}/{c.denominator}"
            elif hasattr(c, '__class__') and 'Fraction' not in str(type(c)): # It's an int or string like "p/q" from API? 
                 pass
            
        return ",".join(str(x) if isinstance(x, (int, float)) else x for x in coeffs_list).strip()

    def get_canonical_latex(coeffs_list):
        try:
            latex = PolynomialOps.format_latex(coeffs_list)
        except Exception as e:
            # Fallback manual construction if format_latex fails on mixed types or specific structures
            return "" 
        return latex
    
    final_result = {
        "question_text": f"計算多項式 \\({dividend_coeffs[0]}x^2+{dividend_coeffs[1]}x\\) 除以 \\({divisor_coeffs[0]}x^{len(divisor_coeffs)-1}\\) 所得的餘式。",
        "correct_answer": {
            "remainder": str(remainder), # Assuming remainder is a list, converting to string representation of the list content? 
                                         # Or maybe just the first element if it's degree based? 
                                         # Let's assume standard JSON serialization of the list elements joined or simply converted.
                                         # Based on similar tasks, 'str' might mean the polynomial expression itself as a string.
            "canonical_latex": PolynomialOps.format_latex(remainder)
        },
        "oracle_payload": frozen_params
    }

# Final refined version ensuring strict adherence to types and API usage:
from fractions import Fraction


def generate(level=1, **kwargs):
    # Re-define variables for clarity within the function scope
    dividend_coeffs = [6, 4, 0]
    divisor_coeffs = [2, 0, 0]

    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)

    # Construct 'remainder' as a string. 
    # The API returns list[int | str]. We need to represent this polynomial's coefficients in text form.
    # If the result is [4], then "4". If ['p/q'], then that string representation?
    # Let's assume it wants the sum of terms or just the coefficient if degree 0? 
    # Actually, for remainder only tasks, often the answer is the polynomial itself represented as a list of coefficients converted to text.
    
    def coeffs_to_str(coeffs):
        res = []
        for c in coeffs:
            if isinstance(c, Fraction):
                val = f"{c.numerator}/{c.denominator}"
            elif hasattr(c, '__class__') and 'Fraction' not in str(type(c)): # int or float
                 pass
            
    return {
        "question_text": "計算多項式 \\(6x^2+4x\\) 除以 \\(2x^2\\) 所得的餘式。",
        "correct_answer": {
            "remainder": str(remainder), # This might be a list, converting to string representation of the list? 
                                         # Or perhaps just the value if it's scalar. 
                                         # Given 'str' type requirement in contract: likely expects something like "[4]" or similar depending on implementation details.
                                         # However, looking at typical outputs for such contracts, it often wants the polynomial expression as a string.
            "canonical_latex": PolynomialOps.format_latex(remainder) if isinstance(remainder, list) else ""
        },
        "oracle_payload": {
            "dividend_coefficients": [6, 4, 0],
            "divisor_coefficients": [2, 0, 0]
        }
    }

# Corrected implementation focusing on exact types and minimal assumptions:
from fractions import Fraction


def generate(level=1, **kwargs):
    dividend_coeffs = [6, 4, 0]
    divisor_coeffs = [2, 0, 0]

    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)

    # Helper to convert list of coefficients to a string representation suitable for 'remainder' field (str type)
    def format_remainder_list(coeffs):
        if not coeffs:
            return "0"
        
        terms = []
        for i, c in enumerate(coeffs):
            term_str = ""
            # Handle Fraction specifically as it might be returned by div_qr if inputs were floats or mixed? 
            # But here inputs are int. So remainder should be ints.
            
            val = str(c)
            terms.append(val)
        
        return ",".join(terms).strip()

    def format_remainder_latex(coeffs):
        try:
            latex_str = PolynomialOps.format_latex(coeffs)
            # Ensure it's not empty or invalid if coeffs is a list of ints/strs that might confuse the formatter?
            # The API handles int/Fraction well. 
            return latex_str
        except Exception as e:
            return ""

    correct_answer = {
        "remainder": format_remainder_list(remainder),
        "canonical_latex": format_remainder_latex(remainder)
    }

    oracle_payload = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }

    return {
        "question_text": correct_answer["canonical_latex"], # Wait, question_text should be the provided stem. 
                     # The prompt says: 'question_text': str (the provided stem string).
                     # So use the frozen_params description directly or reconstruct it?
                     # Frozen params don't have text, but task block has "Frozen task description".
        }

# Final Correct Implementation
from fractions import Fraction


def generate(level=1, **kwargs):
    dividend_coeffs = [6, 4, 0]
    divisor_coeffs = [2, 0, 0]

    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)

    # Convert list of coefficients to string representation for 'remainder' field (str type)
    def coeffs_to_str(coeffs):
        if not coeffs:
            return "0"
        
        parts = []
        for c in coeffs:
            val = str(c)
            parts.append(val)
        
        # Join with commas or similar separator? Usually lists are represented as comma-separated values.
        return ",".join(parts).strip()

    def format_latex_list(coeffs):
        try:
            latex_str = PolynomialOps.format_latex(coeffs)
            if not latex_str:
                return ""
            # Ensure it's a valid polynomial string representation
            return latex_str
        except Exception as e:
            return str(remainder).replace("list", "")

    correct_answer = {
        "remainder": coeffs_to_str(remainder),
        "canonical_latex": format_latex_list(remainder)
    }

    oracle_payload = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }

    return {
        "question_text": f"計算多項式 \\({dividend_coeffs[0]}x^2+{dividend_coeffs[1]}x\\) 除以 \\({divisor_coeffs[0]}x^{len(divisor_coeffs)-1}\\) 所得的餘式。",
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }

# Final check: The question text must be the provided stem. 
# Stem: "計算多項式 \(6x^2+4x\) 除以 \(2x^2\) 所得的餘式。"
