def generate(level=1, **kwargs):
    question_text = r"Select a prime factor from $n$. Given candidates $\{c_1, c_2\}$ where each is either composite or prime such that one divides $n$, choose the correct candidate. Here $n = 156$ and the provided list of candidates to evaluate for divisibility into $n$ includes values derived from a sample set containing composites like $14$. Determine which specific number in the given subset $\{c_i\}$ is actually prime AND divides $n$, or if no such candidate exists among those that divide, select based on primality. Specifically, consider candidates including $13$. Does $13$ divide $156$? Is it prime?"
    correct_answer = 0
    oracle_payload = {"candidates": [11, 12, 13, 14], "n": 156}

    n_val = kwargs.get("frozen_n", 156) if level == 0 else kwargs.get("oracle_params", {}).get("n", 156)
    
    # Reconstructing logic to ensure correct_answer is non-trivial for the specific problem instance implied by frozen params
    # The task implies selecting a prime factor. 
    # Candidates: [11, 12, 13, 14]
    # n = 156
    # Factors of 156: 1, 2, 3, 4, 6, 12, 13, 26, 39, 52, 78, 156. Primes dividing 156 are 2, 3, 13.
    # From candidates [11, 12, 13, 14], only 13 is both a candidate and a prime factor of n (wait, 11 does not divide). 
    # Actually: 
    # 156 / 2 = 78
    # 156 / 3 = 52
    # 156 / 4 = 39
    # ...
    # Check divisibility for candidates in [11, 12, 13, 14]:
    # 11: 156 % 11 != 0 (11*14=154) -> Not a factor.
    # 12: 156 / 12 = 13 -> Factor. Is 12 prime? No.
    # 13: 156 / 13 = 12 -> Factor. Is 13 prime? Yes.
    # 14: 156 % 14 != 0 (14*11=154) -> Not a factor.
    
    # The question asks to select a PRIME factor from the candidates that divides n.
    # Only 13 satisfies both conditions (is prime AND divides n).
    
    correct_answer = 13
    
    return {
        "question_text": r"Given $n=156$ and candidate list $\{c_1, c_2\} \subseteq [11, 12, 13, 14]$, identify the element that is both a prime number AND divides $n$. Express your answer as an integer.",
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }