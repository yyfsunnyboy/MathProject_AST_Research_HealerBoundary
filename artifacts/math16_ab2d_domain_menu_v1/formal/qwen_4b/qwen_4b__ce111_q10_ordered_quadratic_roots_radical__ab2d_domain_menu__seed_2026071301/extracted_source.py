from core.prompts.domain_function_library import RadicalOps, Fraction


def generate(level=1, **kwargs):
    # Solve (x-2)^2 = 3 for x.
    # Take square root: |x - 2| = sqrt(3) => x - 2 = ±sqrt(3).
    # Roots are a = 2 + sqrt(3), b = 2 - sqrt(3).
    # Given a > b, we have the correct assignment.
    
    rational_part = Fraction(0, 1)
    radical_coefficient_a = 1
    radicand_a = 3
    
    # Verify simplification of term for formatting consistency if needed
    coeff_a, rad_a = RadicalOps.simplify_term(radical_coefficient_a, radicand_a)
    
    rational_part_b = Fraction(0, 1)
    radical_coefficient_b = -1
    radicand_b = 3
    
    # Verify simplification for b term (coefficient is negative)
    coeff_b, rad_b = RadicalOps.simplify_term(radical_coefficient_b, radicand_b)

    # Calculate target: 2a + b
    # a = rational_part_a + radical_coefficient_a * sqrt(radicand_a)
    #   = 0 + 1*sqrt(3) -> Wait, the root is just sqrt(3). 
    # The term structure in LinearRadical usually represents c + d*sqrt(n).
    # Here a = 2 + sqrt(3)? No. (x-2)^2=3 => x^2 -4x +4 =3 => x^2 -4x +1=0.
    # Roots: [4 ± sqrt(16-4)]/2 = [4 ± sqrt(12)]/2 = 2 ± sqrt(3).
    # So a = 2 + sqrt(3), b = 2 - sqrt(3).
    
    rational_part_a = Fraction(2, 1)
    radical_coefficient_a_final = 1
    radicand_a_final = 3
    
    rational_part_b = Fraction(2, 1)
    radical_coefficient_b_final = -1
    radicand_b_final = 3

    # Ensure terms are normalized/simplified via API if necessary for consistency
    term_a_dict = RadicalOps.scale_linear_radical({"rational": int(rational_part_a), "radical_coefficient": int(radical_coefficient_a_final), "radicand": int(radicand_a_final)}, 1)
    
    # Calculate value of a and b to ensure precision before final assembly? 
    # Actually, the question asks for exact form. We construct it directly from roots.
    # a = 2 + sqrt(3) -> rational=2, coeff=1, radicand=3
    # b = 2 - sqrt(3) -> rational=2, coeff=-1, radicand=3
    
    term_a = {"rational": int(rational_part_a), "radical_coefficient": int(radical_coefficient_a_final), "radicand": int(radicand_a_final)}
    
    # Calculate 2a + b
    # (2 * rational_a) + radical_coefficient_a*sqrt(3)*2 + rational_b + radical_coefficient_b*sqrt(3)
    # Rational part: 2*(2) + 2 = 4 + 2 = 6? No. 
    # Expression is linear combination of a and b.
    # Value = 2 * (rational_a + coeff_a * sqrt(rad)) + (rational_b + coeff_b * sqrt(rad))
    #       = (2*rational_a + rational_b) + (2*coeff_a + coeff_b)*sqrt(rad)
    
    final_rational = int(rational_part_a * 2 + rational_part_b)
    final_coefficient = int(int(radical_coefficient_a_final) * 2 + radical_coefficient_b_final)
    final_radicand = radicand_a_final
    
    # Format the result term for canonical_latex using API
    latex_str = RadicalOps.format_term(final_rational, final_radicand if final_coefficient == 1 else None) 
    # Wait format_term takes coeff and radicand. If coeff is not 1 or -1?
    # The example shows '2\sqrt{3}'. It handles coefficient inside the term string generation logic presumably.
    # Let's use scale_linear_radical to ensure structure, then format linear radical if needed, 
    # but we need a single expression "6 + \sqrt{5}" or similar? Or just one term dict formatted?
    # The contract asks for canonical_latex of the result 2a+b.
    
    # Let's construct the final LinearRadical structure to be safe and format it properly using available APIs.
    # We have rational=6, coeff=1 (since -1 + 2 = 1), radicand=3? 
    # Wait: a = 2+sqrt(3). b = 2-sqrt(3).
    # 2a+b = 2*(2+sqrt(3)) + (2-sqrt(3)) = 4 + 2*sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3).
    
    final_rational_val = int(rational_part_a * 2 + rational_part_b) # 2*2+2=6
    final_coeff_val = int(int(radical_coefficient_a_final)*2 + radical_coefficient_b_final) # 1*2-1=1
    
    term_result_dict = {"rational": final_rational_val, "radical_coefficient": final_coeff_val, "radicand": radicand_a_final}
    
    latex_output = RadicalOps.format_linear_radical(term_result_dict)

    correct_answer_data = {
        "result": {
            "rational": int(final_rational_val),
            "radical_coefficient": int(final_coeff_val),
            "radicand": int(radicand_a_final),
            "canonical_latex": latex_output
        }
    }

    return {
        "question_text": kwargs.get("stem", "一元二次方程式 (x-2)^2=3 的兩根為 a,b，且 a>b。求 2a+b，答案須保持精確根式形式。"),
        "correct_answer": correct_answer_data,
        "oracle_payload": {
            "equation": "(x-2)^2=3",
            "order": "a>b",
            "target": "2a+b"
        }
    }
