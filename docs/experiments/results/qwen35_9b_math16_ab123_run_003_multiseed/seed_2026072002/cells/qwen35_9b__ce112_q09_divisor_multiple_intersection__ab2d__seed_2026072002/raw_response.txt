import json
from core.prompts.domain_function_library import IntegerOps


def generate(level=1, **kwargs):
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]

    # Calculate the smallest positive number that is both a divisor of 'a' and a multiple of 'b'.
    # This occurs when x divides 'a' AND b divides x.
    # Therefore, x must be a common element in {d : d|a} intersected with {k*b : k>=1}.
    # The smallest such positive integer is the Least Common Multiple (LCM) of all divisors of 'a'.
    # Actually, let's re-evaluate: 
    # Condition 1: x divides a.
    # Condition 2: b divides x.
    # From Cond 2: x = k * b for some integer k >= 1.
    # Substitute into Cond 1: (k*b) must divide a => k * b <= a and a % (k*b) == 0.
    # We need the smallest positive x satisfying this? Or just count them in a range? 
    # The task name implies finding an intersection property. Usually, these tasks ask for the count of such numbers within [1, LCM(a,b)] or similar bounds if not specified.
    # However, looking at standard math problems: "How many integers are both divisors of A and multiples of B?"
    # Let x be a number satisfying conditions. 
    # x must divide A => x <= A (assuming positive).
    # x must be multiple of B => x >= B.
    # So we count k such that 1*k*B divides A, where k is integer and k*B > 0.
    
    limit = divisor_val
    
    valid_count = 0
    for k in range(1, (limit // multiple_val) + 1):
        candidate_x = k * multiple_val
        
        # Check if candidate_x divides the 'divisor_of' value
        is_divisible_result = IntegerOps.is_divisible(divisor_val, candidate_x)
        
        # The domain API returns bool directly for divisibility check? 
        # Signature: (a, b) -> returns bool. Let's assume a % b == 0.
        if is_divisible_result:
            valid_count += 1
            
    correct_answer = {"count": valid_count}

    return {
        "question_text": r"Find the number of positive integers that are both divisors of $216$ and multiples of $18$.",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }