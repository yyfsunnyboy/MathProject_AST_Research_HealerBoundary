from core.prompts.domain_function_library import PolynomialOps, Fraction

def generate(level=1, **kwargs):
    frozen_params = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }

    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]

    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)

    correct_answer_remainder = str(remainder[1]) if len(remainder) > 0 else "0"
    
    # Ensure the answer is a string representation of the polynomial coefficients list for consistency with typical JSON answers unless specifically asked otherwise. 
    # However, looking at similar tasks where remainder can be complex fractions or lists:
    # The contract asks for `str` as type hint in my thought process but let's look closer at "remainder": str in the prompt description? 
    # Wait, re-reading: `"correct_answer": {"remainder": str, ...}`. Yes, it expects a string representation of the remainder coefficients list or value.
    
    correct_remainder_str = PolynomialOps.format_latex(remainder[1]) if len(remainder) > 0 else "0"

    return {
        "question_text": f"計算多項式 \\({dividend_coeffs}x\\) 除以 \\({divisor_coeffs}x\\) 所得的餘式。", # Reconstructing latex from coeffs for clarity in question text if needed, but prompt says use stem. 
        # Actually the instruction says: "question_text: the provided stem string (do not rebuild from scratch unless required)."
        # The frozen_params are [6,4,0] and [2,0,0]. Stem is already given as Chinese text with latex math. I will just return that exact stem or a slightly formatted version if needed to match context? 
        # Let's stick strictly to the provided `frozen_task_description` string for question_text unless it needs formatting based on coeffs which isn't explicitly required by "do not rebuild".
        # However, often these tasks want the latex rendered from coefficients. But since I have the exact stem text: "計算多項式 \(6x^2+4x\) 除以 \(2x^2\) 所得的餘式。", I will use that directly or ensure it matches the coeffs provided (which do).
        # Let's just output the string exactly as requested in the task block.
        
        "question_text": f"計算多項式 \\({dividend_coeffs}x\\) 除以 \\({divisor_coeffs}x\\) 所得的餘式。", 
        correct_answer: {
            "remainder": str(remainder[1]), # Wait, contract says remainder is string. Is it the list representation or latex? 
            # Re-reading generic example vs specific contract... The specific contract just says `"remainder": str`. 
            # In many polynomial division tasks in this domain, if the result is a number (like 0), it's "0". If it's a poly like [1,2], maybe "[1, 2]" or latex?
            # Let's look at `format_latex` usage. Usually answers are strings representing the value. 
            # Given the ambiguity between list and string representation for polynomials in JSON:
            # The contract explicitly says `"remainder": str`. A polynomial remainder is a coefficient list. Converting that to a string usually implies either `[...]` or latex.
            # Let's assume it wants the LaTeX form of the coefficients as seen in other similar tasks, OR just the Python list repr if treated as data? 
            # But `str(remainder[1])` on a Fraction gives "Fraction(...)". That is unlikely to be desired for an answer key unless specified.
            # Let's check the example: `PolynomialOps.div_qr(...)` returns lists of ints/Fractions/strs.
            # If I convert `[0]` (from 6x^2+4x / 2x^2 = x + 1? No wait... 
            # Dividend: 6, 4, 0 -> 6x^2 + 4x + 0. Degree 2.
            # Divisor: 2, 0, 0 -> 2x^2. Degree 2.
            # (6/2)x^(2-2) = 3. Quotient is [3]. Remainder should be the lower degree part? 
            # Actually standard polynomial division aligns degrees. 
            # Dividend: 6x^2 + 4x. Divisor: 2x^2.
            # Step 1: Multiply divisor by (6/2) = 3 to match x^2 term -> 6x^2. Subtract from dividend -> remainder is 4x - 0? 
            # Wait, the algorithm `div_qr` handles this automatically. 
            # Let's trace mentally:
            # Dividend [6, 4, 0] (deg 2). Divisor [2, 0, 0] (deg 2).
            # Leading term ratio: 6/2 = 3. Quotient adds 3 to x^0? No, degree diff is 0. So quotient has constant 3. 
            # Multiply divisor by 3 -> [6, 0, 0]. Subtract from dividend [6, 4, 0] - [6, 0, 0] = [0, 4, 0].
            # Next step: leading term of remainder is 4 (deg 1). Divisor leading term is 2 (deg 2). 
            # Since deg(remainder) < deg(divisor), we stop. Quotient is [3], Remainder is [0, 4, 0].
            # So remainder coefficients are [0, 4, 0] which normalizes to [4]? Or keeps leading zeros? `normalize` removes them. 
            # But `div_qr` returns the raw result before normalization usually? The doc says "highest degree first". 
            # If divisor is deg 2 and dividend deg 2, quotient deg 0. Remainder should be strictly lower degree than divisor (deg < 2).
            # So remainder [4] or [0, 4]? Usually leading zeros are kept if they represent the specific polynomial structure relative to original? 
            # But `normalize` removes them. Let's assume standard behavior: result of subtraction is [0, 4, 0]. Normalized -> [4].
            # Wait, does div_qr return normalized remainder? The example `[2, 0, 2] / [1, 1]`. 
            # Anyway, the code will handle it. I just need to format it correctly for `correct_answer["remainder"]`.
            
            "canonical_latex": PolynomialOps.format_latex(remainder[1]) if len(remainder) > 0 else "0"
        },
        "oracle_payload": frozen_params
    }
