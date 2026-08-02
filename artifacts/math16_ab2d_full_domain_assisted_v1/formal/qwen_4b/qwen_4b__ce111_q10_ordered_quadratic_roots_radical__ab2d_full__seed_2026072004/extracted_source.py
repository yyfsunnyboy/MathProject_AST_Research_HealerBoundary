from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    # Step 1: Solve (x-2)^2 = 3 for roots a and b where a > b
    # x - 2 = ±√3 => x = 2 + √3 or x = 2 - √3
    # Root terms are represented as LinearRadical dicts with rational part, radical coefficient, radicand
    
    term_a_raw = {"rational": 2, "radical_coefficient": 1, "radicand": 3}   # a = 2 + sqrt(3)
    term_b_raw = {"rational": 2, "radical_coefficient": -1, "radicand": 3}  # b = 2 - sqrt(3)

    # Verify ordering: since coefficient of radical part is positive for a and negative for b (same radicand),
    # term_a corresponds to the larger root. We proceed with term_a as 'a' and term_b as 'b'.

    # Step 2: Compute target expression 2*a + b
    # First, scale term_a by 2 using RadicalOps.scale_linear_radical
    scaled_term = RadicalOps.scale_linear_radical(term_a_raw, 2)
    
    # Then add the smaller root (term_b) using RadicalOps.add_linear_radicals
    result_terms = RadicalOps.add_linear_radicals(scaled_term, term_b_raw)

    # Step 3: Format for canonical LaTeX representation if needed, 
    # though we will construct correct_answer based on numeric fields per contract.
    
    # Extract values from the resulting LinearRadical dict (rational + radical part combined)
    rational_part = result_terms["rational"]
    rad_coeff = result_terms["radical_coefficient"]
    radicand = result_terms["radicand"]

    # Step 4: Assemble correct_answer per contract schema
    canonical_latex = RadicalOps.format_linear_radical(result_terms)

    return {
        "question_text": "一元二次方程式\n\\[(x-2)^2=3\\]\n的兩根為 \\(a,b\\)，且 \\(a>b\\)。求 \\(2a+b\\)，答案須保持精確根式形式。",
        "correct_answer": {
            "result": {
                "rational": rational_part,
                "radical_coefficient": rad_coeff,
                "radicand": radicand,
                "canonical_latex": canonical_latex
            }
        },
        "oracle_payload": kwargs.get("frozen_params", {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"})
    }
