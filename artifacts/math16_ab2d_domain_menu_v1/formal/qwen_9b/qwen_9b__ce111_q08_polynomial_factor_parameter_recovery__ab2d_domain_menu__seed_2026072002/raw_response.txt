from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen_params = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }

    # The task asks to solve for a+2c given (3x+a)(bx+c) = 39x^2 + 5x - 14.
    # We are told the first factor is fixed as (3x+a).
    # Let's expand (3x+a)(bx+c):
    # 3b x^2 + (3c+ab)x + ac = 39x^2 + 5x - 14
    
    # From x^2 coeff: 3*b = 39 => b = 13.
    # From constant term: a*c = -14.
    # We need to find integer pairs (a, c) such that ac = -14 and they satisfy the middle term condition with b=13.
    # Middle term coeff: 3c + ab = 5 => 3c + 13a = 5.
    
    # Substitute a*c = -14 into possibilities for integers a, c.
    # Factors of -14: (1, -14), (-1, 14), (2, -7), (-2, 7), (7, -2), (-7, 2), (14, -1), (-14, 1).
    
    possible_a = [1, -1, 2, -2, 7, -7, 14, -14]
    valid_pairs = []
    
    for a in possible_a:
        c = -14 // a # Since ac=-14 and integers
        
        if 3*c + 13*a == 5:
            valid_pairs.append((a, c))
            
    # The problem implies a unique solution or asks for the value derived from it.
    # Let's check which pair works.
    
    solutions = []
    b_val = 39 // 3
    
    for candidate_a in possible_a:
        if -14 % candidate_a != 0: continue
        c_candidate = -14 // candidate_a
        
        if 3*c_candidate + (b_val * candidate_a) == 5:
            solutions.append((candidate_a, c_candidate))
            
    # Calculate a+2c for valid solution(s). The problem likely has one unique integer answer.
    
    results = []
    for a_sol, c_sol in solutions:
        val = a_sol + 2 * c_sol
        results.append(val)
        
    if not results:
         return {
            "question_text": frozen_params["quadratic_coefficients"], # Fallback placeholder logic shouldn't happen with valid inputs but safety first.
            "correct_answer": None, 
            "oracle_payload": frozen_params
          }

    # If multiple solutions exist mathematically (unlikely for this specific setup unless symmetric), 
    # usually the context implies a unique one or we return all? The contract says `int`.
    # Let's assume uniqueness based on standard problem design.
    
    final_answer = results[0] if len(results) == 1 else sum(set(results)) 
    
    return {
        "question_text": r"已知 $39x^2+5x-14=(3x+a)(bx+c)$，其中 $a,b,c$ 均為整數，求 $a+2c$。",
        "correct_answer": final_answer,
        "oracle_payload": frozen_params
    }