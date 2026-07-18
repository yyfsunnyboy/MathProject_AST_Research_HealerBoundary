from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    expression = "(2*sqrt(3) + sqrt(6))*sqrt(2)"
    
    # Distribute sqrt(2):
    # 2*sqrt(3)*sqrt(2) + sqrt(6)*sqrt(2) = 2*sqrt(6) + sqrt(12)
    # Term 1: coeff=2, radicand=6
    # Term 2: coeff=1, radicand=12
    
    t1_coeff, t1_rad = RadicalOps.simplify_term(2, 6)
    t2_coeff, t2_rad = RadicalOps.simplify_term(1, 12)
    
    raw_terms = [
        {"coefficient": t1_coeff, "radicand": t1_rad},
        {"coefficient": t2_coeff, "radicand": t2_rad}
    ]
    
    normalized_terms = RadicalOps.normalize_term_list(raw_terms)
    
    formatted_terms = []
    for term in normalized_terms:
        coeff = term["coefficient"]
        # Convert to standard Python int/float for JSON compatibility
        try:
            if float(coeff).is_integer():
                coeff = int(coeff)
            else:
                coeff = float(coeff)
        except (TypeError, ValueError):
            coeff = str(coeff)
            
        formatted_terms.append({
            "coefficient": coeff,
            "radicand": int(term["radicand"])
        })
        
    question_text = f"Simplify the expression: {expression}"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "terms": formatted_terms
        },
        "oracle_payload": {
            "expression": expression
        }
    }