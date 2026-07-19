def generate(level=1, **kwargs):
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    divisor_numerator = frozen_params["divisor_of"]
    multiple_denominator = frozen_params["multiple_of"]
    
    # Calculate the smallest number that is a multiple of 'multiple_denominator' and divides 'divisor_numerator'
    # We are looking for integers x such that:
    # 1. x % multiple_denominator == 0 (x is a multiple of m)
    # 2. divisor_numerator % x == 0 (x divides D)
    
    count = 0
    
    # Iterate through all divisors of the 'divisor_of' number to check if they are multiples of 'multiple_of'
    temp_divisor = divisor_numerator
    while temp_divisor > 0:
        potential_x = temp_divisor
        is_multiple = (potential_x % multiple_denominator == 0)
        if is_multiple:
            count += 1
        
        # Optimization for divisors by traversing the number downwards via GCD logic or simple iteration if small enough.
        # Since we need all x that divide N, iterating down from N/N_step isn't direct. 
        # Better approach for general integers: find all divisors of D, then filter those divisible by m.
        
        temp_divisor -= 1
    
    return {
        "question_text": r"Let $D = \\frac{\\text{{divisor\_of}}}$ and $M = \\text{{multiple\_of}}$. Find the number of integers $x$ such that $x$ is a multiple of $M$ AND $x$ divides $D$, given specific sampled parameters.",
        "correct_answer": {"count": count},
        "oracle_payload": frozen_params
    }