def generate(level=1, **kwargs):
    frozen_params = {"expression": "(2*sqrt(3) + sqrt(6))*sqrt(2)"}
    
    # Parse the expression manually based on the string provided in frozen_params
    # Expression: (2*sqrt(3) + sqrt(6)) * sqrt(2)
    # Term 1 inside bracket: 2*sqrt(3) -> coeff=2, radicand=3
    # Term 2 inside bracket: sqrt(6) -> coeff=1, radicand=6
    
    terms_inside = [
        (2, 3),
        (1, 6)
    ]
    
    outer_coefficient = 1
    outer_radicand = 2
    
    # Distribute the multiplication by sqrt(2) to each term inside
    simplified_terms_list = []
    
    for coeff_in, radicand_in in terms_inside:
        new_radicand = radicand_in * outer_radicand
        
        if new_radicand % (outer_radicand ** 2) == 0 or new_radicand < outer_radicand: # Simplification logic check
            pass 
        
        # We need to simplify sqrt(radicand1 * radicand2). 
        # Here we multiply the radicands and then try to pull out perfect squares.
        
        combined_coeff = coeff_in * outer_coefficient
        
        # Calculate new radicand after multiplication of radicals
        final_radicand_val = radicand_in * (outer_radicand ** 2) if False else radicand_in * outer_radicand
        # Actually, sqrt(a)*sqrt(b) = sqrt(ab). So we just multiply the numbers under root.
        
        current_product = radicand_in * outer_radicand
        
        # Simplify the term: pull out perfect squares from current_product
        simplified_coeff, final_radicand = simplify_term(combined_coeff, current_product)
        simplified_terms_list.append((simplified_coeff, final_radicand))

    def simplify_term(coeff: int, radicand: int):
        """Simplify sqrt(radicand). Returns (coefficient, square_free_radicand)"""
        # Find largest perfect square factor of radicand
        i = 2
        while i * i <= radicand:
            if radicand % (i * i) == 0:
                count = 1
                temp_radicand = radicand // (i*i)
                coeff *= int(i**count) # Pull out the square root part
                return coeff, temp_radicand
            
        return coeff, radicand

    simplified_terms_list = []
    
    for term in terms_inside:
        c_in, r_in = term
        
        # Multiply by outer sqrt(2): effectively multiplying radicands and coefficients
        new_radicand_val = r_in * 4 # because (sqrt(x))^2 is x? No. 
        # Wait, the expression is (A + B) * C. This equals A*C + B*C.
        # Term 1: 2*sqrt(3). Multiply by sqrt(2): coeff becomes 2, radicand becomes 3*2=6.
        # Simplify sqrt(6)? No perfect square factor > 1 in 6 (other than 1). So stays as is? 
        # Wait, the domain API simplifies term. Let's re-evaluate manually to be safe with logic flow without calling external simplify_term for every step if not needed, but I must use it.
        
        # Re-calculation:
        # Term A = 2 * sqrt(3). Multiply by outer sqrt(2) -> coeff=2*1=2, radicand=3*2=6. 
        # Simplify term (coeff=2, radicand=6): No square factor in 6? Correct. Result: (2, 6).
        
        # Term B = 1 * sqrt(6). Multiply by outer sqrt(2) -> coeff=1*1=1, radicand=6*2=12. 
        # Simplify term (coeff=1, radicand=12): 4 is a square factor of 12? Yes.
        # sqrt(12) = sqrt(4*3) = 2 * sqrt(3). So coeff becomes 1*2=2, radicand becomes 3. Result: (2, 3).

        term_a_coeff, term_a_rad = simplify_term(c_in, r_in * outer_radicand)
        
        # Wait, the domain API signature is `simplify_term(coeff, radicand)` returning `(outer coefficient, square-free radicand)`.
        # It assumes the input is a single radical sqrt(radicand). 
        # My manual logic above: Term A becomes 2*sqrt(6). The function call should be simplify_term(2, 6)? No.
        # If I pass (coeff=2, radicand=6), it treats it as coeff * sqrt(6). It checks if 6 has square factors. 
        # Since 6 = 1^2 * 6, no change? But wait, the function description says "simplify_term".
        # Usually simplify_term handles pulling out squares from radicand and multiplying into coefficient.
        
        # Let's trace Term A: Original (2,3). Multiply by sqrt(2) -> coeff=2, radicand=6. 
        # Call simplify_term(2, 6): checks if 6 has square factor >1? No. Returns (2, 6). Correct.
        
        # Let's trace Term B: Original (1,6). Multiply by sqrt(2) -> coeff=1, radicand=12. 
        # Call simplify_term(1, 12): checks if 12 has square factor? Yes, 4. 
        # Pulls out 2 into coefficient. Returns (2, 3). Correct.
        
        term_a_coeff, term_a_rad = simplify_term(c_in * outer_coefficient, r_in * outer_radicand)
        simplified_terms_list.append((term_a_coeff, term_a_rad))

    # Merge terms with same radicands and sort by increasing radicand
    merged_dict: Dict[int, int] = {}
    
    for coeff, rad in simplified_terms_list:
        if rad not in merged_dict:
            merged_dict[rad] = 0
        
        merged_dict[rad] += coeff
    
    # Convert back to list of tuples and sort by radicand (increasing)
    final_terms = []
    for rad in sorted(merged_dict.keys()):
        final_terms.append((merged_dict[rad], rad))

    correct_answer: Dict[str, List[Tuple[int, int]]] = {"terms": final_terms}
    
    oracle_payload = frozen_params
    
    return {
        "question_text": f"Simplify the radical product expression provided in the parameters.",
        "correct_answer": json.dumps(correct_answer), # Ensure JSON compatible string or dict? 
        # Specification says: correct_answer must be a JSON-compatible dict. So it should be a Python dict that can be serialized, not necessarily a string itself unless specified as such. 
        # The prompt says "must return a dict with ... correct_answer". And "correct_answer must be a JSON-compatible dict".
        # I will keep it as the raw dict structure to ensure compatibility without double encoding if json.dumps is used inside.
        # However, usually in these tasks, returning the actual Python object that represents valid JSON is key. 
        # Let's return the dict directly.
    }

# Re-implementing strictly with domain API usage and correct types as per spec constraints to avoid any runtime errors or type mismatches.
from core.prompts.domain_function_library import RadicalOps.simplify_term

def generate(level=1, **kwargs):
    frozen_params = {"expression": "(2*sqrt(3) + sqrt(6))*sqrt(2)"}
    
    # Step 1: Identify terms inside the parenthesis before multiplication by outer term.
    # Term 1: coeff=2, radicand=3
    # Term 2: coeff=1, radicand=6
    
    initial_terms = [(2, 3), (1, 6)]
    
    # Step 2: Multiply each inner term by the outer sqrt(2).
    # This means multiplying the coefficient by 1 and the radicand by 4? No. 
    # Mathematically: a * sqrt(x) + b * sqrt(y) multiplied by c * sqrt(z)
    # = (a*c)*sqrt(x*z) + (b*c)*sqrt(y*z).
    
    outer_coeff = 1
    outer_radicand_val = 2
    
    processed_terms = []
    
    for coeff, radicand in initial_terms:
        new_radicand = radicand * outer_radicand_val
        
        # Apply domain API to simplify the resulting radical term
        simplified_c, simplified_r = simplify_term(coeff, new_radicand)
        
        if simplified_r == 0 or (simplified_c != coeff and simplified_r != new_radicand):
            processed_terms.append((simplified_c, simplified_r))
        else:
            # If no simplification happened inside the function logic for this specific input format? 
            # Actually simplify_term should handle it. Let's assume standard behavior.
            pass
            
    # Step 3: Merge terms with identical radicands and sort by increasing radicand.
    
    term_map = {}
    for c, r in processed_terms:
        if r not in term_map:
            term_map[r] = 0
        
        term_map[r] += c
    
    final_list = []
    # Sort keys (radicands) ascending
    sorted_radicands = sorted(term_map.keys())
    
    for r in sorted_radicands:
        final_list.append((term_map[r], r))
        
    correct_answer_dict = {"terms": final_list}
    
    oracle_payload = frozen_params
    
    return {
        "question_text": f"Simplify the expression given by parameters.",
        "correct_answer": correct_answer_dict, 
        "oracle_payload": oracle_payload
    }