from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    # Solve (x-2)^2 = 3 for x.
    # Take square root: |x - 2| = sqrt(3) => x - 2 = ±sqrt(3).
    # Roots are a = 2 + sqrt(3), b = 2 - sqrt(3).
    # Given a > b, this assignment is correct.
    
    rational_part = Fraction(2, 1)
    radical_coefficient_a = 1
    radicand_a = 3
    
    # Verify simplification for term A: coeff=1, radicand=3 (already square-free).
    simplified_a = RadicalOps.simplify_term(radical_coefficient_a, radicand_a)
    
    rational_part_b = Fraction(2, 1)
    radical_coefficient_b = -1
    
    # Verify simplification for term B: coeff=-1, radicand=3.
    simplified_b = RadicalOps.simplify_term(radical_coefficient_b, radicand_a)
    
    # Calculate target expression: 2a + b
    # a = rational_part_a + sqrt(radicand_a) -> value is (rational_part_a + radical_coefficient_a * sqrt(radicand))
    # Actually the terms are of form c1*sqrt(d). 
    # Let's represent roots as linear radicals: 2+√3 and 2-√3.
    
    term_a = {"rational": int(Fraction(2, 1)), "radical_coefficient": 1, "radicand": 3}
    term_b = {"rational": int(Fraction(2, 1)), "radical_coefficient": -1, "radicand": 3}
    
    # We need to compute the value of 2a + b.
    # a corresponds to rational part 2 and radical coeff 1 (since sqrt(3) is positive).
    # Wait, standard form for linear radicals in this domain usually separates integer parts if present?
    # The example `add_linear_radicals` handles terms like {rational: x, radical_coefficient: y}.
    # Here roots are exactly of the form 2 + sqrt(3) and 2 - sqrt(3).
    
    # Let's construct the final result as a single linear radical term if possible? 
    # No, 2a+b = 2*(2+sqrt(3)) + (2-sqrt(3)) = 4 + 2*sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3).
    
    final_rational_coefficient = int(Fraction(6, 1)) # The rational part of the sum is 6. 
    # Wait, looking at `add_linear_radicals`, it adds two terms with same radicand.
    # Term A: {rational: 2, radical_coefficient: 1} -> represents 2 + sqrt(3) ? Or just sqrt term?
    # Example in API doc: add_linear_radicals({"rational": 1...}, {"rational": 3...}) returns dict with rational and coeff.
    # This implies the input dicts represent terms like `rational_part + radical_coefficient * sqrt(radicand)`.
    
    # So term_a is (2, 1), term_b is (2, -1).
    # We want to compute 2*term_a + term_b.
    # Scale term a by 2: {rational: 4, radical_coefficient: 2}.
    scaled_term_a = RadicalOps.scale_linear_radical(term_a, 2)
    
    # Add scaled_term_a and term_b? 
    # Wait, the result should be in form `result_rational + result_coeff * sqrt(result_radicand)`.
    # Let's re-evaluate: 
    # a = 2 + sqrt(3). b = 2 - sqrt(3).
    # 2a + b = 4 + 2sqrt(3) + 2 - sqrt(3) = (4+2) + (2-1)sqrt(3) = 6 + sqrt(3).
    
    # Construct the final term dict.
    result_rational = int(Fraction(6, 1))
    result_radical_coefficient = 1
    
    # The domain API `add_linear_radicals` expects two terms with identical radicand to add them directly?
    # Or we can just construct the final answer manually since it's a simple arithmetic operation on coefficients.
    
    # Let's use scale and then format, or simply compute the components.
    # Since 2a+b is a single linear radical term (6 + sqrt(3)), 
    # rational part = 6, coeff = 1, radicand = 3.
    
    final_term_dict = {
        "rational": int(Fraction(6, 1)),
        "radical_coefficient": 1,
        "radicand": 3
    }
    
    # Generate LaTeX for the result term
    latex_result = RadicalOps.format_linear_radical(final_term_dict)
    
    return {
        "question_text": kwargs.get("stem", r"一元二次方程式 \[ (x-2)^2=3 \] 的兩根為 \(a,b\)，且 \(a>b\)。求 \(2a+b\)，答案須保持精確根式形式。"),
        "correct_answer": {
            "result": {
                "rational": int(Fraction(6, 1)), # Integer value as per contract
                "radical_coefficient": 1,
                "radicand": 3,
                "canonical_latex": latex_result
            }
        },
        "oracle_payload": kwargs.get("frozen_params", {
            "equation": "(x-2)^2=3", 
            "order": "a>b", 
            "target": "2a+b"
        })
    }
