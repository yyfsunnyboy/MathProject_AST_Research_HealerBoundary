import json

def generate(level=1, **kwargs):
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    from core.prompts.domain_function_library import IntegerOps
    
    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]
    
    # Calculate the count of numbers up to a reasonable bound that satisfy both conditions.
    # Condition: n % divisor == 0 AND (n * k) is divisible by multiple for some integer k? 
    # Re-reading task "divisor_multiple_intersection": usually implies finding integers x such that
    # x divides A and B divides x, or similar intersections in a specific range.
    # Given the context of typical math tasks: Find count of numbers <= N (default 100 for level 1) 
    # where number is divisible by 'divisor_of' AND some relation to 'multiple_of'.
    
    # Interpretation based on standard "intersection" logic in these datasets:
    # Count integers x such that:
    # 1. x is a divisor of 'divisor_of' (216)
    # 2. x is a multiple of 'multiple_of' (18) -> i.e., x % 18 == 0
    
    count = 0
    limit = 500 # Sufficient upper bound for level 1
    
    for n in range(1, limit + 1):
        cond1 = IntegerOps.is_divisible(n, divisor_val) # Is n a divisor of 216? (Usually phrased as "divisor_of" means the number divides this value)
        # Wait, standard naming: "x is a divisor of Y". 
        # Let's check logic: if oracle says x=36. 36*6 = 216. So n must divide 216.
        
        cond2 = (n % multiple_val == 0) # Is n a multiple of 18?
        
        # However, often these tasks are "Count numbers divisible by A and B". 
        # But parameters are named specifically: divisor_of, multiple_of.
        # Let's assume the intersection is: {x | x divides D} INTERSECT {x | M divides x}.
        if cond1 and cond2:
            count += 1
            
    correct_answer = {"count": int(count)}
    
    return {
        "question_text": r"Find the number of positive integers $n$ such that $n$ is a divisor of $\frac{d}{divisor\_of}$ (interpreted as $n \mid D$) and $n$ is also a multiple of $\frac{m}{multiple\_of}$ (interpreted as $M \mid n$), where $D=216$ and $M=18$. Specifically, count integers satisfying: 216 modulo $n$ equals 0 AND $n$ modulo 18 equals 0.",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }