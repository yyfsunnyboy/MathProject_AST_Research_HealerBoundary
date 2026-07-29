def generate(level=1, **kwargs):
    question_text = r"Given the set of candidate integers $C = \{11, 12, 13, 14\}$ and a target integer $n = 156$, select a subset of candidates such that their product equals $n$. If no such subset exists or if multiple subsets exist with different products equal to $n$ (which is impossible for unique factorization), handle appropriately. However, in this specific instance, determine the sum of all distinct prime factors present in the canonical prime factorization of $n = 156$, where each prime factor is counted only once regardless of its multiplicity."
    correct_answer = 20
    oracle_payload = {"candidates": [11, 12, 13, 14], "n": 156}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }