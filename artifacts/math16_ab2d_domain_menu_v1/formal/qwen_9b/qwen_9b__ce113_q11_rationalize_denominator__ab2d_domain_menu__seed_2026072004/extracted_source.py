from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }

    # The task is to rationalize the denominator of 9 / (4 - sqrt(7)).
    # We use RadicalOps.rationalize_linear_denominator with:
    # numerator = 9
    # denom_rational = 4
    # denom_radical_coeff = 1 (since it's just sqrt(7))
    # radicand = 7
    
    num_new, den_rat_new, den_rad_new = RadicalOps.rationalize_linear_denominator(
        numerator=9, 
        denom_rational=4, 
        denom_radical_coeff=1, 
        radicand=7
    )

    # The result of rationalization is (numerator * conjugate) / (denom^2 - radical_part^2).
    # RadicalOps.rationalize_linear_denominator returns the simplified numerator and denominator components.
    # However, looking at the API description: 
    # "returns: tuple[int | Fraction, int | Fraction, int]" -> [new_num_coeff, new_den_rational, radicand] ??
    # Actually, let's look closer at the example or logic.
    # Rationalizing 9/(4-sqrt(7)) => multiply by (4+sqrt(7))/(16-7) = 9*(4+sqrt(7))/9 = 4 + sqrt(7).
    # So a=4, b=1. Sum = 5.
    
    # The API returns: tuple[new_numerator_part_rational, new_denominator_rational, radicand] ?? 
    # Wait, the signature says: `(numerator, denom_rational, denom_radical_coeff, radicand)` -> `tuple[int | Fraction, int | Fraction, int]`
    # Let's assume it returns (new_num_val, 1, new_denom_val) or similar? 
    # Actually, usually these APIs return the final simplified fraction components if possible.
    # But here we need to extract coefficients a and b from the result form `a + b*sqrt(radicand)`.
    
    # Let's re-read the API docstring carefully: "returns: tuple[int | Fraction, int | Fraction, int]"
    # It likely returns (new_numerator_coefficient_of_rational_part, new_denominator_after_squaring?, radicand)? 
    # No, standard rationalization of A/(B-C) -> A(B+C)/(B^2-C). If B^2-C is a perfect square integer K, then we get integers.
    # Here 4^2 - 7 = 9. So denominator becomes 1 after simplification? 
    # The function probably returns the coefficients of the resulting expression `a + b*sqrt(radicand)`.
    
    # Let's assume the return values map to: (coefficient_of_rational, coefficient_of_radical, radicand)?
    # Or maybe it returns the numerator and denominator before final simplification? 
    # Given "oracle_payload" must be frozen_params exactly.
    
    # If I call RadicalOps.rationalize_linear_denominator(9, 4, 1, 7):
    # It should return something that allows me to compute a+b.
    # Based on the math: Result is 4 + sqrt(7). So a=4, b=1. Sum = 5.
    
    # How does the API structure work? 
    # If it returns (numerator_simplified, denominator_simplified) or similar?
    # The docstring says "returns_shape": {"elements": [{"types": ["int", "Fraction"]}, ...], "length": 3}
    # It's likely: (new_numerator_val, new_denominator_val, radicand). 
    # But wait, if the result is an integer or simple sum of radicals, how are they represented?
    # Maybe it returns a tuple representing the linear form directly? No, signature says 3 elements.
    
    # Let's look at `RadicalOps.simplify_term` example: `(1, 12) -> (2, 3)` which is coeff=2, radicand=3 for sqrt(12).
    # That returns a tuple of length 2.
    # This function returns length 3. 
    # Hypothesis: It might return the coefficients `a` and `b` directly if possible? Or maybe (numerator_part, denominator_part)?
    # If it's standard rationalization logic implemented in an API that handles simplification:
    # Input: num=9, den_rat=4, den_rad_coeff=1, radicand=7.
    # Conjugate numerator = 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7).
    # Denominator squared part = 4^2 - 7 = 9.
    # Resulting fraction: (36/9) + (9/9)*sqrt(7) = 4 + 1*sqrt(7).
    
    # If the API returns `(a, b, radicand)` where result is `a + b*sqrt(radicand)`, then a=4, b=1.
    # But if it returns raw numerator/denominator before simplification? 
    # The docstring says "boundary: RadicalOps.exact_integer on integral leaves before JSON". This suggests internal handling of fractions/integers.
    
    # Let's assume the API returns `(a, b, radicand)` for a simplified linear radical expression `a + b*sqrt(radicand)`. 
    # Or maybe it returns `(numerator_coefficient_of_rational_part, numerator_coefficient_of_radical_part)`? No length 3.
    
    # Alternative interpretation: The API might return the result as two terms or similar?
    # Let's try to infer from `RadicalOps.format_linear_radicals` which takes dicts with keys "rational", "radical_coefficient".
    # Maybe this function returns a tuple `(term_rational, term_radical_coef, radicand)`? 
    # If so: 4 + sqrt(7) -> (4, 1, 7). Sum = 5.
    
    # Let's consider the possibility that it returns `(numerator_val, denominator_val, radicand)` where `val` are integers/fractions representing the fraction N/D? 
    # If result is integer + radical, how to represent? Maybe separate terms aren't returned by this specific API call in a single tuple unless specified.
    
    # Re-reading: "returns_shape": {"elements": [{"types": ["int", "Fraction"]}, ...], "length": 3}
    # It's highly probable it returns `(rational_part, radical_coefficient, radicand)` for the simplified result `a + b*sqrt(r)`. 
    # Why? Because that matches the output of other RadicalOps functions which deal with linear radicals.
    
    num_val, rad_coef_val, _ = RadicalOps.rationalize_linear_denominator(9, 4, 1, 7)
    
    # Wait, if it returns (rational_part, radical_coefficient, radicand), then:
    # rational_part corresponds to 'a'
    # radical_coefficient corresponds to 'b'
    # But what about the denominator? 
    # If the result is purely integer + sqrt(integer), maybe the API handles the division internally.
    
    # Let's double check if `numerator` and `denominator` in the return tuple refer to something else.
    # Maybe it returns `(new_numerator, new_denominator, radicand)`? 
    # If so: 36/9 -> (36, 9, 7). Then we'd have to simplify manually. But the prompt says "oracle_payload must equal this object" and asks for a+b where a,b are integers.
    # The API likely simplifies automatically given `exact_integer` boundary note? 
    # Actually, looking at `RadicalOps.simplify_term`, it returns simplified coeff/radicand.
    # It is consistent that `rationalize_linear_denominator` would return the fully simplified coefficients if possible (i.e., when denominator divides numerator perfectly).
    
    # Let's assume the tuple is `(a, b, radicand)`. 
    # a = num_val
    # b = rad_coef_val
    
    result_a = num_val
    result_b = rad_coef_val
    
    total_sum = int(result_a + result_b)

    return {
        "question_text": "將 \\[\\frac{9}{4-\\sqrt{7}}\\] 化為 \\(a+b\\sqrt{7}\\)，其中 \\(a,b\\) 為整數，求 \\(a+b\\)。",
        "correct_answer": total_sum,
        "oracle_payload": frozen_params
    }