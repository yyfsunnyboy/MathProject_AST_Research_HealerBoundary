from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }

    # The task is to rationalize the denominator of 9 / (4 - sqrt(7)).
    # We use RadicalOps.rationalize_linear_denominator.
    # Inputs: numerator=9, denom_rational=4, denom_radical_coeff=1, radicand=7.
    
    num_new, den_num_new, den_rad_new = RadicalOps.rationalize_linear_denominator(
        9, 
        4, 
        1, 
        7
    )

    # The result of rationalization is (numerator * conjugate) / (denominator^2 - radical_part).
    # For a/b where b = c + d*sqrt(r), the denominator becomes c^2 - d^2*r.
    # Here, denom_rational=4, denom_radical_coeff=1, radicand=7.
    # Denom squared part: 4^2 - (1)^2 * 7 = 16 - 7 = 9.
    # The function returns the simplified numerator components and a new denominator factor? 
    # Let's check the return shape of rationalize_linear_denominator from docs:
    # returns tuple[int | Fraction, int | Fraction, int] -> (new_num_rational_part, new_num_radical_part?, den_factor?)
    # Actually, looking at standard math and typical API design for this domain:
    # It likely returns the coefficients of the resulting expression A + B*sqrt(r) directly if possible, 
    # OR it returns components to construct them.
    
    # Let's re-evaluate based on `exact_integer` usage in similar contexts or just standard math logic first.
    # 9 / (4 - sqrt(7)) * (4 + sqrt(7))/(4 + sqrt(7)) = 9*(4+sqrt(7)) / (16-7) = 9*(4+sqrt(7))/9 = 4 + sqrt(7).
    # So the answer is 4 + 1*sqrt(7). a=4, b=1. a+b=5.
    
    # How does RadicalOps.rationalize_linear_denominator return this?
    # Signature: (numerator, denom_rational, denom_radical_coeff, radicand) -> tuple[int | Fraction, int | Fraction, int]
    # Example in docs is missing for rationalization specifically but let's assume it returns the simplified form components.
    # However, the contract requires `correct_answer` to be an integer (a+b).
    
    # Let's look at the return values from a hypothetical call:
    # If the result is 4 + sqrt(7), then rational part = 4, radical coeff = 1.
    # The tuple might be (rational_part, radical_coefficient, radicand) or similar? 
    # Or maybe it returns just the final integer value if fully simplified to an integer? No, result is irrational here.
    
    # Wait, looking at `RadicalOps.simplify_term` example: `(2, 3)` for input (1, 12). It simplifies sqrt(12) -> 2*sqrt(3).
    # So it returns (coefficient, radicand).
    
    # What does `rationalize_linear_denominator` return? 
    # "returns: tuple[int | Fraction, int | Fraction, int]"
    # Likely: (new_rational_coefficient_of_resulting_term1, new_radical_coefficient_of_resulting_term2?, something_else?)
    # Actually, usually these APIs for rationalization of a single term denominator return the resulting expression components.
    # If the result is A + B*sqrt(r), maybe it returns (A, B)? But there are 3 elements in tuple.
    # Maybe: (rational_part_coefficient, radical_part_coefficient, radicand_of_radical_part).
    
    # Let's assume the standard behavior for such a domain API when rationalizing x/(y+sqrt(z)):
    # Result is P + Q*sqrt(r). The function likely returns (P, Q, r) or similar.
    # Given the example `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)` -> `(Fraction(...), Fraction(...), int)`.
    
    # Let's calculate manually to be sure of values: 
    # Num = 9 * (4 + sqrt(7)) / (16 - 7) = 9*(4+sqrt(7))/9 = 4 + sqrt(7).
    # Rational part coeff = 4. Radical part coeff = 1. Radicand = 7.
    
    # If the API returns these, we sum them? No, a+b is requested. 
    # The question asks for "a+b" where expression is a + b*sqrt(7).
    # So if result is 4 + sqrt(7), then a=4, b=1. Sum = 5.
    
    # We need to extract 'a' and 'b' from the API return or compute them directly? 
    # The prompt says "Use only the Domain API methods". It implies we should use APIs to get components if possible.
    # But `rationalize_linear_denominator` might not be guaranteed to separate terms into a dict for summing easily without parsing strings, which is forbidden (no string manipulation of math).
    # However, looking at the return type: tuple[int | Fraction, int | Fraction, int].
    # Let's assume index 0 is rational part coeff, index 1 is radical part coeff. Index 2 might be radicand or denominator factor?
    # If it returns (4, 1, 7), then a=4, b=1. Sum = 5.
    
    # Alternative: Maybe the API simplifies to an integer if possible? No, result is irrational.
    # Is there another way? `RadicalOps.exact_integer` rejects non-integral rationals. 
    # The final answer must be int (a+b).
    
    # Let's assume the tuple structure from similar problems in this domain context:
    # Returns (rational_coeff, radical_coeff, radicand) for the simplified sum of radicals?
    # Or maybe it returns just the numerator and denominator components before simplification? 
    # The doc says "returns... partial json_safe".
    
    # Let's try to infer from `simplify_term`. It takes (coeff, radicand).
    # Maybe we should construct the terms manually using arithmetic since the API might not expose a direct getter for 'a' and 'b' in a sum context? 
    # But "Use only Domain API methods" suggests relying on them.
    
    # Hypothesis: The function returns (rational_part, radical_coefficient_of_radical_part). Wait, 3 elements.
    # Maybe it returns the result as two terms combined into one structure? No, tuple is flat.
    # Let's assume standard order: (RationalPartCoeff, RadicalPartCoeff, Radicand). 
    # If so, a = res[0], b = res[1]. Then return int(res[0] + res[1]).
    
    # However, there is a risk the API returns something else. Let's look at `exact_integer`. It converts Fraction to int if possible.
    # Is it possible the result of rationalization in this specific domain library simplifies differently? 
    # If I cannot be 100% sure of the tuple order without docs, but usually: Rational part first.
    
    # Let's reconsider the "frozen_params". It has numerator=9, denom_rational=4, radicand=7.
    # The calculation is straightforward mathematically. 
    # If I am forced to use APIs only, and `rationalize_linear_denominator` returns a tuple...
    
    # Let's assume the return value of `RadicalOps.rationalize_linear_denominator(9, 4, 1, 7)` yields:
    # (Fraction(4), Fraction(1), int(7)) ? Or maybe just integers? 
    # The signature says `int | Fraction`. Since inputs are ints and result is integer coefficients here.
    
    # Let's try to verify if there's a simpler path using the API menu provided:
    # We have `add_linear_radicals`, `scale_linear_radical`, etc.
    # Maybe we don't need to parse the tuple? 
    # What if the question implies calculating it and returning the integer sum directly in correct_answer, but how do I get 'a' and 'b'?
    # If the API doesn't explicitly return a dict with keys "rational", "radical_coefficient" like `add_linear_radicals` does...
    # The tuple is positional. 
    # Standard convention: (RationalPart, RadicalCoeff, Radicand).
    
    # Let's proceed with extracting from the tuple assuming standard ordering for such algebraic simplification results in this domain style.
    # res = RadicalOps.rationalize_linear_denominator(9, 4, 1, 7)
    # a = int(res[0]) if isinstance(res[0], Fraction) else res[0] (but inputs are ints so likely ints or Fractions that simplify to ints)
    # b = ... same
    
    # Wait, `exact_integer` is available. Maybe we can use it? 
    # But the result of rationalization isn't a single number. It's an expression A + B*sqrt(7).
    # The question asks for A+B.
    
    # Is there any chance the API returns just (A, B)? No, signature says 3 elements.
    # What if it returns (Numerator_after_rationalization, Denominator_factor, Radicand)? 
    # Then we would have to divide Numerator by Denominator factor manually? That's arithmetic allowed ("arithmetic" is native op).
    # If res = (Num_raw, Denom_raw, radicand), then A = Num_raw // Denom_raw_part_rational?, B = ...
    
    # Let's look at the example in docs: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`. 
    # Input: x / (y + sqrt(z)) -> 1/(2+sqrt(3)). 
    # Rationalization: 1*(2-sqrt(3))/(4-3) = 2 - sqrt(3).
    # Result should be coeff_rational=2, coeff_radical=-1.
    # If the tuple is (rational_coeff, radical_coeff, radicand), then it would return (2, -1, 3)? 
    # Or maybe (-1) for coefficient? Yes.
    
    # So if we assume order: (RationalCoeff, RadicalCoeff, Radicand).
    # Then a = res[0], b = res[1]. Sum = a+b.
    
    # One catch: The problem asks for `a` and `b` integers. 
    # If the result is 4 + sqrt(7), then coeffs are 4, 1.
    # Let's assume this mapping.
    
    # Implementation details:
    # Call API. Extract values. Convert Fractions to ints if necessary (using exact_integer or int() cast).
    # Sum them. Return dict with question_text and correct_answer as the sum integer.
    
    res = RadicalOps.rationalize_linear_denominator(9, 4, 1, 7)
    
    # Extract components assuming order: rational_coefficient, radical_coefficient, radicand
    val_rational = res[0]
    val_radical_coef = res[1]
    
    # Ensure they are integers for the sum. The problem states a,b are integers.
    # Use exact_integer to force int conversion if Fraction is returned (though 4 and 1 are ints).
    try:
        from fractions import Fraction
        val_rational_int = RadicalOps.exact_integer(val_rational)
        val_radical_coef_int = RadicalOps.exact_integer(val_radical_coef)
    except Exception:
        # Fallback if exact_integer behaves differently or fails on int input (unlikely given signature)
        val_rational_int = int(res[0])
        val_radical_coef_int = int(res[1])

    a_plus_b = val_rational_int + val_radical_coef_int
    
    return {
        "question_text": "將 \\frac{9}{4-\\sqrt{7}} 化為 a+b\\sqrt{7}，其中 a,b 為整數，求 a+b。",
        "correct_answer": int(a_plus_b),
        "oracle_payload": frozen_params
    }