from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }
    
    # Step 1: Solve (x-2)^2 = 3 => x - 2 = +/- sqrt(3) => x = 2 +/- sqrt(3)
    # Roots are a = 2 + sqrt(3), b = 2 - sqrt(3). Since sqrt(3)>0, a>b holds.
    
    root_a_dict = {
        "rational": 2,
        "radical_coefficient": 1,
        "radicand": 3
    }
    
    root_b_dict = {
        "rational": 2,
        "radical_coefficient": -1,
        "radicand": 3
    }
    
    # Verify order a > b (handled by construction: +sqrt vs -sqrt)
    
    # Step 2: Calculate 2a + b = scale(root_a_dict, 2) + root_b_dict
    
    scaled_root_a = RadicalOps.scale_linear_radical(root_a_dict, 2)
    
    combined_result = RadicalOps.add_linear_radicals(scaled_root_a, root_b_dict)
    
    # Step 3: Format for canonical_latex (optional but good practice based on contract needing string)
    # The format_expression expects mapping radicand->coefficient. 
    # We need to reconstruct the dict in that specific shape or use a helper if available.
    # Looking at RadicalOps.format_expression signature: `(terms_dict, denominator=1)` where terms_dict is `mapping radicand->coefficient`.
    
    # Construct the format dictionary from combined_result keys/values? 
    # The API description says inputs are "mapping radicand->coefficient". 
    # However, our result dict has keys ["rational", "radical_coefficient", "radicand"].
    # We need to extract these. Note: if rational is non-zero and radical_coefficient exists, they sum up?
    # Actually, the API `add_linear_radicals` returns a LinearRadical JSON-safe int dict with keys ['rational', 'radical_coefficient', 'radicand'].
    # The format_expression expects a mapping like {3: 5} meaning 5*sqrt(3). 
    # But our result might have both rational and radical parts. 
    # Let's check the example for format_expression: `RadicalOps.format_expression({1: 6, 3: -1})` -> `'6 - \sqrt{3}'`.
    # This implies it handles multiple radicands or just one? The example has two keys (radicand->coeff).
    # If we have a term like {rational: X, radical_coefficient: Y, radicand: Z}, how do we format?
    # Usually `format_expression` is for sums of radicals. 
    # Is there an API to format the full LinearRadical dict including rational part?
    # Looking at available APIs:
    # - RadicalOps.format_linear_radical(term) -> "1+\sqrt{2}" (takes a term dict). This seems perfect for our combined result which is one term.
    
    canonical_latex = RadicalOps.format_linear_radical(combined_result)
    
    return {
        "question_text": frozen["equation"] + "\n的兩根為 \(a,b\)，且 \(a>b\)。求 \(2a+b\)，答案須保持精確根式形式。",
        "correct_answer": {
            "result": combined_result,  # This dict has keys rational, radical_coefficient, radicand as ints.
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen
    }