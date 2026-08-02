from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "divisor_of": 216,
        "multiple_of": 18
    }
    
    # Calculate the Least Common Multiple (LCM) of multiple_of and divisor_of.
    # Any number that is a multiple of 'a' and a divisor of 'b' must be a multiple of LCM(a,b).
    # Also, it must divide b. So we are looking for multiples of LCM(a,b) that also divide b.
    
    m = frozen_params["multiple_of"]  # 18
    d = frozen_params["divisor_of"]   # 216
    
    # Calculate GCD using IntegerOps.safe_eval to avoid direct import if restricted, 
    # but since we can use native ops and the library is imported, let's compute LCM.
    # LCM(a, b) = (a * b) // GCD(a, b). We need a way to get GCD or calculate it manually.
    # Since IntegerOps.safe_eval allows arithmetic expressions including *, we can't directly call gcd if not in API.
    # However, the problem asks for count of numbers x such that:
    # 1) m | x (x is multiple of m) => x = k * m
    # 2) x | d (x divides d) => x <= d and d % x == 0
    
    # So we need to find how many multiples of 'm' are divisors of 'd'.
    # These numbers form an arithmetic progression: m, 2*m, 3*m, ... up to the largest multiple of m that divides d.
    
    # Let's iterate through all positive integers k such that (k * m) <= d and check divisibility? 
    # Actually, if x is a divisor of d, then x must be one of IntegerOps.positive_divisors(d).
    # We can filter those divisors to see which are multiples of m.
    
    candidates = IntegerOps.positive_divisors(d)
    
    count = 0
    for num in candidates:
        if IntegerOps.is_divisible(num, m):
            count += 1
            
    return {
        "question_text": "有多少個正整數同時是 \(18\) 的倍數，也是 \(216\) 的因數？",
        "correct_answer": {"count": count},
        "oracle_payload": frozen_params
    }