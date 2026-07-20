def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    # Calculate LCM of divisor and multiple to find the step size for intersection
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    lcm_value = (divisor_of * multiple_of) // gcd(divisor_of, multiple_of)
    
    # Find smallest number that is both divisor and multiple
    # We need x such that x % divisor_of == 0 AND x % multiple_of == 0
    # This means x must be a multiple of LCM(divisor_of, multiple_of)
    # The question asks for count in range [1, lcm_value] which is exactly 1
    
    correct_answer = {"count": 1}
    
    return {
        "question_text": f"Find the number of positive integers less than or equal to $\\text{lcm}(\\{divisor_of\\}, \\{multiple_of\\})$ that are both divisors of $\\{divisor_of\\}$ and multiples of $\\{multiple_of\\}$. Note: $\\text{lcm}(a, b)$ denotes the least common multiple.",
        "correct_answer": correct_answer,
        "oracle_payload": {"divisor_of": divisor_of, "multiple_of": multiple_of}
    }