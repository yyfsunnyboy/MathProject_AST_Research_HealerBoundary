def generate(level=1, **kwargs):
    candidates = kwargs.get("candidates", [11, 12, 13, 14])
    n = kwargs["n"]
    
    question_text = r"The prime factorization of $N$ is given by the set $\{p \in S : p | N\}$. Given that $S=\{11, 12, 13, 14\}$ and $N=156$, determine which elements from $S$ are prime factors."
    
    correct_answer = None
    
    for c in candidates:
        if n % c == 0:
            if all(n // i != j or not any(i * j == n for i, j in [(c, n//c)])): # Check no other factorization exists within S context logic simplified to just divisibility check here as per typical selection task structure where we pick the subset that divides N uniquely by definition of prime factors
                pass 
            correct_answer = c
    
    oracle_payload = {"candidates": candidates, "n": n}

    return {
        "question_text": question_text,
        "correct_answer": int(correct_answer),
        "oracle_payload": oracle_payload
    }
