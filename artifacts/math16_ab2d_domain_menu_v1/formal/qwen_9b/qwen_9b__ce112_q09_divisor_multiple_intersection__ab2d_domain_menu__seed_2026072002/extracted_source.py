from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "divisor_of": 216,
        "multiple_of": 18
    }
    
    # Calculate the Least Common Multiple (LCM) of multiple_of and divisor_of.
    # Any number that is a multiple of 'a' and a divisor of 'b' must be a multiple of LCM(a, b).
    # Also, it must be <= b.
    # So we are looking for multiples of LCM(18, 216) within the range [LCM(18, 216), 216].
    
    m = frozen_params["multiple_of"]
    d = frozen_params["divisor_of"]
    
    # Calculate GCD using safe_eval to avoid direct import of math.gcd if restricted, 
    # but IntegerOps.safe_eval supports arithmetic. However, we don't have a gcd API directly listed.
    # We can compute LCM(a,b) as (a*b)//gcd(a,b). Since no gcd is in the allowed list explicitly by name like 'IntegerOps.gcd',
    # and safe_eval doesn't support custom functions easily without defining them first which isn't an option here,
    # we must rely on the fact that 216 is a multiple of 18.
    # If d % m == 0 (which implies LCM(a,b) = b), then any number x such that:
    #   x % m == 0 AND x <= d AND x > 0
    # Since d=216 and m=18, 216 is a multiple of 18. 
    # The condition "multiple of 18" means x = k * 18.
    # The condition "divisor of 216" means x divides 216.
    # Since 216 itself is a multiple of 18, the set of numbers that are multiples of 18 and divisors of 216 
    # corresponds exactly to the divisors of (LCM(18, 216)) which is just 216.
    # Wait, logic check:
    # Set A = {x | x > 0 AND x % m == 0} -> Multiples of 18: 18, 36, ..., 216, ...
    # Set B = {x | x > 0 AND d % x == 0} -> Divisors of 216.
    # We want A intersect B.
    # Since m divides d (18 divides 216), LCM(m, d) = d.
    # The multiples of m that are <= d are exactly the divisors of d? No.
    # Example: m=2, d=4. Multiples of 2 <= 4: {2, 4}. Divisors of 4: {1, 2, 4}. Intersection: {2, 4}. Count = 2.
    # Formula for count when m|d is (d // m). 
    # Let's verify with IntegerOps.safe_eval to ensure arithmetic correctness without external gcd logic if possible,
    # but simple integer division in Python works fine for positive ints. The constraint says "Allowed native ops: ...".
    
    lcm_val = d  # Because 216 is a multiple of 18
    
    # We need count of x such that:
    # 1. x % m == 0
    # 2. d % x == 0 (x divides d)
    # Since LCM(m, d) = d, the condition "multiple of m" combined with "divisor of d" 
    # simplifies to counting divisors of d that are also multiples of m? No.
    # Actually, if we list all divisors of d: 1, 2, 3, 4, 6, 8, 9, 12, ...
    # Which ones are divisible by m (18)? Only those >= 18 and multiples of 18.
    # Since max is 216, the candidates are 18, 36, ..., up to largest multiple <= 216 that divides 216.
    # Actually, any divisor x of d satisfies x | d. If we also require m | x, then x must be a common multiple of m and a divisor of d.
    # Since LCM(m, d) = d (because m|d), the smallest positive number satisfying "multiple of m" is m itself? No.
    # The numbers are k*m such that k*m divides d.
    # So we need count of integers k >= 1 where (k * m) | d.
    # This implies k * m <= d and d % (k * m) == 0.
    # Since m|d, let d = q * m. Then condition is (k*m) | (q*m) => k | q.
    # So we need count of divisors of q where q = d // m.
    
    quotient = IntegerOps.safe_eval(f"{d} // {m}")
    
    # Now find number of positive divisors of quotient.
    # We can use IntegerOps.positive_divisors to get the list and take its length.
    divisor_list = IntegerOps.positive_divisors(quotient)
    count = len(divisor_list)
    
    return {
        "question_text": frozen_params.get("divisor_of") is not None, # Placeholder logic for text? No, use provided string from task block description if available in kwargs or hardcode based on params.
        # The prompt says: "Frozen task description (use as question_text)" -> "有多少個正整數同時是 \(18\) 的倍數，也是 \(216\) 的因數？"
        "question_text": "有多少個正整數同時是 \\(18\\) 的倍數，也是 \\(216\\) 的因數？", 
        # Wait, the instruction says: "Frozen task description (use as question_text)" and provides it in the block.
        # I should use that exact string.
    }

# Re-writing to strictly follow instructions for return value construction inside generate function properly without external variables leaking logic errors.
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "divisor_of": 216,
        "multiple_of": 18
    }
    
    # Logic: Count divisors of (d // m) because d is a multiple of m.
    divisor_val = IntegerOps.safe_eval(f"{frozen_params['divisor_of']} // {frozen_params['multiple_of']}")
    candidates = IntegerOps.positive_divisors(divisor_val)
    
    return {
        "question_text": "有多少個正整數同時是 \\(18\\) 的倍數，也是 \\(216\\) 的因數？", 
        # Note: The prompt text in the task block uses LaTeX delimiters. I will preserve them as requested by "use as question_text".
        "correct_answer": {"count": len(candidates)},
        "oracle_payload": frozen_params
    }