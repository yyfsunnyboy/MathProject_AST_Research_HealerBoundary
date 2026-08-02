from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "divisor_of": 216,
        "multiple_of": 18
    }
    
    # Calculate the number of positive integers that are multiples of 18 and divisors of 216.
    # A number x is a multiple of 18 if x = k * 18 for some integer k >= 1.
    # Also, x must be <= 216 (since it's a divisor).
    # So we need to count integers in the range [18, 342] that divide 216 evenly? 
    # No: "divisor of" means x divides 216. Since divisors are positive and <= n, max is 216.
    # Multiples of 18 start at 18, then 36, ... up to the largest multiple <= 216.
    
    divisor_of = frozen_params["divisor_of"]
    multiple_of = frozen_params["multiple_of"]
    
    max_multiple = (divisor_of // multiple_of) * multiple_of
    
    # We need count of x such that:
    # 1. x is a positive integer
    # 2. x % divisor_of == 0? No, "is a divisor" means divisor_of % x == 0 or equivalently x divides divisor_of.
    # Wait the text says "是 ...的因數", which in Chinese math context usually means: 
    #   - A is B's factor (A | B). So if n is a multiple of m, then m|n. If n is a divisor of d, then n|d.
    # The question asks for numbers that are BOTH multiples of 18 AND divisors of 216.
    
    count = IntegerOps.safe_eval(f"sum(1 for x in range({multiple_of}, {max_multiple + 1}) if {divisor_of} % x == 0)")

    return {
        "question_text": f"有多少個正整數同時是 \(18\) 的倍數，也是 \(216\) 的因數？",
        "correct_answer": {"count": count},
        "oracle_payload": frozen_params,
    }
