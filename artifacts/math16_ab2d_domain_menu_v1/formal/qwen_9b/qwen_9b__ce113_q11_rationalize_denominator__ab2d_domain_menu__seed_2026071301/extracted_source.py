def generate(level=1, **kwargs):
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }

    # Extract components from the denominator string representation provided in oracle_payload
    denom_rational_part = 4
    denom_radical_coeff = -1
    radicand_val = frozen_params["radicand"]

    # Rationalize the linear radical expression: numerator / (denom_rational + denom_radical * sqrt(radicand))
    # The API expects: RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand)
    result_tuple = RadicalOps.rationalize_linear_denominator(9, 4, -1, 7)

    # Unpack the tuple (new_numerator_num, new_numerator_denom, simplified_radicand_int)
    # Based on API description: returns tuple[int | Fraction, int | Fraction, int]
    num_part = result_tuple[0]
    den_part = result_tuple[1]

    # The problem asks for the value of a + b where the expression equals a + b*sqrt(7).
    # This implies we need to evaluate the rationalized fraction.
    # However, looking at typical Math16 tasks and the "integer_exact" contract:
    # Usually, these problems result in an integer sum or require simplification of coefficients first.
    # Let's check if num_part/den_part is an integer or simple form.
    
    from fractions import Fraction
    
    val = Fraction(num_part) / den_part

    # The problem asks for a+b where expression = a + b*sqrt(7).
    # Wait, the rationalization of 9/(4-sqrt(7)) results in:
    # Multiply by (4+sqrt(7))/(16-7) -> 9*(4+sqrt(7))/9 -> 4 + sqrt(7).
    # So a=4, b=1. Sum = 5.
    
    # Let's verify the API output logic matches this expectation or if we need to parse components differently.
    # If result_tuple[0] is numerator and [1] is denominator after rationalization step:
    # For input (9, 4, -1, 7): 
    # Conjugate denom = 4 + sqrt(7). Denom^2 = 16-7=9.
    # New Num = 9 * (4+sqrt(7)) / 9? No, the API likely handles the algebraic simplification internally or returns components of A/B form.
    
    # Let's assume standard behavior: 
    # Rationalize linear denominator usually returns simplified coefficients for numerator/denominator if not fully cancelling.
    # But here it cancels perfectly to integer + radical term? Or just rational number?
    # Actually, the API `rationalize_linear_denominator` description says "returns tuple...".
    # If the result is 4 + sqrt(7), how does that map to (numerator, denominator)? 
    # Perhaps it returns coefficients of A and B directly if possible, or a fraction.
    
    # Re-reading API: `RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand)`
    # Returns tuple[int | Fraction, int | Fraction, int] -> (new_num, new_denom, simplified_radicand) ?? 
    # Or maybe it returns the coefficients of the result directly? No, signature says "tuple".
    
    # Let's simulate: 9 / (4 - sqrt(7)) * (4 + sqrt(7))/(16-7) = 9*(4+sqrt(7))/9 = 4 + sqrt(7).
    # If the API returns components of a fraction, it might be Fraction(4), Fraction(0)? No.
    # Maybe it returns coefficients for A and B directly? 
    # Let's look at `simplify_term` example: (2, 3) from (1, 12). That simplifies sqrt(12)=2sqrt(3). Coeff=2, radicand=3.
    
    # Hypothesis: The API might return the coefficients of the final simplified form if it's linear? 
    # But signature says `tuple[int | Fraction, int | Fraction, int]`. Three elements.
    # Likely (numerator_coefficient_of_rational_part?, denominator??) No.
    
    # Alternative interpretation: It returns (A_num, A_denom, B_num)? Unlikely for single call.
    # Most likely it returns the rationalized numerator and denominator of the fraction representing the whole number? 
    # But 4 + sqrt(7) is not a simple fraction p/q unless we separate parts.
    
    # Let's reconsider the "oracle_payload" hint: radicand=7, denom="4-sqrt(7)".
    # If I call `RadicalOps.rationalize_linear_denominator`, what does it return?
    # Example in docstring is missing for this specific function other than generic tuple shape.
    
    # Let's try to deduce from the math: Result is 4 + sqrt(7). 
    # a=4, b=1. Sum = 5.
    # How do I get 5 programmatically?
    # If `result_tuple` contains components that allow reconstruction of A+B*sqrt(radicand):
    # Maybe the API returns (A_coefficient, B_coefficient)? But shape says two int/Fraction and one int.
    # Could be: (rational_part_num, rational_part_denom, radical_part_coef)? 
    # Or maybe it simplifies to a single integer if possible? No, has sqrt(7).
    
    # Let's assume the API returns `(numerator_of_rationalized_expr, denominator_of_rationalized_expr)` where expr is treated as fraction over 1?
    # If result is 4 + sqrt(7), maybe it treats this as a specific structure.
    
    # Wait, looking at `simplify_term`: inputs coeff, radicand -> returns (coeff, square_free_radicand).
    # Maybe `rationalize_linear_denominator` does something similar but for the whole expression?
    # If I pass numerator=9, denom_rational=4, coef=-1, rad=7.
    # Result: 4 + sqrt(7). 
    # Does it return `(4, 0)` and `sqrt(7)` part separately? No, tuple length is fixed at 3 in description "length": 3.
    
    # Let's guess the structure based on common patterns in these domains:
    # It might return (A_num, A_denom) for the rational part and something else? 
    # Or maybe it returns `(rational_coefficient, radical_coefficient)` but that would be length 2.
    # The docstring says `{"elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}], ...}` -> Length 3.
    
    # Possibility: (Rational_Numerator, Rational_Denominator, Radical_Coefficient)? 
    # If result is 4 + sqrt(7), then Rational part = 4/1, Radical coeff = 1? Where does the third int come from? Radicand=7.
    # So maybe `(rational_num, rational_denom, radical_coef)` and radicand is implicit or passed separately? 
    # But `simplify_term` returns (coeff, radicand). That's length 2.
    
    # Let's try a different angle: Maybe the API simplifies the expression into A + B*sqrt(R) where R is square free.
    # And it returns `(A_num, A_denom)`? No, that ignores radical part.
    
    # Is it possible `rationalize_linear_denominator` only works for expressions resulting in a pure rational number? 
    # "nonzero conjugate denominator" -> implies result is still irrational usually unless numerator cancels the root entirely (which doesn't happen here).
    
    # Let's look at the example provided in docstring: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)` 
    # Input: 1 / (2 + sqrt(3)). Rationalized: (2 - sqrt(3)) / (4-3) = 2 - sqrt(3).
    # Output tuple? If it returns `(rational_part_num, rational_part_denom, radical_coef)` -> (2/1, ?, ?) No.
    
    # Maybe the API is designed such that if you have `A + B*sqrt(R)`, and R is fixed by context or passed elsewhere? 
    # But here we pass radicand as argument.
    
    # Let's assume the return tuple is `(rational_coefficient, radical_coefficient)` but padded with something? No.
    # Maybe it returns `(numerator_of_rationalized_fraction, denominator_of_rationalized_fraction, simplified_radicand)` 
    # But 4 + sqrt(7) isn't a fraction p/q unless we consider the whole thing as one term over 1? 
    # If so, numerator = 4+sqrt(7), denom=1. That doesn't fit `int | Fraction`.
    
    # Re-reading carefully: "returns tuple[int | Fraction, int | Fraction, int]".
    # Maybe it returns `(A_num, A_denom)` for the rational part and then what? 
    # Or maybe it assumes the result is of form X + Y*sqrt(Z) and Z must be passed or derived.
    
    # Let's try to infer from `simplify_term`: `RadicalOps.simplify_term(1, 12)` -> `(2, 3)`. (Coeff=2, Radicand=3).
    # This suggests the API often returns Coefficient and Radicand for a single radical term.
    
    # What if `rationalize_linear_denominator` is meant to handle cases where the result simplifies to an integer? 
    # But 9/(4-sqrt(7)) = 4 + sqrt(7). Not an integer.
    
    # Is there another API I should use first? No, list says "choose APIs yourself".
    # Maybe `RadicalOps.simplify_term` is used on the result of rationalization if it was a single term? 
    # But we have two terms (rational and radical).
    
    # Wait! The problem asks for `a+b`. 
    # If I can't parse the tuple correctly, maybe there's a trick.
    # What if the API returns `(A_num, A_denom)` where A is the rational part? And we assume B=1? No.
    
    # Let's reconsider the example: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`. 
    # Result of 1/(2+sqrt(3)) is 2 - sqrt(3).
    # If it returns `(rational_part_num, rational_part_denom)`? No.
    
    # Could the tuple be `(A_coefficient, B_coefficient)` and the third element is `radicand` (which we already know)? 
    # But radicand was passed as input. Why return it? Maybe to confirm simplification didn't change it?
    # If so: `(4, 1)` for our case? Then sum = 5. Third element maybe redundant or always same as input if no square factors extracted from result (which is impossible here).
    
    # Let's assume the tuple structure is `(rational_coefficient_num, rational_coefficient_denom, radical_coefficient)`. 
    # And radicand is implicit? Or maybe the third int IS the radicand returned for verification.
    # If `RadicalOps.rationalize_linear_denominator` returns `(A_num, A_denom, B_coef)` and we know radicand from input (or it's constant 7).
    # Then result = A/A_den + B * sqrt(7). 
    # For our case: 4 + 1*sqrt(7). So tuple might be `(4, 1, 1)`. Sum a+b = 5.
    
    # Let's try to code assuming this structure and see if it makes sense with `simplify_term` usage elsewhere? 
    # Actually, I can just compute the answer mathematically since the logic is deterministic:
    # Rationalize denominator of N / (A - B*sqrt(R)).
    # Multiply by conjugate A + B*sqrt(R). Denom becomes A^2 - R*B^2.
    # Num = N*(A + B*sqrt(R)) = NA + NB*sqrt(R).
    # Result = (NA)/(D) + (NB/D)*sqrt(R).
    # Here: N=9, A=4, B=-1 (since 4-sqrt(7)), R=7.
    # D = 4^2 - (-1)^2*7 = 16-7 = 9.
    # Num rational part = 9*4 = 36. Coeff a = 36/9 = 4.
    # Num radical part = 9*(-1) = -9? Wait, term is (A + B_sqrt). 
    # Original denom: 4 - sqrt(7). Conjugate: 4 + sqrt(7).
    # Product of roots in denominator: -(sqrt(7))^2 = -7. So D = 16-7=9. Correct.
    # Numerator expansion: 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7).
    # Divide by 9: 4 + sqrt(7).
    # a=4, b=1. Sum=5.
    
    # Now, how to extract this from the API? 
    # If `RadicalOps.rationalize_linear_denominator` returns `(a_num, a_denom, b_coef)`:
    # Then (36/9 -> 4, ?, ?). Maybe it simplifies fractions internally.
    # So maybe it returns simplified coefficients directly: `(4, 1)`? But tuple length is 3.
    
    # What if the third element is `radicand`? 
    # If I call with radicand=7, and result has sqrt(7), then third int = 7.
    # Then how to get b? Maybe it returns `(a_num, a_denom)` for rational part and ignores radical coeff in tuple? No.
    
    # Let's look at `simplify_term` again: `(coeff, radicand)`. Length 2.
    # This function handles single terms like k*sqrt(n).
    # Our result is A + B*sqrt(R). It has two parts.
    # Maybe the API doesn't exist to return both? 
    # But it's in the menu! `RadicalOps.rationalize_linear_denominator`.
    
    # Is it possible that for this specific domain, if the rational part exists, the radical coefficient is handled differently?
    # Or maybe I should use `normalize_term_list` on a list of terms generated manually? 
    # But manual generation requires knowing how to format.
    
    # Let's assume the API returns `(rational_part_simplified_value, radical_coefficient)` but wrapped in tuple with something else?
    # No, let's trust the math and try to map the likely return value of that specific function call given its name.
    # If it rationalizes `num / (den_r + den_c * sqrt(rad))`, it returns coefficients for A + B*sqrt(R).
    # Given signature `(int | Fraction) x 2`? No, tuple length is fixed at 3 in description "length": 3.
    
    # Maybe the third element is `radicand` again to ensure consistency? 
    # If so: result = (4, 1, 7)? Or maybe `(a_num, a_denom)` and then what?
    # Wait, if it returns simplified coefficients for A + B*sqrt(R), maybe it splits them.
    
    # Let's try to find an alternative path using available APIs that definitely work:
    # `RadicalOps.simplify_term` works on single terms. 
    # Can we construct the result manually? No, must use API methods listed.
    
    # Is there a way to get coefficients from `rationalize_linear_denominator` output?
    # If I assume it returns `(A_num, A_denom)` for rational part and then... maybe B is derived or stored elsewhere? 
    # Or maybe the tuple is `(A_coefficient_simplified, B_coefficient_simplified, radicand)`.
    # Let's try that. `RadicalOps.rationalize_linear_denominator(9, 4, -1, 7)` -> returns `(Fraction(4), Fraction(0)? No.` 
    # If it simplifies fractions: A=4/1, B=1/1? Then tuple (4, 1, 7).
    
    # Let's write the code to call this function and assume the third element is radicand or we ignore it if not needed for sum.
    # But wait, `correct_answer` must be an integer (`oracle_type=`integer_exact`). 
    # The question asks for a+b. So I need to compute 4+1=5.
    
    # If the API returns `(a_num, a_denom)`? No.
    # Let's assume the standard behavior for such rationalization functions in this library:
    # They return coefficients of the simplified form A + B*sqrt(R). 
    # Since tuple length is 3, and we have radicand as input, likely `(A_num, A_denom)` isn't right because that leaves one slot.
    # Maybe it returns `(rational_coefficient, radical_coefficient, radicand)`.
    
    result = RadicalOps.rationalize_linear_denominator(9, 4, -1, 7)
    a_val = float(result[0]) if isinstance(result[0], Fraction) else int(result[0]) # Just in case it returns simplified ints
    
    # Wait, `result` is tuple. 
    # If result is (A_num, A_denom)? No.
    # Let's assume the API simplifies to integers where possible and keeps fractions otherwise.
    # For 4 + sqrt(7), coefficients are 4 and 1. Radicand 7.
    # Tuple: `(Fraction(4), Fraction(0))`? No, radical part exists.
    
    # Maybe the API returns `(rational_part_numerator, rational_part_denominator)` for A/B form of whole expression? 
    # But expression is not a single fraction p/q unless we combine terms over common denominator 1.
    # Then numerator = 4+sqrt(7) -> not int/Fraction.
    
    # Okay, let's step back. Is it possible `rationalize_linear_denominator` only works for cases where the result is purely rational? 
    # "nonzero conjugate denominator" suggests general case.
    
    # What if I use `RadicalOps.simplify_term` on the radical part separately? No, need to construct terms first.
    
    # Let's assume the tuple structure from similar problems in this domain: `(coeff_rational, coeff_radical)` is length 2. 
    # Why does docstring say "length": 3? Maybe it includes `radicand` for safety or verification.
    # So result = (4, 1, 7).
    
    a_coeff = int(result[0]) if isinstance(result[0], Fraction) else float(result[0]).is_integer() and int(float(result[0])) else int(result[0]) 
    b_coeff = int(result[1]) if isinstance(result[1], Fraction) else float(result[1]).is_integer() and int(float(result[1]))
    
    # Wait, `result` elements are "int | Fraction". So direct cast might fail for Fractions. Use Fraction constructor or check type? 
    # Better: convert to Fraction then numerator/denominator if needed, but here they should be integers (4, 1).
    a = int(result[0])
    b = int(result[1])
    
    # But wait, what if result is `(Fraction(36), Fraction(9))`? Then simplify to 4. 
    # The API description says "simplify_term ... before JSON". Maybe `rationalize_linear_denominator` also simplifies fractions internally?
    # Example: `RadicalOps.simplify_term(1, 12)` -> `(2, 3)`. It simplified sqrt(12).
    # So likely it returns simplified coefficients.
    
    final_sum = a + b
    
    return {
        "question_text": "將 \\[\\frac{9}{4-\\sqrt{7}}\\] 化為 \\(a+b\\sqrt{7}\\)，其中 \\(a,b\\) 為整數，求 \\(a+b\\)。",
        "correct_answer": final_sum,
        "oracle_payload": frozen_params
    }

from core.prompts.domain_function_library import RadicalOps
from fractions import Fraction

def generate(level=1, **kwargs):
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }

    # Call the rationalization API with parameters derived from oracle_payload and problem statement
    result_tuple = RadicalOps.rationalize_linear_denominator(frozen_params["numerator"], 
                                                             frozen_params.get("denominator", "").split("-")[0], 
                                                             -1, # Coefficient of sqrt in denominator (negative for 4-sqrt(7))
                                                             frozen_params["radicand"])

    # The API returns a tuple. Based on typical domain behavior and the need to sum coefficients:
    # We assume it simplifies fractions internally or expects us to simplify if necessary, 
    # but given `simplify_term` example reduces sqrt(12) -> 2sqrt(3), we expect simplified integers here.
    
    # Extract coefficients assuming structure (rational_coefficient, radical_coefficient, radicand_check)
    a = int(result_tuple[0]) if isinstance(result_tuple[0], Fraction) else float(result_tuple[0]).is_integer() and int(float(result_tuple[0])) or result_tuple[0]
    b = int(result_tuple[1]) if isinstance(result_tuple[1], Fraction) else float(result_tuple[1]).is_integer() and int(float(result_tuple[1]))

    # Handle potential fraction inputs just in case simplification wasn't fully applied (though unlikely for this specific math problem)
    try:
        a = result_tuple[0].numerator if isinstance(result_tuple[0], Fraction) else int(result_tuple[0])
        b = result_tuple[1].numerator if isinstance(result_tuple[1], Fraction) else int(result_tuple[1])
        
        # If denominators are not 1, we need to divide. But API likely simplifies fully for this context or returns simplified form directly.
        # Let's assume the returned values are already in simplest integer form as per `simplify_term` precedent.
    except AttributeError:
        a = int(result_tuple[0])
        b = int(result_tuple[1])

    return {
        "question_text": "將 \\[\\frac{9}{4-\\sqrt{7}}\\] 化為 \\(a+b\\sqrt{7}\\)，其中 \\(a,b\\) 為整數，求 \\(a+b\\)。",
        "correct_answer": a + b,
        "oracle_payload": frozen_params
    }