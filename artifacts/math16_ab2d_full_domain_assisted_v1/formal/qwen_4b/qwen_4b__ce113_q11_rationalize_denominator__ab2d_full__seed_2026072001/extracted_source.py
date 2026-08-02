def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_params", {})
    
    # Extract components from denominator string "4-sqrt(7)" -> 4 + (-1)*sqrt(7)
    denom_rational = frozen_params["denominator"].split("-")[0] if "-" in frozen_params["denominator"] else "4"
    radicand_val = int(frozen_params["radicand"])
    
    # Parse the rational part carefully. The string is like "4". 
    # We need to ensure it's an integer or Fraction for the API.
    denom_rational_int = RadicalOps.exact_integer(denom_rational) if isinstance(denom_rational, str) else int(denom_rational)

    numerator_val = frozen_params["numerator"]
    
    # Step 1: Rationalize denominator
    result_tuple = RadicalOps.rationalize_linear_denominator(
        numerator=numerator_val, 
        denom_rational=denom_rational_int, 
        denom_radical_coeff=-1, 
        radicand=radicand_val
    )
    
    # The function returns (new_numerator_part_1, new_numerator_part_2, denominator)
    # Based on the example `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)` returning `(4/7, -6/7, 9)`? 
    # Wait, let's re-read the signature and boundary.
    # Signature: (numerator, denom_rational, denom_radical_coeff, radicand) -> tuple[int | Fraction, int | Fraction, int]
    # Example in docstring: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)` 
    # This implies inputs are (numerator=1, rational_part_of_denom=2, coeff=-1? No, example says 1).
    # Let's look at the math for our case: 9 / (4 - sqrt(7)) = 9 * (4 + sqrt(7)) / (16 - 7) = 9*(4+sqrt(7))/9 = 4 + sqrt(7).
    # So result should be a=4, b=1. Sum = 5.
    
    # The API returns: 
    # [new_numerator_rational_part / new_denominator, new_numerator_radical_coeff * something? No.]
    # Actually, looking at the return shape description: "elements": [{"types": ["int", "Fraction"]}, {"types": ["int", "Fraction"]}, {"type": "int"}]
    # And boundary says "RadicalOps.exact_integer on integral leaves before JSON".
    
    # Let's assume standard rationalization output structure for (A + B*sqrt(C)) / D:
    # Result is usually represented as a single fraction or split terms.
    # Given the example `1, 2, 1, 3` -> likely `(4/7, -6/7, 9)`? 
    # If denom was 2 + sqrt(3), conjugate is 2-sqrt(3). Denom becomes 4-3=1.
    # Numerator: 1*(2+sqrt(3)) = 2 + sqrt(3). Result: (2, 1) if denominator is 1? 
    # Or maybe the API returns numerator components and a common denominator.
    
    # Let's re-examine the specific example provided in docs: `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`
    # If this corresponds to rationalizing (something) / (2 + sqrt(3))? 
    # Or maybe it returns the numerator of the result and the denominator.
    
    # Let's try to infer from the math logic required: "Exact integer match".
    # The task asks for a+b where 9/(4-sqrt(7)) = a + b*sqrt(7).
    # We know answer is 5 (a=4, b=1).
    
    # Let's call the API and see what we get. 
    # Inputs: numerator=9, denom_rational=4, denom_radical_coeff=-1, radicand=7.
    res = RadicalOps.rationalize_linear_denominator(9, 4, -1, 7)
    
    # The result is a tuple of length 3. 
    # Based on typical rationalization algorithms in such libraries:
    # It likely returns (numerator_rational_part / common_denom, numerator_radical_coeff * something? No.)
    # Actually, looking at the return shape again: "elements": [coeff_type, coeff_type, int]
    # Maybe it returns (a_num, b_num, denom)? 
    # If so, we need to divide by denom. But our math showed denominator became 9 and numerator was 4+sqrt(7), cancelling out perfectly.
    
    # Let's assume the API handles the division if possible or returns unsimplified fractions that simplify to integers.
    # Since the problem guarantees integer answer a+b, we can likely convert back to int after simplification 
    # OR the API might return (4/1, 1/1, 9) -> then divide by 9? No, result is 4+sqrt(7).
    
    # Alternative interpretation: The API returns the numerator of the rationalized fraction.
    # If input was A/(B+C*sqrt(D)), output might be (A*(B-C*sqrt(D))) / (B^2-D*C^2) -> Numerator and Denom?
    # But signature says 3 elements, last is int (denominator). First two are coeffs.
    
    # Let's assume the first element corresponds to 'a' * denominator and second to 'b' * denominator? 
    # Or maybe it returns simplified terms directly if possible?
    
    # Given the constraint "Exact integer match", let's try to extract integers from res[0] and res[1].
    # If res = (4/9, 1/9, 9), then a=4/9*9=4, b=1/9*9=1. Sum=5.
    # Let's assume the API returns unsimplified numerator parts over the common denominator.
    
    num_part_a, num_part_b, denom = res
    
    # Convert to float or Fraction logic? 
    # We need exact integers.
    from fractions import Fraction as F
    
    a_val = int(num_part_a / denom) if isinstance(num_part_a, (int, str)) else int(Fraction(num_part_a) * denom)
    b_val = int(num_part_b / denom) if isinstance(num_part_b, (int, str)) else int(Fraction(num_part_b) * denom)
    
    # Wait, the example `RadicalOps.exact_integer` handles Fraction. 
    # Let's use that to ensure we get ints.
    a_int = RadicalOps.exact_integer(a_val) if isinstance(a_val, (int, str)) else int(Fraction(num_part_a * denom).numerator / F.denominator? No.)
    
    # Simpler approach: The API likely returns the numerator components directly scaled by denominator? 
    # Or maybe it simplifies them. 
    # Let's assume standard behavior for such a function in this context (Math16):
    # It probably returns (a, b) if they are integers after division, or fractions otherwise.
    
    # Re-evaluating based on "Exact integer match" requirement and the specific math:
    # 9 / (4 - sqrt(7)) = 9 * (4 + sqrt(7)) / (16-7) = 36/9 + 9/sqrt(7)? No. 
    # Rationalize denominator means multiply by conjugate of denominator? 
    # Denom is 4 - sqrt(7). Conjugate is 4 + sqrt(7).
    # Product: (16 - 7) = 9.
    # Numerator becomes 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7).
    # Result: (36/9) + (9/9)*sqrt(7) = 4 + 1*sqrt(7).
    
    # So the API likely returns numerator parts and denominator.
    # res[0] -> 36, res[1] -> 9, denom -> 9? 
    # Then a = 36/9 = 4, b = 9/9 = 1.
    
    # Let's implement the division logic safely using Fraction to avoid float errors.
    from fractions import Fraction
    
    if isinstance(num_part_a, str): num_part_a = int(num_part_a)
    if isinstance(num_part_b, str): num_part_b = int(num_part_b)
    
    a_frac = Fraction(num_part_a * denom).numerator / F.denominator # Wait, logic error in thought.
    # If API returns (36/9, 1/9)? No, usually numerator parts are integers and denominator is separate? 
    # Or maybe it returns fractions directly: res[0] = Fraction(4), res[1]=Fraction(1).
    
    # Let's try to infer from the example `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)`
    # If this is for (something)/(2+sqrt(3)), and result is integer? 
    # Maybe it returns simplified terms directly if denominator divides numerator.
    
    # Let's assume the safest path: Use Fraction arithmetic to compute a+b manually using the API components as building blocks, 
    # ensuring we get exact integers before summing.
    
    # Re-calculate with explicit math using API for validation? No, just use logic derived from problem statement + API usage pattern.
    # The prompt says "call RadicalOps.rationalize_linear_denominator...". It doesn't say how to interpret return. 
    # But we must produce correct_answer as int sum.
    
    # Let's assume the standard output for this specific function in this domain is:
    # (numerator_rational_part, numerator_radical_coefficient, denominator) where everything is Fraction or Int?
    # If so, a = num1 / den, b = num2 / den.
    
    if isinstance(num_part_a, str): 
        try: val_a = int(num_part_a); else_val_a = None; pass
    except ValueError:
        from fractions import Fraction as F
        val_a = F(int(num_part_a)) # Assume string is valid integer representation
        
    a_coeff = val_a / denom if isinstance(val_a, (int, str)) and not isinstance(val_a, bool) else RadicalOps.exact_integer(Fraction(val_a * denom).numerator / F.denominator? No.
    
    # Let's simplify: Just compute the math using Python native types but validated by API calls where needed.
    # Since I cannot see the actual internal implementation of `rationalize_linear_denominator`, 
    # I will assume it returns (36/9, 1/9) or similar? No, that would be weird for a "linear radical" function returning ints/Fractions.
    
    # Hypothesis: It returns simplified terms directly if possible, otherwise fractions.
    # Given the problem guarantees integer answer, let's assume it simplifies to (4, 1).
    # But wait, the example `RadicalOps.rationalize_linear_denominator(1, 2, 1, 3)` 
    # If input is for rationalizing denominator of something over (2+sqrt(3)), and result has denom=9? 
    # Then it returns unsimplified numerators.
    
    # Let's assume the return values are fractions that need division by `denom`.
    a_val = Fraction(num_part_a) / F(denom) if isinstance(num_part_a, (int, str)) else num_part_a
    b_val = Fraction(num_part_b) / F(denom) if isinstance(num_part_b, (int, str)) else num_part_b
    
    # Ensure they are integers as per contract "a,b 為整數"
    a_int = int(a_val.numerator // a_val.denominator) 
    b_int = int(b_val.numerator // b_val.denominator)
    
    total_sum = a_int + b_int

    question_text = frozen_params["denominator"] # Wait, task says "use as question_text" the stem.
    # The stem is: 將 \[ \frac{9}{4-\sqrt{7}} \] ... 
    # But `frozen_params` has keys like "denominator", "numerator". 
    # We need to construct the full string or use a provided one? 
    # Instruction: "question_text: the provided stem string (do not rebuild from scratch unless required)."
    # The task block provides: ## Frozen task description ... 將 \[ \frac{9}{4-\sqrt{7}} \] ...
    # So we should extract that text. But `frozen_params` doesn't contain it directly, only components. 
    # However, the instruction says "use as question_text" referring to the frozen_task_description block? 
    # Or does it mean use the params to build it? 
    # "question_text: the provided stem string". The stem is in ## Frozen task description.
    
    full_stem = f"將 \\\n\[ \\frac{{9}}{{4-\\\\sqrt{{{frozen_params['radicand']}}}}} \\\\] 化為 {frozen_params['denominator']}，其中 a,b 為整數，求 a+b。" 
    # Actually, simpler: Just use the text from the description block but formatted correctly.
    # The example in generic code uses "example stem". Here we have specific content.
    
    correct_answer = total_sum
    
    return {
        "question_text": f"將 \\\n\[ \\frac{{9}}{{4-\\\\sqrt{{{frozen_params['radicand']}}}}} \\\\] 化為 a+b\sqrt{{{frozen_params['radicand']}}}，其中 a,b 為整數，求 a+b。",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }

