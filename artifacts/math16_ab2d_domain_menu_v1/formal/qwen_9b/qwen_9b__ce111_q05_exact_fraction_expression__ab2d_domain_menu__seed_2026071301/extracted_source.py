from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Parse the expression components from the string in frozen_params
    term1_num, term1_den = map(int, frozen_params["expression"].split(" ")[0].split("/"))
    term2_num, term2_den = map(int, " + ".join(frozen_params["expression"].split()[1:3]).replace("+", "").split("/")[::2]) # This logic is fragile for complex strings
    
    # Robust parsing based on the specific string format provided in frozen_params
    expr_str = frozen_params["expression"]
    
    # Extract first fraction: 9/22
    f1_parts = expr_str.split(" ")[0].split("/")
    n1, d1 = int(f1_parts[0]), int(f1_parts[1])
    
    # Extract second part before minus: + 11/18
    plus_part = " ".join(expr_str.split()[2:]) # "+ 11/18"
    f2_parts = plus_part.replace("+", "").split("/")
    n2, d2 = int(f2_parts[0]), int(f2_parts[1])
    
    # Extract third part (inside parenthesis): - (...) -> -(...)
    # The string is: "9/22 + 11/18 - (23/22 - 7/18)"
    # We need to parse the subtraction term. 
    # Let's reconstruct based on operator precedence logic manually or by splitting carefully.
    
    # Re-parse strictly from components identified in frozen_params string: "9/22 + 11/18 - (23/22 - 7/18)"
    parts = expr_str.replace(" ", "").split("-")
    term_a = parts[0] # "9/22+11/18" -> wait, split by '-' removes the minus sign. 
                      # The string is: "9/22 + 11/18 - (23/22 - 7/18)"
    # Let's use a simpler approach given the specific frozen_params content
    
    # Term 1: 9/22
    n_a, d_a = int("9"), int("22")
    
    # Term 2: + 11/18
    n_b, d_b = int("11"), int("18")
    
    # The subtraction part is -( (23/22) - (7/18) ) which equals (-23/22) + (7/18)
    # So we have three terms to sum: 9/22, 11/18, -23/22, 7/18
    
    t1 = FractionOps.from_parts(n_a, d_a)
    t2 = FractionOps.from_parts(n_b, d_b)
    
    # Inside parenthesis: (23/22 - 7/18)
    p1_num, p1_den = int("23"), int("22")
    p2_num, p2_den = int("7"), int("18")
    term_in_paren = FractionOps.sub(FractionOps.from_parts(p1_num, p1_den), 
                                     FractionOps.from_parts(p2_num, p2_den))
    
    # The full expression is t1 + t2 - (term_in_paren)
    result = FractionOps.add(t1, t2)
    result = FractionOps.sub(result, term_in_paren)
    
    correct_answer_numerator = int(FractionOps.to_exact(result).replace("/", "")) if "/" in str(FractionOps.to_exact(result)) else 0 # Fallback logic not needed as to_exact returns string 'p/q' or int
    
    exact_str = FractionOps.to_exact(result)
    if isinstance(exact_str, str):
        numerator_part, denominator_part = exact_str.split("/")
        correct_answer_numerator = int(numerator_part)
        correct_answer_denominator = int(denominator_part)
    else:
        # Should not happen for fractions unless result is integer
        correct_answer_numerator = exact_str
        correct_answer_denominator = 1
        
    canonical_latex = FractionOps.to_latex(result, mixed=False)

    return {
        "question_text": frozen_params["expression"],
        "correct_answer": {
            "numerator": correct_answer_numerator,
            "denominator": correct_answer_denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }