from core.prompts.domain_function_library import IntegerOps


def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", None) or 216
    multiple_of = kwargs.get("multiple_of", None) or 18
    
    # Calculate the least common multiple (LCM) of 18 and 216.
    # A number is a multiple of 'a' if it can be written as k*a for some integer k >= 0.
    # In our case, we are looking for positive integers that are multiples of 18.
    
    # Calculate LCM using prime factorization to ensure correctness and avoid floating point issues with division
    
    def get_prime_factorization(n):
        return IntegerOps.prime_factorization(abs(n))

    factors_18 = get_prime_factorization(18)
    factors_216 = get_prime_factorization(divisor_of)
    
    # Calculate LCM by taking the maximum exponent for each prime factor present in either number.
    lcm_factors = {}
    all_primes = set(factors_18.keys()) | set(factors_216.keys())
    
    for p in all_primes:
        exp_18 = factors_18.get(p, 0)
        exp_216 = factors_216.get(p, 0)
        lcm_factors[p] = max(exp_18, exp_216)
    
    # Calculate LCM value using safe_eval to avoid potential overflow or type issues with large numbers if any.
    lcm_expr_parts = []
    for p in sorted(lcm_factors.keys()):
        e = lcm_factors[p]
        term = f"{p}**{e}"
        lcm_expr_parts.append(term)
    
    # Construct the LCM expression string and evaluate it safely to get an integer.
    if not lcm_expr_parts:
        lcm_value = 1
    else:
        lcm_str = "+".join(lcm_expr_parts)
        lcm_value = IntegerOps.safe_eval(f"({lcm_str})")

    # The number of positive integers that are multiples of 'a' and divisors of 'b' is equal to the count 
    # of divisors of LCM(a, b). This is because any such integer must be a multiple of lcm(a,b) (since it's divisible by both),
    # but wait... let me re-evaluate.

    # Let x be a positive integer that satisfies:
    # 1. x = k * m for some integer k >= 0, where m is the "multiple_of" value (18). So x is a multiple of 18.
    # 2. x divides n for some integer q >= 1, where n is the "divisor_of" value (216). So x | 216.

    # From condition 1: x = k * m => x/m = k (integer) -> x must be a multiple of m
    # From condition 2: x divides n -> x <= n and n % x == 0
    
    # Combining these conditions, we are looking for positive integers x such that:
    # - x is divisible by m (x >= m if x > 0)
    # - x divides n

    # Let's think about the properties of such numbers. If x satisfies both conditions, then:
    # x = k * m and x | n
    
    # This implies that x must be a multiple of LCM(m, something)? No... 
    # Actually, let me rephrase this more carefully.

    # We want to find the number of positive integers x such that:
    # 18 divides x AND x divides 216.
    
    # Let's denote these conditions as:
    # - x % 18 == 0 (x is a multiple of 18)
    # - 216 % x == 0 (x is a divisor of 216)

    # From the first condition, we know that x must be at least 18. 
    # Also, since x divides 216, x cannot exceed 216.
    
    # Let's consider what values satisfy both conditions:
    # - If x is a multiple of 18 and also a divisor of 216...

    # Actually, let me think about this differently using the concept of LCM/GCD or prime factorization directly on constraints.
    
    # Key insight: 
    # Any number that divides both A and B must divide GCD(A,B). But here we have different conditions!
    # We want x such that m|x AND x|n
    
    # Let's use the property of LCM again but in reverse direction...

    # Actually, let me just enumerate all divisors of 216 and check which ones are multiples of 18. This is safe for small numbers like 216!
    
    candidates = IntegerOps.positive_divisors(divisor_of)
    
    count = sum(1 for c in candidates if multiple_of <= c % (multiple_of + divisor_of)) # Wait, this logic is wrong
    
    # Let me restart the counting logic properly:
    # We need to check each candidate from positive_divisors of 216.
    # For a number x to be valid, it must satisfy: 
    # - It divides 216 (already satisfied by being in candidates)
    # - It is divisible by 18
    
    count = sum(1 for c in candidates if IntegerOps.is_divisible(c, multiple_of))

    return {
        "question_text": f"有多少個正整數同時是 \(18\) 的倍數，也是 \(216\) 的因數？",
        "correct_answer": {"count": count},
        "oracle_payload": {
            "divisor_of": divisor_of,
            "multiple_of": multiple_of
        }
    }
