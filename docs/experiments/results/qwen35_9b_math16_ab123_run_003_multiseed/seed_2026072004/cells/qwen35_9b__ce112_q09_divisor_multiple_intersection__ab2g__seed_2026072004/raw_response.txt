def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    question_text = r"""Find the number of positive integers that are both a divisor of $n_1$ and a multiple of $n_2$, where $n_1 = \text{{divisor\_of}}$ and $n_2 = \text{{multiple\_of}}$. If no such integer exists within standard bounds, consider only the trivial solution or state count as 0 if strictly positive integers are required beyond multiples. Specifically, find all $x > 0$ such that $x | n_1$ and $n_2 | x$."""
    
    # Logic: We need x such that x divides divisor_of AND multiple_of divides x.
    # So, LCM(multiple_of) <= x <= divisor_of? No.
    # Condition 1: x % divisor_of == 0 is FALSE. It says "divisor of n1". So x | n1.
    # Condition 2: "multiple of n2". So n2 | x.
    # We need count of integers x where (x divides A) AND (B divides x).
    # Let A = divisor_of, B = multiple_of.
    # Constraints on x: 
    #   x <= A (since x|A and A>0 implies x is a factor of A, so x<=A usually for positive integers unless A=0 which isn't the case here)
    #   x >= B (since B|x and x>0 implies x>=B)
    # So we are looking for factors of A that are also multiples of B.
    # This is equivalent to finding k such that x = k * LCM(A, B)? No.
    # Let's re-evaluate: 
    #   1. x divides A => A % x == 0
    #   2. B divides x => x % B == 0
    # Combining these: x must be a multiple of B and a divisor of A.
    # Therefore, LCM(B, ?) ... actually, simply iterate or calculate logically.
    # Since x is a divisor of A, x <= A.
    # Since x is a multiple of B, x >= B (for positive integers).
    # Also, since x divides A and x is a multiple of B, then LCM(B, ?) must divide A? 
    # Actually, if such an x exists, it implies that B <= A. If B > A, count is 0.
    # Furthermore, any common solution x must satisfy: x = k * B for some integer k >= 1.
    # Substitute into first condition: (k*B) divides A => A % (k*B) == 0.
    # So we need to find number of integers k such that (k*B) <= A and A % (k*B) == 0.
    
    count = 0
    
    if multiple_of > divisor_of:
        count = 0
    else:
        for x in range(multiple_of, divisor_of + 1):
            if x % multiple_of == 0 and divisor_of % x == 0:
                count += 1
                
    correct_answer = {"count": count}
    
    oracle_payload = kwargs.get("oracle", {
        "divisor_of": int(divisor_of), 
        "multiple_of": int(multiple_of)
    })

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }