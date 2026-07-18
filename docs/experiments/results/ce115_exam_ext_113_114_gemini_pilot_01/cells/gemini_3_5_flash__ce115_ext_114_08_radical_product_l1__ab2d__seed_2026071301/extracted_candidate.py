from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    expression = "(2*sqrt(3) + sqrt(6))*sqrt(2)"
    
    # (2*sqrt(3) + sqrt(6)) * sqrt(2) = 2*sqrt(6) + sqrt(12)
    coeff1, rad1 = RadicalOps.simplify_term(2, 6)
    coeff2, rad2 = RadicalOps.simplify_term(1, 12)
    
    merged = {}
    for c, r in [(coeff1, rad1), (coeff2, rad2)]:
        merged[r] = merged.get(r, 0) + c
        
    sorted_radicands = sorted(merged.keys())
    terms = []
    for r in sorted_radicands:
        c = merged[r]
        if c != 0:
            terms.append({
                "coefficient": int(c),
                "radicand": int(r)
            })
            
    question_text = f"Simplify the expression: {expression}"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "terms": terms
        },
        "oracle_payload": {
            "expression": expression
        }
    }