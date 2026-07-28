# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen parameters defined directly as per specification
    divisor_of = 216
    multiple_of = 18
    
    # Count positive integers x satisfying both conditions:
    # 1. x % multiple_of == 0 (x is a multiple of 18)
    # 2. divisor_of % x == 0 (divisor_of is divisible by x, i.e., x divides 216)
    
    count = 0
    
    # Iterate through positive integers up to the maximum possible candidate (max(divisor_of, multiple_of))
    max_candidate = max(divisor_of, multiple_of)
    
    for x in range(1, max_candidate + 1):
        if x % multiple_of == 0 and divisor_of % x == 0:
            count += 1
    
    correct_answer_dict = {"count": int(count)}
    
    question_text = r"Find the number of positive integers $x$ such that $x$ is a multiple of $\{multiple\_of}$ AND $\{divisor\_of\}$ is divisible by $x$. Express your answer as an integer."

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": {"divisor_of": divisor_of, "multiple_of": multiple_of}
    }