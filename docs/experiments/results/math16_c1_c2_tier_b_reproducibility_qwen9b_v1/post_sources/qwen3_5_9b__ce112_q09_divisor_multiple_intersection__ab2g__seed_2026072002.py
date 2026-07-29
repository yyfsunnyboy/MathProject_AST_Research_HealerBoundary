def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    # Calculate count of numbers that are both divisors of 'divisor_of' and multiples of 'multiple_of'.
    # A number x must satisfy: x % divisor_of == 0 AND x % multiple_of == 0.
    # This implies x is a common multiple, so LCM(divisor_of, multiple_of) divides x.
    # However, the constraint "divisors of N" limits x <= N.
    # So we need count of multiples of LCM(N, M) that are <= N.
    
    import math
    
    def lcm(a, b):
        return abs(a * b) // math.gcd(a, b)
    
    common_multiple = lcm(divisor_of, multiple_of)
    
    # Count how many multiples of 'common_multiple' exist within range [1, divisor_of] inclusive.
    count = 0
    if common_multiple <= divisor_of:
        count = (divisor_of // common_multiple) + 1
    
    return {
        "question_text": f"Find the number of positive integers that are both divisors of $\\{divisor_of}\\$ and multiples of $\\{multiple_of}\\$.",
        "correct_answer": {"count": count},
        "oracle_payload": kwargs.get("frozen_params", {"divisor_of": divisor_of, "multiple_of": multiple_of}) if "frozen_params" in kwargs else {"divisor_of": divisor_of, "multiple_of": multiple_of}
    }