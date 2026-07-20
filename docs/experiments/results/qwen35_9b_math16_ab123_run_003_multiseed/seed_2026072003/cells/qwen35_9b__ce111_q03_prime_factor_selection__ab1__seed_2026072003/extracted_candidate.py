def generate(level=1, **kwargs):
    candidates = [11, 12, 13, 14]
    n = 156
    
    # Calculate prime factorization of each candidate and find the one that divides n with maximum sum of distinct prime factors or a specific selection criteria.
    # Task: math16_prime_factor_selection usually implies selecting candidates whose product equals n or finding factors. 
    # Given n=156 = 2^2 * 3 * 13. Candidates are [11, 12, 13, 14].
    # Only 12 and 13 divide 156? No, 11 does not (156/11 != int), 14 does not (156/14 = 78/7). 
    # Wait, let's re-evaluate standard "prime factor selection" tasks. Often it asks to select a subset of candidates that multiply to n or satisfy divisibility.
    # However, looking at the specific numbers: 12 divides 156 (156 = 12 * 13). 
    # If the task is "Select from candidates those that are factors of n", then {12} and maybe others?
    # Let's assume a common logic for this dataset ID style: Find the candidate(s) in `candidates` such that they divide `n`.
    # 156 / 11 = 14.18... (No)
    # 156 / 12 = 13 (Yes)
    # 156 / 13 = 12 (Yes)
    # 156 / 14 = 11.14... (No)
    # If the task is to find all valid candidates, answer might be a list or sum? 
    # Specification says `correct_answer` must be a single exact integer.
    # Perhaps it asks for the count of such numbers? Or their product? 
    # Let's assume the question text frames it as "How many integers in the candidate set are factors of n?" -> Count is 2 (12 and 13).
    # OR, maybe it selects one specific based on a rule. 
    # Given the ambiguity without explicit prompt template for ce111_q03_prime_factor_selection, I will construct a standard math problem: "Count how many numbers in candidates divide n."
    
    valid_count = 0
    for c in candidates:
        if n % c == 0:
            valid_count += 1
            
    question_text = f"Given the set of candidate integers $C = {candidates}$ and an integer target $N = {n}$, determine how many elements from $C$ are exact divisors of $N$. Express your answer as a single integer."
    
    correct_answer = valid_count
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {"candidates": [11, 12, 13, 14], "n": 156}
    }