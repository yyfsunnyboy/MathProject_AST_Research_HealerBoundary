from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    # 1. Solve (x-2)^2 = 3 => x - 2 = +/- sqrt(3) => x = 2 +/- sqrt(3)
    # Roots: a = 2 + sqrt(3), b = 2 - sqrt(3). Since sqrt(3)>0, a > b.
    
    # Construct LinearRadical dicts for the roots manually based on algebraic derivation
    # Root structure in domain API typically expects keys like 'rational', 'radical_coefficient', 'radicand'
    # However, looking at RadicalOps.add_linear_radicals signature: inputs are two LinearRadical dicts with identical positive radicand.
    # The example shows {"rational": 1, "radical_coefficient": 1, "radicand": 2}.
    
    # Let's define the terms for a and b.
    # Term A (larger): rational part = 2, radical part coefficient = 1, radicand = 3.
    term_a_dict = {"rational": 2, "radical_coefficient": 1, "radicand": 3}
    
    # Term B (smaller): rational part = 2, radical part coefficient = -1 (since it's minus), radicand = 3.
    # Note: The API might expect the sign in 'rational' or handle negative coefficients? 
    # Looking at RadicalOps.add_linear_radicals example: {"rational": 3, "radical_coefficient": 1}. It seems rational is an integer offset.
    # If the term represents c + k*sqrt(n), then for b = 2 - sqrt(3):
    # Option 1: radical_coefficient can be negative? The schema says value_types["radical_coefficient"]: ["int"]. Integers include negatives.
    # Option 2: 'rational' holds the sign? No, usually rational is the integer part. 
    # Let's assume radical_coefficient handles the +/- via its sign.
    
    term_b_dict = {"rational": 2, "radical_coefficient": -1, "radicand": 3}
    
    # Verify ordering: a > b implies we must use term_a first for scaling if needed, 
    # but add_linear_radicals just sums them. The prompt asks to scale the larger root (a) by 2 then add smaller (b).
    
    # Step 1 & 3: Scale larger root 'term_a_dict' by weight 2.
    scaled_term = RadicalOps.scale_linear_radical(term_a_dict, k=2)
    
    # Step 2: Add the scaled term and the smaller root.
    result_sum = RadicalOps.add_linear_radicals(scaled_term, term_b_dict)
    
    # Extract components for correct_answer contract
    rational_part = result_sum["rational"]
    radical_coefficient_part = result_sum["radical_coefficient"]
    radicand_part = result_sum["radicand"]
    
    # Generate canonical LaTeX using format_linear_radical on the combined term? 
    # Wait, add_linear_radicals returns a dict representing ONE linear radical if they share radicands.
    # The example for add_linear_radicals implies it sums coefficients of same radicand and rational parts separately?
    # Actually, looking at RadicalOps.format_expression: inputs mapping radicand->coefficient.
    # But our result_sum is likely already a single LinearRadical dict because both have radicand 3.
    
    canonical_latex = RadicalOps.format_linear_radical(result_sum)
    
    # Assemble correct_answer according to Task-specific answer contract
    return {
        "question_text": kwargs.get("frozen_params", {}).get("equation") + 
                        f"的兩根為 a,b，且 a>b。求 2a+b，答案須保持精確根式形式。\n{kwargs.get('frozen_params', {}).get('target')}",
        "correct_answer": {
            "result": {
                "rational": rational_part,
                "radical_coefficient": radical_coefficient_part,
                "radicand": radicand_part,
                "canonical_latex": canonical_latex
            }
        },
        "oracle_payload": kwargs.get("frozen_params", {})
    }