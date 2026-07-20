def generate(level=1, **kwargs):
    # Frozen parameters from the prompt specification for this specific run logic or general use?
    # The prompt says "Frozen sampled parameters". In a real system these come in kwargs. 
    # Here we must ensure they are used if provided, otherwise default to task spec example?
    # Instruction: "oracle_payload must exactly equal the frozen sampled parameters."
    
    div_coeffs = kwargs.get('dividend_coefficients', [6, 4, 0])
    den_coeffs = kwargs.get('divisor_coefficients', [2, 0, 0])
    
    oracle_payload = {
        "dividend_coefficients": div_coeffs,
        "divisor_coefficients": den_coeffs
    }

    # Perform division using domain API (mocked logic inside PolynomialOps.div_qr above)
    quotient_coefs, remainder_coefs = PolynomialOps.div_qr(div_coeffs, den_coeffs)
    
    # Format the answer. The correct_answer must include only remainder and canonical_latex.
    # Note: "quotient is not scored". But we still need to compute it for the division operation logic.
    # Does 'correct_answer' dict contain keys? 
    # Spec: "return a dict with exactly question_text, correct_answer, and oracle_payload."
    # "correct_answer must include only remainder and canonical_latex" -> This likely means the value of key 'correct_answer' is an object/dict containing these two.
    
    rem_str = PolynomialOps.format_latex(remainder_coefs)
    
    # Construct question_text using formal LaTeX delimiters
    div_rem_str = PolynomialOps.format_latex(div_coeffs, var='x')
    den_rem_str = PolynomialOps.format_latex(den_coeffs, var='x')
    
    q_str = "?" 
    
    # We need to format the quotient too for the text if we want it complete? 
    # "correct_answer must include only remainder and canonical_latex" implies the answer object.
    # question_text should describe the problem: Find R(x) where P(x)/Q(x).
    
    q_coefs = [c] if len(quotient_coefs)==1 else quotient_coefs
    
    canon_rem_latex = PolynomialOps.format_latex(remainder_coefs, var='x')
    
    # Constructing a robust question text template: "Given $P(x) = ...$ and $Q(x) = ...$, find the remainder when dividing by $R(x)$." 
    # Or simply stating the problem.
    question_text = f"Find the remainder of polynomial division given dividend coefficients {div_coeffs} and divisor coefficients {den_coeffs}. Let P(x) be defined by {div_rem_str} and Q(x) by {den_rem_str}. Compute R(x)."

    correct_answer_obj = {
        "remainder": rem_str, # The raw string or latex? Spec says canonical_latex is separate. 
                             # Wait: "correct_answer must include only remainder and canonical_latex".
                             # Maybe 'remainder' key holds the numeric/list value? Or the string representation of it?
                             # Usually in these tasks, 'canonical_latex' is the formatted version for grading display/scoring if needed, but here quotient not scored.
                             # Let's put the latex string in canonical_latex and maybe a simplified form or just reuse in remainder? 
                             # Re-reading: "correct_answer must include only remainder and canonical_latex".
                             # Interpretation 1: The value for key 'correct_answer' is a dict {remainder, canonical_latex}.
                             # What should be the type of 'remainder'? Usually the string representation or list. Given oracle_payload has lists, maybe remainder here is also list? 
                             # But it asks to format latex in correct_answer. Let's assume 'canonical_latex' holds the final answer string and 'remainder' might hold a simpler version or just duplicate for safety if not specified strictly as different types.
                             # However, standard practice: canonical_latex = formatted string. remainder could be the same or list. 
                             # Given "correct_answer must include only remainder and canonical_latex", I will provide both strings where remainder is likely the latex too unless a raw form exists. 
                             # Let's set 'remainder' to the latex string of coefficients, and 'canonical_latex' also to that? Or maybe quotient was intended but excluded from scoring.
                             # Actually, looking at similar tasks: often 'correct_answer' value is { "value": ..., "latex": ... }. Here keys are explicitly named remainder and canonical_latex inside correct_answer dict? 
                             # No, the function returns a dict with keys question_text, correct_answer, oracle_payload.
                             # So `generate()` -> `{question_text: "...", correct_answer: {...}, oracle_payload: {...}}`.
                             # Inside `correct_answer`, we need keys 'remainder' and 'canonical_latex'. 
                             
    }

    # Let's refine the structure of correct_answer based on "include only remainder and canonical_latex" inside it.
    answer_dict = {
        "remainder": rem_str, # Using latex string for consistency unless raw list required (unlikely given formatting requirement)
        "canonical_latex": canon_rem_latex 
    }

    return {
        "question_text": question_text,
        "correct_answer": answer_dict,
        "oracle_payload": oracle_payload
    }