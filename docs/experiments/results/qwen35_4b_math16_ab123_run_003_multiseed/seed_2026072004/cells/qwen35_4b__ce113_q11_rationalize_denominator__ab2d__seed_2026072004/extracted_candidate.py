def generate(level=1, **kwargs):
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }
    
    from core.prompts.domain_function_library import FractionOps
    
    numerator_val = int(frozen_params["numerator"])
    denominator_str = str(frozen_params["denominator"])
    radicand_int = int(frozen_params["radicand"])
    
    a, b = 4, 1
    term_frac_a = FractionOps.create(a)
    term_frac_b = FractionOps.create(b) * (FractionOps.create(radicand_int)) ** (0.5)
    denominator_val = term_frac_a + term_frac_b
    
    numerator_frac = FractionOps.create(numerator_val)
    
    conjugate_term1 = term_frac_a - term_frac_b
    product_conj = num_denom_mul = None # Placeholder for logic flow correction below

    correct_answer_int = 0
    
    from core.prompts.domain_function_library import to_exact
    numerator_exact = to_exact(numerator_val)
    
    denominator_part1 = FractionOps.create(4) * (FractionOps.create(radicand_int)) ** 2
    denominator_part2 = term_frac_b.pow(2).simplify() # sqrt(x)^2 = x
    
    rationalized_num, den_denom = None, None

    correct_answer_int = numerator_val // int(FractionOps.add(denominator_part1, denominator_part2)) + (numerator_val * radicand_int)
    
    return {
        "question_text": r"Rationalize the denominator of $\frac{9}{4-\sqrt{7}}$. Express your answer as a single integer representing the numerator after rationalization and simplification.",
        "correct_answer": correct_answer_int,
        "oracle_payload": frozen_params
    }