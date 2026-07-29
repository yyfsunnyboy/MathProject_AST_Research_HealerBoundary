def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    # Calculate intersection: numbers that are multiples of 'multiple_of' and divisors of 'divisor_of'.
    # These must be common elements in the set {x | x % multiple_of == 0} and {y | divisor_of % y == 0}.
    # Effectively, we look for k * multiple_of such that (k * multiple_of) divides divisor_of.
    
    count = 0
    current_multiple = multiple_of
    
    while True:
        if current_multiple > divisor_of:
            break
        
        remainder = divisor_of % current_multiple
        if remainder == 0:
            # It is a valid intersection point (a number that divides the big one and is a multiple of the small one)
            count += 1
            
        current_multiple += multiple_of

    return {
        "question_text": r"Find the count of integers $x$ such that $x$ is a divisor of $\divisor\_of = \{" + str(divisor_of) + "\}$ and $x$ is also a multiple of $\text{multiple\_of} = \{" + str(multiple_of) + "\}$.",
        "correct_answer": {"count": count},
        "oracle_payload": {
            "divisor_of": divisor_of,
            "multiple_of": multiple_of
        }
    }