from typing import Dict, Any

def generate(level=1, **kwargs):
    frozen_params = {"candidates": [11, 12, 13, 14], "n": 156}
    
    # Task: Find a subset of candidates whose product equals n.
    # Candidates: 11, 12, 13, 14
    # Target n: 156
    
    from math import sqrt
    def IntegerOps_is_divisible(a, b):
        return (a % b) == 0

    def IntegerOps_safe_eval(expr):
        try:
            result = eval(expr)
            if isinstance(result, bool) or isinstance(result, list) or isinstance(result, tuple) or isinstance(result, set):
                raise ValueError("Non-numeric result")
            return result
        except Exception as e:
            raise ValueError(f"Evaluation failed: {e}")

    # Brute force subset product check for candidates [11, 12, 13, 14] to find n=156
    import itertools
    
    found_subset = None
    all_subsets = []
    
    for r in range(0, len(frozen_params["candidates"]) + 1):
        for subset in itertools.combinations(frozen_params["candidates"], r):
            product_expr = "*".join(map(str, subset)) if subset else "1"
            
            # Check divisibility or direct calculation using domain API logic where possible, 
            # but since we need exact equality and safe_eval handles eval:
            try:
                calc_prod = IntegerOps_safe_eval(product_expr)
                is_match = (calc_prod == frozen_params["n"])
                
                if is_match:
                    found_subset = subset
                    all_subsets.append(subset)
                    
                    # Optimization/Verification using domain API for divisibility logic if needed, 
                    # though direct eval suffices here. Let's verify with a simple check against n factors.
            except ValueError:
                continue

    candidates_list = frozen_params["candidates"]
    
    # Construct the question text formally
    candidate_str = ", ".join([f"c_{i}" for i in range(len(candidates_list))])
    
    if found_subset is None:
        raise RuntimeError("No solution found")
        
    correct_ans_int = IntegerOps_safe_eval(f"{' * '.join(map(str, found_subset))}")

    question_text = (
        r"The set of candidate integers is defined as $c_0=11$, $c_1=12$, $c_2=13$, and $c_3=14$. "
        r"Let $\mathcal{S}$ be a subset of these candidates such that the product of elements in $\mathcal{S}$ equals $n = 156$. "
        r"Determine which specific indices from the set $\{0, 1, 2, 3\}$ correspond to the integers forming this valid subset."
    )

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_ans_int,
        "oracle_payload": oracle_payload
    }