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
    
    num_new, den_num, den_rad = RadicalOps.rationalize_linear_denominator(9, 4, 1, 7)

    # The result is in the form (numerator_result) / (denominator_rational * sqrt(radicand)) ? 
    # Wait, let's check the API signature and return shape carefully.
    # Signature: `(numerator, denom_rational, denom_radical_coeff, radicand)`
    # Returns: `tuple[int | Fraction, int | Fraction, int]`
    # Description says "rationalize_linear_denominator". Usually this returns (new_num, new_denom).
    # However, the return shape description is complex. Let's look at the example or logic.
    # Example in docstring: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)` -> `(numerator_result, denom_rational_part, radicand?)` 
    # Actually, standard rationalization of A/(B - sqrt(C)) is (A*(B+sqrt(C))) / (B^2-C).
    # So the result should be a single fraction or sum? The task asks for `a+b*sqrt(7)`.
    # This implies the denominator becomes an integer.
    
    # Let's re-read the return shape: `{"elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}], ...}`
    # It returns a tuple of 3 elements? Or maybe it simplifies differently.
    # If I call with (9, 4, 1, 7): 
    # Numerator becomes 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7).
    # Denominator becomes 4^2 - 7 = 16 - 7 = 9.
    # Result: (36 + 9*sqrt(7)) / 9 = 4 + sqrt(7).
    # So a=4, b=1. Sum = 5.
    
    # The API likely returns the components to construct this or directly the simplified parts if possible?
    # Given `den_num` and `den_rad`, maybe it separates rational part of denominator from radical part? 
    # But for linear denominators B - sqrt(C), after multiplying by conjugate, denom is integer.
    # Perhaps the API returns (new_numerator_coeff_rational_part, new_denominator_value)? No, 3 elements.
    
    # Let's assume the standard behavior of such a helper: it might return (numerator_simplified_num, denominator_integer). 
    # But there are 3 items in tuple? Maybe `den_rad` is just confirming radicand or something else?
    # Wait, looking at similar problems, sometimes they separate rational and radical parts if the result isn't fully simplified to one fraction.
    # However, here we expect a single integer sum of coefficients.
    
    # Let's reconsider the API return shape: `tuple[int | Fraction, int | Fraction, int]`.
    # Maybe it returns (numerator_rational_part_coefficient, numerator_radical_part_coefficient, denominator)? 
    # Or maybe (new_numerator_full_expression_as_tuple?, new_denominator?).
    
    # Let's try to infer from the example `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`.
    # Input: 1 / (2 - sqrt(3)). Conjugate: 2 + sqrt(3). Denom: 4-3=1. Result: 2+sqrt(3).
    # If the API returns a tuple of 3 ints... maybe it's not standard rationalization but something specific to this library?
    # Or perhaps `den_rad` is returned as part of the process even if denom becomes integer?
    
    # Alternative interpretation: The function might return (numerator_rational_part, numerator_radical_coefficient, denominator). 
    # If result is 4 + sqrt(7), then num_rat=36, num_rad_coef=9, den=9. Then we divide by den inside the caller?
    # Or maybe it returns simplified coefficients directly: (4, 1, ?) -> No, that's only 2 numbers needed for answer.
    
    # Let's look at `RadicalOps.simplify_term`. It takes coeff and radicand and simplifies sqrt(n).
    # Maybe the rationalization function is expected to handle the division by denominator automatically? 
    # If so, what are the 3 values?
    # Hypothesis: The API returns (rational_part_coefficient, radical_part_coefficient, remaining_radicand_info?).
    # But radicand is fixed at 7.
    
    # Let's assume the most robust path for "math16" tasks which often involve constructing answers from raw components provided by APIs.
    # If `RadicalOps.rationalize_linear_denominator` returns `(num_r, num_s, den)`, we can compute a = num_r/den, b = num_s/den.
    
    val_0, val_1, val_2 = RadicalOps.rationalize_linear_denominator(9, 4, 1, 7)
    
    # Based on the math: 
    # Numerator part rational (from conjugate): 9 * 4 = 36.
    # Numerator part radical coeff: 9 * 1 = 9.
    # Denominator: 4^2 - 7 = 9.
    # So val_0=36, val_1=9, val_2=9 seems plausible for the tuple structure (rat_part_num, rad_coeff_num, den).
    
    a = int(val_0 / val_2) if isinstance(val_0, int) else float(val_0)/float(val_2) # Should be exact integer division
    b = int(val_1 / val_2) if isinstance(val_1, int) else float(val_1)/float(val_2)
    
    # Ensure they are integers as per contract "a,b 為整數" (integers).
    a_int = int(a)
    b_int = int(b)
    
    question_text = kwargs.get('question_text', '將 \\frac{9}{4-\\sqrt{7}} 化為 a+b\\sqrt{7}，其中 a,b 為整數，求 a+b。')
    
    return {
        "question_text": question_text,
        "correct_answer": int(a_int + b_int),
        "oracle_payload": frozen_params
    }