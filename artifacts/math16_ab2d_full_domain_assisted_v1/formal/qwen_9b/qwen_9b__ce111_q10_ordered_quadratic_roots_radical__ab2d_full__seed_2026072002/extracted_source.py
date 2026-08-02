def generate(level=1, **kwargs):
    # Step 0: Parse frozen_params from kwargs or defaults if not passed explicitly in this context
    # The task description provides specific values for the equation and target.
    # We reconstruct the roots manually using native arithmetic to ensure control over ordering (a > b).
    
    # Equation: (x-2)^2 = 3 => x - 2 = +/- sqrt(3) => x = 2 +/- sqrt(3)
    # Roots are a = 2 + sqrt(3), b = 2 - sqrt(3). Since sqrt(3) > 0, a > b holds naturally.
    
    # Construct LinearRadical dict for the radical part: coefficient=1, radicand=3
    root_radical_part = {
        "rational": 2,      # The rational shift (x-2 -> x)
        "radical_coefficient": 1,
        "radicand": 3       # sqrt(3)
    }
    
    # Construct LinearRadical dict for the negative root part: coefficient=-1, radicand=3
    neg_root_radical_part = {
        "rational": 2,      # The rational shift (x-2 -> x)
        "radical_coefficient": -1,
        "radicand": 3       # sqrt(3), but coefficient is negative effectively in the term structure? 
                            # Wait, standard LinearRadical usually stores sign in 'rational' or separate coeff.
                            # Looking at add_linear_radicals example: {"rational": 1, ...} + {"rational": 3, ...} -> rational sums.
                            # If we have x = 2 - sqrt(3), the term is (-1)*sqrt(3) + 2? 
                            # Or does 'radical_coefficient' handle sign and 'rational' handles constant?
                            # Example: RadicalOps.format_linear_radical({"rational": 1, "radical_coefficient": 1, "radicand": 2}) -> "1+\sqrt{2}"
                            # If we want -sqrt(3), likely radical_coefficient=-1. Let's assume sign is in coefficient.
    
    # Re-evaluating the structure based on `add_linear_radicals` example: 
    # inputs: two LinearRadical dicts with identical positive radicand
    # returns rational sum, etc.
    # If term A has coeff 1 and term B has coeff -1, adding them should work if they share radicand?
    # But here we are scaling the POSITIVE root (a) by 2, then ADDING the SMALLER root (b).
    
    # Root a: x = 2 + sqrt(3). 
    # Representation: rational=2, radical_coefficient=1, radicand=3.
    term_a_raw = { "rational": 2, "radical_coefficient": 1, "radicand": 3 }
    
    # Root b: x = 2 - sqrt(3). 
    # Representation: rational=2, radical_coefficient=-1, radicand=3. (Assuming sign is in coeff)
    term_b_raw = { "rational": 2, "radical_coefficient": -1, "radicand": 3 }
    
    # Verify ordering a > b: 
    # term_a has +sqrt(3), term_b has -sqrt(3). Clearly term_a > term_b.
    
    # Step 1 & 2 from instructions:
    # Call RadicalOps.scale_linear_radical on the larger root (term_a_raw) with weight 2.
    scaled_term_a = RadicalOps.scale_linear_radical(term_a_raw, k=2)
    
    # Then call RadicalOps.add_linear_radicals with the smaller root (term_b_raw).
    # Note: add_linear_radicals expects two dicts with identical radicand. Both have radicand 3.
    final_result_dict = RadicalOps.add_linear_radicals(scaled_term_a, term_b_raw)
    
    # Step 4: Assemble correct_answer exactly according to the Answer contract.
    # Schema requires: result -> { rational, radical_coefficient, radicand, canonical_latex }
    
    latex_str = RadicalOps.format_expression(final_result_dict)
    
    return {
        "question_text": "一元二次方程式 (x-2)^2=3 的兩根為 a,b，且 a>b。求 2a+b，答案須保持精確根式形式。",
        "correct_answer": {
            "result": final_result_dict, # This dict contains rational, radical_coefficient, radicand as ints
            "canonical_latex": latex_str
        },
        "oracle_payload": {
            "equation": "(x-2)^2=3",
            "order": "a>b",
            "target": "2a+b"
        }
    }