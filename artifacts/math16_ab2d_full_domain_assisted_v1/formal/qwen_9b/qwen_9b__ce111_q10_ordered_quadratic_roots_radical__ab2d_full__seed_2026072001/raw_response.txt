from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    frozen_params = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }

    # Step 1: Solve (x-2)^2 = 3 => x - 2 = +/- sqrt(3) => x = 2 +/- sqrt(3)
    # Roots are a = 2 + sqrt(3), b = 2 - sqrt(3). Since sqrt(3)>0, a > b.
    
    # Construct LinearRadical dict for the term: coefficient=1, radicand=3 (implicit rational part handled separately or combined?)
    # The API expects "LinearRadical" dicts with keys: "rational", "radical_coefficient", "radicand".
    # For x = 2 + sqrt(3): rational=2, radical_coefficient=1, radicand=3.
    
    root_a_dict = {
        "rational": 2,
        "radical_coefficient": 1,
        "radicand": 3
    }
    
    # For x = 2 - sqrt(3): rational=2, radical_coefficient=-1, radicand=3.
    root_b_dict = {
        "rational": 2,
        "radical_coefficient": -1,
        "radicand": 3
    }

    # Verify order: a > b is satisfied by construction (coeff +1 vs -1)
    
    # Step 2: Calculate 2a + b.
    # First scale root_a_dict by weight 2.
    scaled_root_a = RadicalOps.scale_linear_radical(root_a_dict, k=2)
    
    # Then add the smaller root (root_b_dict). Note that add_linear_radicals expects identical radicands and adds coefficients/rational parts linearly.
    final_result_dict = RadicalOps.add_linear_radicals(scaled_root_a, root_b_dict)

    # Step 3: Format for canonical_latex if needed, though format_term might be safer for single terms or we construct manually? 
    # The contract asks for "canonical_latex". Let's try to reconstruct the expression from the final dict components.
    # However, RadicalOps.format_linear_radical takes a term (dict). Our result is already combined in one dict via add_linear_radicals logic usually resulting in simplified form if possible, but here we have rational + radical_coeff*sqrt(radicand).
    # The API format_linear_radical expects keys: "rational", "radical_coefficient", "radicand".
    
    canonical_latex = RadicalOps.format_linear_radical(final_result_dict)

    correct_answer = {
        "result": final_result_dict,  # This dict contains rational, radical_coefficient, radicand as ints per contract
        "canonical_latex": canonical_latex
    }

    return {
        "question_text": frozen_params["equation"] + "\n的兩根為 a,b，且 a>b。求 2a+b，答案須保持精確根式形式。",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }